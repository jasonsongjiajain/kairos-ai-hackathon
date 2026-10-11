from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.db.session import get_session
from app.domain.tool_schemas import (
    ToolCatalogItemRead,
    ToolConfirmRequest,
    ToolExecutionRead,
    ToolProposalRead,
    ToolProposeRequest,
)
from app.services import tool_execution
from app.services.tool_execution import (
    ToolForbiddenError,
    ToolNotFoundError,
    ToolValidationError,
)

router = APIRouter(prefix="/tickets", tags=["tools"])


@router.get("/{ticket_id}/tools/catalog", response_model=list[ToolCatalogItemRead])
def get_tool_catalog(
    ticket_id: str,
    user: AuthenticatedUser = Depends(get_current_user),
) -> list[ToolCatalogItemRead]:
    return [
        ToolCatalogItemRead(
            name=item.name,
            description=item.description,
            kind=item.kind,
            requires_confirmation=item.requires_confirmation,
        )
        for item in tool_execution.catalog(user)
    ]


@router.get("/{ticket_id}/tools", response_model=list[ToolProposalRead])
def list_tool_proposals(
    ticket_id: str,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user),
) -> list[ToolProposalRead]:
    try:
        records = tool_execution.list_proposals(session, ticket_id, user)
    except ToolNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found") from error
    return [_proposal_read(record) for record in records]


@router.post("/{ticket_id}/tools/propose", response_model=ToolProposalRead, status_code=status.HTTP_201_CREATED)
def propose_tool(
    ticket_id: str,
    payload: ToolProposeRequest,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user),
) -> ToolProposalRead:
    parameters = {"device_id": payload.device_id, **payload.parameters}
    try:
        record = tool_execution.propose_tool(session, ticket_id, user, payload.tool_name, parameters)
    except ToolNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tool or ticket not found") from error
    except ToolForbiddenError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This action is not permitted here") from error
    except ToolValidationError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error
    return _proposal_read(record)


@router.post("/{ticket_id}/tools/{proposal_id}/confirm", response_model=ToolExecutionRead)
def confirm_tool(
    ticket_id: str,
    proposal_id: str,
    payload: ToolConfirmRequest,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user),
) -> ToolExecutionRead:
    try:
        record = tool_execution.confirm_tool(
            session, ticket_id, proposal_id, user, payload.confirmation_id
        )
    except ToolNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found") from error
    except ToolForbiddenError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action cannot be confirmed here",
        ) from error
    except ToolValidationError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error
    return _execution_read(record)


def _proposal_read(record: tool_execution.ToolProposalRecord) -> ToolProposalRead:
    return ToolProposalRead(
        id=record.id,
        ticket_id=record.ticket_id,
        tool_name=record.tool_name,
        device_id=record.device_id,
        device_ref=record.device_ref,
        kind=record.kind,
        requires_confirmation=record.requires_confirmation,
        parameters=record.parameters,
        status=record.status,
        summary=record.summary,
        created_at=record.created_at,
    )


def _execution_read(record: tool_execution.ToolExecutionRecord) -> ToolExecutionRead:
    return ToolExecutionRead(
        id=record.id,
        ticket_id=record.ticket_id,
        tool_name=record.tool_name,
        device_id=record.device_id,
        device_ref=record.device_ref,
        status=record.status,
        message=record.message,
        correlation_id=record.correlation_id,
        executed_at=record.executed_at,
    )
