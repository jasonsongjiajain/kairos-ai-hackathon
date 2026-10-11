"""Assignment-scoped ticket, customer, and topology queries.

Every function here re-checks authorization with ``app.auth.policy`` before it
returns data. The HTTP layer only translates records into response schemas, so a
caller cannot read another user's work by calling the service directly either.
"""

from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import AuthenticatedUser
from app.auth.policy import require_assigned_ticket, require_customer_scope, require_role
from app.domain.models import (
    AuditEvent,
    Customer,
    NetworkDevice,
    Service,
    Ticket,
    TopologyEdge,
    User,
)
from app.domain.schemas import find_credential

TICKET_FULL_SCOPE_ROLES = ("operator", "supervisor")
TECHNICIAN_ROLE = ("technician",)
_SEVERITY_RANK = {"high": 0, "medium": 1, "low": 2}


class TicketNotFoundError(Exception):
    pass


class CustomerNotFoundError(Exception):
    pass


class CredentialUnavailableError(Exception):
    pass


@dataclass(frozen=True)
class AssignedTicketRecord:
    id: str
    source_event_id: str
    customer_id: str
    service_id: str | None
    assigned_technician_id: str
    severity: str
    status: str
    summary: str
    customer_ref: str
    customer_name: str
    service_type: str | None
    service_ref: str | None


@dataclass(frozen=True)
class DeviceRecord:
    id: str
    device_ref: str
    device_type: str
    name: str
    status: str
    credential_available: bool


@dataclass(frozen=True)
class TicketDetailRecord:
    ticket: Ticket
    assigned_technician_name: str
    customer: Customer
    services: list[Service]
    devices: list[DeviceRecord]


@dataclass(frozen=True)
class CustomerDetailRecord:
    customer: Customer
    services: list[Service]
    devices: list[DeviceRecord]


@dataclass(frozen=True)
class TopologyNodeRecord:
    device_id: str
    device_ref: str
    device_type: str
    name: str
    status: str
    service_id: str | None
    service_ref: str | None


@dataclass(frozen=True)
class TopologyEdgeRecord:
    source_device_id: str
    target_device_id: str
    service_id: str | None
    service_ref: str | None


@dataclass(frozen=True)
class TopologyPathRecord:
    ticket_id: str
    service_id: str | None
    service_ref: str | None
    nodes: list[TopologyNodeRecord]
    edges: list[TopologyEdgeRecord]


@dataclass(frozen=True)
class CredentialRevealRecord:
    device_id: str
    device_ref: str
    credential_type: str
    credential: str


def list_assigned_tickets(session: Session, actor: AuthenticatedUser) -> list[AssignedTicketRecord]:
    require_role(actor.role, TECHNICIAN_ROLE)
    rows = session.execute(
        select(Ticket, Customer, Service)
        .join(Customer, Customer.id == Ticket.customer_id)
        .outerjoin(Service, Service.id == Ticket.service_id)
        .where(Ticket.assigned_technician_id == actor.id)
    ).all()
    records = [
        AssignedTicketRecord(
            id=ticket.id,
            source_event_id=ticket.source_event_id,
            customer_id=ticket.customer_id,
            service_id=ticket.service_id,
            assigned_technician_id=ticket.assigned_technician_id,
            severity=ticket.severity,
            status=ticket.status,
            summary=ticket.summary,
            customer_ref=customer.customer_ref,
            customer_name=customer.name,
            service_type=service.service_type if service is not None else None,
            service_ref=service.service_ref if service is not None else None,
        )
        for ticket, customer, service in rows
    ]
    records.sort(key=lambda record: (_SEVERITY_RANK.get(record.severity, 3), record.id))
    return records


