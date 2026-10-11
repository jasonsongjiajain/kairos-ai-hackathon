"""Idempotent knowledge indexing for the curated markdown corpus.

``python -m app.ai.ingestion`` parses every ``*.md`` under ``seed/knowledge``,
upserts documents and chunks by their stable versioned keys, and fills missing
embeddings. Running it twice adds no rows and reuses existing embeddings.
"""

from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.chunking import DocumentChunkSpec, ParsedDocument, parse_document
from app.ai.ports import EmbeddingProvider
from app.config import get_settings
from app.domain.models import KnowledgeChunk, KnowledgeDocument
from app.integrations.embeddings import build_embedding_provider

DEFAULT_KNOWLEDGE_DIR = Path(__file__).resolve().parents[2] / "seed" / "knowledge"


@dataclass(frozen=True)
class IngestionReport:
    documents: int
    chunks: int
    embeddings_generated: int
    embeddings_reused: int


def index_knowledge(
    session: Session,
    embedder: EmbeddingProvider,
    *,
    directory: Path | str = DEFAULT_KNOWLEDGE_DIR,
    source_type: str = "curated_procedure",
) -> IngestionReport:
    parsed = _parse_directory(directory, source_type)
    for document_spec in parsed:
        document = _upsert_document(session, document_spec)
        for chunk_spec in document_spec.chunks:
            _upsert_chunk(session, document, chunk_spec)
    session.flush()

    generated, reused = embed_missing_chunks(session, embedder)
    session.flush()
    return IngestionReport(
        documents=len(parsed),
        chunks=sum(len(document_spec.chunks) for document_spec in parsed),
        embeddings_generated=generated,
        embeddings_reused=reused,
    )


def embed_missing_chunks(session: Session, embedder: EmbeddingProvider) -> tuple[int, int]:
    """Fill embeddings on any persisted chunk that lacks one; reuse existing ones."""
    titles = {
        document.id: document.title
        for document in session.scalars(select(KnowledgeDocument)).all()
    }
    generated = 0
    reused = 0
    for chunk in session.scalars(select(KnowledgeChunk).order_by(KnowledgeChunk.id)).all():
        if chunk.embedding is not None:
            reused += 1
            continue
        text = _embedding_text(titles.get(chunk.document_id, ""), chunk.section, chunk.content)
        chunk.embedding = embedder.embed_documents([text])[0]
        generated += 1
    session.flush()
    return generated, reused


def _parse_directory(directory: Path | str, source_type: str) -> list[ParsedDocument]:
    return [
        parse_document(path.read_text(encoding="utf-8"), source_type=source_type)
        for path in sorted(Path(directory).glob("*.md"))
    ]


def _upsert_document(session: Session, spec: ParsedDocument) -> KnowledgeDocument:
    document = session.get(KnowledgeDocument, spec.document_key)
    if document is None:
        document = KnowledgeDocument(
            id=spec.document_key,
            document_key=spec.document_key,
            title=spec.title,
            source_type=spec.source_type,
            version=spec.version,
        )
        session.add(document)
        session.flush()
        return document
    _require_canonical(
        document,
        document_key=spec.document_key,
        title=spec.title,
        source_type=spec.source_type,
        version=spec.version,
    )
    return document


def _upsert_chunk(
    session: Session,
    document: KnowledgeDocument,
    spec: DocumentChunkSpec,
) -> KnowledgeChunk:
    chunk = session.get(KnowledgeChunk, spec.chunk_id)
    if chunk is None:
        chunk = KnowledgeChunk(
            id=spec.chunk_id,
            document_id=document.id,
            section=spec.section,
            content=spec.content,
        )
        session.add(chunk)
        session.flush()
        return chunk
    _require_canonical(chunk, document_id=document.id, section=spec.section, content=spec.content)
    return chunk


def _embedding_text(title: str, section: str, content: str) -> str:
    return "\n".join(part for part in (title, section, content) if part)


def _require_canonical(row: object, **expected_fields: str) -> None:
    divergent = [name for name, expected in expected_fields.items() if getattr(row, name) != expected]
    if divergent:
        identity = getattr(row, "id", "unknown")
        raise RuntimeError(
            f"Knowledge index conflict for {identity}: noncanonical fields {', '.join(divergent)}"
        )


def main() -> None:
    from app.db.session import SessionLocal

    embedder = build_embedding_provider(get_settings())
    with SessionLocal() as session:
        report = index_knowledge(session, embedder)
        session.commit()
    print(
        f"Indexed {report.documents} documents, {report.chunks} chunks; "
        f"generated {report.embeddings_generated} embeddings, reused {report.embeddings_reused}"
    )


if __name__ == "__main__":
    main()
