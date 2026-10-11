from pathlib import Path

from argon2 import PasswordHasher
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domain.models import (
    Customer, KnowledgeChunk, KnowledgeDocument, NetworkDevice, NetworkEvent,
    Role, Service, TopologyEdge, User,
)

DEMO_ACCOUNTS = {
    "operator@demo.invalid": "Demo-Operator-Only-2026!",
    "technician@demo.invalid": "Demo-Technician-Only-2026!",
}
KNOWLEDGE_DIR = Path(__file__).resolve().parents[2] / "seed" / "knowledge"


def seed_demo_data(session: Session) -> dict[str, int]:
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
    for email, password in DEMO_ACCOUNTS.items():
        user = session.scalar(select(User).where(User.email == email))
        if user is None:
            name = "Demo Operator" if "operator" in email else "Demo Technician"
            session.add(User(email=email, display_name=name, password_hash=hasher.hash(password), role_id=roles[account_roles[email]].id, is_demo=True))

    customer = session.scalar(select(Customer).where(Customer.customer_ref == "DEMO-CUST-001"))
    if customer is None:
        customer = Customer(customer_ref="DEMO-CUST-001", name="Sample Household (Demo)", address="100 Example Lane, Sampleton", is_demo=True)
        session.add(customer)
        session.flush()

    services = {}
    for kind, ref in (("Granite", "DEMO-GR-001"), ("HSI", "DEMO-HSI-001"), ("VoBB", "DEMO-VOBB-001")):
        service = session.scalar(select(Service).where(Service.service_ref == ref))
        if service is None:
            service = Service(customer_id=customer.id, service_type=kind, service_ref=ref, status="active", details={"demo": True})
            session.add(service)
            session.flush()
        services[kind] = service

    devices = {}
    for ref, dtype, name, status, details in (
        ("DEMO-OLT-001", "OLT", "Demo access node", "online", {}),
        ("DEMO-ONT-001", "ONU", "Demo optical network unit", "offline", {"onu_password": "Synthetic-ONU-Credential-Only-7f3!"}),
        ("DEMO-RTR-001", "router", "Demo home router", "unreachable", {}),
    ):
        device = session.scalar(select(NetworkDevice).where(NetworkDevice.device_ref == ref))
        if device is None:
            device = NetworkDevice(customer_id=customer.id, device_ref=ref, device_type=dtype, name=name, status=status, details=details)
            session.add(device)
            session.flush()
        devices[ref] = device

    for upstream, downstream, service in (("DEMO-OLT-001", "DEMO-ONT-001", services["Granite"]), ("DEMO-ONT-001", "DEMO-RTR-001", services["HSI"])):
        exists = session.scalar(select(TopologyEdge).where(TopologyEdge.source_device_id == devices[upstream].id, TopologyEdge.target_device_id == devices[downstream].id))
        if not exists:
            session.add(TopologyEdge(source_device_id=devices[upstream].id, target_device_id=devices[downstream].id, service_id=service.id))

    if session.scalar(select(NetworkEvent).where(NetworkEvent.source_event_id == "DEMO-EVENT-ONU-OFFLINE-001")) is None:
        session.add(NetworkEvent(source_event_id="DEMO-EVENT-ONU-OFFLINE-001", event_type="ONU_OFFLINE", device_id=devices["DEMO-ONT-001"].id, service_id=services["Granite"].id, payload={"demo": True, "signal_state": "no_link"}))

    for path in sorted(KNOWLEDGE_DIR.glob("*.md")):
        document_id, title, version, *section_data = path.read_text().splitlines()
        document = session.get(KnowledgeDocument, document_id)
        if document is None:
            document = KnowledgeDocument(id=document_id, document_key=document_id, title=title, source_type="curated_procedure", version=version)
            session.add(document)
            session.flush()
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
            if session.get(KnowledgeChunk, chunk_id) is None:
                session.add(KnowledgeChunk(id=chunk_id, document_id=document.id, section=section, content="\n".join(lines)))

    session.commit()
    pending = session.scalar(select(func.count()).select_from(NetworkEvent).where(NetworkEvent.processed_at.is_(None)))
    accounts = session.scalar(select(func.count()).select_from(User).where(User.email.in_(DEMO_ACCOUNTS)))
    if pending != 1 or accounts != len(DEMO_ACCOUNTS):
        raise RuntimeError(f"Seed verification failed: pending_events={pending}, demo_accounts={accounts}")
    return {"pending_events": pending, "demo_accounts": accounts}


def main() -> None:
    from app.db.session import SessionLocal

    with SessionLocal() as session:
        result = seed_demo_data(session)
    print(f"Seed verified: {result['pending_events']} pending event; {result['demo_accounts']} demo accounts")


if __name__ == "__main__":
    main()