def get_ticket_detail(session: Session, ticket_id: str, actor: AuthenticatedUser) -> TicketDetailRecord:
    ticket = _authorized_ticket(session, ticket_id, actor)
    customer = session.get(Customer, ticket.customer_id)
    if customer is None:
        raise TicketNotFoundError(ticket_id)
    assigned = session.get(User, ticket.assigned_technician_id)
    services = list(
        session.scalars(
            select(Service)
            .where(Service.customer_id == ticket.customer_id)
            .order_by(Service.service_type)
        ).all()
    )
    devices = _customer_devices(session, ticket.customer_id)
    return TicketDetailRecord(
        ticket=ticket,
        assigned_technician_name=assigned.display_name if assigned is not None else "",
        customer=customer,
        services=services,
        devices=devices,
    )


def get_customer_detail(session: Session, customer_id: str, actor: AuthenticatedUser) -> CustomerDetailRecord:
    require_role(actor.role, TECHNICIAN_ROLE + TICKET_FULL_SCOPE_ROLES)
    customer = session.get(Customer, customer_id)
    if customer is None:
        raise CustomerNotFoundError(customer_id)

    if actor.role == "technician":
        assignment = session.scalar(
            select(Ticket).where(
                Ticket.customer_id == customer_id,
                Ticket.assigned_technician_id == actor.id,
            )
        )
        if assignment is None:
            raise CustomerNotFoundError(customer_id)
        ticket_assignee_id = assignment.assigned_technician_id
    else:
        ticket_assignee_id = actor.id

    require_customer_scope(
        actor.id,
        actor.role,
        allowed_roles=TICKET_FULL_SCOPE_ROLES,
        ticket_assignee_id=ticket_assignee_id,
        ticket_customer_id=customer_id,
        requested_customer_id=customer_id,
    )

    services = list(
        session.scalars(
            select(Service)
            .where(Service.customer_id == customer_id)
            .order_by(Service.service_type)
        ).all()
    )
    return CustomerDetailRecord(
        customer=customer,
        services=services,
        devices=_customer_devices(session, customer_id),
    )


def get_ticket_topology(session: Session, ticket_id: str, actor: AuthenticatedUser) -> TopologyPathRecord:
    ticket = _authorized_ticket(session, ticket_id, actor)
    devices = {device.id: device for device in _customer_devices_orm(session, ticket.customer_id)}
    if not devices:
        return TopologyPathRecord(ticket_id=ticket.id, service_id=ticket.service_id, service_ref=None, nodes=[], edges=[])

    edges = list(
        session.scalars(
            select(TopologyEdge)
            .where(
                TopologyEdge.source_device_id.in_(list(devices)),
                TopologyEdge.target_device_id.in_(list(devices)),
            )
            .order_by(TopologyEdge.id)
        ).all()
    )
    if ticket.service_id is not None:
        scoped = [edge for edge in edges if edge.service_id in (ticket.service_id, None)]
        edges = scoped or edges

    ordered_ids = _order_path(edges)
    service_ids = {edge.service_id for edge in edges if edge.service_id is not None}
    service_lookup = _service_refs(session, service_ids)

    nodes = []
    for device_id in ordered_ids:
        device = devices[device_id]
        node_service_id = _node_service_id(device_id, edges)
        nodes.append(
            TopologyNodeRecord(
                device_id=device_id,
                device_ref=device.device_ref,
                device_type=device.device_type,
                name=device.name,
                status=device.status,
                service_id=node_service_id,
                service_ref=service_lookup.get(node_service_id),
            )
        )
    edge_records = [
        TopologyEdgeRecord(
            source_device_id=edge.source_device_id,
            target_device_id=edge.target_device_id,
            service_id=edge.service_id,
            service_ref=service_lookup.get(edge.service_id),
        )
        for edge in edges
    ]
    ticket_service_ref = service_lookup.get(ticket.service_id)
    return TopologyPathRecord(
        ticket_id=ticket.id,
        service_id=ticket.service_id,
        service_ref=ticket_service_ref,
        nodes=nodes,
        edges=edge_records,
    )


