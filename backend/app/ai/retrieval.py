"""Cited retrieval over knowledge chunks with a dialect-aware vector search.

PostgreSQL uses pgvector cosine distance. SQLite (the test database) has no
pgvector, so retrieval falls back to an in-memory cosine scan over the same
stored vectors. Both paths return the same ``ChunkMatch`` shape.
"""

import math
from collections.abc import Sequence

from sqlalchemy import Select, func, or_, select
from sqlalchemy.orm import Session

from app.ai.ports import ChunkMatch, EmbeddingProvider, VectorSearch
from app.ai.embedding_space import EmbeddingError, EmbeddingSpace, space_for, validate_vector
from app.auth.dependencies import AuthenticatedUser
from app.domain.models import KnowledgeChunk, KnowledgeDocument
from app.services import ticket_queries

SCOPED_SOURCE_TYPES = frozenset({"granite", "hsi", "vobb"})
DEFAULT_LIMIT = 5


def document_applies_to_service(source_type: str | None, service_category: str | None) -> bool:
    """Category-scoped documents match only their category; all others are global."""
    if service_category is None or source_type is None:
        return True
    normalized = source_type.strip().lower()
    if normalized in SCOPED_SOURCE_TYPES:
        return normalized == service_category.strip().lower()
    return True


def retrieve(
    session: Session,
    query: str,
    embedder: EmbeddingProvider,
    *,
    service_category: str | None = None,
    limit: int = DEFAULT_LIMIT,
) -> list[ChunkMatch]:
    space = space_for(embedder)
    query_vector = validate_vector(embedder.embed_query(query), space.dimension)
    return resolve_vector_search(session).search(
        session,
        query_vector,
        service_category=service_category,
        limit=limit,
        embedding_space=space,
    )


def retrieve_for_ticket(
    session: Session,
    ticket_id: str,
    actor: AuthenticatedUser,
    query: str,
    embedder: EmbeddingProvider,
    *,
    limit: int = DEFAULT_LIMIT,
) -> list[ChunkMatch]:
    """Retrieve with the service-category filter derived from an authorized ticket."""
    detail = ticket_queries.get_ticket_detail(session, ticket_id, actor)
    return retrieve(
        session,
        query,
        embedder,
        service_category=_ticket_service_category(detail),
        limit=limit,
    )


def resolve_vector_search(session: Session) -> VectorSearch:
    if session.get_bind().dialect.name == "postgresql":
        return PgVectorSearch()
    return InMemoryVectorSearch()


class PgVectorSearch:
    """pgvector cosine distance (``<=>``) ordered from most to least similar."""

    def search(
        self,
        session: Session,
        query_vector: Sequence[float],
        *,
        service_category: str | None,
        limit: int,
        embedding_space: EmbeddingSpace,
    ) -> list[ChunkMatch]:
        vector_column = getattr(KnowledgeChunk, embedding_space.vector_attribute)
        profile_column = getattr(KnowledgeChunk, embedding_space.profile_attribute)
        distance = vector_column.cosine_distance(list(query_vector))
        statement: Select = (
            select(KnowledgeChunk, KnowledgeDocument, distance.label("distance"))
            .join(KnowledgeDocument, KnowledgeDocument.id == KnowledgeChunk.document_id)
            .where(vector_column.is_not(None), profile_column == embedding_space.profile)
            .order_by(distance)
            .limit(limit)
        )
        statement = _filter_by_category(statement, service_category)
        rows = session.execute(statement).all()
        return [_match(chunk, document, 1.0 - float(distance_value)) for chunk, document, distance_value in rows]


class InMemoryVectorSearch:
    """Cosine scan over stored vectors, used when pgvector is unavailable."""

    def search(
        self,
        session: Session,
        query_vector: Sequence[float],
        *,
        service_category: str | None,
        limit: int,
        embedding_space: EmbeddingSpace,
    ) -> list[ChunkMatch]:
        rows = session.execute(
            select(KnowledgeChunk, KnowledgeDocument)
            .join(KnowledgeDocument, KnowledgeDocument.id == KnowledgeChunk.document_id)
            .where(
                getattr(KnowledgeChunk, embedding_space.vector_attribute).is_not(None),
                getattr(KnowledgeChunk, embedding_space.profile_attribute) == embedding_space.profile,
            )
        ).all()
        matches = [
            _match(chunk, document, cosine_similarity(query_vector, getattr(chunk, embedding_space.vector_attribute)))
            for chunk, document in rows
            if document_applies_to_service(document.source_type, service_category)
        ]
        matches.sort(key=lambda match: match.score, reverse=True)
        return matches[:limit]


def cosine_similarity(left: Sequence[float], right: Sequence[float] | None) -> float:
    if right is None:
        return 0.0
    if len(left) != len(right):
        raise EmbeddingError("Cannot compare embeddings with different dimensions")
    dot = 0.0
    left_norm = 0.0
    right_norm = 0.0
    for left_value, right_value in zip(left, right):
        dot += left_value * right_value
        left_norm += left_value * left_value
        right_norm += right_value * right_value
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (math.sqrt(left_norm) * math.sqrt(right_norm))


def _filter_by_category(statement: Select, service_category: str | None) -> Select:
    if service_category is None:
        return statement
    source_type = func.lower(KnowledgeDocument.source_type)
    return statement.where(
        or_(source_type.notin_(SCOPED_SOURCE_TYPES), source_type == service_category.strip().lower())
    )


def _match(chunk: KnowledgeChunk, document: KnowledgeDocument, score: float) -> ChunkMatch:
    return ChunkMatch(
        chunk_id=chunk.id,
        document_id=document.id,
        document_title=document.title,
        section=chunk.section,
        source_type=document.source_type,
        content=chunk.content,
        score=score,
    )


def _ticket_service_category(detail: ticket_queries.TicketDetailRecord) -> str | None:
    if detail.ticket.service_id is None:
        return None
    for service in detail.services:
        if service.id == detail.ticket.service_id:
            return service.service_type
    return None
