"""Local synthetic demo seed, disabled unless DEMO_SEED_ENABLED is explicitly true.

Knowledge section headings must be lowercase ASCII slug-safe because they form chunk IDs.
"""

from pathlib import Path

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import Settings
from app.domain.models import (
    Customer, KnowledgeChunk, KnowledgeDocument, NetworkDevice, NetworkEvent,
    Role, Service, TopologyEdge, User,
)

DEMO_ACCOUNTS = {
    "operator@demo.invalid": "Demo-Operator-Only-2026!",
    "technician@demo.invalid": "Demo-Technician-Only-2026!",
}
DEMO_EVENT_SOURCE_ID = "DEMO-EVENT-ONU-OFFLINE-001"

CUSTOMERS = (
    {"ref": "DEMO-CUST-001", "name": "Sample Household (Demo)", "address": "100 Example Lane, Sampleton"},
    {"ref": "DEMO-CUST-002", "name": "Riverbend Cafe (Demo)", "address": "42 Riverside Walk, Sampleton"},
)

SERVICES = (
    ("DEMO-CUST-001", "Granite", "DEMO-GR-001"),
    ("DEMO-CUST-001", "HSI", "DEMO-HSI-001"),
    ("DEMO-CUST-001", "VoBB", "DEMO-VOBB-001"),
    ("DEMO-CUST-002", "Granite", "DEMO-GR-002"),
    ("DEMO-CUST-002", "HSI", "DEMO-HSI-002"),
    ("DEMO-CUST-002", "VoBB", "DEMO-VOBB-002"),
)

DEVICES = (
    ("DEMO-CUST-001", "DEMO-OLT-001", "OLT", "Demo access node", "online", {}),
    ("DEMO-CUST-001", "DEMO-ONT-001", "ONU", "Demo optical network unit", "offline", {"onu_password": "Synthetic-ONU-Credential-Only-7f3!"}),
    ("DEMO-CUST-001", "DEMO-RTR-001", "router", "Demo home router", "unreachable", {}),
    ("DEMO-CUST-002", "DEMO-OLT-002", "OLT", "Riverbend access node", "online", {}),
    ("DEMO-CUST-002", "DEMO-ONT-002", "ONU", "Riverbend optical network unit", "degraded", {"onu_password": "Synthetic-ONU-Credential-Only-2c9!"}),
    ("DEMO-CUST-002", "DEMO-RTR-002", "router", "Riverbend home router", "online", {"wifi_password": "Synthetic-WiFi-Credential-Only-4a6!"}),
)

TOPOLOGY_EDGES = (
    ("DEMO-OLT-001", "DEMO-ONT-001", "DEMO-GR-001"),
    ("DEMO-ONT-001", "DEMO-RTR-001", "DEMO-HSI-001"),
    ("DEMO-OLT-002", "DEMO-ONT-002", "DEMO-GR-002"),
    ("DEMO-ONT-002", "DEMO-RTR-002", "DEMO-HSI-002"),
)

EVENTS = (
    {
        "source_event_id": DEMO_EVENT_SOURCE_ID,
        "event_type": "ONU_OFFLINE",
        "device_ref": "DEMO-ONT-001",
        "service_ref": "DEMO-GR-001",
        "payload": {"demo": True, "signal_state": "no_link"},
    },
    {
        "source_event_id": "DEMO-EVENT-OPTICAL-LOSS-001",
        "event_type": "OPTICAL_LOSS",
        "device_ref": "DEMO-ONT-002",
        "service_ref": "DEMO-GR-002",
        "payload": {"demo": True, "loss_db": 34.5},
    },
    {
        "source_event_id": "DEMO-EVENT-HSI-DEGRADED-001",
        "event_type": "HSI_DEGRADED",
        "device_ref": "DEMO-RTR-001",
        "service_ref": "DEMO-HSI-001",
        "payload": {"demo": True, "download_mbps": 12, "expected_mbps": 500},
    },
)
DEMO_EVENT_SOURCE_IDS = tuple(event["source_event_id"] for event in EVENTS)
KNOWLEDGE_DIR = Path(__file__).resolve().parents[2] / "seed" / "knowledge"


def seed_demo_data(session: Session) -> dict[str, int]:
    if not Settings().demo_seed_enabled:
        raise RuntimeError("Demo seeding is disabled. Set DEMO_SEED_ENABLED=true only in a local/demo environment.")
    try:
        return _seed_demo_data(session)
    except Exception:
        session.rollback()
        raise


