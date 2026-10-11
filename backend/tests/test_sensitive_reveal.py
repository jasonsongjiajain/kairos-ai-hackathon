import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.db.session import get_session
from app.domain.models import (
    AuditEvent,
    Customer,
    NetworkDevice,
    NetworkEvent,
    Role,
    Service,
    Ticket,
    User,
)
from app.main import app
from app.services import ticket_queries

SECRET = "Synthetic-ONU-Credential-Only-7f3!"


@pytest.fixture
def workspace(db_session: Session) -> dict[str, object]:
    operator_role = Role(name="operator")
    technician_role = Role(name="technician")
    db_session.add_all([operator_role, technician_role])
    db_session.flush()

    operator = User(
        email="operator@test.invalid",
        display_name="Test Operator",
        password_hash="synthetic-test-hash",
        role_id=operator_role.id,
        is_active=True,
    )
    technician_a = User(
        email="technician-a@test.invalid",
        display_name="Technician A",
        password_hash="synthetic-test-hash",
        role_id=technician_role.id,
        is_active=True,
    )
    technician_b = User(
        email="technician-b@test.invalid",
        display_name="Technician B",
        password_hash="synthetic-test-hash",
        role_id=technician_role.id,
        is_active=True,
    )
    assigned_customer = Customer(
        customer_ref="CUST-1", name="Assigned Customer", address="1 Test Way", is_demo=True
    )
    other_customer = Customer(
        customer_ref="CUST-2", name="Other Customer", address="2 Other Way", is_demo=True
    )
    db_session.add_all([operator, technician_a, technician_b, assigned_customer, other_customer])
    db_session.flush()

    assigned_service = Service(
        customer_id=assigned_customer.id,
        service_type="Granite",
        service_ref="SVC-GR-1",
        status="active",
    )
    other_service = Service(
        customer_id=other_customer.id,
        service_type="Granite",
        service_ref="SVC-GR-2",
        status="active",
    )
    onu = NetworkDevice(
        customer_id=assigned_customer.id,
        device_ref="DEV-ONU-1",
        device_type="ONU",
        name="Test ONU",
        status="offline",
        details={"onu_password": SECRET},
    )
    olt = NetworkDevice(
        customer_id=assigned_customer.id,
        device_ref="DEV-OLT-1",
        device_type="OLT",
        name="Test OLT",
        status="online",
        details={},
    )
    other_device = NetworkDevice(
        customer_id=other_customer.id,
        device_ref="DEV-ONU-2",
        device_type="ONU",
        name="Other ONU",
        status="offline",
        details={"onu_password": "other-synthetic-secret"},
    )
    db_session.add_all([assigned_service, other_service, onu, olt, other_device])
    db_session.flush()

    event = NetworkEvent(
        source_event_id="EVT-A",
        event_type="ONU_OFFLINE",
        device_id=onu.id,
        service_id=assigned_service.id,
        payload={},
    )
    db_session.add(event)
    db_session.flush()

    ticket = Ticket(
        source_event_id=event.id,
        customer_id=assigned_customer.id,
        service_id=assigned_service.id,
        assigned_technician_id=technician_a.id,
        severity="high",
        status="open",
        summary="ONU_OFFLINE reported for Test ONU",
    )
    db_session.add(ticket)
    db_session.commit()

    return {
        "session": db_session,
        "operator": operator,
        "technician_a": technician_a,
        "technician_b": technician_b,
        "assigned_customer": assigned_customer,
        "other_customer": other_customer,
        "onu": onu,
        "olt": olt,
        "other_device": other_device,
        "ticket": ticket,
    }


def operator_actor(workspace: dict[str, object]) -> AuthenticatedUser:
    operator = workspace["operator"]
    return AuthenticatedUser(id=operator.id, email=operator.email, role="operator")


def technician_a_actor(workspace: dict[str, object]) -> AuthenticatedUser:
    technician = workspace["technician_a"]
    return AuthenticatedUser(id=technician.id, email=technician.email, role="technician")


def technician_b_actor(workspace: dict[str, object]) -> AuthenticatedUser:
    technician = workspace["technician_b"]
    return AuthenticatedUser(id=technician.id, email=technician.email, role="technician")


def audit_count(session: Session, event_type: str) -> int:
    return session.scalar(
        select(func.count()).select_from(AuditEvent).where(AuditEvent.event_type == event_type)
    )


def test_assigned_technician_reveals_only_requested_credential_and_records_audit(db_session, workspace):
    app.dependency_overrides[get_session] = lambda: db_session
    try:
        app.dependency_overrides[get_current_user] = lambda: technician_a_actor(workspace)
        response = TestClient(app).get(
            f"/tickets/{workspace['ticket'].id}/devices/{workspace['onu'].id}/credential"
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert body["credential_type"] == "onu_password"
    assert body["credential"] == SECRET
    assert body["device_ref"] == "DEV-ONU-1"
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["pragma"] == "no-cache"

    audit = db_session.scalar(select(AuditEvent).where(AuditEvent.event_type == "credential_revealed"))
    assert audit is not None
    assert audit.actor_id == workspace["technician_a"].id
    assert audit.ticket_id == workspace["ticket"].id
    assert audit.details["device_id"] == workspace["onu"].id
    assert audit.details["credential_type"] == "onu_password"
    assert SECRET not in str(audit.details)


def test_operator_cannot_reveal_a_credential(db_session, workspace):
    with pytest.raises(HTTPException) as error:
        ticket_queries.reveal_device_credential(
            db_session, workspace["ticket"].id, workspace["onu"].id, operator_actor(workspace)
        )
    assert error.value.status_code == 403
    assert audit_count(db_session, "credential_revealed") == 0


def test_unassigned_technician_cannot_reveal_a_credential(db_session, workspace):
    with pytest.raises(HTTPException) as error:
        ticket_queries.reveal_device_credential(
            db_session, workspace["ticket"].id, workspace["onu"].id, technician_b_actor(workspace)
        )
    assert error.value.status_code == 404
    assert audit_count(db_session, "credential_revealed") == 0


def test_reveal_rejects_device_outside_the_ticket_customer(db_session, workspace):
    with pytest.raises(HTTPException) as error:
        ticket_queries.reveal_device_credential(
            db_session, workspace["ticket"].id, workspace["other_device"].id, technician_a_actor(workspace)
        )
    assert error.value.status_code == 404
    assert audit_count(db_session, "credential_revealed") == 0


def test_reveal_rejects_device_without_a_credential(db_session, workspace):
    with pytest.raises(HTTPException) as error:
        ticket_queries.reveal_device_credential(
            db_session, workspace["ticket"].id, workspace["olt"].id, technician_a_actor(workspace)
        )
    assert error.value.status_code == 404
    assert audit_count(db_session, "credential_revealed") == 0


def test_reveal_endpoint_records_one_audit_event_per_call(db_session, workspace):
    app.dependency_overrides[get_session] = lambda: db_session
    try:
        app.dependency_overrides[get_current_user] = lambda: technician_a_actor(workspace)
        client = TestClient(app)
        first = client.get(f"/tickets/{workspace['ticket'].id}/devices/{workspace['onu'].id}/credential")
        second = client.get(f"/tickets/{workspace['ticket'].id}/devices/{workspace['onu'].id}/credential")
    finally:
        app.dependency_overrides.clear()

    assert first.status_code == 200
    assert second.status_code == 200
    assert audit_count(db_session, "credential_revealed") == 2
