from collections.abc import Iterable

from fastapi import HTTPException, status


def require_role(user_role: str, allowed_roles: Iterable[str]) -> None:
    if user_role not in allowed_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")


def require_assigned_ticket(user_id: str, assigned_technician_id: str, user_role: str) -> None:
    if user_role == "technician" and user_id != assigned_technician_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found")


def require_customer_scope(
    user_id: str,
    user_role: str,
    *,
    allowed_roles: Iterable[str],
    ticket_assignee_id: str,
    ticket_customer_id: str,
    requested_customer_id: str,
) -> None:
    if requested_customer_id != ticket_customer_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    if user_role == "technician":
        if user_id != ticket_assignee_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
        return
    require_role(user_role, allowed_roles)


def require_audit_scope(user_id: str, audit_actor_id: str | None, user_role: str) -> None:
    if user_role == "technician" and audit_actor_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audit record not found")
