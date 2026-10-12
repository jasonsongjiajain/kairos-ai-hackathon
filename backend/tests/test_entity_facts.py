import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai import retrieval
from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.db.session import get_session
from app.domain.models import (
    AuditEvent,
    Customer,
    EntityFact,
    EntityFactSheet,
    NetworkDevice,
    NetworkEvent,
    Role,
    Service,
    Ticket,
    User,
)
from app.integrations.embeddings import LocalDeterministicEmbeddingProvider
from app.main import app
from app.services import entity_facts


@pytest.fixture
def embedder() -> LocalDeterministicEmbeddingProvider:
    return LocalDeterministicEmbeddingProvider(1024)


def _workspace(session: Session) -> dict[str, object]:
    technician_role = Role(name="technician")
    session.add(technician_role)
    session.flush()

    technician = User(
        email="technician@test.invalid",
        display_name="Test Technician",
        password_hash="synthetic-test-hash",
        role_id=technician_role.id,
        is_active=True,
        staff_code="TM1234",
    )
    customer = Customer(customer_ref="CUST-1", name="Test Customer", address="1 Test Way")
    session.add_all([technician, customer])
    session.flush()

    service = Service(
        customer_id=customer.id,
        service_type="VoBB",
        service_ref="SVC-VOBB-1",
        status="active",
        details={
            "vobb_status": "Active",
            "service_number": "03-1234-5678",
            "vobb_password": "Synthetic-VoBB-Credential-Only-1a2!",
        },
    )
    router = NetworkDevice(
        customer_id=customer.id,
        device_ref="DEV-RTR-1",
        device_type="router",
        name="Test Router",
        status="online",
        details={
            "mac_address": "30:f9:47:d3:fe:0e",
            "friendly_name": "Root",
            "manufacturer": "Shenzhen Skyworth Digital Technology CO.",
            "ssid_2g": "TestVilla_2.4G",
            "ssid_5g": "TestVilla_5G",
            "channel_2g": 11,
            "channel_5g": 44,
            "bandwidth_5g": "160 MHz",
            "protocol_5g": "11ax",
            "platform": "SKYWORTH",
            "parent_mac": "ff:ff:ff:ff:ff:ff",
            "ip_address": "192.168.0.1",
        },
    )
    session.add_all([service, router])
    session.flush()

    event = NetworkEvent(
        source_event_id="EVT-1",
        event_type="HSI_DEGRADED",
        device_id=router.id,
        service_id=service.id,
        payload={"signal_state": "no_link"},
    )
    session.add(event)
    session.flush()

    ticket = Ticket(
        source_event_id=event.id,
        customer_id=customer.id,
        service_id=service.id,
        assigned_technician_id=technician.id,
        severity="medium",
        status="open",
        summary="HSI degraded at the test customer",
        tm_ticket_no="TT-EVT-1",
        ctt_activity_id="CTT-DEV-RTR-1",
        login_id="CUST-1",
        ticket_category="HSI_DEGRADED",
        staff_code="TM1234",
    )
    session.add(ticket)
    session.flush()

    entity_facts.sync_device_facts(session, router)
    entity_facts.sync_service_facts(session, service)
    entity_facts.sync_ticket_facts(session, ticket)
    session.commit()

    return {
        "technician": technician,
        "customer": customer,
        "service": service,
        "router": router,
        "ticket": ticket,
    }


def _actor(workspace: dict[str, object]) -> AuthenticatedUser:
    technician = workspace["technician"]
    return AuthenticatedUser(id=technician.id, email=technician.email, role="technician")


def test_sync_device_facts_stores_typed_values_and_embeddable_content(db_session):
    workspace = _workspace(db_session)
    router = workspace["router"]

    sheet = db_session.get(EntityFactSheet, entity_facts.sheet_id("device", router.id, "router"))
    assert sheet is not None
    assert "SSID 5 GHz: TestVilla_5G" in sheet.content
    assert sheet.embedding is None

    channel = db_session.scalar(
        select(EntityFact).where(
            EntityFact.entity_id == router.id, EntityFact.field_key == "channel_5g"
        )
    )
    assert channel.value_number == 44.0
    assert channel.is_sensitive is False


def test_sync_service_facts_keeps_sensitive_values_out_of_embedded_content(db_session):
    workspace = _workspace(db_session)
    service = workspace["service"]

    sheet = db_session.get(EntityFactSheet, entity_facts.sheet_id("service", service.id, "vobb"))
    assert sheet is not None
    assert "Synthetic-VoBB-Credential-Only-1a2!" not in sheet.content

    password = db_session.scalar(
        select(EntityFact).where(
            EntityFact.entity_id == service.id, EntityFact.field_key == "vobb_password"
        )
    )
    assert password.is_sensitive is True
    assert password.value_text == "Synthetic-VoBB-Credential-Only-1a2!"


def test_embed_missing_entity_facts_is_idempotent(db_session, embedder):
    _workspace(db_session)

    generated, reused = entity_facts.embed_missing_entity_facts(db_session, embedder)
    db_session.commit()
    assert generated == 3
    assert reused == 0
    sheets = list(db_session.scalars(select(EntityFactSheet)).all())
    assert all(len(sheet.embedding) == 1024 for sheet in sheets)

    generated, reused = entity_facts.embed_missing_entity_facts(db_session, embedder)
    assert (generated, reused) == (0, 3)


def test_retrieve_for_ticket_returns_citable_device_and_service_facts(db_session, embedder):
    workspace = _workspace(db_session)
    entity_facts.embed_missing_entity_facts(db_session, embedder)
    db_session.commit()

    matches = retrieval.retrieve_for_ticket(
        db_session, workspace["ticket"].id, _actor(workspace), "ssid 5 ghz", embedder, limit=5
    )

    assert matches
    device_matches = [match for match in matches if match.source_type == "device"]
    assert device_matches
    assert device_matches[0].document_id == f"device:{workspace['router'].id}"
    assert "TestVilla_5G" in device_matches[0].content


def test_ticket_facts_endpoint_redacts_sensitive_values(db_session):
    workspace = _workspace(db_session)

    app.dependency_overrides[get_session] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: _actor(workspace)
    try:
        response = TestClient(app).get(f"/tickets/{workspace['ticket'].id}/facts")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["ticket_id"] == workspace["ticket"].id
    by_key = {fact["field_key"]: fact for fact in body["facts"]}
    assert by_key["vobb_password"]["value_text"] == "[redacted]"
    assert by_key["ssid_5g"]["value_text"] == "TestVilla_5G"
    assert by_key["tm_ticket_no"]["value_text"] == "TT-EVT-1"


def test_reveal_service_credential_is_audited(db_session):
    workspace = _workspace(db_session)

    app.dependency_overrides[get_session] = lambda: db_session
    app.dependency_overrides[get_current_user] = lambda: _actor(workspace)
    try:
        response = TestClient(app).get(
            f"/tickets/{workspace['ticket'].id}/services/{workspace['service'].id}/credential"
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["credential"] == "Synthetic-VoBB-Credential-Only-1a2!"
    audit = db_session.scalar(
        select(AuditEvent).where(AuditEvent.event_type == "credential_revealed")
    )
    assert audit.details["service_ref"] == "SVC-VOBB-1"
    assert "Synthetic-VoBB-Credential-Only-1a2!" not in str(audit.details)
