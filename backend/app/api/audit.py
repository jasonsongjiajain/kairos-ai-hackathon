from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.db.session import get_session
from app.domain.tool_schemas import AuditEventRead
from app.services import audit_query
from app.services.audit_query import AuditScopeError

router = APIRouter(prefix="/tickets", tags=["audit"])


@router.get("/{ticket_id}/audit", response_model=list[AuditEventRead])
def list_ticket_audit(
    ticket_id: str,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user),
) -> list[AuditEventRead]:
    try:
        records = audit_query.list_ticket_audit(session, ticket_id, user)
    except AuditScopeError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found") from error
    return [
        AuditEventRead(
            id=record.id,
            event_type=record.event_type,
            actor_id=record.actor_id,
            actor_name=record.actor_name,
            ticket_id=record.ticket_id,
            details=record.details,
            created_at=record.created_at,
        )
        for record in records
    ]
