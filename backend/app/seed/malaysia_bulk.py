"""Destructive Malaysian bulk reset for demos.

Wipes every application table and regenerates a realistic, Malaysia-flavoured
field-operations dataset: customers with Granite/HSI/VoBB/IPTV services, UniFi
network devices, routers, topology, customer summaries, and network events that
are pushed through the real event pipeline into tickets.

Disabled unless ``DEMO_SEED_ENABLED=true``. Run with::

    docker compose exec -T api python -m app.seed.malaysia_bulk
"""

from __future__ import annotations

import random
import sys
from datetime import UTC, datetime, timedelta
from hashlib import sha1

from argon2 import PasswordHasher
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.auth.dependencies import AuthenticatedUser
from app.config import Settings
from app.domain.models import (
    AuditEvent,
    Customer,
    CustomerSummary,
    NetworkDevice,
    NetworkEvent,
    Role,
    Router,
    Service,
    Ticket,
    TopologyEdge,
    User,
)
from app.seed.demo_data import DEMO_ACCOUNTS, DEMO_STAFF_CODES
from app.services import event_processing
from app.services.entity_facts import sync_all_facts

DEFAULT_CUSTOMER_COUNT = 40
DEFAULT_TICKET_COUNT = 100
DEFAULT_SEED = 20261012

PUBLIC_TABLES = (
    "assistant_messages",
    "assistant_sessions",
    "audit_events",
    "tool_executions",
    "tickets",
    "network_events",
    "topology_edges",
    "entity_facts",
    "entity_fact_sheets",
    "network_devices",
    "routers",
    "customer_summaries",
    "services",
    "customers",
    "knowledge_chunks",
    "knowledge_documents",
    "users",
    "roles",
)

RESIDENT_NAMES = (
    "TAN TICK SEW",
    "AZLINA BINTI MOHD NOOR",
    "MUHAMMAD DANIAL BIN ZAKARIA",
    "KENNETH LOH KAH SENG",
    "HASNAH BINTI SALLEH",
    "CHONG KAH FAI",
    "ARUN A/L KRISHNAN",
    "ZAINAL ABIDIN BIN MOHD",
    "DIVYA A/P RAJENDRAN",
    "MOHD RIZAL BIN OMAR",
    "LEE CHIN HUA",
    "LIM WEI MING",
    "GOH SOON HUAT",
    "NORHAYATI BINTI OSMAN",
    "VIGNESH A/L SUBRAMANIAM",
    "WONG MEI LING",
    "NUR AISYAH BINTI HASSAN",
    "TEOH BEE CHOO",
    "YAP KEAN SENG",
    "RAJESH A/L MURUGAN",
    "SITI ZALEHA BINTI IBRAHIM",
    "MOHAMAD HAFIZ BIN ISMAIL",
    "ROSLI BIN AHMAD",
    "TAN CHWEE MENG",
    "PRIYA A/P SAMY",
    "SAIFUL AZMAN BIN RAMLI",
    "CHEAH SWEE LAN",
    "FARAH NABILA BINTI YUSOF",
    "KUMARAN A/L SIVAM",
    "NORAINI BINTI ABDULLAH",
    "TAN WEI JIE",
    "SURESH A/L RAMASAMY",
    "SITI NURHALIZA BINTI OMAR",
    "KHOO BOON KEAT",
    "MOHD FAIZAL BIN YUSOFF",
    "DEVI A/P MURUGAN",
    "WONG SIEW CHENG",
    "AHMAD ZAKI BIN ISMAIL",
)

BUSINESS_NAMES = (
    "Kopi Tarik Corner Sdn Bhd",
    "Restoran Makanan Laut Ah Hock",
    "Kedai Runcit Sri Murni",
    "Bengkel Auto Jaya Sdn Bhd",
    "Salon Cantik Murni",
    "Farmasi Sihat Selalu",
    "Kedai Emas Permata Jaya",
    "Nasi Lemak Wangi Sdn Bhd",
    "Klinik Pergigian Ceria",
    "Pusat Komputer Mega Tech",
)

