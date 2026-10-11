from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import Ticket


def get_by_source_event(session: Session, event_id: str) -> Ticket | None:
    return session.scalar(select(Ticket).where(Ticket.source_event_id == event_id))


def add(session: Session, ticket: Ticket) -> Ticket:
    session.add(ticket)
    return ticket
