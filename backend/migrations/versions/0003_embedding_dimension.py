"""Resize knowledge_chunks.embedding to the configured embedding dimension.

The hosted GIGX embedding model (qwen3-embedding-0.6b) returns 1024 dimensions,
so the original fixed 1536 column cannot store its vectors. This migration clears
stale vectors (they belong to a different model and cannot be cast) and resizes
the column to ``EMBEDDING_DIMENSIONS``. Re-ingest with ``--reembed`` afterwards.
"""

from alembic import op

from app.config import get_settings

revision = "0003_embedding_dimension"
down_revision = "0002_tool_execution_message"
branch_labels = None
depends_on = None

PREVIOUS_DIMENSION = 1536


def _resize(dimension: int) -> None:
    # Vectors from a different model are not comparable and cannot be cast, so
    # discard them before changing the column width.
    op.execute("UPDATE knowledge_chunks SET embedding = NULL")
    op.execute(
        f"ALTER TABLE knowledge_chunks ALTER COLUMN embedding TYPE vector({dimension})"
    )


def upgrade() -> None:
    _resize(get_settings().embedding_dimensions)


def downgrade() -> None:
    _resize(PREVIOUS_DIMENSION)