STREETS = (
    "JALAN ANGGERIK ARANDA",
    "JALAN DELIMA",
    "JALAN MAWAR",
    "JALAN CEMPAKA",
    "JALAN BUNGA RAYA",
    "JALAN KIARA",
    "JALAN MERANTI",
    "JALAN SAGA",
    "JALAN NURI",
    "JALAN PANDAN",
    "JALAN DAMAI",
    "JALAN BAKTI",
    "PERSIARAN SUNGAI",
    "LORONG SERI KENANGA",
)

LOCALITIES = (
    ("40460", "SHAH ALAM", "SELANGOR"),
    ("40150", "SHAH ALAM", "SELANGOR"),
    ("30450", "IPOH", "PERAK"),
    ("31400", "IPOH", "PERAK"),
    ("93350", "KUCHING", "SARAWAK"),
    ("93000", "KUCHING", "SARAWAK"),
    ("80100", "JOHOR BAHRU", "JOHOR"),
    ("80250", "JOHOR BAHRU", "JOHOR"),
    ("50000", "KUALA LUMPUR", "WILAYAH PERSEKUTUAN"),
    ("50480", "KUALA LUMPUR", "WILAYAH PERSEKUTUAN"),
    ("10450", "GEORGE TOWN", "PULAU PINANG"),
    ("10050", "GEORGE TOWN", "PULAU PINANG"),
    ("88100", "KOTA KINABALU", "SABAH"),
    ("88000", "KOTA KINABALU", "SABAH"),
)

EMAIL_DOMAINS = ("gmail.com", "hotmail.com", "yahoo.com", "outlook.com")

HSI_PACKAGES = (
    ("unifi 100Mbps", 100, 50),
    ("unifi 300Mbps", 300, 100),
    ("unifi 500Mbps", 500, 100),
    ("unifi 800Mbps", 800, 200),
    ("unifi 1Gbps", 1000, 500),
)

ACCESS_PLATFORMS = ("Deco X90", "Deco X50", "Deco X60", "Huawei AX3", "ZTE H3600")

CLIENT_TEMPLATES = (
    ("phone", "Samsung", "5 GHz", "WiFi"),
    ("phone", "Apple", "5 GHz", "WiFi"),
    ("laptop", "Apple", "5 GHz", "WiFi"),
    ("laptop", "Dell", "5 GHz", "WiFi"),
    ("tv", "LG", "5 GHz", "Ethernet"),
    ("tv", "Samsung", "5 GHz", "Ethernet"),
    ("tablet", "Lenovo", "2.4 GHz", "WiFi"),
    ("camera", "TP-Link", "2.4 GHz", "WiFi"),
    ("speaker", "Sonos", "2.4 GHz", "WiFi"),
    ("console", "Sony", "5 GHz", "Ethernet"),
)

EVENT_TEMPLATES = (
    ("ONU_OFFLINE", "ONU", "Granite"),
    ("OPTICAL_LOSS", "ONU", "Granite"),
    ("OPTICAL_DEGRADE", "ONU", "Granite"),
    ("HSI_DEGRADED", "router", "HSI"),
    ("DNS_RESOLUTION_FAILURE", "router", "HSI"),
    ("WIFI_INTERFERENCE", "router", "HSI"),
    ("CPE_REBOOT_LOOP", "router", "HSI"),
    ("VOBB_REGISTRATION_FAILED", "router", "VoBB"),
    ("IPTV_STREAM_DEGRADED", "router", "IPTV"),
    ("DEVICE_OFFLINE", "client", "HSI"),
)

TICKET_STATUSES = ("open", "open", "open", "open", "open", "open", "in_progress", "in_progress", "in_progress", "resolved")


