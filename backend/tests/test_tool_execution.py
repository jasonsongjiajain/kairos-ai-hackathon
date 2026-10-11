from sqlalchemy import func, select

from app.auth.dependencies import AuthenticatedUser
from app.domain.models import AuditEvent
from app.services import tool_execution


def actor(workspace, key: str, role: str) -> AuthenticatedUser:
    user = workspace[key]
    return AuthenticatedUser(id=user.id, email=user.email, role=role)


def audit_count(session, event_type: str) -> int:
    return session.scalar(
        select(func.count()).select_from(AuditEvent).where(AuditEvent.event_type == event_type)
    )


def test_proposal_does_not_change_device_until_confirmed(db_session, tool_workspace):
    technician = actor(tool_workspace, "technician_a", "technician")
    router = tool_workspace["router"]

    proposal = tool_execution.propose_tool(
        db_session, tool_workspace["ticket"].id, technician,
        "reboot_router", {"device_id": router.id},
    )

    assert proposal.status == "proposed"
    assert proposal.requires_confirmation is True
    assert router.status == "unreachable"
    assert audit_count(db_session, "tool_proposed") == 1
    assert audit_count(db_session, "tool_executed") == 0


def test_confirm_executes_and_updates_device_state(db_session, tool_workspace):
    technician = actor(tool_workspace, "technician_a", "technician")
    router = tool_workspace["router"]

    proposal = tool_execution.propose_tool(
        db_session, tool_workspace["ticket"].id, technician,
        "reboot_router", {"device_id": router.id},
    )
    result = tool_execution.confirm_tool(
        db_session, tool_workspace["ticket"].id, proposal.id, technician, proposal.correlation_id
    )

    assert result.status == "succeeded"
    assert result.message
    db_session.refresh(router)
    assert router.status == "online"
    assert audit_count(db_session, "tool_executed") == 1
    executed = db_session.scalar(select(AuditEvent).where(AuditEvent.event_type == "tool_executed"))
    assert executed.ticket_id == tool_workspace["ticket"].id
    assert executed.details["outcome"] == "succeeded"


def test_read_only_tool_reports_status_without_confirmation_change(db_session, tool_workspace):
    technician = actor(tool_workspace, "technician_a", "technician")
    proposal = tool_execution.propose_tool(
        db_session, tool_workspace["ticket"].id, technician,
        "get_device_status", {"device_id": tool_workspace["onu"].id},
    )
    result = tool_execution.confirm_tool(
        db_session, tool_workspace["ticket"].id, proposal.id, technician, proposal.correlation_id
    )

    assert result.status == "succeeded"
    assert "offline" in result.message


def test_update_config_applies_bounded_settings(db_session, tool_workspace):
    technician = actor(tool_workspace, "technician_a", "technician")
    router = tool_workspace["router"]
    proposal = tool_execution.propose_tool(
        db_session, tool_workspace["ticket"].id, technician,
        "update_config", {"device_id": router.id, "settings": {"wifi_channel": 6, "tx_power_dbm": 18}},
    )
    result = tool_execution.confirm_tool(
        db_session, tool_workspace["ticket"].id, proposal.id, technician, proposal.correlation_id
    )

    assert result.status == "succeeded"
    db_session.refresh(router)
    assert router.details["settings"] == {"wifi_channel": 6, "tx_power_dbm": 18}


def test_list_proposals_requires_ticket_access(db_session, tool_workspace):
    technician = actor(tool_workspace, "technician_a", "technician")
    tool_execution.propose_tool(
        db_session, tool_workspace["ticket"].id, technician,
        "reboot_router", {"device_id": tool_workspace["router"].id},
    )
    records = tool_execution.list_proposals(db_session, tool_workspace["ticket"].id, technician)
    assert len(records) == 1
    assert records[0].tool_name == "reboot_router"
