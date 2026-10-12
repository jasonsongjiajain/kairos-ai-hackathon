"""Idempotent knowledge indexing for the curated markdown corpus.

``python -m app.ai.ingestion`` parses every ``*.md`` under ``seed/knowledge``,
upserts documents and chunks by their stable versioned keys, and fills missing
embeddings. Running it twice adds no rows and reuses existing embeddings.
"""

import argparse
import math
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.chunking import DocumentChunkSpec, ParsedDocument, parse_document
from app.ai.ports import EmbeddingProvider
from app.ai.embedding_space import EmbeddingError, space_for, validate_vector
from app.config import get_settings
from app.domain.models import KnowledgeChunk, KnowledgeDocument
from app.integrations.embeddings import LOCAL_EMBEDDING_PROFILE, build_embedding_provider

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
    """Index the selected model space without altering the other dimension's vectors."""
    space = space_for(embedder)
    titles = {
        document.id: document.title
        for document in session.scalars(select(KnowledgeDocument)).all()
    }
    generated = 0
    reused = 0
    for chunk in session.scalars(select(KnowledgeChunk).order_by(KnowledgeChunk.id)).all():
        existing_vector = getattr(chunk, space.vector_attribute)
        existing_profile = getattr(chunk, space.profile_attribute)
        if existing_vector is not None and existing_profile == space.profile:
            validate_vector(list(existing_vector), space.dimension)
            reused += 1
            continue
        text = _embedding_text(titles.get(chunk.document_id, ""), chunk.section, chunk.content)
        vectors = embedder.embed_documents([text])
        if len(vectors) != 1:
            raise EmbeddingError("The embedding provider must return one vector for each document")
        vector = validate_vector(vectors[0], space.dimension)
        if existing_vector is not None and existing_profile is None and space.dimension == 1536:
            # Only label legacy local vectors when recomputation proves their provenance.
            matches_local = space.profile == LOCAL_EMBEDDING_PROFILE and len(existing_vector) == len(vector) and all(
                math.isclose(float(left), right, rel_tol=1e-6, abs_tol=1e-8)
                for left, right in zip(existing_vector, vector)
            )
            if not matches_local:
                raise EmbeddingError("Unlabelled legacy vectors could not be verified; use the separate 1024-dimensional space")
            setattr(chunk, space.profile_attribute, space.profile)
            reused += 1
            continue
        setattr(chunk, space.vector_attribute, vector)
        setattr(chunk, space.profile_attribute, space.profile)
        generated += 1
    session.flush()
    return generated, reused


def verify_embeddings(session: Session, embedder: EmbeddingProvider) -> int:
    space = space_for(embedder)
    chunks = list(session.scalars(select(KnowledgeChunk)))
    if not chunks:
        raise EmbeddingError("There is no knowledge text to verify; index the knowledge documents first")
    missing = 0
    for chunk in chunks:
        vector = getattr(chunk, space.vector_attribute)
        if vector is None or getattr(chunk, space.profile_attribute) != space.profile:
            missing += 1
        else:
            validate_vector(list(vector), space.dimension)
    if missing:
        raise EmbeddingError(f"{missing} of {len(chunks)} knowledge chunks are not indexed for the selected model")
    return len(chunks)


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

    parser = argparse.ArgumentParser(description="Index knowledge with the configured embedding model")
    parser.add_argument("--probe", action="store_true", help="Test the provider using one generic sentence; no database writes")
    parser.add_argument("--embeddings-only", action="store_true", help="Re-index all existing knowledge text in the selected model space")
    parser.add_argument("--verify", action="store_true", help="Check all existing chunks have valid vectors for the selected model; no network or writes")
    args = parser.parse_args()
    embedder = build_embedding_provider(get_settings())
    try:
        if args.probe:
            vector = validate_vector(embedder.embed_query("How should slow Internet be investigated?"), embedder.dimension)
            print(f"Embedding probe succeeded: {len(vector)} dimensions; profile {embedder.profile}")
            return
        if args.verify:
            with SessionLocal() as session:
                count = verify_embeddings(session, embedder)
            print(f"Verified {count} knowledge embeddings at {embedder.dimension} dimensions; profile {embedder.profile}")
            return
        with SessionLocal() as session:
            if args.embeddings_only:
                generated, reused = embed_missing_chunks(session, embedder)
                session.commit()
                print(f"Generated {generated} embeddings, reused {reused}; dimension {embedder.dimension}")
                return
            report = index_knowledge(session, embedder)
            session.commit()
    except EmbeddingError as error:
        parser.exit(1, f"Embedding operation failed: {error}\n")
    print(
        f"Indexed {report.documents} documents, {report.chunks} chunks; "
        f"generated {report.embeddings_generated} embeddings, reused {report.embeddings_reused}"
    )


if __name__ == "__main__":
    main()
