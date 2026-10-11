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
from app.repositories import events as events_repo
from app.services import event_processing
from app.services.event_processing import EventNotFoundError


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
    technician = User(
        email="technician@test.invalid",
        display_name="Test Technician",
        password_hash="synthetic-test-hash",
        role_id=technician_role.id,
        is_active=True,
    )
    customer = Customer(customer_ref="CUST-1", name="Test Customer", address="1 Test Way")
    db_session.add_all([operator, technician, customer])
    db_session.flush()

    service = Service(
        customer_id=customer.id,
        service_type="Granite",
        service_ref="SVC-1",
        status="active",
    )
    device = NetworkDevice(
        customer_id=customer.id,
        device_ref="DEV-1",
        device_type="ONU",
        name="Test ONU",
        status="offline",
    )
    db_session.add_all([service, device])
    db_session.flush()

    event = NetworkEvent(
        source_event_id="EVT-1",
        event_type="ONU_OFFLINE",
        device_id=device.id,
        service_id=service.id,
        payload={"signal_state": "no_link"},
    )
    db_session.add(event)
    db_session.commit()

    return {
        "session": db_session,
        "operator": operator,
        "technician": technician,
        "customer": customer,
        "service": service,
        "device": device,
        "event": event,
    }


def operator_actor(workspace: dict[str, object]) -> AuthenticatedUser:
    operator = workspace["operator"]
    return AuthenticatedUser(id=operator.id, email=operator.email, role="operator")


def technician_actor(workspace: dict[str, object]) -> AuthenticatedUser:
    technician = workspace["technician"]
    return AuthenticatedUser(id=technician.id, email=technician.email, role="technician")


def count(db_session: Session, model: type) -> int:
    return db_session.scalar(select(func.count()).select_from(model))


def test_operator_processing_creates_assigned_ticket_and_audit(db_session, workspace):
    result = event_processing.process_event(db_session, workspace["event"].id, operator_actor(workspace))

    assert result.created is True
    assert result.ticket.assigned_technician_id == workspace["technician"].id
    assert result.ticket.customer_id == workspace["customer"].id
    assert result.ticket.service_id == workspace["service"].id
    assert result.ticket.severity == "high"
    assert result.assigned_technician_name == "Test Technician"

    db_session.refresh(workspace["event"])
    assert workspace["event"].processed_at is not None

    audit = db_session.scalar(select(AuditEvent))
    assert audit.event_type == "event_processed"
    assert audit.actor_id == workspace["operator"].id
    assert audit.ticket_id == result.ticket.id
    assert audit.details["source_event_id"] == "EVT-1"


def test_technician_cannot_process_events(db_session, workspace):
    with pytest.raises(HTTPException) as error:
        event_processing.process_event(db_session, workspace["event"].id, technician_actor(workspace))
    assert error.value.status_code == 403
    assert count(db_session, Ticket) == 0


def test_processing_unknown_event_raises_not_found(db_session, workspace):
    with pytest.raises(EventNotFoundError):
        event_processing.process_event(db_session, "does-not-exist", operator_actor(workspace))


def test_repeat_processing_returns_existing_ticket_without_duplicate(db_session, workspace):
    first = event_processing.process_event(db_session, workspace["event"].id, operator_actor(workspace))
    second = event_processing.process_event(db_session, workspace["event"].id, operator_actor(workspace))

    assert first.created is True
    assert second.created is False
    assert second.ticket.id == first.ticket.id
    assert count(db_session, Ticket) == 1
    assert count(db_session, AuditEvent) == 1


def test_database_failure_rolls_back_event_and_ticket(db_session, workspace, monkeypatch):
    def explode(*args, **kwargs):
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(events_repo, "record_audit_event", explode)

    with pytest.raises(RuntimeError):
        event_processing.process_event(db_session, workspace["event"].id, operator_actor(workspace))

    assert count(db_session, Ticket) == 0
    db_session.refresh(workspace["event"])
    assert workspace["event"].processed_at is None


def test_pending_event_listing_is_operator_only(db_session, workspace):
    records = event_processing.list_pending_events(db_session, operator_actor(workspace))
    assert [record.source_event_id for record in records] == ["EVT-1"]
    assert records[0].device_ref == "DEV-1"
    assert records[0].service_ref == "SVC-1"

    with pytest.raises(HTTPException) as error:
        event_processing.list_pending_events(db_session, technician_actor(workspace))
    assert error.value.status_code == 403


def test_pending_events_endpoint_enforces_role(db_session, workspace):
    app.dependency_overrides[get_session] = lambda: db_session
    try:
        app.dependency_overrides[get_current_user] = lambda: operator_actor(workspace)
        allowed = TestClient(app).get("/events/pending")
        app.dependency_overrides[get_current_user] = lambda: technician_actor(workspace)
        denied = TestClient(app).get("/events/pending")
    finally:
        app.dependency_overrides.clear()

    assert allowed.status_code == 200
    assert allowed.json()[0]["source_event_id"] == "EVT-1"
    assert denied.status_code == 403


def test_process_endpoint_returns_ticket_then_duplicate(db_session, workspace):
    app.dependency_overrides[get_session] = lambda: db_session
    try:
        app.dependency_overrides[get_current_user] = lambda: operator_actor(workspace)
        client = TestClient(app)
        created = client.post(f"/events/{workspace['event'].id}/process")
        duplicate = client.post(f"/events/{workspace['event'].id}/process")
        app.dependency_overrides[get_current_user] = lambda: technician_actor(workspace)
        denied = client.post(f"/events/{workspace['event'].id}/process")
    finally:
        app.dependency_overrides.clear()

    assert created.status_code == 200
    assert created.json()["created"] is True
    assert created.json()["duplicate"] is False

    assert duplicate.status_code == 200
    assert duplicate.json()["duplicate"] is True
    assert duplicate.json()["ticket"]["id"] == created.json()["ticket"]["id"]
    assert count(db_session, Ticket) == 1

    assert denied.status_code == 403


def test_process_endpoint_rejects_unknown_event(db_session, workspace):
    app.dependency_overrides[get_session] = lambda: db_session
    try:
        app.dependency_overrides[get_current_user] = lambda: operator_actor(workspace)
        response = TestClient(app).post("/events/missing/process")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404
