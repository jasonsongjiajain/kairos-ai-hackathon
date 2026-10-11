import pytest
from fastapi import HTTPException

from app.auth.policy import (
    require_assigned_ticket,
    require_audit_scope,
    require_customer_for_assigned_ticket,
    require_customer_scope,
    require_role,
)


def test_technician_cannot_access_another_technicians_ticket_by_id():
    with pytest.raises(HTTPException) as error:
        require_assigned_ticket("technician-a", "technician-b", "technician")
    assert error.value.status_code == 404


def test_technician_cannot_access_customer_outside_assignment_scope():
    with pytest.raises(HTTPException) as error:
        require_customer_scope("technician-a", "technician-b", "technician")
    assert error.value.status_code == 404


def test_technician_cannot_access_customer_by_id_through_another_ticket():
    with pytest.raises(HTTPException) as error:
        require_customer_for_assigned_ticket("technician-a", "technician-b", "technician")
    assert error.value.status_code == 404


def test_operator_can_read_customer_for_assigned_ticket():
    require_customer_scope("operator-id", "technician-id", "operator")


def test_role_check_rejects_roles_not_in_policy():
    with pytest.raises(HTTPException) as error:
        require_role("technician", {"operator"})
    assert error.value.status_code == 403


def test_audit_scope_is_limited_to_technicians_own_records():
    with pytest.raises(HTTPException) as error:
        require_audit_scope("technician-a", "technician-b", "technician")
    assert error.value.status_code == 404