def reset_and_seed(
    session: Session,
    *,
    customer_count: int = DEFAULT_CUSTOMER_COUNT,
    ticket_count: int = DEFAULT_TICKET_COUNT,
    seed: int = DEFAULT_SEED,
    include_unifi: bool = False,
) -> dict[str, int]:
    if not Settings().demo_seed_enabled:
        raise RuntimeError("Bulk seeding is disabled. Set DEMO_SEED_ENABLED=true only in a local/demo environment.")

    rng = random.Random(seed)
    _truncate(session, include_unifi=include_unifi)
    roles = _create_roles(session)
    users = _create_users(session, roles)
    operator = users["operator@demo.invalid"]
    actor = AuthenticatedUser(id=operator.id, email=operator.email, role="operator")

    customers, service_index, device_index = _create_customers(session, rng, customer_count)
    _create_topology(session, service_index, device_index)
    _create_summaries(session, rng, customers)
    _create_routers(session, rng, customers)
    event_ids = _create_events(session, rng, ticket_count, service_index, device_index)
    session.commit()

    for event_id in event_ids:
        event_processing.process_event(session, event_id, actor)

    _apply_ticket_history(session, rng)
    sync_all_facts(session)
    session.commit()

    return {
        "users": len(users),
        "customers": len(customers),
        "services": sum(len(entry["services"]) for entry in service_index.values()),
        "network_devices": len(device_index),
        "tickets": ticket_count,
    }


def _truncate(session: Session, *, include_unifi: bool) -> None:
    table_list = ", ".join(f"public.{name}" for name in PUBLIC_TABLES)
    session.execute(text(f"TRUNCATE TABLE {table_list} RESTART IDENTITY CASCADE"))
    if include_unifi:
        session.execute(
            text(
                "TRUNCATE TABLE unifi.customer_summaries, unifi.devices, unifi.routers, unifi.customers CASCADE"
            )
        )
    session.commit()


def _create_roles(session: Session) -> dict[str, Role]:
    roles: dict[str, Role] = {}
    for name in ("operator", "technician", "supervisor"):
        role = Role(name=name)
        session.add(role)
        session.flush()
        roles[name] = role
    return roles


def _create_users(session: Session, roles: dict[str, Role]) -> dict[str, User]:
    hasher = PasswordHasher()
    account_roles = {
        "operator@demo.invalid": ("operator", "00000000-0000-0000-0000-000000000001"),
        "technician@demo.invalid": ("technician", "00000000-0000-0000-0000-000000000002"),
    }
    account_names = {
        "operator@demo.invalid": "Nurul Aina binti Hassan",
        "technician@demo.invalid": "Rajesh Kumar a/l Suresh",
    }
    users: dict[str, User] = {}
    for email, (role_name, user_id) in account_roles.items():
        user = User(
            id=user_id,
            email=email,
            display_name=account_names[email],
            password_hash=hasher.hash(DEMO_ACCOUNTS[email]),
            role_id=roles[role_name].id,
            is_active=True,
            is_demo=True,
            staff_code=DEMO_STAFF_CODES[email],
        )
        session.add(user)
        users[email] = user
    session.flush()
    return users


