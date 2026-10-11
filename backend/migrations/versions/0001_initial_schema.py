"""Initial operational schema and pgvector support."""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

from app.config import get_settings

revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    dimensions = get_settings().embedding_dimensions
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "roles",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_roles")),
        sa.UniqueConstraint("name", name=op.f("uq_roles_name")),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role_id", sa.String(length=36), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_demo", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["role_id"], ["roles.id"], name=op.f("fk_users_role_id_roles")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
    )
    op.create_table(
        "customers",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("customer_ref", sa.String(length=80), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("address", sa.String(length=255), nullable=False),
        sa.Column("is_demo", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_customers")),
        sa.UniqueConstraint("customer_ref", name=op.f("uq_customers_customer_ref")),
    )
    op.create_table(
        "services",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("customer_id", sa.String(length=36), nullable=False),
        sa.Column("service_type", sa.String(length=40), nullable=False),
        sa.Column("service_ref", sa.String(length=100), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], name=op.f("fk_services_customer_id_customers")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_services")),
        sa.UniqueConstraint("service_ref", name=op.f("uq_services_service_ref")),
        sa.UniqueConstraint("customer_id", "service_type", name="uq_services_customer_type"),
    )
    op.create_table(
        "network_devices",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("customer_id", sa.String(length=36), nullable=True),
        sa.Column("device_ref", sa.String(length=100), nullable=False),
        sa.Column("device_type", sa.String(length=40), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], name=op.f("fk_network_devices_customer_id_customers")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_network_devices")),
        sa.UniqueConstraint("device_ref", name=op.f("uq_network_devices_device_ref")),
    )
    op.create_table(
        "knowledge_documents",
        sa.Column("id", sa.String(length=120), nullable=False),
        sa.Column("document_key", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("source_type", sa.String(length=40), nullable=False),
        sa.Column("version", sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_knowledge_documents")),
        sa.UniqueConstraint("document_key", "version", name="uq_document_version"),
    )
    op.create_table(
        "topology_edges",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("source_device_id", sa.String(length=36), nullable=False),
        sa.Column("target_device_id", sa.String(length=36), nullable=False),
        sa.Column("service_id", sa.String(length=36), nullable=True),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], name=op.f("fk_topology_edges_service_id_services")),
        sa.ForeignKeyConstraint(["source_device_id"], ["network_devices.id"], name=op.f("fk_topology_edges_source_device_id_network_devices")),
        sa.ForeignKeyConstraint(["target_device_id"], ["network_devices.id"], name=op.f("fk_topology_edges_target_device_id_network_devices")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_topology_edges")),
        sa.UniqueConstraint("source_device_id", "target_device_id", name="uq_topology_edge_path"),
    )
    op.create_table(
        "network_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("source_event_id", sa.String(length=120), nullable=False),
        sa.Column("event_type", sa.String(length=80), nullable=False),
        sa.Column("device_id", sa.String(length=36), nullable=False),
        sa.Column("service_id", sa.String(length=36), nullable=True),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["device_id"], ["network_devices.id"], name=op.f("fk_network_events_device_id_network_devices")),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], name=op.f("fk_network_events_service_id_services")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_network_events")),
        sa.UniqueConstraint("source_event_id", name=op.f("uq_network_events_source_event_id")),
    )
    op.create_table(
        "knowledge_chunks",
        sa.Column("id", sa.String(length=160), nullable=False),
        sa.Column("document_id", sa.String(length=120), nullable=False),
        sa.Column("section", sa.String(length=160), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("embedding", Vector(dimensions), nullable=True),
        sa.ForeignKeyConstraint(["document_id"], ["knowledge_documents.id"], name=op.f("fk_knowledge_chunks_document_id_knowledge_documents")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_knowledge_chunks")),
        sa.UniqueConstraint("document_id", "section", name="uq_chunk_document_section"),
    )
    op.create_table(
        "tickets",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("source_event_id", sa.String(length=36), nullable=False),
        sa.Column("customer_id", sa.String(length=36), nullable=False),
        sa.Column("service_id", sa.String(length=36), nullable=True),
        sa.Column("assigned_technician_id", sa.String(length=36), nullable=False),
        sa.Column("severity", sa.String(length=30), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("summary", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["assigned_technician_id"], ["users.id"], name=op.f("fk_tickets_assigned_technician_id_users")),
        sa.ForeignKeyConstraint(["customer_id"], ["customers.id"], name=op.f("fk_tickets_customer_id_customers")),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], name=op.f("fk_tickets_service_id_services")),
        sa.ForeignKeyConstraint(["source_event_id"], ["network_events.id"], name=op.f("fk_tickets_source_event_id_network_events")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tickets")),
        sa.UniqueConstraint("source_event_id", name=op.f("uq_tickets_source_event_id")),
    )
    op.create_table(
        "assistant_sessions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("ticket_id", sa.String(length=36), nullable=False),
        sa.Column("user_id", sa.String(length=36), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"], name=op.f("fk_assistant_sessions_ticket_id_tickets")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_assistant_sessions_user_id_users")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_assistant_sessions")),
    )
    op.create_table(
        "assistant_messages",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("session_id", sa.String(length=36), nullable=False),
        sa.Column("role", sa.String(length=30), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("citations", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["assistant_sessions.id"], name=op.f("fk_assistant_messages_session_id_assistant_sessions")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_assistant_messages")),
    )
    op.create_table(
        "tool_executions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("ticket_id", sa.String(length=36), nullable=False),
        sa.Column("actor_id", sa.String(length=36), nullable=False),
        sa.Column("tool_name", sa.String(length=100), nullable=False),
        sa.Column("parameters", sa.JSON(), nullable=False),
        sa.Column("outcome", sa.String(length=40), nullable=False),
        sa.Column("correlation_id", sa.String(length=120), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["actor_id"], ["users.id"], name=op.f("fk_tool_executions_actor_id_users")),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"], name=op.f("fk_tool_executions_ticket_id_tickets")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tool_executions")),
        sa.UniqueConstraint("correlation_id", name=op.f("uq_tool_executions_correlation_id")),
    )
    op.create_table(
        "audit_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("actor_id", sa.String(length=36), nullable=True),
        sa.Column("ticket_id", sa.String(length=36), nullable=True),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["actor_id"], ["users.id"], name=op.f("fk_audit_events_actor_id_users")),
        sa.ForeignKeyConstraint(["ticket_id"], ["tickets.id"], name=op.f("fk_audit_events_ticket_id_tickets")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_audit_events")),
    )


def downgrade() -> None:
    op.drop_table("audit_events")
    op.drop_table("tool_executions")
    op.drop_table("assistant_messages")
    op.drop_table("assistant_sessions")
    op.drop_table("tickets")
    op.drop_table("knowledge_chunks")
    op.drop_table("network_events")
    op.drop_table("topology_edges")
    op.drop_table("network_devices")
    op.drop_table("services")
    op.drop_table("knowledge_documents")
    op.drop_table("customers")
    op.drop_table("users")
    op.drop_table("roles")
