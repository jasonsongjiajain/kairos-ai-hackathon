"""Bounded, secret-free context assembly from an authorized ticket.

Only authorized ticket/customer/topology fields are included, sizes are capped,
and credential-shaped values are dropped or redacted before they can reach a
model prompt.
"""

from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.auth.dependencies import AuthenticatedUser
from app.domain.models import Service
from app.domain.schemas import CREDENTIAL_KEYS
from app.services import ticket_queries

MAX_SUMMARY = 300
MAX_ADDRESS = 160
MAX_DETAIL_VALUE = 200
MAX_DETAIL_ENTRIES = 12
MAX_SERVICES = 20
MAX_DEVICES = 20
MAX_TOPOLOGY_NODES = 20
MAX_TOPOLOGY_EDGES = 40

_CREDENTIAL_MARKERS = ("secret", "token", "password", "passphrase", "credential")


@dataclass(frozen=True)
class ServiceContext:
    service_type: str
    service_ref: str
    status: str
    details: dict[str, str]


@dataclass(frozen=True)
class DeviceContext:
    device_ref: str
    device_type: str
    name: str
    status: str


@dataclass(frozen=True)
class BoundedContext:
    ticket_id: str
    summary: str
    severity: str
    status: str
    customer_ref: str
    customer_name: str
    address: str
    services: list[ServiceContext]
    devices: list[DeviceContext]
    topology_nodes: list[str]
    topology_edges: list[tuple[str, str]]

    def as_dict(self) -> dict[str, object]:
        return {
            "ticket": {
                "id": self.ticket_id,
                "summary": self.summary,
                "severity": self.severity,
                "status": self.status,
            },
            "customer": {
                "ref": self.customer_ref,
                "name": self.customer_name,
                "address": self.address,
            },
            "services": [
                {
                    "type": service.service_type,
                    "ref": service.service_ref,
                    "status": service.status,
                    "details": service.details,
                }
                for service in self.services
            ],
            "devices": [
                {
                    "ref": device.device_ref,
                    "type": device.device_type,
                    "name": device.name,
                    "status": device.status,
                }
                for device in self.devices
            ],
            "topology": {"nodes": self.topology_nodes, "edges": self.topology_edges},
        }

    def as_prompt_text(self) -> str:
        lines = [
            f"Ticket {self.ticket_id} [{self.severity}/{self.status}]: {self.summary}",
            f"Customer {self.customer_ref} at {self.address}",
        ]
        for service in self.services:
            lines.append(f"Service {service.service_type} {service.service_ref} ({service.status})")
        for device in self.devices:
            lines.append(f"Device {device.device_ref} {device.device_type} ({device.status})")
        if self.topology_edges:
            path = " -> ".join(self.topology_nodes)
            lines.append(f"Topology: {path}")
        return "\n".join(lines)


def assemble_context(session: Session, ticket_id: str, actor: AuthenticatedUser) -> BoundedContext:
    detail = ticket_queries.get_ticket_detail(session, ticket_id, actor)
    topology = ticket_queries.get_ticket_topology(session, ticket_id, actor)
    ticket = detail.ticket
    node_refs = {node.device_id: node.device_ref for node in topology.nodes}
    return BoundedContext(
        ticket_id=ticket.id,
        summary=ticket.summary[:MAX_SUMMARY],
        severity=ticket.severity,
        status=ticket.status,
        customer_ref=detail.customer.customer_ref,
        customer_name=detail.customer.name,
        address=detail.customer.address[:MAX_ADDRESS],
        services=[_service_context(service) for service in detail.services[:MAX_SERVICES]],
        devices=[_device_context(device) for device in detail.devices[:MAX_DEVICES]],
        topology_nodes=[node.device_ref for node in topology.nodes[:MAX_TOPOLOGY_NODES]],
        topology_edges=[
            (
                node_refs.get(edge.source_device_id, edge.source_device_id),
                node_refs.get(edge.target_device_id, edge.target_device_id),
            )
            for edge in topology.edges[:MAX_TOPOLOGY_EDGES]
        ],
    )


def _service_context(service: Service) -> ServiceContext:
    return ServiceContext(
        service_type=service.service_type,
        service_ref=service.service_ref,
        status=service.status,
        details=_safe_details(service.details),
    )


def _device_context(device: ticket_queries.DeviceRecord) -> DeviceContext:
    return DeviceContext(
        device_ref=device.device_ref,
        device_type=device.device_type,
        name=device.name,
        status=device.status,
    )


def _safe_details(details: dict | None) -> dict[str, str]:
    if not details:
        return {}
    safe: dict[str, str] = {}
    for key in sorted(details):
        lowered = key.lower()
        if lowered in CREDENTIAL_KEYS or any(marker in lowered for marker in _CREDENTIAL_MARKERS):
            continue
        safe[key] = _safe_value(details[key])
        if len(safe) >= MAX_DETAIL_ENTRIES:
            break
    return safe


def _safe_value(value: object) -> str:
    text = "" if value is None else str(value)
    if any(marker in text.lower() for marker in _CREDENTIAL_MARKERS):
        return "[redacted]"
    return text[:MAX_DETAIL_VALUE]