def _seed_demo_data(session: Session) -> dict[str, int]:
    hasher = PasswordHasher()
    roles = {}
    for name in ("operator", "technician"):
        role = session.scalar(select(Role).where(Role.name == name))
        if role is None:
            role = Role(name=name)
            session.add(role)
            session.flush()
        roles[name] = role

    account_roles = {"operator@demo.invalid": "operator", "technician@demo.invalid": "technician"}
    account_names = {"operator@demo.invalid": "Demo Operator", "technician@demo.invalid": "Demo Technician"}
    for email, password in DEMO_ACCOUNTS.items():
        user = session.scalar(select(User).where(User.email == email))
        if user is None:
            user = User(email=email, display_name=account_names[email], password_hash=hasher.hash(password), role_id=roles[account_roles[email]].id, is_active=True, is_demo=True)
            session.add(user)
        _require_canonical(
            user,
            display_name=account_names[email],
            role_id=roles[account_roles[email]].id,
            is_active=True,
            is_demo=True,
        )
        try:
            password_matches = hasher.verify(user.password_hash, password)
        except VerificationError:
            password_matches = False
        if not password_matches:
            raise RuntimeError(f"Seed conflict for demo account {email}: password hash does not match demo credentials")

    customers = {}
    for spec in CUSTOMERS:
        customer = session.scalar(select(Customer).where(Customer.customer_ref == spec["ref"]))
        if customer is None:
            customer = Customer(customer_ref=spec["ref"], name=spec["name"], address=spec["address"], is_demo=True)
            session.add(customer)
            session.flush()
        _require_canonical(customer, name=spec["name"], address=spec["address"], is_demo=True)
        customers[spec["ref"]] = customer

    services = {}
    for customer_ref, kind, ref in SERVICES:
        service = session.scalar(select(Service).where(Service.service_ref == ref))
        if service is None:
            service = Service(customer_id=customers[customer_ref].id, service_type=kind, service_ref=ref, status="active", details={"demo": True})
            session.add(service)
            session.flush()
        _require_canonical(service, customer_id=customers[customer_ref].id, service_type=kind, status="active", details={"demo": True})
        services[ref] = service

    devices = {}
    for customer_ref, ref, dtype, name, status, details in DEVICES:
        device = session.scalar(select(NetworkDevice).where(NetworkDevice.device_ref == ref))
        if device is None:
            device = NetworkDevice(customer_id=customers[customer_ref].id, device_ref=ref, device_type=dtype, name=name, status=status, details=details)
            session.add(device)
            session.flush()
        _require_canonical(device, customer_id=customers[customer_ref].id, device_type=dtype, name=name, status=status, details=details)
        devices[ref] = device

    for upstream, downstream, service_ref in TOPOLOGY_EDGES:
        edge = session.scalar(select(TopologyEdge).where(TopologyEdge.source_device_id == devices[upstream].id, TopologyEdge.target_device_id == devices[downstream].id))
        if edge is None:
            edge = TopologyEdge(source_device_id=devices[upstream].id, target_device_id=devices[downstream].id, service_id=services[service_ref].id)
            session.add(edge)
        _require_canonical(edge, service_id=services[service_ref].id)

    for spec in EVENTS:
        event = session.scalar(select(NetworkEvent).where(NetworkEvent.source_event_id == spec["source_event_id"]))
        if event is None:
            event = NetworkEvent(source_event_id=spec["source_event_id"], event_type=spec["event_type"], device_id=devices[spec["device_ref"]].id, service_id=services[spec["service_ref"]].id, payload=spec["payload"])
            session.add(event)
        _require_canonical(event, event_type=spec["event_type"], device_id=devices[spec["device_ref"]].id, service_id=services[spec["service_ref"]].id, payload=spec["payload"], processed_at=None)

    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        document_id, title, version, *section_data = path.read_text().splitlines()
        document = session.get(KnowledgeDocument, document_id)
        if document is None:
            document = KnowledgeDocument(id=document_id, document_key=document_id, title=title, source_type="curated_procedure", version=version)
            session.add(document)
            session.flush()
        _require_canonical(document, document_key=document_id, title=title, source_type="curated_procedure", version=version)
        sections = {}
        current = None
        for line in section_data:
            if line.startswith("## "):
                current = line[3:].strip()
                sections[current] = []
            elif current and line.strip():
                sections[current].append(line.strip())
        for section, lines in sections.items():
            chunk_id = f"{document_id}:{version}:{section.lower().replace(' ', '-')}"
            content = "\n".join(lines)
            chunk = session.get(KnowledgeChunk, chunk_id)
            if chunk is None:
                chunk = KnowledgeChunk(id=chunk_id, document_id=document.id, section=section, content=content)
                session.add(chunk)
            _require_canonical(chunk, document_id=document.id, section=section, content=content)

    session.flush()
    pending_count = session.scalar(
        select(func.count())
        .select_from(NetworkEvent)
        .where(
            NetworkEvent.source_event_id.in_(DEMO_EVENT_SOURCE_IDS),
            NetworkEvent.processed_at.is_(None),
        )
    )
    if pending_count != len(EVENTS):
        raise RuntimeError(
            f"Seed verification failed: expected {len(EVENTS)} pending demo events, found {pending_count}"
        )

    expected_roles = {"operator@demo.invalid": "operator", "technician@demo.invalid": "technician"}
    verified_accounts = 0
    for email, role_name in expected_roles.items():
        user = session.scalar(select(User).where(User.email == email))
        if user is None or user.role_id != roles[role_name].id or not user.is_active:
            raise RuntimeError(f"Seed verification failed for demo account {email}")
        verified_accounts += 1

    session.commit()
    return {"pending_events": len(EVENTS), "demo_accounts": verified_accounts}


def _require_canonical(row, **expected_fields) -> None:
    divergent = [name for name, expected in expected_fields.items() if getattr(row, name) != expected]
    if divergent:
        identity = getattr(row, "email", None) or getattr(row, "customer_ref", None) or getattr(row, "service_ref", None) or getattr(row, "device_ref", None) or getattr(row, "source_event_id", None) or getattr(row, "id", "unknown")
        raise RuntimeError(f"Seed conflict for demo row {identity}: noncanonical fields {', '.join(divergent)}")


def main() -> None:
    from app.db.session import SessionLocal

    with SessionLocal() as session:
        result = seed_demo_data(session)
    print(f"Seed verified: {result['pending_events']} pending events; {result['demo_accounts']} demo accounts")


if __name__ == "__main__":
    main()
