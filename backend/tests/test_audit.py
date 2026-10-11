import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.db.session import get_session
from app.main import app
from app.services import audit_query, tool_execution

SECRET = "Synthetic-ONU-Credential-Only-7f3!"


def actor(workspace, key: str, role: str) -> AuthenticatedUser:
    user = workspace[key]
    return AuthenticatedUser(id=user.id, email=user.email, role=role)


def test_audit_lists_events_for_assigned_technician(db_session, tool_workspace):
    technician = actor(tool_workspace, "technician_a", "technician")
    proposal = tool_execution.propose_tool(
        db_session,
        tool_workspace["ticket"].id,
        technician,
        "reboot_router",
        {"device_id": tool_workspace["router"].id},
    )
    tool_execution.confirm_tool(
        db_session, tool_workspace["ticket"].id, proposal.id, technician, proposal.correlation_id
    )

    records = audit_query.list_ticket_audit(db_session, tool_workspace["ticket"].id, technician)
    event_types = [record.event_type for record in records]

    assert "tool_proposed" in event_types
    assert "tool_executed" in event_types
    assert all(record.ticket_id == tool_workspace["ticket"].id for record in records)
    assert any(record.actor_name == "Technician A" for record in records)


def test_audit_denies_another_technician(db_session, tool_workspace):
    with pytest.raises(HTTPException) as error:
        audit_query.list_ticket_audit(
            db_session,
            tool_workspace["ticket"].id,
            actor(tool_workspace, "technician_b", "technician"),
        )
    assert error.value.status_code == 404


def test_operator_can_read_audit_scope(db_session, tool_workspace):
    records = audit_query.list_ticket_audit(
        db_session, tool_workspace["ticket"].id, actor(tool_workspace, "operator", "operator")
    )
    assert isinstance(records, list)


def test_audit_endpoint_returns_events_without_secrets(db_session, tool_workspace):
    technician = actor(tool_workspace, "technician_a", "technician")
    proposal = tool_execution.propose_tool(
        db_session,
        tool_workspace["ticket"].id,
        technician,
        "reboot_router",
        {"device_id": tool_workspace["router"].id},
    )
    tool_execution.confirm_tool(
        db_session, tool_workspace["ticket"].id, proposal.id, technician, proposal.correlation_id
    )

    app.dependency_overrides[get_session] = lambda: db_session
    try:
        app.dependency_overrides[get_current_user] = lambda: technician
        response = TestClient(app).get(f"/tickets/{tool_workspace['ticket'].id}/audit")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert SECRET not in response.text
    body = response.json()
    assert any(item["event_type"] == "tool_executed" for item in body)
