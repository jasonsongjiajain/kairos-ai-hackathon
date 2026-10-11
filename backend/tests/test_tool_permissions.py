import pytest

from app.auth.dependencies import AuthenticatedUser
from app.services import tool_execution
from app.services.tool_execution import (
    ToolForbiddenError,
    ToolNotFoundError,
    ToolValidationError,
)


def actor(workspace, key: str, role: str) -> AuthenticatedUser:
    user = workspace[key]
    return AuthenticatedUser(id=user.id, email=user.email, role=role)


def test_unknown_tool_is_rejected(db_session, tool_workspace):
    with pytest.raises(ToolNotFoundError):
        tool_execution.propose_tool(
            db_session, tool_workspace["ticket"].id, actor(tool_workspace, "technician_a", "technician"),
            "drop_database", {"device_id": tool_workspace["router"].id},
        )


def test_operator_cannot_propose_a_stateful_tool(db_session, tool_workspace):
    with pytest.raises(ToolForbiddenError):
        tool_execution.propose_tool(
            db_session, tool_workspace["ticket"].id, actor(tool_workspace, "operator", "operator"),
            "reboot_router", {"device_id": tool_workspace["router"].id},
        )


def test_unassigned_technician_cannot_propose(db_session, tool_workspace):
    with pytest.raises(ToolNotFoundError):
        tool_execution.propose_tool(
            db_session, tool_workspace["ticket"].id, actor(tool_workspace, "technician_b", "technician"),
            "reboot_router", {"device_id": tool_workspace["router"].id},
        )


def test_device_outside_the_ticket_customer_is_rejected(db_session, tool_workspace):
    with pytest.raises(ToolForbiddenError):
        tool_execution.propose_tool(
            db_session, tool_workspace["ticket"].id, actor(tool_workspace, "technician_a", "technician"),
            "reboot_router", {"device_id": tool_workspace["other_device"].id},
        )


def test_wrong_device_type_is_rejected(db_session, tool_workspace):
    with pytest.raises(ToolForbiddenError):
        tool_execution.propose_tool(
            db_session, tool_workspace["ticket"].id, actor(tool_workspace, "technician_a", "technician"),
            "reboot_router", {"device_id": tool_workspace["onu"].id},
        )


@pytest.mark.parametrize("settings", [{"wifi_channel": 99}, {"tx_power_dbm": -1}, {"unsupported_key": 1}, {}])
def test_invalid_configuration_is_rejected(db_session, tool_workspace, settings):
    with pytest.raises(ToolValidationError):
        tool_execution.propose_tool(
            db_session, tool_workspace["ticket"].id, actor(tool_workspace, "technician_a", "technician"),
            "update_config", {"device_id": tool_workspace["router"].id, "settings": settings},
        )


def test_missing_approval_is_rejected(db_session, tool_workspace):
    proposal = tool_execution.propose_tool(
        db_session, tool_workspace["ticket"].id, actor(tool_workspace, "technician_a", "technician"),
        "reboot_router", {"device_id": tool_workspace["router"].id},
    )
    with pytest.raises(ToolForbiddenError):
        tool_execution.confirm_tool(
            db_session, tool_workspace["ticket"].id, proposal.id,
            actor(tool_workspace, "technician_a", "technician"), "wrong-confirmation-id",
        )


def test_replayed_confirmation_id_does_not_execute_twice(db_session, tool_workspace):
    technician = actor(tool_workspace, "technician_a", "technician")
    proposal = tool_execution.propose_tool(
        db_session, tool_workspace["ticket"].id, technician,
        "reboot_router", {"device_id": tool_workspace["router"].id},
    )
    first = tool_execution.confirm_tool(
        db_session, tool_workspace["ticket"].id, proposal.id, technician, proposal.correlation_id
    )
    second = tool_execution.confirm_tool(
        db_session, tool_workspace["ticket"].id, proposal.id, technician, proposal.correlation_id
    )

    assert first.status == "succeeded"
    assert second.status == "succeeded"
    assert second.executed_at == first.executed_at
