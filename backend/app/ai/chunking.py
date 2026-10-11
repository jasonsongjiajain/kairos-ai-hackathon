"""Heading-aware chunking for curated knowledge documents.

Sections delimited by ``## Section`` are the chunk boundary. This mirrors the
seed loader exactly so chunk IDs and content stay stable between seed and
ingestion.
"""

from dataclasses import dataclass

SECTION_PREFIX = "## "
HEADER_LINES = 3


@dataclass(frozen=True)
class DocumentChunkSpec:
    chunk_id: str
    document_key: str
    title: str
    version: str
    source_type: str
    section: str
    content: str


@dataclass(frozen=True)
class ParsedDocument:
    document_key: str
    title: str
    version: str
    source_type: str
    chunks: list[DocumentChunkSpec]


def section_slug(section: str) -> str:
    return section.strip().lower().replace(" ", "-")


def chunk_id_for(document_key: str, version: str, section: str) -> str:
    return f"{document_key}:{version}:{section_slug(section)}"


def parse_document(text: str, *, source_type: str = "curated_procedure") -> ParsedDocument:
    lines = text.splitlines()
    if len(lines) < HEADER_LINES:
        raise ValueError("Knowledge document is missing its key/title/version header")
    document_key, title, version = (line.strip() for line in lines[:HEADER_LINES])
    if not document_key or not title or not version:
        raise ValueError("Knowledge document header fields must not be empty")

    chunks = [
        DocumentChunkSpec(
            chunk_id=chunk_id_for(document_key, version, section),
            document_key=document_key,
            title=title,
            version=version,
            source_type=source_type,
            section=section,
            content="\n".join(body),
        )
        for section, body in _split_sections(lines[HEADER_LINES:])
    ]
    return ParsedDocument(
        document_key=document_key,
        title=title,
        version=version,
        source_type=source_type,
        chunks=chunks,
    )


def _split_sections(lines: list[str]) -> list[tuple[str, list[str]]]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in lines:
        if line.startswith(SECTION_PREFIX):
            current = line[len(SECTION_PREFIX):].strip()
            sections[current] = []
        elif current and line.strip():
            sections[current].append(line.strip())
    return [(section, body) for section, body in sections.items() if body]
