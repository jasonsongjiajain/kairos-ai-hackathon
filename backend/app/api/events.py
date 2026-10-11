from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import AuthenticatedUser, require_roles
from app.db.session import get_session
from app.domain.event_rules import EVENT_PROCESSING_ROLES
from app.domain.schemas import (
    PendingEventRead,
    ProcessEventResponse,
    ProcessedTicketRead,
)
from app.services import event_processing
from app.services.event_processing import (
    EventNotFoundError,
    EventNotActionableError,
    NoTechnicianAvailableError,
)

router = APIRouter(prefix="/events", tags=["events"])
require_event_roles = require_roles(*EVENT_PROCESSING_ROLES)


@router.get("/pending", response_model=list[PendingEventRead])
def get_pending_events(
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(require_event_roles),
) -> list[PendingEventRead]:
    records = event_processing.list_pending_events(session, user)
    return [
        PendingEventRead(
            id=record.id,
            source_event_id=record.source_event_id,
            event_type=record.event_type,
            device_id=record.device_id,
            device_ref=record.device_ref,
            device_name=record.device_name,
            device_status=record.device_status,
            service_id=record.service_id,
            service_ref=record.service_ref,
            payload=record.payload,
            received_at=record.received_at,
        )
        for record in records
    ]


@router.post("/{event_id}/process", response_model=ProcessEventResponse)
def process_event(
    event_id: str,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(require_event_roles),
) -> ProcessEventResponse:
    try:
        result = event_processing.process_event(session, event_id, user)
    except EventNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found") from error
    except EventNotActionableError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Event cannot be turned into a ticket",
        ) from error
    except NoTechnicianAvailableError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No technician is available for assignment",
        ) from error

    return ProcessEventResponse(
        ticket=ProcessedTicketRead.model_validate(result.ticket),
        created=result.created,
        duplicate=not result.created,
        source_event_id=result.source_event_id,
        assigned_technician_name=result.assigned_technician_name,
    )
