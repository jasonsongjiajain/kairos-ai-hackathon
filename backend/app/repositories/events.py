from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import AuditEvent, NetworkDevice, NetworkEvent, Service


@dataclass(frozen=True)
class PendingEventRecord:
    id: str
    source_event_id: str
    event_type: str
    device_id: str
    device_ref: str
    device_name: str
    device_status: str
    service_id: str | None
    service_ref: str | None
    payload: dict
    received_at: datetime


def list_pending(session: Session) -> list[PendingEventRecord]:
    rows = session.execute(
        select(NetworkEvent, NetworkDevice, Service)
        .join(NetworkDevice, NetworkDevice.id == NetworkEvent.device_id)
        .outerjoin(Service, Service.id == NetworkEvent.service_id)
        .where(NetworkEvent.processed_at.is_(None))
        .order_by(NetworkEvent.received_at, NetworkEvent.id)
    ).all()
    return [
        PendingEventRecord(
            id=event.id,
            source_event_id=event.source_event_id,
            event_type=event.event_type,
            device_id=event.device_id,
            device_ref=device.device_ref,
            device_name=device.name,
            device_status=device.status,
            service_id=event.service_id,
            service_ref=service.service_ref if service is not None else None,
            payload=event.payload,
            received_at=event.received_at,
        )
        for event, device, service in rows
    ]


def get_by_id(session: Session, event_id: str) -> NetworkEvent | None:
    return session.get(NetworkEvent, event_id)


def get_by_id_for_update(session: Session, event_id: str) -> NetworkEvent | None:
    return session.scalar(
        select(NetworkEvent).where(NetworkEvent.id == event_id).with_for_update()
    )


def record_audit_event(
    session: Session,
    *,
    actor_id: str,
    ticket_id: str,
    source_event_id: str,
    assigned_technician_id: str,
    severity: str,
) -> AuditEvent:
    audit = AuditEvent(
        actor_id=actor_id,
        ticket_id=ticket_id,
        event_type="event_processed",
        details={
            "source_event_id": source_event_id,
            "ticket_id": ticket_id,
            "assigned_technician_id": assigned_technician_id,
            "severity": severity,
        },
    )
    session.add(audit)
    return audit
