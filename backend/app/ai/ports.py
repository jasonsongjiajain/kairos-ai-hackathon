"""Provider and storage boundaries for retrieval-grounded answers.

Callers depend on these protocols rather than a concrete provider, so tests can
inject deterministic fakes and deployment can swap in a hosted provider.
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol

from sqlalchemy.orm import Session

if TYPE_CHECKING:
    from app.ai.embedding_space import EmbeddingSpace


@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str


@dataclass(frozen=True)
class ChunkMatch:
    chunk_id: str
    document_id: str
    document_title: str
    section: str
    source_type: str
    content: str
    score: float


class EmbeddingProvider(Protocol):
    dimension: int
    profile: str

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]: ...

    def embed_query(self, text: str) -> list[float]: ...


class ChatCompletionProvider(Protocol):
    def complete(self, messages: Sequence[ChatMessage], *, temperature: float = 0.0) -> str: ...


class VectorSearch(Protocol):
    def search(
        self,
        session: Session,
        query_vector: Sequence[float],
        *,
        service_category: str | None,
        limit: int,
        embedding_space: "EmbeddingSpace",
    ) -> list[ChunkMatch]: ...