def _create_customers(
    session: Session, rng: random.Random, count: int
) -> tuple[list[Customer], dict[str, dict], dict[str, NetworkDevice]]:
    customers: list[Customer] = []
    service_index: dict[str, dict] = {}
    device_index: dict[str, NetworkDevice] = {}

    for index in range(1, count + 1):
        is_business = index <= len(BUSINESS_NAMES)
        name = BUSINESS_NAMES[index - 1] if is_business else rng.choice(RESIDENT_NAMES)
        customer_ref = f"MY-CUST-{index:03d}"
        postcode, city, state = rng.choice(LOCALITIES)
        address = (
            f"{rng.randint(1, 120)} {rng.choice(STREETS)} {postcode} {city} {state} MALAYSIA"
        )
        contact_no = _phone(rng)
        email = _email(name, index)
        start = datetime(2022, 1, 1) + timedelta(days=rng.randint(0, 1100))
        term = rng.choice((1, 2, 2, 3))
        customer = Customer(
            customer_ref=customer_ref,
            name=name,
            address=address,
            is_demo=False,
            account_no=f"1{rng.randint(10_000_000, 99_999_999)}",
            contact_no=contact_no,
            email_address=email,
            contract_term=term,
            commitment_start=start,
            commitment_end=start + timedelta(days=365 * term),
        )
        session.add(customer)
        session.flush()
        customers.append(customer)

        services = _create_services(session, rng, index, customer, email, contact_no)
        devices = _create_devices(session, rng, index, customer, email)
        service_index[customer_ref] = {"customer": customer, "services": services}
        device_index.update(devices)

    session.flush()
    return customers, service_index, device_index


def _create_services(
    session: Session, rng: random.Random, index: int, customer: Customer, email: str, contact_no: str
) -> dict[str, Service]:
    package_name, download, upload = rng.choice(HSI_PACKAGES)
    specs = {
        "Granite": {
            "service_ref": f"MY-GR-{index:03d}",
            "details": {"circuit_id": f"GR-{index:05d}", "bandwidth": "1 Gbps", "status": "Active"},
        },
        "HSI": {
            "service_ref": f"MY-HSI-{index:03d}",
            "details": {
                "package": package_name,
                "download_mbps": download,
                "upload_mbps": upload,
                "static_ip": rng.choice((True, False)),
            },
        },
        "VoBB": {
            "service_ref": f"MY-VOBB-{index:03d}",
            "details": {
                "vobb_status": rng.choice(("Active", "Active", "Active", "Suspended")),
                "service_number": contact_no if contact_no.startswith("0") else f"03-{rng.randint(2000, 7999)} {rng.randint(1000, 9999)}",
                "vobb_password": f"Synthetic-VoBB-Credential-{index:03d}-{rng.randint(1000, 9999)}!",
            },
        },
        "IPTV": {
            "service_ref": f"MY-IPTV-{index:03d}",
            "details": {
                "iptv_login": email,
                "iptv_password": f"Synthetic-IPTV-Credential-{index:03d}-{rng.randint(1000, 9999)}!",
            },
        },
    }
    services: dict[str, Service] = {}
    for service_type, spec in specs.items():
        service = Service(
            customer_id=customer.id,
            service_type=service_type,
            service_ref=spec["service_ref"],
            status="active",
            details=spec["details"],
        )
        session.add(service)
        services[service_type] = service
    session.flush()
    return services


