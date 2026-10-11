"""Assignment-scoped audit history queries."""

from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import AuthenticatedUser
from app.auth.policy import require_assigned_ticket
from app.domain.models import AuditEvent, Ticket, User

TICKET_FULL_SCOPE_ROLES = ("operator", "supervisor")


class AuditScopeError(Exception):
    pass


@dataclass(frozen=True)
class AuditEventRecord:
    id: str
    event_type: str
    actor_id: str | None
    actor_name: str | None
    ticket_id: str | None
    details: dict
    created_at: datetime


def list_ticket_audit(session: Session, ticket_id: str, actor: AuthenticatedUser) -> list[AuditEventRecord]:
    ticket = session.get(Ticket, ticket_id)
    if ticket is None:
        raise AuditScopeError(ticket_id)
    if actor.role == "technician":
        require_assigned_ticket(actor.id, ticket.assigned_technician_id, actor.role)
    elif actor.role not in TICKET_FULL_SCOPE_ROLES:
        raise AuditScopeError(ticket_id)

    rows = list(
        session.scalars(
            select(AuditEvent)
            .where(AuditEvent.ticket_id == ticket_id)
            .order_by(AuditEvent.created_at, AuditEvent.id)
        ).all()
    )
    actor_ids = {row.actor_id for row in rows if row.actor_id is not None}
    names = _actor_names(session, actor_ids)
    return [
        AuditEventRecord(
            id=row.id,
            event_type=row.event_type,
            actor_id=row.actor_id,
            actor_name=names.get(row.actor_id or ""),
            ticket_id=row.ticket_id,
            details=row.details or {},
            created_at=row.created_at or datetime.now(UTC),
        )
        for row in rows
    ]


def _actor_names(session: Session, actor_ids: set[str]) -> dict[str, str]:
    if not actor_ids:
        return {}
    return {
        user.id: user.display_name
        for user in session.scalars(select(User).where(User.id.in_(actor_ids))).all()
    }