def reveal_device_credential(
    session: Session,
    ticket_id: str,
    device_id: str,
    actor: AuthenticatedUser,
) -> CredentialRevealRecord:
    require_role(actor.role, TECHNICIAN_ROLE)
    ticket = session.get(Ticket, ticket_id)
    if ticket is None:
        raise TicketNotFoundError(ticket_id)
    require_assigned_ticket(actor.id, ticket.assigned_technician_id, actor.role)

    device = session.get(NetworkDevice, device_id)
    if device is None or device.customer_id != ticket.customer_id:
        raise CredentialUnavailableError(device_id)
    found = find_credential(device.details)
    if found is None:
        raise CredentialUnavailableError(device_id)
    credential_type, credential = found

    session.add(
        AuditEvent(
            actor_id=actor.id,
            ticket_id=ticket.id,
            event_type="credential_revealed",
            details={
                "device_id": device.id,
                "device_ref": device.device_ref,
                "credential_type": credential_type,
            },
        )
    )
    session.commit()

    return CredentialRevealRecord(
        device_id=device.id,
        device_ref=device.device_ref,
        credential_type=credential_type,
        credential=credential,
    )


def _authorized_ticket(session: Session, ticket_id: str, actor: AuthenticatedUser) -> Ticket:
    ticket = session.get(Ticket, ticket_id)
    if ticket is None:
        raise TicketNotFoundError(ticket_id)
    require_assigned_ticket(actor.id, ticket.assigned_technician_id, actor.role)
    require_customer_scope(
        actor.id,
        actor.role,
        allowed_roles=TICKET_FULL_SCOPE_ROLES,
        ticket_assignee_id=ticket.assigned_technician_id,
        ticket_customer_id=ticket.customer_id,
        requested_customer_id=ticket.customer_id,
    )
    return ticket


def _customer_devices(session: Session, customer_id: str) -> list[DeviceRecord]:
    return [_device_record(device) for device in _customer_devices_orm(session, customer_id)]


def _customer_devices_orm(session: Session, customer_id: str) -> list[NetworkDevice]:
    return list(
        session.scalars(
            select(NetworkDevice)
            .where(NetworkDevice.customer_id == customer_id)
            .order_by(NetworkDevice.device_ref)
        ).all()
    )


def _device_record(device: NetworkDevice) -> DeviceRecord:
    return DeviceRecord(
        id=device.id,
        device_ref=device.device_ref,
        device_type=device.device_type,
        name=device.name,
        status=device.status,
        credential_available=find_credential(device.details) is not None,
    )


def _service_refs(session: Session, service_ids: set[str]) -> dict[str, str]:
    if not service_ids:
        return {}
    return {
        service.id: service.service_ref
        for service in session.scalars(select(Service).where(Service.id.in_(service_ids))).all()
    }


def _node_service_id(device_id: str, edges: list[TopologyEdge]) -> str | None:
    for edge in edges:
        if edge.source_device_id == device_id or edge.target_device_id == device_id:
            if edge.service_id is not None:
                return edge.service_id
    return None


def _order_path(edges: list[TopologyEdge]) -> list[str]:
    """Order devices into a forward path for the given edges, tolerating branches."""
    if not edges:
        return []
    adjacency: dict[str, list[str]] = {}
    nodes: list[str] = []
    for edge in edges:
        adjacency.setdefault(edge.source_device_id, []).append(edge.target_device_id)
        for device_id in (edge.source_device_id, edge.target_device_id):
            if device_id not in nodes:
                nodes.append(device_id)
    targets = {edge.target_device_id for edge in edges}
    starts = [node for node in nodes if node not in targets] or [nodes[0]]

    ordered: list[str] = []
    seen: set[str] = set()
    stack = list(reversed(starts))
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        ordered.append(node)
        stack.extend(reversed(adjacency.get(node, [])))
    for node in nodes:
        if node not in seen:
            ordered.append(node)
    return ordered