def _create_devices(
    session: Session, rng: random.Random, index: int, customer: Customer, email: str
) -> dict[str, NetworkDevice]:
    devices: dict[str, NetworkDevice] = {}
    olt_ref = f"MY-OLT-{index:03d}"
    onu_ref = f"MY-ONT-{index:03d}"
    router_ref = f"MY-RTR-{index:03d}"
    onu_status = rng.choice(("online", "online", "online", "offline", "degraded"))

    devices[olt_ref] = NetworkDevice(
        customer_id=customer.id,
        device_ref=olt_ref,
        device_type="OLT",
        name=f"{customer.name.split()[0]} access node",
        status="online",
        details={},
    )
    devices[onu_ref] = NetworkDevice(
        customer_id=customer.id,
        device_ref=onu_ref,
        device_type="ONU",
        name="Internet",
        status=onu_status,
        details={
            "onu_password": f"Synthetic-ONU-Credential-{index:03d}-{rng.randint(1000, 9999)}!",
            "los_status": "LOS" if onu_status == "offline" else "OK",
            "rx_power_db": round(rng.uniform(-42.0, -16.0), 1),
        },
    )
    hsi_service = f"MY-HSI-{index:03d}"

    router_mac = _mac(rng)
    ssid_base = _ssid_base(customer, index)
    devices[router_ref] = _access_point(
        rng,
        index,
        customer,
        device_ref=router_ref,
        name="Root",
        friendly_name=f"{ssid_base} Deco",
        device_type="router",
        parent_mac="ff:ff:ff:ff:ff:ff",
        ip_address=f"192.168.{rng.randint(0, 20)}.1",
        ssid_base=ssid_base,
        link_type="Ethernet",
        mac=router_mac,
        service_ref=hsi_service,
    )

    mesh_count = rng.randint(1, 2)
    mesh_names = ("Bedroom Deco", "Study Deco", "Living Room Deco", "Dining Deco")
    for mesh_index in range(mesh_count):
        mesh_ref = f"MY-DEC-{index:03d}-{mesh_index + 1}"
        devices[mesh_ref] = _access_point(
            rng,
            index,
            customer,
            device_ref=mesh_ref,
            name="Satellite",
            friendly_name=mesh_names[mesh_index % len(mesh_names)],
            device_type="mesh",
            parent_mac=router_mac,
            ip_address=f"192.168.{rng.randint(0, 20)}.{mesh_index + 2}",
            ssid_base=ssid_base,
            link_type="Wireless",
            mac=_mac(rng),
            service_ref=None,
            platform="Deco X50",
        )

    router_ip_base = devices[router_ref].ip_address
    octets = str(router_ip_base).split(".")
    client_count = rng.randint(3, 5)
    for client_index in range(client_count):
        device_type, vendor, band, connection = rng.choice(CLIENT_TEMPLATES)
        client_ref = f"MY-{index:03d}-CL{client_index + 1}"
        signal = rng.randint(-72, -42)
        devices[client_ref] = NetworkDevice(
            customer_id=customer.id,
            device_ref=client_ref,
            device_type=device_type,
            name=f"{vendor} {device_type}",
            status=rng.choice(("online", "online", "online", "degraded")),
            details={
                "vendor": vendor,
                "mac_address": _mac(rng),
                "ip_address": f"{octets[0]}.{octets[1]}.{octets[2]}.{30 + client_index}",
                "connection": connection,
                "band": band,
                "signal_dbm": signal,
            },
        )

    for device in devices.values():
        session.add(device)
    session.flush()
    return devices


def _access_point(
    rng: random.Random,
    index: int,
    customer: Customer,
    *,
    device_ref: str,
    name: str,
    friendly_name: str,
    device_type: str,
    parent_mac: str,
    ip_address: str,
    ssid_base: str,
    link_type: str,
    mac: str,
    service_ref: str | None,
    platform: str | None = None,
) -> NetworkDevice:
    platform = platform or rng.choice(ACCESS_PLATFORMS)
    channel_2g = rng.choice((1, 6, 11))
    channel_5g = rng.choice((36, 44, 149, 157))
    bandwidth_2g = rng.choice(("20 MHz", "40 MHz"))
    bandwidth_5g = rng.choice(("80 MHz", "160 MHz"))
    last_seen = (datetime.now(UTC) - timedelta(minutes=rng.randint(1, 240))).strftime("%d/%m/%Y %H:%M:%S")
    return NetworkDevice(
        customer_id=customer.id,
        device_ref=device_ref,
        device_type=device_type,
        name=name,
        status=rng.choice(("online", "online", "online", "offline")),
        details={
            "mac_address": mac,
            "friendly_name": friendly_name,
            "manufacturer": "TP-Link",
            "device_type": device_type,
            "cloud_device_type": "Access Point",
            "link_type": link_type,
            "ip_address": ip_address,
            "ssid_2g": f"{ssid_base}_2.4G",
            "ssid_5g": f"{ssid_base}_5G",
            "channel_2g": channel_2g,
            "channel_5g": channel_5g,
            "antenna_2g": "2x2",
            "antenna_5g": "4x4",
            "protocol_2g": "11ax",
            "protocol_5g": "11ax",
            "bandwidth_2g": bandwidth_2g,
            "bandwidth_5g": bandwidth_5g,
            "platform": platform,
            "parent_mac": parent_mac,
            "last_seen": last_seen,
            "wifi_password": f"Synthetic-WiFi-Credential-{index:03d}-{rng.randint(1000, 9999)}!",
        },
        mac_address=mac,
        login_id=customer.customer_ref,
        friendly_name=friendly_name,
        manufacturer="TP-Link",
        brand="TP-Link",
        cloud_device_type="Access Point",
        link_type=link_type,
        ip_address=ip_address,
        ssid_2_4ghz=f"{ssid_base}_2.4G",
        ssid_5ghz=f"{ssid_base}_5G",
        channel_2_4ghz=channel_2g,
        channel_5ghz=channel_5g,
        antenna_2_4ghz="2x2",
        antenna_5ghz="4x4",
        protocol_2_4ghz="11ax",
        protocol_5ghz="11ax",
        bandwidth_2_4ghz=bandwidth_2g,
        bandwidth_5ghz=bandwidth_5g,
        platform=platform,
        parent_mac=parent_mac,
        last_seen=datetime.now(UTC) - timedelta(minutes=rng.randint(1, 240)),
    )


