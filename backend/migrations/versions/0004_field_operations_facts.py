"""Field-operations facts: TMFORCE ticket fields and embedded entity facts.

Adds TMFORCE metadata columns and a retrievable entity-fact index that mirrors
knowledge_chunks: one embeddable row per entity fact group plus typed rows for
exact display. Sensitive values never enter the embedded content.
"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

from app.config import get_settings

revision = "0004_field_operations_facts"
down_revision = "0003_embedding_dimension"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("staff_code", sa.String(length=20), nullable=True))
    op.create_unique_constraint("uq_users_staff_code", "users", ["staff_code"])

    op.add_column("tickets", sa.Column("tm_ticket_no", sa.String(length=60), nullable=True))
    op.add_column("tickets", sa.Column("ctt_activity_id", sa.String(length=60), nullable=True))
    op.add_column("tickets", sa.Column("login_id", sa.String(length=60), nullable=True))
    op.add_column("tickets", sa.Column("ticket_category", sa.String(length=60), nullable=True))
    op.add_column("tickets", sa.Column("ticket_created_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("tickets", sa.Column("staff_code", sa.String(length=20), nullable=True))
    op.create_unique_constraint("uq_tickets_tm_ticket_no", "tickets", ["tm_ticket_no"])

    op.create_table(
        "entity_fact_sheets",
        sa.Column("id", sa.String(length=160), nullable=False),
        sa.Column("entity_type", sa.String(length=20), nullable=False),
        sa.Column("entity_id", sa.String(length=36), nullable=False),
        sa.Column("group_key", sa.String(length=40), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("embedding", Vector(get_settings().embedding_dimensions), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_entity_fact_sheets")),
        sa.UniqueConstraint("entity_type", "entity_id", "group_key", name="uq_fact_sheet_entity_group"),
    )
    op.create_table(
        "entity_facts",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("entity_type", sa.String(length=20), nullable=False),
        sa.Column("entity_id", sa.String(length=36), nullable=False),
        sa.Column("group_key", sa.String(length=40), nullable=False),
        sa.Column("field_key", sa.String(length=60), nullable=False),
        sa.Column("label", sa.String(length=120), nullable=False),
        sa.Column("value_text", sa.Text(), nullable=True),
        sa.Column("value_number", sa.Float(), nullable=True),
        sa.Column("is_sensitive", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("source_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_entity_facts")),
        sa.UniqueConstraint("entity_type", "entity_id", "field_key", name="uq_fact_entity_field"),
    )
    op.create_index("ix_entity_facts_entity", "entity_facts", ["entity_type", "entity_id"])

    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_entity_fact_sheets_embedding "
        "ON entity_fact_sheets USING hnsw (embedding vector_cosine_ops)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_entity_fact_sheets_embedding")
    op.drop_index("ix_entity_facts_entity", table_name="entity_facts")
    op.drop_table("entity_facts")
    op.drop_table("entity_fact_sheets")
    op.drop_constraint("uq_tickets_tm_ticket_no", "tickets", type_="unique")
    op.drop_column("tickets", "staff_code")
    op.drop_column("tickets", "ticket_created_at")
    op.drop_column("tickets", "ticket_category")
    op.drop_column("tickets", "login_id")
    op.drop_column("tickets", "ctt_activity_id")
    op.drop_column("tickets", "tm_ticket_no")
    op.drop_constraint("uq_users_staff_code", "users", type_="unique")
    op.drop_column("users", "staff_code")
