from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.auth.dependencies import AuthenticatedUser
from app.auth.policy import require_role
from app.domain import event_rules
from app.domain.models import NetworkDevice, Ticket, User
from app.repositories import events as events_repo
from app.repositories import tickets as tickets_repo


class EventNotFoundError(Exception):
    pass


class EventNotActionableError(Exception):
    pass


class NoTechnicianAvailableError(Exception):
    pass


@dataclass(frozen=True)
class ProcessEventResult:
    ticket: Ticket
    created: bool
    source_event_id: str
    assigned_technician_name: str


def list_pending_events(session: Session, actor: AuthenticatedUser) -> list[events_repo.PendingEventRecord]:
    require_role(actor.role, event_rules.EVENT_PROCESSING_ROLES)
    return events_repo.list_pending(session)


def process_event(session: Session, event_id: str, actor: AuthenticatedUser) -> ProcessEventResult:
    require_role(actor.role, event_rules.EVENT_PROCESSING_ROLES)

    event = events_repo.get_by_id_for_update(session, event_id)
    if event is None:
        raise EventNotFoundError(event_id)

    existing = tickets_repo.get_by_source_event(session, event.id)
    if existing is not None:
        return _duplicate_result(session, existing, event.source_event_id)

    device = session.get(NetworkDevice, event.device_id)
    customer_id = device.customer_id if device is not None else None
    if customer_id is None:
        raise EventNotActionableError(event_id)

    technician = event_rules.select_technician(session)
    if technician is None:
        raise NoTechnicianAvailableError(event_id)

    ticket = Ticket(
        source_event_id=event.id,
        customer_id=customer_id,
        service_id=event.service_id,
        assigned_technician_id=technician.id,
        severity=event_rules.severity_for_event(event.event_type),
        status="open",
        summary=event_rules.summary_for_event(event, device),
    )

    try:
        tickets_repo.add(session, ticket)
        session.flush()
        event.processed_at = datetime.now(UTC)
        events_repo.record_audit_event(
            session,
            actor_id=actor.id,
            ticket_id=ticket.id,
            source_event_id=event.source_event_id,
            assigned_technician_id=technician.id,
            severity=ticket.severity,
        )
        session.commit()
    except IntegrityError:
        session.rollback()
        duplicate = tickets_repo.get_by_source_event(session, event.id)
        if duplicate is None:
            raise
        return _duplicate_result(session, duplicate, event.source_event_id)
    except Exception:
        session.rollback()
        raise

    return ProcessEventResult(
        ticket=ticket,
        created=True,
        source_event_id=event.source_event_id,
        assigned_technician_name=technician.display_name,
    )


def _duplicate_result(session: Session, ticket: Ticket, source_event_id: str) -> ProcessEventResult:
    technician = session.get(User, ticket.assigned_technician_id)
    return ProcessEventResult(
        ticket=ticket,
        created=False,
        source_event_id=source_event_id,
        assigned_technician_name=technician.display_name if technician is not None else "",
    )
