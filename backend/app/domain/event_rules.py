"""Deterministic rules that turn a network event into an assigned ticket.

Assignment rule (single, documented):
    Assign the ticket to the lowest-id active user whose role is "technician".
    The demo seed contains exactly one technician, so the rule resolves to that
    technician. When more than one active technician exists, ordering by user id
    keeps the choice deterministic and repeatable for tests and demos.

Severity rule (single, documented):
    Event types with a known outage meaning map to "high". Any other event type
    falls back to "medium". The mapping is explicit so the value is auditable.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import NetworkDevice, NetworkEvent, Role, User

EVENT_PROCESSING_ROLES = ("operator", "supervisor")

_SEVERITY_BY_EVENT_TYPE = {
    "ONU_OFFLINE": "high",
    "OPTICAL_LOSS": "high",
}
_DEFAULT_SEVERITY = "medium"


def severity_for_event(event_type: str) -> str:
    return _SEVERITY_BY_EVENT_TYPE.get(event_type, _DEFAULT_SEVERITY)


def select_technician(session: Session) -> User | None:
    return session.scalar(
        select(User)
        .join(Role, Role.id == User.role_id)
        .where(Role.name == "technician", User.is_active.is_(True))
        .order_by(User.id)
        .limit(1)
    )


def summary_for_event(event: NetworkEvent, device: NetworkDevice | None) -> str:
    target = device.name if device is not None else event.device_id
    return f"{event.event_type} reported for {target}"[:255]
