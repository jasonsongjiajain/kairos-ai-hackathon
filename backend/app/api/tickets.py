from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.db.session import get_session
from app.domain.schemas import (
    AssignedTicketRead,
    CredentialRevealRead,
    CustomerRead,
    DeviceRead,
    ServiceRead,
    TicketDetailRead,
    TicketRead,
    TopologyEdgeRead,
    TopologyNodeRead,
    TopologyPathRead,
)
from app.services import ticket_queries
from app.services.ticket_queries import (
    CredentialUnavailableError,
    TicketNotFoundError,
)

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.get("/mine", response_model=list[AssignedTicketRead])
def list_my_tickets(
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user),
) -> list[AssignedTicketRead]:
    records = ticket_queries.list_assigned_tickets(session, user)
    return [
        AssignedTicketRead(
            id=record.id,
            source_event_id=record.source_event_id,
            customer_id=record.customer_id,
            service_id=record.service_id,
            assigned_technician_id=record.assigned_technician_id,
            severity=record.severity,
            status=record.status,
            summary=record.summary,
            customer_ref=record.customer_ref,
            customer_name=record.customer_name,
            service_type=record.service_type,
            service_ref=record.service_ref,
        )
        for record in records
    ]


@router.get("/{ticket_id}", response_model=TicketDetailRead)
def get_ticket(
    ticket_id: str,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user),
) -> TicketDetailRead:
    try:
        record = ticket_queries.get_ticket_detail(session, ticket_id, user)
    except TicketNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found") from error

    return TicketDetailRead(
        ticket=TicketRead.model_validate(record.ticket),
        assigned_technician_name=record.assigned_technician_name,
        customer=CustomerRead.model_validate(record.customer),
        services=[ServiceRead.model_validate(service) for service in record.services],
        devices=[_device_read(device) for device in record.devices],
    )


@router.get("/{ticket_id}/topology", response_model=TopologyPathRead)
def get_ticket_topology(
    ticket_id: str,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user),
) -> TopologyPathRead:
    try:
        record = ticket_queries.get_ticket_topology(session, ticket_id, user)
    except TicketNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found") from error

    return TopologyPathRead(
        ticket_id=record.ticket_id,
        service_id=record.service_id,
        service_ref=record.service_ref,
        nodes=[
            TopologyNodeRead(
                device_id=node.device_id,
                device_ref=node.device_ref,
                device_type=node.device_type,
                name=node.name,
                status=node.status,
                service_id=node.service_id,
                service_ref=node.service_ref,
            )
            for node in record.nodes
        ],
        edges=[
            TopologyEdgeRead(
                source_device_id=edge.source_device_id,
                target_device_id=edge.target_device_id,
                service_id=edge.service_id,
                service_ref=edge.service_ref,
            )
            for edge in record.edges
        ],
    )


@router.get("/{ticket_id}/devices/{device_id}/credential", response_model=CredentialRevealRead)
def reveal_device_credential(
    ticket_id: str,
    device_id: str,
    response: Response,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user),
) -> CredentialRevealRead:
    try:
        record = ticket_queries.reveal_device_credential(session, ticket_id, device_id, user)
    except TicketNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found") from error
    except CredentialUnavailableError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No demo credential is available for this device",
        ) from error

    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    return CredentialRevealRead(
        device_id=record.device_id,
        device_ref=record.device_ref,
        credential_type=record.credential_type,
        credential=record.credential,
    )


def _device_read(device: ticket_queries.DeviceRecord) -> DeviceRead:
    return DeviceRead(
        id=device.id,
        device_ref=device.device_ref,
        device_type=device.device_type,
        name=device.name,
        status=device.status,
        credential_available=device.credential_available,
    )
