"""Preserve legacy vectors and add model-tagged 1024-dimensional storage."""

from alembic import op
from pgvector.sqlalchemy import Vector
import sqlalchemy as sa

revision = "0005_embedding_1024"
down_revision = "0004_customer_accounts"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("knowledge_chunks", sa.Column("embedding_profile", sa.String(80), nullable=True))
    op.add_column("knowledge_chunks", sa.Column("embedding_1024", Vector(1024), nullable=True))
    op.add_column("knowledge_chunks", sa.Column("embedding_1024_profile", sa.String(80), nullable=True))


def downgrade() -> None:
    op.drop_column("knowledge_chunks", "embedding_1024_profile")
    op.drop_column("knowledge_chunks", "embedding_1024")
    op.drop_column("knowledge_chunks", "embedding_profile")
