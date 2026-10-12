"""Derived, embeddable entity facts for devices, services, and tickets.

Each entity group (a router, an optical reading, a VoBB service, a ticket's
TMFORCE metadata) is rendered into one secret-free text block and stored as a
retrievable ``EntityFactSheet``. The individual typed values are stored in
``EntityFact`` so the UI can render exact fields. Sensitive values never enter
the embedded content; they are marked ``is_sensitive`` and redacted on read.
"""

from dataclasses import dataclass
from datetime import UTC, datetime

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.ai.ports import EmbeddingProvider
from app.domain.models import EntityFact, EntityFactSheet, NetworkDevice, Service, Ticket

GROUP_TITLES = {
    "router": "Router details",
    "optical": "Optical signal",
    "client": "Client device",
    "vobb": "VoBB service",
    "iptv": "IPTV service",
    "tmforce": "Ticket operations",
}


@dataclass(frozen=True)
class FactField:
    key: str
    label: str
    numeric: bool = False
    sensitive: bool = False


DEVICE_FACT_GROUPS: dict[str, tuple[FactField, ...]] = {
    "router": (
        FactField("mac_address", "MAC address"),
        FactField("friendly_name", "Friendly name"),
        FactField("manufacturer", "Manufacturer"),
        FactField("device_type", "Device type"),
        FactField("cloud_device_type", "Cloud device type"),
        FactField("link_type", "Link type"),
        FactField("ip_address", "IP address"),
        FactField("ssid_2g", "SSID 2.4 GHz"),
        FactField("ssid_5g", "SSID 5 GHz"),
        FactField("channel_2g", "Channel 2.4 GHz", numeric=True),
        FactField("channel_5g", "Channel 5 GHz", numeric=True),
        FactField("antenna_2g", "Antenna 2.4 GHz"),
        FactField("antenna_5g", "Antenna 5 GHz"),
        FactField("protocol_2g", "Protocol 2.4 GHz"),
        FactField("protocol_5g", "Protocol 5 GHz"),
        FactField("bandwidth_2g", "Bandwidth 2.4 GHz"),
        FactField("bandwidth_5g", "Bandwidth 5 GHz"),
        FactField("platform", "Platform"),
        FactField("parent_mac", "Parent MAC"),
        FactField("last_seen", "Last seen"),
    ),
    "optical": (
        FactField("los_status", "LOS status"),
        FactField("rx_power_db", "dB reading", numeric=True),
    ),
    "client": (
        FactField("vendor", "Vendor"),
        FactField("mac_address", "MAC address"),
        FactField("ip_address", "IP address"),
        FactField("connection", "Connection"),
        FactField("band", "Band"),
        FactField("signal_dbm", "Signal (dBm)", numeric=True),
    ),
}

SERVICE_FACT_GROUPS: dict[str, tuple[FactField, ...]] = {
    "vobb": (
        FactField("vobb_status", "VoBB status"),
        FactField("service_number", "Service number"),
        FactField("vobb_password", "VoBB password", sensitive=True),
    ),
    "iptv": (
        FactField("iptv_login", "IPTV login"),
        FactField("iptv_password", "IPTV password", sensitive=True),
    ),
}

TICKET_FACT_FIELDS: tuple[FactField, ...] = (
    FactField("tm_ticket_no", "Ticket number"),
    FactField("ctt_activity_id", "Activity ID (CTT)"),
    FactField("login_id", "Login ID"),
    FactField("ticket_category", "Ticket category"),
    FactField("status", "Ticket status"),
    FactField("ticket_created_at", "Ticket created"),
    FactField("staff_code", "Staff ID"),
)


def sheet_id(entity_type: str, entity_id: str, group_key: str) -> str:
    return f"{entity_type}:{entity_id}:{group_key}"


_ACCESS_TYPES = frozenset({"router", "ap", "access point", "mesh", "extender", "gateway"})
_LINE_TYPES = frozenset({"onu", "ont", "olt", "switch"})


def device_group_key(device_type: str) -> str:
    normalized = device_type.strip().lower()
    if normalized in _ACCESS_TYPES:
        return "router"
    if normalized in _LINE_TYPES:
        return "optical"
    return "client"


def sync_device_facts(session: Session, device: NetworkDevice) -> None:
    details = device.details or {}
    group_key = device_group_key(device.device_type)
    fields = DEVICE_FACT_GROUPS[group_key]
    _sync_group(
        session,
        entity_type="device",
        entity_id=device.id,
        group_key=group_key,
        entity_label=device.name,
        fields=fields,
        values={field.key: details.get(field.key) for field in fields},
    )


