"""Local synthetic demo seed, disabled unless DEMO_SEED_ENABLED is explicitly true.

Synthetic stand-in for real Malaysian field-operations data. Knowledge section
headings must be lowercase ASCII slug-safe because they form chunk IDs.
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
from app.services.entity_facts import sync_device_facts, sync_service_facts

DEMO_ACCOUNTS = {
    "operator@demo.invalid": "Demo-Operator-Only-2026!",
    "technician@demo.invalid": "Demo-Technician-Only-2026!",
}
DEMO_STAFF_CODES = {
    "operator@demo.invalid": "OP1042",
    "technician@demo.invalid": "TM1234",
}
DEMO_EVENT_SOURCE_ID = "MY-EVENT-ONU-OFFLINE-001"

CUSTOMERS = (
    {
        "ref": "MY-CUST-001",
        "name": "Ahmad Faizal bin Ramli",
        "address": "No. 12, Jalan SS2/24, Taman Sea, 47300 Petaling Jaya, Selangor",
    },
    {
        "ref": "MY-CUST-002",
        "name": "Kopi Tarik Corner Sdn Bhd",
        "address": "18, Lebuh Armenian, 10200 George Town, Pulau Pinang",
    },
)

SERVICES = (
    {"customer": "MY-CUST-001", "type": "Granite", "ref": "MY-GR-001", "details": {}},
    {"customer": "MY-CUST-001", "type": "HSI", "ref": "MY-HSI-001", "details": {}},
    {
        "customer": "MY-CUST-001", "type": "VoBB", "ref": "MY-VOBB-001",
        "details": {
            "vobb_status": "Active",
            "service_number": "03-7955 2201",
            "vobb_password": "Synthetic-VoBB-Credential-Only-1a2!",
        },
    },
    {
        "customer": "MY-CUST-001", "type": "IPTV", "ref": "MY-IPTV-001",
        "details": {
            "iptv_login": "faizal.ramli@unifi.my",
            "iptv_password": "Synthetic-IPTV-Credential-Only-3b4!",
        },
    },
    {"customer": "MY-CUST-002", "type": "Granite", "ref": "MY-GR-002", "details": {}},
    {"customer": "MY-CUST-002", "type": "HSI", "ref": "MY-HSI-002", "details": {}},
    {
        "customer": "MY-CUST-002", "type": "VoBB", "ref": "MY-VOBB-002",
        "details": {
            "vobb_status": "Active",
            "service_number": "04-261 8802",
            "vobb_password": "Synthetic-VoBB-Credential-Only-5c6!",
        },
    },
    {
        "customer": "MY-CUST-002", "type": "IPTV", "ref": "MY-IPTV-002",
        "details": {
            "iptv_login": "kopitarik@unifi.my",
            "iptv_password": "Synthetic-IPTV-Credential-Only-7d8!",
        },
    },
)

ROUTER_DETAILS_001 = {
    "mac_address": "9c:53:22:4a:1b:7e",
    "friendly_name": "Living Room Deco",
    "manufacturer": "TP-Link",
    "device_type": "Root",
    "cloud_device_type": "Access Point",
    "link_type": "Ethernet",
    "ip_address": "192.168.68.1",
    "ssid_2g": "RamliHome_2.4G",
    "ssid_5g": "RamliHome_5G",
    "channel_2g": 6,
    "channel_5g": 44,
    "antenna_2g": "2x2",
    "antenna_5g": "4x4",
    "protocol_2g": "11ax",
    "protocol_5g": "11ax",
    "bandwidth_2g": "40 MHz",
    "bandwidth_5g": "160 MHz",
    "platform": "Deco X90",
    "parent_mac": "ff:ff:ff:ff:ff:ff",
    "last_seen": "12/10/2026 17:42:11",
    "wifi_password": "Synthetic-WiFi-Credential-Only-9k2!",
}

MESH_DETAILS_001 = {
    "mac_address": "9c:53:22:4a:1c:11",
    "friendly_name": "Bedroom Deco",
    "manufacturer": "TP-Link",
    "device_type": "Satellite",
    "cloud_device_type": "Access Point",
    "link_type": "Wireless",
    "ip_address": "192.168.68.2",
    "platform": "Deco X50",
    "parent_mac": "9c:53:22:4a:1b:7e",
    "last_seen": "12/10/2026 17:41:48",
}

MESH_DETAILS_002 = {
    "mac_address": "9c:53:22:4a:1c:22",
    "friendly_name": "Study Deco",
    "manufacturer": "TP-Link",
    "device_type": "Satellite",
    "cloud_device_type": "Access Point",
    "link_type": "Wireless",
    "ip_address": "192.168.68.3",
    "platform": "Deco X50",
    "parent_mac": "9c:53:22:4a:1b:7e",
    "last_seen": "12/10/2026 17:41:55",
}

ROUTER_DETAILS_002 = {
    "mac_address": "8c:4b:14:aa:21:7d",
    "friendly_name": "Counter Deco",
    "manufacturer": "TP-Link",
    "device_type": "Root",
    "cloud_device_type": "Access Point",
    "link_type": "Ethernet",
    "ip_address": "192.168.50.1",
    "ssid_2g": "KopiTarik_2.4G",
    "ssid_5g": "KopiTarik_5G",
    "channel_2g": 1,
    "channel_5g": 36,
    "antenna_2g": "2x2",
    "antenna_5g": "4x4",
    "protocol_2g": "11ax",
    "protocol_5g": "11ax",
    "bandwidth_2g": "20 MHz",
    "bandwidth_5g": "80 MHz",
    "platform": "Deco X90",
    "parent_mac": "ff:ff:ff:ff:ff:ff",
    "last_seen": "12/10/2026 17:39:03",
    "wifi_password": "Synthetic-WiFi-Credential-Only-4a6!",
}

MESH_DETAILS_003 = {
    "mac_address": "8c:4b:14:aa:21:8e",
    "friendly_name": "Dining Deco",
    "manufacturer": "TP-Link",
    "device_type": "Satellite",
    "cloud_device_type": "Access Point",
    "link_type": "Wireless",
    "ip_address": "192.168.50.2",
    "platform": "Deco X50",
    "parent_mac": "8c:4b:14:aa:21:7d",
    "last_seen": "12/10/2026 17:38:40",
}

DEVICES = (
    ("MY-CUST-001", "MY-OLT-001", "OLT", "Taman Sea access node", "online", {}),
    (
        "MY-CUST-001", "MY-ONT-001", "ONU", "Internet", "offline",
        {"onu_password": "Synthetic-ONU-Credential-Only-7f3!", "los_status": "LOS", "rx_power_db": -40.0},
    ),
    ("MY-CUST-001", "MY-RTR-001", "router", "Living Room Deco", "unreachable", ROUTER_DETAILS_001),
    ("MY-CUST-001", "MY-DEC-001", "mesh", "Bedroom Deco", "online", MESH_DETAILS_001),
    ("MY-CUST-001", "MY-DEC-002", "mesh", "Study Deco", "online", MESH_DETAILS_002),
    ("MY-CUST-001", "MY-PH-001", "phone", "Aisyah's phone", "online", {"mac_address": "a4:83:e7:11:22:01", "ip_address": "192.168.68.21", "connection": "WiFi", "band": "5 GHz", "signal_dbm": -52, "vendor": "Samsung"}),
    ("MY-CUST-001", "MY-PH-002", "phone", "Faizal's phone", "online", {"mac_address": "a4:83:e7:11:22:02", "ip_address": "192.168.68.22", "connection": "WiFi", "band": "5 GHz", "signal_dbm": -49, "vendor": "Apple"}),
    ("MY-CUST-001", "MY-LT-001", "laptop", "Work laptop", "online", {"mac_address": "a4:83:e7:11:22:03", "ip_address": "192.168.68.23", "connection": "WiFi", "band": "5 GHz", "signal_dbm": -46, "vendor": "Apple"}),
    ("MY-CUST-001", "MY-TV-001", "tv", "Living room TV", "online", {"mac_address": "a4:83:e7:11:22:04", "ip_address": "192.168.68.24", "connection": "Ethernet", "vendor": "LG"}),
    ("MY-CUST-001", "MY-TB-001", "tablet", "Kids tablet", "degraded", {"mac_address": "a4:83:e7:11:22:05", "ip_address": "192.168.68.25", "connection": "WiFi", "band": "2.4 GHz", "signal_dbm": -71, "vendor": "Lenovo"}),
    ("MY-CUST-001", "MY-CAM-001", "camera", "Front door camera", "online", {"mac_address": "a4:83:e7:11:22:06", "ip_address": "192.168.68.26", "connection": "WiFi", "band": "2.4 GHz", "signal_dbm": -63, "vendor": "TP-Link"}),
    ("MY-CUST-001", "MY-SPK-001", "speaker", "Kitchen speaker", "online", {"mac_address": "a4:83:e7:11:22:07", "ip_address": "192.168.68.27", "connection": "WiFi", "band": "2.4 GHz", "signal_dbm": -58, "vendor": "Amazon"}),
    ("MY-CUST-001", "MY-PRN-001", "printer", "Study printer", "online", {"mac_address": "a4:83:e7:11:22:08", "ip_address": "192.168.68.28", "connection": "WiFi", "band": "2.4 GHz", "signal_dbm": -66, "vendor": "HP"}),
    ("MY-CUST-001", "MY-CON-001", "console", "PlayStation 5", "online", {"mac_address": "a4:83:e7:11:22:09", "ip_address": "192.168.68.29", "connection": "Ethernet", "vendor": "Sony"}),
    ("MY-CUST-002", "MY-OLT-002", "OLT", "George Town access node", "online", {}),
    (
        "MY-CUST-002", "MY-ONT-002", "ONU", "Internet", "degraded",
        {"onu_password": "Synthetic-ONU-Credential-Only-2c9!", "los_status": "OK", "rx_power_db": -22.5},
    ),
    ("MY-CUST-002", "MY-RTR-002", "router", "Counter Deco", "online", ROUTER_DETAILS_002),
    ("MY-CUST-002", "MY-DEC-003", "mesh", "Dining Deco", "online", MESH_DETAILS_003),
    ("MY-CUST-002", "MY-PH-003", "phone", "Counter phone", "online", {"mac_address": "b8:27:eb:33:44:01", "ip_address": "192.168.50.31", "connection": "WiFi", "band": "5 GHz", "signal_dbm": -47, "vendor": "Google"}),
    ("MY-CUST-002", "MY-LT-002", "laptop", "POS laptop", "online", {"mac_address": "b8:27:eb:33:44:02", "ip_address": "192.168.50.32", "connection": "Ethernet", "vendor": "Dell"}),
    ("MY-CUST-002", "MY-TB-002", "tablet", "Menu tablet", "online", {"mac_address": "b8:27:eb:33:44:03", "ip_address": "192.168.50.33", "connection": "WiFi", "band": "5 GHz", "signal_dbm": -54, "vendor": "Samsung"}),
    ("MY-CUST-002", "MY-TV-002", "tv", "Menu display TV", "online", {"mac_address": "b8:27:eb:33:44:04", "ip_address": "192.168.50.34", "connection": "Ethernet", "vendor": "Samsung"}),
    ("MY-CUST-002", "MY-CAM-002", "camera", "Cafe camera", "degraded", {"mac_address": "b8:27:eb:33:44:05", "ip_address": "192.168.50.35", "connection": "WiFi", "band": "2.4 GHz", "signal_dbm": -70, "vendor": "Hikvision"}),
    ("MY-CUST-002", "MY-SPK-002", "speaker", "Cafe speaker", "online", {"mac_address": "b8:27:eb:33:44:06", "ip_address": "192.168.50.36", "connection": "WiFi", "band": "2.4 GHz", "signal_dbm": -60, "vendor": "Sonos"}),
)

TOPOLOGY_EDGES = (
    ("MY-OLT-001", "MY-ONT-001", "MY-GR-001"),
    ("MY-ONT-001", "MY-RTR-001", None),
    ("MY-RTR-001", "MY-DEC-001", None),
    ("MY-RTR-001", "MY-DEC-002", None),
    ("MY-RTR-001", "MY-PH-001", None),
    ("MY-RTR-001", "MY-PH-002", None),
    ("MY-RTR-001", "MY-LT-001", None),
    ("MY-RTR-001", "MY-TV-001", None),
    ("MY-RTR-001", "MY-TB-001", None),
    ("MY-RTR-001", "MY-CAM-001", None),
    ("MY-RTR-001", "MY-SPK-001", None),
    ("MY-RTR-001", "MY-PRN-001", None),
    ("MY-RTR-001", "MY-CON-001", None),
    ("MY-OLT-002", "MY-ONT-002", "MY-GR-002"),
    ("MY-ONT-002", "MY-RTR-002", None),
    ("MY-RTR-002", "MY-DEC-003", None),
    ("MY-RTR-002", "MY-PH-003", None),
    ("MY-RTR-002", "MY-LT-002", None),
    ("MY-RTR-002", "MY-TB-002", None),
    ("MY-RTR-002", "MY-TV-002", None),
    ("MY-RTR-002", "MY-CAM-002", None),
    ("MY-RTR-002", "MY-SPK-002", None),
)

EVENTS = (
    {
        "source_event_id": DEMO_EVENT_SOURCE_ID,
        "event_type": "ONU_OFFLINE",
        "device_ref": "MY-ONT-001",
        "service_ref": "MY-GR-001",
        "payload": {
            "reported_by": "subscriber",
            "signal_state": "no_link",
            "los_indicator": "LOS",
            "incident_started": "2026-10-12T09:51:00Z",
            "customer_note": "No internet since this morning, ONU power light on but no PON light.",
        },
    },
    {
        "source_event_id": "MY-EVENT-OPTICAL-LOSS-001",
        "event_type": "OPTICAL_LOSS",
        "device_ref": "MY-ONT-002",
        "service_ref": "MY-GR-002",
        "payload": {
            "loss_db": 34.5,
            "rx_power_db": -31.2,
            "baseline_rx_power_db": -21.4,
            "alert": "optical_loss_minor",
            "shared_splitter_endpoints": 1,
        },
    },
    {
        "source_event_id": "MY-EVENT-HSI-DEGRADED-001",
        "event_type": "HSI_DEGRADED",
        "device_ref": "MY-RTR-001",
        "service_ref": "MY-HSI-001",
        "payload": {
            "download_mbps": 12.4,
            "upload_mbps": 3.1,
            "expected_mbps": 500,
            "test_method": "wired_single_stream",
            "samples": 3,
        },
    },
    {
        "source_event_id": "MY-EVENT-VOBB-REG-001",
        "event_type": "VOBB_REGISTRATION_FAILED",
        "device_ref": "MY-RTR-001",
        "service_ref": "MY-VOBB-001",
        "payload": {
            "adapter": "ATA-190",
            "sip_status": 408,
            "dial_tone": False,
            "last_registered": "2026-10-11T21:14:00Z",
        },
    },
    {
        "source_event_id": "MY-EVENT-IPTV-FREEZE-001",
        "event_type": "IPTV_STREAM_DEGRADED",
        "device_ref": "MY-RTR-002",
        "service_ref": "MY-IPTV-002",
        "payload": {
            "channel": "Channel 101 HD",
            "buffering_events": 14,
            "packet_loss_pct": 2.7,
            "measured_bitrate_mbps": 6.1,
            "expected_bitrate_mbps": 18.0,
        },
    },
    {
        "source_event_id": "MY-EVENT-WIFI-INTERFERENCE-001",
        "event_type": "WIFI_INTERFERENCE",
        "device_ref": "MY-RTR-002",
        "service_ref": "MY-HSI-002",
        "payload": {
            "band": "2.4 GHz",
            "channel": 11,
            "neighbour_ap_count": 19,
            "retries_pct": 31,
            "channel_utilisation_pct": 78,
        },
    },
    {
        "source_event_id": "MY-EVENT-ONT-OPTICAL-DEGRADE-001",
        "event_type": "OPTICAL_DEGRADE",
        "device_ref": "MY-ONT-001",
        "service_ref": "MY-GR-001",
        "payload": {
            "rx_power_db": -28.9,
            "baseline_rx_power_db": -21.6,
            "olt_rx_power_db": -27.4,
            "threshold_db": -27.0,
        },
    },
    {
        "source_event_id": "MY-EVENT-CPE-REBOOT-001",
        "event_type": "CPE_REBOOT_LOOP",
        "device_ref": "MY-RTR-002",
        "service_ref": "MY-HSI-002",
        "payload": {
            "reboot_count_24h": 7,
            "uptime_seconds": 180,
            "firmware": "SRCX_2.4.1",
            "power_state": "unstable",
        },
    },
    {
        "source_event_id": "MY-EVENT-DNS-001",
        "event_type": "DNS_RESOLUTION_FAILURE",
        "device_ref": "MY-RTR-001",
        "service_ref": "MY-HSI-001",
        "payload": {
            "resolver": "203.0.113.10",
            "query_error_pct": 42,
            "test_domain": "portal.unifi.my",
        },
    },
    {
        "source_event_id": "MY-EVENT-CAM-OFFLINE-001",
        "event_type": "DEVICE_OFFLINE",
        "device_ref": "MY-CAM-002",
        "service_ref": "MY-HSI-002",
        "payload": {
            "mac_address": "b8:27:eb:33:44:05",
            "last_seen": "2026-10-12T06:02:11Z",
            "signal_dbm": -70,
            "device_kind": "camera",
        },
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
    account_names = {"operator@demo.invalid": "Nurul Aina binti Hassan", "technician@demo.invalid": "Rajesh Kumar a/l Suresh"}
    for email, password in DEMO_ACCOUNTS.items():
        user = session.scalar(select(User).where(User.email == email))
        if user is None:
            user = User(email=email, display_name=account_names[email], password_hash=hasher.hash(password), role_id=roles[account_roles[email]].id, is_active=True, is_demo=True, staff_code=DEMO_STAFF_CODES[email])
            session.add(user)
        _require_canonical(
            user,
            display_name=account_names[email],
            role_id=roles[account_roles[email]].id,
            is_active=True,
            is_demo=True,
            staff_code=DEMO_STAFF_CODES[email],
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
    for spec in SERVICES:
        service = session.scalar(select(Service).where(Service.service_ref == spec["ref"]))
        if service is None:
            service = Service(customer_id=customers[spec["customer"]].id, service_type=spec["type"], service_ref=spec["ref"], status="active", details=spec["details"])
            session.add(service)
            session.flush()
        _require_canonical(service, customer_id=customers[spec["customer"]].id, service_type=spec["type"], status="active", details=spec["details"])
        sync_service_facts(session, service)
        services[spec["ref"]] = service

    devices = {}
    for customer_ref, ref, dtype, name, status, details in DEVICES:
        device = session.scalar(select(NetworkDevice).where(NetworkDevice.device_ref == ref))
        if device is None:
            device = NetworkDevice(customer_id=customers[customer_ref].id, device_ref=ref, device_type=dtype, name=name, status=status, details=details)
            session.add(device)
            session.flush()
        _require_canonical(device, customer_id=customers[customer_ref].id, device_type=dtype, name=name, status=status, details=details)
        sync_device_facts(session, device)
        devices[ref] = device

    for upstream, downstream, service_ref in TOPOLOGY_EDGES:
        service_id = services[service_ref].id if service_ref is not None else None
        edge = session.scalar(select(TopologyEdge).where(TopologyEdge.source_device_id == devices[upstream].id, TopologyEdge.target_device_id == devices[downstream].id))
        if edge is None:
            edge = TopologyEdge(source_device_id=devices[upstream].id, target_device_id=devices[downstream].id, service_id=service_id)
            session.add(edge)
        _require_canonical(edge, service_id=service_id)

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