def _create_topology(
    session: Session, service_index: dict[str, dict], device_index: dict[str, NetworkDevice]
) -> None:
    for customer_ref, entry in service_index.items():
        index = int(customer_ref.rsplit("-", 1)[1])
        olt = device_index[f"MY-OLT-{index:03d}"]
        onu = device_index[f"MY-ONT-{index:03d}"]
        router = device_index[f"MY-RTR-{index:03d}"]
        granite = entry["services"]["Granite"]
        edges = [
            (olt, onu, granite.id),
            (onu, router, None),
        ]
        for ref, device in device_index.items():
            if device.device_type == "mesh" and ref.startswith(f"MY-DEC-{index:03d}"):
                edges.append((router, device, None))
            elif ref.startswith(f"MY-{index:03d}-CL"):
                edges.append((router, device, None))
        for source, target, service_id in edges:
            session.add(
                TopologyEdge(
                    source_device_id=source.id,
                    target_device_id=target.id,
                    service_id=service_id,
                )
            )
    session.flush()


def _create_summaries(session: Session, rng: random.Random, customers: list[Customer]) -> None:
    recommendations = (
        "Schedule a truck roll to verify the drop cable and splitter port.",
        "Dispatch a technician to re-terminate the ONU pigtail and re-test optical power.",
        "Monitor for 24 hours; escalate to the access team if degradation persists.",
        "Reboot the router during a maintenance window and confirm the reboot loop clears.",
        "Advise the customer on mesh placement to reduce 2.4 GHz congestion.",
    )
    for customer in customers:
        session.add(
            CustomerSummary(
                login_id=customer.customer_ref,
                summary=(
                    f"{customer.name} is on a bundled unifi plan with Granite, HSI, VoBB, and IPTV. "
                    "Recent telemetry shows a mix of normal and degraded client health."
                ),
                recommendation=rng.choice(recommendations),
                model="gigx-gemma-4-e2b-it",
                generated_at=datetime.now(UTC),
            )
        )
    session.flush()


def _create_routers(session: Session, rng: random.Random, customers: list[Customer]) -> None:
    manufacturers = (("TP-Link", "Archer AX73"), ("Huawei", "AX3 Pro"), ("ZTE", "H3600"), ("Nokia", "Beacon 6"))
    for customer in customers:
        manufacturer, model = rng.choice(manufacturers)
        index = int(customer.customer_ref.rsplit("-", 1)[1])
        session.add(
            Router(
                serial_number=f"RTR-{index:05d}",
                login_id=customer.customer_ref,
                manufacturer=manufacturer,
                model=model,
                cpu_usage_pct=rng.randint(5, 80),
                cpu_temperature_c=rng.randint(40, 72),
                memory_usage_pct=rng.randint(20, 88),
                monthly_usage_gb=round(rng.uniform(40.0, 1800.0), 1),
                rx_power_dbm=round(rng.uniform(-30.0, -15.0), 1),
            )
        )
    session.flush()