def sync_service_facts(session: Session, service: Service) -> None:
    details = service.details or {}
    for group_key, fields in SERVICE_FACT_GROUPS.items():
        _sync_group(
            session,
            entity_type="service",
            entity_id=service.id,
            group_key=group_key,
            entity_label=service.service_type,
            fields=fields,
            values={field.key: details.get(field.key) for field in fields},
        )


def sync_ticket_facts(session: Session, ticket: Ticket) -> None:
    _sync_group(
        session,
        entity_type="ticket",
        entity_id=ticket.id,
        group_key="tmforce",
        entity_label=ticket.tm_ticket_no or ticket.summary[:60],
        fields=TICKET_FACT_FIELDS,
        values={field.key: getattr(ticket, field.key, None) for field in TICKET_FACT_FIELDS},
    )


def sync_customer_facts(session: Session, customer_id: str) -> None:
    for service in session.scalars(
        select(Service).where(Service.customer_id == customer_id)
    ).all():
        sync_service_facts(session, service)
    for device in session.scalars(
        select(NetworkDevice).where(NetworkDevice.customer_id == customer_id)
    ).all():
        sync_device_facts(session, device)


def sync_all_facts(session: Session) -> None:
    for service in session.scalars(select(Service)).all():
        sync_service_facts(session, service)
    for device in session.scalars(select(NetworkDevice)).all():
        sync_device_facts(session, device)
    for ticket in session.scalars(select(Ticket)).all():
        sync_ticket_facts(session, ticket)
    session.flush()


def list_facts_for_entities(session: Session, entity_ids: list[str]) -> list[EntityFact]:
    if not entity_ids:
        return []
    return list(
        session.scalars(
            select(EntityFact)
            .where(EntityFact.entity_id.in_(entity_ids))
            .order_by(
                EntityFact.entity_type,
                EntityFact.group_key,
                EntityFact.field_key,
            )
        ).all()
    )


def embed_missing_entity_facts(
    session: Session, embedder: EmbeddingProvider, *, reembed: bool = False
) -> tuple[int, int]:
    """Fill embeddings on every fact sheet that lacks one; reuse existing ones."""
    generated = 0
    reused = 0
    for sheet in session.scalars(select(EntityFactSheet).order_by(EntityFactSheet.id)).all():
        if sheet.embedding is not None and not reembed:
            reused += 1
            continue
        sheet.embedding = embedder.embed_documents([sheet.content])[0]
        generated += 1
    session.flush()
    return generated, reused


def _sync_group(
    session: Session,
    *,
    entity_type: str,
    entity_id: str,
    group_key: str,
    entity_label: str,
    fields: tuple[FactField, ...],
    values: dict[str, object],
) -> None:
    sheet_pk = sheet_id(entity_type, entity_id, group_key)
    session.execute(
        delete(EntityFact).where(
            EntityFact.entity_type == entity_type,
            EntityFact.entity_id == entity_id,
            EntityFact.group_key == group_key,
        )
    )

    rows: list[tuple[FactField, str, float | None]] = []
    for field in fields:
        raw = values.get(field.key)
        if raw is None or raw == "":
            continue
        rows.append((field, str(raw), _number(raw) if field.numeric else None))

    if not rows:
        sheet = session.get(EntityFactSheet, sheet_pk)
        if sheet is not None:
            session.delete(sheet)
        return

    now = datetime.now(UTC)
    content = "\n".join(
        f"{field.label}: {text}" for field, text, _ in rows if not field.sensitive
    )
    title = f"{entity_label} · {GROUP_TITLES[group_key]}"[:160]
    sheet = session.get(EntityFactSheet, sheet_pk)
    if sheet is None:
        session.add(
            EntityFactSheet(
                id=sheet_pk,
                entity_type=entity_type,
                entity_id=entity_id,
                group_key=group_key,
                title=title,
                content=content,
                embedding=None,
                updated_at=now,
            )
        )
    elif sheet.content != content or sheet.title != title:
        sheet.title = title
        sheet.content = content
        sheet.embedding = None
        sheet.updated_at = now

    for field, text, number in rows:
        session.add(
            EntityFact(
                entity_type=entity_type,
                entity_id=entity_id,
                group_key=group_key,
                field_key=field.key,
                label=field.label,
                value_text=text,
                value_number=number,
                is_sensitive=field.sensitive,
                source_updated_at=now,
            )
        )


def _number(value: object) -> float | None:
    try:
        return float(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return None
