import uuid
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from fastapi.responses import StreamingResponse
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
from app.services.event_stream import event_stream
from app.services.event_processing import (
    EventNotFoundError,
    EventNotActionableError,
    NoTechnicianAvailableError,
)

router = APIRouter(prefix="/events", tags=["events"])
require_event_roles = require_roles(*EVENT_PROCESSING_ROLES)


@router.post("/runs", status_code=status.HTTP_201_CREATED)
def create_event_run(
    user: AuthenticatedUser = Depends(require_event_roles),
) -> dict[str, object]:
    _ = user
    run_id = str(uuid.uuid4())
    state = event_stream.create_run(run_id)
    return {"run_id": run_id, "status": state.status, "events": state.events}


@router.get("/runs/{run_id}")
def get_event_run(
    run_id: str,
    user: AuthenticatedUser = Depends(require_event_roles),
) -> dict[str, object]:
    _ = user
    try:
        run_id = str(uuid.UUID(run_id))
    except ValueError as error:
        raise HTTPException(status_code=404, detail="Run not found") from error
    state = event_stream.get_run(run_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"run_id": run_id, "status": state.status, "events": state.events}


@router.get("/runs/{run_id}/events")
async def stream_event_run(
    run_id: str,
    last_event_id: Annotated[int | None, Header(alias="Last-Event-ID", ge=0)] = None,
    user: AuthenticatedUser = Depends(require_event_roles),
) -> StreamingResponse:
    _ = user
    try:
        run_id = str(uuid.UUID(run_id))
    except ValueError as error:
        raise HTTPException(status_code=404, detail="Run not found") from error
    state = event_stream.get_run(run_id)
    if state is None:
        raise HTTPException(status_code=404, detail="Run not found")
    cursor = len(state.events) if last_event_id is None else last_event_id

    async def messages():
        async for message in event_stream.subscribe(run_id, after=cursor):
            yield message

    return StreamingResponse(
        messages(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


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
    run_id: Annotated[str | None, Query()] = None,
) -> ProcessEventResponse:
    if run_id is not None:
        try:
            run_id = str(uuid.UUID(run_id))
        except ValueError as error:
            raise HTTPException(status_code=422, detail="run_id must be a UUID") from error
        event_stream.create_run_if_missing(run_id)
        event_stream.publish_nowait(
            run_id,
            "processing",
            {"event_id": event_id, "status": "processing", "occurred_at": datetime.now(UTC).isoformat()},
        )

    try:
        result = event_processing.process_event(session, event_id, user)
    except EventNotFoundError as error:
        if run_id:
            event_stream.publish_nowait(
                run_id,
                "failed",
                {"event_id": event_id, "status": "failed", "occurred_at": datetime.now(UTC).isoformat()},
            )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found") from error
    except EventNotActionableError as error:
        if run_id:
            event_stream.publish_nowait(
                run_id,
                "failed",
                {"event_id": event_id, "status": "failed", "occurred_at": datetime.now(UTC).isoformat()},
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Event cannot be turned into a ticket",
        ) from error
    except NoTechnicianAvailableError as error:
        if run_id:
            event_stream.publish_nowait(
                run_id,
                "failed",
                {"event_id": event_id, "status": "failed", "occurred_at": datetime.now(UTC).isoformat()},
            )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No technician is available for assignment",
        ) from error
    except Exception:
        if run_id:
            event_stream.publish_nowait(
                run_id,
                "failed",
                {"event_id": event_id, "status": "failed", "occurred_at": datetime.now(UTC).isoformat()},
            )
        raise

    if run_id:
        event_stream.publish_nowait(
            run_id,
            "ticket_created",
            {
                "event_id": event_id,
                "ticket_id": result.ticket.id,
                "created": result.created,
                "status": "completed",
                "occurred_at": datetime.now(UTC).isoformat(),
            },
        )

    return ProcessEventResponse(
        ticket=ProcessedTicketRead.model_validate(result.ticket),
        created=result.created,
        duplicate=not result.created,
        source_event_id=result.source_event_id,
        assigned_technician_name=result.assigned_technician_name,
    )