def _create_events(
    session: Session,
    rng: random.Random,
    ticket_count: int,
    service_index: dict[str, dict],
    device_index: dict[str, NetworkDevice],
) -> list[str]:
    customer_refs = list(service_index.keys())
    suffixes: set[str] = set()
    event_ids: list[str] = []
    serial = 0
    while len(event_ids) < ticket_count:
        source_event_id = f"MY-EV-{serial:05d}"
        suffix = sha1(source_event_id.encode()).hexdigest()[:4].upper()
        serial += 1
        if suffix in suffixes:
            continue
        suffixes.add(suffix)

        customer_ref = rng.choice(customer_refs)
        entry = service_index[customer_ref]
        event_type, device_kind, service_type = rng.choice(EVENT_TEMPLATES)
        index = int(customer_ref.rsplit("-", 1)[1])
        device = _pick_device(rng, device_index, index, device_kind)
        service = entry["services"][service_type]
        session.add(
            NetworkEvent(
                source_event_id=source_event_id,
                event_type=event_type,
                device_id=device.id,
                service_id=service.id,
                payload=_event_payload(rng, event_type, device),
            )
        )
        event_ids.append(source_event_id)
    session.flush()
    saved = list(
        session.scalars(
            select(NetworkEvent.id).where(NetworkEvent.source_event_id.in_(event_ids))
        ).all()
    )
    return saved


def _pick_device(
    rng: random.Random, device_index: dict[str, NetworkDevice], index: int, device_kind: str
) -> NetworkDevice:
    if device_kind == "ONU":
        return device_index[f"MY-ONT-{index:03d}"]
    if device_kind == "router":
        return device_index[f"MY-RTR-{index:03d}"]
    clients = [
        device
        for ref, device in device_index.items()
        if ref.startswith(f"MY-{index:03d}-CL")
    ]
    return rng.choice(clients) if clients else device_index[f"MY-RTR-{index:03d}"]


def _event_payload(rng: random.Random, event_type: str, device: NetworkDevice) -> dict:
    if event_type == "ONU_OFFLINE":
        return {"reported_by": "subscriber", "signal_state": "no_link", "los_indicator": "LOS", "customer_note": "No internet since this morning."}
    if event_type == "OPTICAL_LOSS":
        return {"loss_db": round(rng.uniform(28, 38), 1), "rx_power_db": round(rng.uniform(-34, -29), 1), "baseline_rx_power_db": -21.5, "alert": "optical_loss_minor"}
    if event_type == "OPTICAL_DEGRADE":
        return {"rx_power_db": round(rng.uniform(-30, -27), 1), "baseline_rx_power_db": -21.6, "olt_rx_power_db": -27.4, "threshold_db": -27.0}
    if event_type == "HSI_DEGRADED":
        return {"download_mbps": round(rng.uniform(8, 60), 1), "upload_mbps": round(rng.uniform(2, 20), 1), "expected_mbps": rng.choice((100, 300, 500, 800, 1000)), "test_method": "wired_single_stream", "samples": 3}
    if event_type == "DNS_RESOLUTION_FAILURE":
        return {"resolver": "203.0.113.10", "query_error_pct": rng.randint(20, 60), "test_domain": "portal.unifi.my"}
    if event_type == "WIFI_INTERFERENCE":
        return {"band": "2.4 GHz", "channel": rng.choice((1, 6, 11)), "neighbour_ap_count": rng.randint(8, 22), "retries_pct": rng.randint(15, 40), "channel_utilisation_pct": rng.randint(60, 90)}
    if event_type == "CPE_REBOOT_LOOP":
        return {"reboot_count_24h": rng.randint(3, 12), "uptime_seconds": rng.randint(60, 600), "firmware": "SRCX_2.4.1", "power_state": "unstable"}
    if event_type == "VOBB_REGISTRATION_FAILED":
        return {"adapter": "ATA-190", "sip_status": rng.choice((408, 503, 401)), "dial_tone": False, "last_registered": "2026-10-11T21:14:00Z"}
    if event_type == "IPTV_STREAM_DEGRADED":
        return {"channel": f"Channel {rng.randint(100, 199)} HD", "buffering_events": rng.randint(5, 25), "packet_loss_pct": round(rng.uniform(0.5, 4.0), 1), "measured_bitrate_mbps": round(rng.uniform(4, 12), 1), "expected_bitrate_mbps": 18.0}
    return {"mac_address": device.mac_address, "last_seen": "2026-10-12T06:02:11Z", "signal_dbm": rng.randint(-75, -55), "device_kind": device.device_type}


