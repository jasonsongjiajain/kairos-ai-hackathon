"""Add execution message to tool_executions."""

from alembic import op
import sqlalchemy as sa

revision = "0002_tool_execution_message"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("tool_executions", sa.Column("message", sa.String(length=400), nullable=True))


def downgrade() -> None:
    op.drop_column("tool_executions", "message")
