from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.ai.ports import ChatCompletionProvider, EmbeddingProvider
from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.config import get_settings
from app.db.session import get_session
from app.domain.assistant_schemas import (
    AssistantAnswerRead,
    AssistantCitationRead,
    AssistantMessageRequest,
    NextBestActionRead,
)
from app.integrations.embeddings import build_embedding_provider
from app.integrations.model_provider import build_chat_provider
from app.services import assistant
from app.services.assistant import AssistantAnswerRecord, AssistantFormatError
from app.services.ticket_queries import TicketNotFoundError

router = APIRouter(prefix="/tickets", tags=["assistant"])


def get_embedding_provider() -> EmbeddingProvider:
    return build_embedding_provider(get_settings())


def get_chat_provider() -> ChatCompletionProvider:
    return build_chat_provider(get_settings())


@router.post("/{ticket_id}/assistant/messages", response_model=AssistantAnswerRead)
def create_assistant_message(
    ticket_id: str,
    payload: AssistantMessageRequest,
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user),
    embedder: EmbeddingProvider = Depends(get_embedding_provider),
    provider: ChatCompletionProvider = Depends(get_chat_provider),
) -> AssistantAnswerRead:
    try:
        record = assistant.answer_ticket_question(
            session,
            ticket_id,
            user,
            payload.question,
            embedder=embedder,
            provider=provider,
        )
    except TicketNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        ) from error
    except AssistantFormatError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The assistant returned an unreadable answer. Retry the question.",
        ) from error

    return _to_read(record)


def _to_read(record: AssistantAnswerRecord) -> AssistantAnswerRead:
    return AssistantAnswerRead(
        session_id=record.session_id,
        answer=record.answer,
        uncertainty=record.uncertainty,
        has_evidence=record.has_evidence,
        citations=[
            AssistantCitationRead(
                chunk_id=citation.chunk_id,
                document_id=citation.document_id,
                document_title=citation.document_title,
                section=citation.section,
                source_type=citation.source_type,
                content=citation.content,
                score=citation.score,
            )
            for citation in record.citations
        ],
        next_best_action=_next_best_action_read(record),
    )


def _next_best_action_read(record: AssistantAnswerRecord) -> NextBestActionRead | None:
    action = record.next_best_action
    if action is None:
        return None
    return NextBestActionRead(
        remediation=action.remediation,
        dispatch_required=action.dispatch_required,
        suggestion=action.suggestion,
        evidence=action.evidence,
        suggestion_evidence=action.suggestion_evidence,
    )
