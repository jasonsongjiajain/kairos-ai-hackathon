from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.ai import retrieval
from app.ai.ports import EmbeddingProvider
from app.auth.dependencies import AuthenticatedUser, get_current_user
from app.config import get_settings
from app.db.session import get_session
from app.integrations.embeddings import build_embedding_provider
from app.services.ticket_queries import TicketNotFoundError

router = APIRouter(prefix="/knowledge", tags=["knowledge"])


def get_embedding_provider() -> EmbeddingProvider:
    return build_embedding_provider(get_settings())


class KnowledgeCitationRead(BaseModel):
    chunk_id: str
    document_id: str
    document_title: str
    section: str
    source_type: str
    content: str
    score: float


@router.get("/search", response_model=list[KnowledgeCitationRead])
def search_knowledge(
    q: str = Query(min_length=1, max_length=300),
    ticket_id: str | None = Query(default=None),
    session: Session = Depends(get_session),
    user: AuthenticatedUser = Depends(get_current_user),
    embedder: EmbeddingProvider = Depends(get_embedding_provider),
) -> list[KnowledgeCitationRead]:
    try:
        if ticket_id is not None:
            matches = retrieval.retrieve_for_ticket(session, ticket_id, user, q, embedder)
        else:
            matches = retrieval.retrieve(session, q, embedder)
    except TicketNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket not found") from error

    return [
        KnowledgeCitationRead(
            chunk_id=match.chunk_id,
            document_id=match.document_id,
            document_title=match.document_title,
            section=match.section,
            source_type=match.source_type,
            content=match.content,
            score=match.score,
        )
        for match in matches
    ]