def _apply_ticket_history(session: Session, rng: random.Random) -> None:
    now = datetime.now(UTC)
    tickets = list(session.scalars(select(Ticket)).all())
    for ticket in tickets:
        created = now - timedelta(days=rng.uniform(0, 29), hours=rng.uniform(0, 23), minutes=rng.uniform(0, 59))
        ticket.ticket_created_at = created
        ticket.status = rng.choice(TICKET_STATUSES)
        event = session.get(NetworkEvent, ticket.source_event_id)
        if event is not None:
            event.received_at = created - timedelta(minutes=rng.randint(1, 180))
            event.processed_at = created
        audit = session.scalar(
            select(AuditEvent).where(
                AuditEvent.ticket_id == ticket.id,
                AuditEvent.event_type == "event_processed",
            )
        )
        if audit is not None:
            audit.created_at = created
    session.flush()


def _phone(rng: random.Random) -> str:
    if rng.random() < 0.7:
        return "60" + rng.choice(("11", "12", "13", "14", "16", "17", "18", "19")) + f"{rng.randint(1000000, 9999999)}"
    area = rng.choice(("3", "4", "5", "7", "8", "9", "82", "88"))
    return f"60{area}{rng.randint(1000000, 9999999)}"


def _email(name: str, index: int) -> str:
    slug = "".join(part.lower() for part in name.split() if part.lower() not in ("bin", "binti", "a/l", "a/p"))[:18]
    return f"{slug or 'customer'}{index:03d}@{EMAIL_DOMAINS[index % len(EMAIL_DOMAINS)]}"


def _ssid_base(customer: Customer, index: int) -> str:
    if "SDN BHD" in customer.name.upper() or "RESTORAN" in customer.name.upper() or "KEDAI" in customer.name.upper():
        return f"Biz{index:03d}WiFi"
    return f"{customer.name.split()[0].title()}Home"


def _mac(rng: random.Random) -> str:
    return ":".join(f"{rng.randint(0, 255):02x}" for _ in range(6))


def main() -> None:
    from app.db.session import SessionLocal

    customer_count = DEFAULT_CUSTOMER_COUNT
    ticket_count = DEFAULT_TICKET_COUNT
    include_unifi = "--include-unifi" in sys.argv[1:]
    for argument in sys.argv[1:]:
        if argument.startswith("--customers="):
            customer_count = int(argument.split("=", 1)[1])
        elif argument.startswith("--tickets="):
            ticket_count = int(argument.split("=", 1)[1])

    with SessionLocal() as session:
        result = reset_and_seed(
            session,
            customer_count=customer_count,
            ticket_count=ticket_count,
            include_unifi=include_unifi,
        )
    print(
        "Reset complete: "
        + ", ".join(f"{value} {key}" for key, value in result.items())
    )


if __name__ == "__main__":
    main()
