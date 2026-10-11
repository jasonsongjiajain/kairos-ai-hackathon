import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.db.session import get_session
from app.domain.models import (
    Customer,
    NetworkDevice,
    NetworkEvent,
    Role,
    Service,
    Ticket,
    TopologyEdge,
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
    customer_one = Customer(
        customer_ref="CUST-1",
        name="Test Customer One",
        address="1 Test Way",
        is_demo=True,
    )
    customer_two = Customer(
        customer_ref="CUST-2",
        name="Other Customer",
        address="2 Other Way",
        is_demo=True,
    )
    db_session.add_all([operator, technician_a, technician_b, customer_one, customer_two])
    db_session.flush()

    granite = Service(
        customer_id=customer_one.id,
        service_type="Granite",
        service_ref="SVC-GR-1",
        status="active",
        details={"demo": True},
    )
    hsi = Service(
        customer_id=customer_one.id,
        service_type="HSI",
        service_ref="SVC-HSI-1",
        status="active",
        details={"demo": True},
    )
    vobb = Service(
        customer_id=customer_one.id,
        service_type="VoBB",
        service_ref="SVC-VOBB-1",
        status="active",
        details={"demo": True},
    )
    other_service = Service(
        customer_id=customer_two.id,
        service_type="Granite",
        service_ref="SVC-GR-2",
        status="active",
    )
    olt = NetworkDevice(
        customer_id=customer_one.id,
        device_ref="DEV-OLT-1",
        device_type="OLT",
        name="Test OLT",
        status="online",
        details={},
    )
    onu = NetworkDevice(
        customer_id=customer_one.id,
        device_ref="DEV-ONU-1",
        device_type="ONU",
        name="Test ONU",
        status="offline",
        details={"onu_password": SECRET},
    )
    router = NetworkDevice(
        customer_id=customer_one.id,
        device_ref="DEV-RTR-1",
        device_type="router",
        name="Test Router",
        status="unreachable",
        details={},
    )
    other_device = NetworkDevice(
        customer_id=customer_two.id,
        device_ref="DEV-ONU-2",
        device_type="ONU",
        name="Other ONU",
        status="offline",
        details={"onu_password": "other-synthetic-secret"},
    )
    db_session.add_all([granite, hsi, vobb, other_service, olt, onu, router, other_device])
    db_session.flush()

    event_a = NetworkEvent(
        source_event_id="EVT-A",
        event_type="ONU_OFFLINE",
        device_id=onu.id,
        service_id=granite.id,
        payload={"signal_state": "no_link"},
    )
    event_b = NetworkEvent(
        source_event_id="EVT-B",
        event_type="ONU_OFFLINE",
        device_id=other_device.id,
        service_id=other_service.id,
        payload={"signal_state": "no_link"},
    )
    db_session.add_all([event_a, event_b])
    db_session.flush()

    ticket_a = Ticket(
        source_event_id=event_a.id,
        customer_id=customer_one.id,
        service_id=granite.id,
        assigned_technician_id=technician_a.id,
        severity="high",
        status="open",
        summary="ONU_OFFLINE reported for Test ONU",
    )
    ticket_b = Ticket(
        source_event_id=event_b.id,
        customer_id=customer_two.id,
        service_id=other_service.id,
        assigned_technician_id=technician_b.id,
        severity="medium",
        status="open",
        summary="ONU_OFFLINE reported for Other ONU",
    )
    topology = [
        TopologyEdge(source_device_id=olt.id, target_device_id=onu.id, service_id=granite.id),
        TopologyEdge(source_device_id=onu.id, target_device_id=router.id, service_id=hsi.id),
    ]
    db_session.add_all([ticket_a, ticket_b, *topology])
    db_session.commit()

    return {
        "session": db_session,
        "operator": operator,
        "technician_a": technician_a,
        "technician_b": technician_b,
        "customer_one": customer_one,
        "customer_two": customer_two,
        "granite": granite,
        "onu": onu,
        "olt": olt,
        "router": router,
        "other_device": other_device,
        "ticket_a": ticket_a,
        "ticket_b": ticket_b,
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


def test_assigned_work_list_returns_only_the_callers_tickets(db_session, workspace):
    records = ticket_queries.list_assigned_tickets(db_session, technician_a_actor(workspace))

    assert [record.id for record in records] == [workspace["ticket_a"].id]
    assert records[0].customer_ref == "CUST-1"
    assert records[0].service_type == "Granite"
    assert records[0].severity == "high"


def test_assigned_work_list_is_technician_only(db_session, workspace):
    with pytest.raises(HTTPException) as error:
        ticket_queries.list_assigned_tickets(db_session, operator_actor(workspace))
    assert error.value.status_code == 403


def test_technician_reads_own_ticket_detail_with_full_service_context(db_session, workspace):
    record = ticket_queries.get_ticket_detail(db_session, workspace["ticket_a"].id, technician_a_actor(workspace))

    assert record.ticket.id == workspace["ticket_a"].id
    assert record.customer.customer_ref == "CUST-1"
    assert {service.service_type for service in record.services} == {"Granite", "HSI", "VoBB"}
    assert {device.device_ref for device in record.devices} >= {"DEV-ONU-1", "DEV-OLT-1"}


def test_technician_cannot_read_another_technicians_ticket(db_session, workspace):
    with pytest.raises(HTTPException) as error:
        ticket_queries.get_ticket_detail(db_session, workspace["ticket_a"].id, technician_b_actor(workspace))
    assert error.value.status_code == 404


def test_operator_can_read_ticket_outside_technician_assignment(db_session, workspace):
    record = ticket_queries.get_ticket_detail(db_session, workspace["ticket_b"].id, operator_actor(workspace))
    assert record.ticket.id == workspace["ticket_b"].id


def test_customer_scope_limits_technician_to_assigned_customers(db_session, workspace):
    allowed = ticket_queries.get_customer_detail(db_session, workspace["customer_one"].id, technician_a_actor(workspace))
    assert allowed.customer.id == workspace["customer_one"].id

    with pytest.raises(ticket_queries.CustomerNotFoundError):
        ticket_queries.get_customer_detail(db_session, workspace["customer_two"].id, technician_a_actor(workspace))

    operator_view = ticket_queries.get_customer_detail(db_session, workspace["customer_two"].id, operator_actor(workspace))
    assert operator_view.customer.id == workspace["customer_two"].id


def test_topology_returns_ordered_path_with_real_device_status(db_session, workspace):
    record = ticket_queries.get_ticket_topology(db_session, workspace["ticket_a"].id, technician_a_actor(workspace))

    assert [node.device_ref for node in record.nodes] == ["DEV-OLT-1", "DEV-ONU-1"]
    assert record.nodes[0].status == "online"
    assert record.nodes[1].status == "offline"
    assert record.service_ref == "SVC-GR-1"


def test_topology_denies_another_technician(db_session, workspace):
    with pytest.raises(HTTPException) as error:
        ticket_queries.get_ticket_topology(db_session, workspace["ticket_a"].id, technician_b_actor(workspace))
    assert error.value.status_code == 404


def test_normal_ticket_response_contains_no_credential(db_session, workspace):
    app.dependency_overrides[get_session] = lambda: db_session
    try:
        app.dependency_overrides[get_current_user] = lambda: technician_a_actor(workspace)
        response = TestClient(app).get(f"/tickets/{workspace['ticket_a'].id}")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert SECRET not in response.text
    assert "onu_password" not in response.text
    body = response.json()
    assert body["ticket"]["id"] == workspace["ticket_a"].id
    assert all("details" not in device for device in body["devices"])


def test_tickets_mine_endpoint_returns_assignments_and_enforces_role(db_session, workspace):
    app.dependency_overrides[get_session] = lambda: db_session
    try:
        app.dependency_overrides[get_current_user] = lambda: technician_a_actor(workspace)
        allowed = TestClient(app).get("/tickets/mine")
        app.dependency_overrides[get_current_user] = lambda: operator_actor(workspace)
        denied = TestClient(app).get("/tickets/mine")
    finally:
        app.dependency_overrides.clear()

    assert allowed.status_code == 200
    assert [item["id"] for item in allowed.json()] == [workspace["ticket_a"].id]
    assert SECRET not in allowed.text
    assert denied.status_code == 403


def test_ticket_detail_endpoint_denies_another_technician(db_session, workspace):
    app.dependency_overrides[get_session] = lambda: db_session
    try:
        app.dependency_overrides[get_current_user] = lambda: technician_b_actor(workspace)
        response = TestClient(app).get(f"/tickets/{workspace['ticket_a'].id}")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 404


def test_ticket_topology_endpoint_returns_nodes_and_edges(db_session, workspace):
    app.dependency_overrides[get_session] = lambda: db_session
    try:
        app.dependency_overrides[get_current_user] = lambda: technician_a_actor(workspace)
        response = TestClient(app).get(f"/tickets/{workspace['ticket_a'].id}/topology")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    body = response.json()
    assert [node["device_ref"] for node in body["nodes"]] == ["DEV-OLT-1", "DEV-ONU-1"]
    assert body["service_ref"] == "SVC-GR-1"
    assert SECRET not in response.text
