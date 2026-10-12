import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, Numeric, String, Text, UniqueConstraint, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.config import Settings
from app.db.base import Base


def new_id() -> str:
    return str(uuid.uuid4())


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[str] = mapped_column(ForeignKey("roles.id"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("true"), nullable=False)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"), nullable=False)
    staff_code: Mapped[str | None] = mapped_column(String(20), unique=True)


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    customer_ref: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"), nullable=False)
    account_no: Mapped[str | None] = mapped_column(Text)
    contact_no: Mapped[str | None] = mapped_column(Text)
    email_address: Mapped[str | None] = mapped_column(Text)
    contract_term: Mapped[int | None] = mapped_column(Integer)
    commitment_start: Mapped[datetime | None] = mapped_column(DateTime)
    commitment_end: Mapped[datetime | None] = mapped_column(DateTime)


class Service(Base):
    __tablename__ = "services"
    __table_args__ = (UniqueConstraint("customer_id", "service_type", name="uq_services_customer_type"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"), nullable=False)
    service_type: Mapped[str] = mapped_column(String(40), nullable=False)
    service_ref: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False)
    details: Mapped[dict] = mapped_column(JSON, default=dict, server_default=text("'{}'"), nullable=False)


class NetworkDevice(Base):
    __tablename__ = "network_devices"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    customer_id: Mapped[str | None] = mapped_column(ForeignKey("customers.id"))
    device_ref: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    device_type: Mapped[str] = mapped_column(String(40), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(40), default="unknown", server_default=text("'unknown'"), nullable=False)
    details: Mapped[dict] = mapped_column(JSON, default=dict, server_default=text("'{}'"), nullable=False)
    mac_address: Mapped[str | None] = mapped_column(Text)
    login_id: Mapped[str | None] = mapped_column(Text)
    friendly_name: Mapped[str | None] = mapped_column(Text)
    manufacturer: Mapped[str | None] = mapped_column(Text)
    brand: Mapped[str | None] = mapped_column(Text)
    cloud_device_type: Mapped[str | None] = mapped_column(Text)
    link_type: Mapped[str | None] = mapped_column(Text)
    ip_address: Mapped[str | None] = mapped_column(INET)
    ssid_2_4ghz: Mapped[str | None] = mapped_column(Text)
    ssid_5ghz: Mapped[str | None] = mapped_column(Text)
    channel_2_4ghz: Mapped[int | None] = mapped_column(Integer)
    channel_5ghz: Mapped[int | None] = mapped_column(Integer)
    antenna_2_4ghz: Mapped[str | None] = mapped_column(Text)
    antenna_5ghz: Mapped[str | None] = mapped_column(Text)
    protocol_2_4ghz: Mapped[str | None] = mapped_column(Text)
    protocol_5ghz: Mapped[str | None] = mapped_column(Text)
    rssi: Mapped[int | None] = mapped_column(Integer)
    rx_rate: Mapped[int | None] = mapped_column(Integer)
    tx_rate: Mapped[int | None] = mapped_column(Integer)
    last_seen: Mapped[datetime | None] = mapped_column(DateTime)
    parent_mac: Mapped[str | None] = mapped_column(Text)
    platform: Mapped[str | None] = mapped_column(Text)
    bandwidth_2_4ghz: Mapped[str | None] = mapped_column(Text)
    bandwidth_5ghz: Mapped[str | None] = mapped_column(Text)


class Router(Base):
    __tablename__ = "routers"
    serial_number: Mapped[str] = mapped_column(Text, primary_key=True)
    login_id: Mapped[str] = mapped_column(Text, nullable=False)
    manufacturer: Mapped[str | None] = mapped_column(Text)
    model: Mapped[str | None] = mapped_column(Text)
    cpu_usage_pct: Mapped[int | None] = mapped_column(Integer)
    cpu_temperature_c: Mapped[int | None] = mapped_column(Integer)
    memory_usage_pct: Mapped[int | None] = mapped_column(Integer)
    monthly_usage_gb: Mapped[float | None] = mapped_column(Numeric(9, 1))
    rx_power_dbm: Mapped[float | None] = mapped_column(Numeric(5, 1))


class CustomerSummary(Base):
    __tablename__ = "customer_summaries"
    login_id: Mapped[str] = mapped_column(Text, primary_key=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    recommendation: Mapped[str | None] = mapped_column(Text)
    model: Mapped[str | None] = mapped_column(Text)
    generated_at: Mapped[datetime | None] = mapped_column(DateTime, server_default=func.now())


class TopologyEdge(Base):
    __tablename__ = "topology_edges"
    __table_args__ = (UniqueConstraint("source_device_id", "target_device_id", name="uq_topology_edge_path"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    source_device_id: Mapped[str] = mapped_column(ForeignKey("network_devices.id"), nullable=False)
    target_device_id: Mapped[str] = mapped_column(ForeignKey("network_devices.id"), nullable=False)
    service_id: Mapped[str | None] = mapped_column(ForeignKey("services.id"))


class NetworkEvent(Base):
    __tablename__ = "network_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    source_event_id: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    event_type: Mapped[str] = mapped_column(String(80), nullable=False)
    device_id: Mapped[str] = mapped_column(ForeignKey("network_devices.id"), nullable=False)
    service_id: Mapped[str | None] = mapped_column(ForeignKey("services.id"))
    payload: Mapped[dict] = mapped_column(JSON, default=dict, server_default=text("'{}'"), nullable=False)
    received_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    source_event_id: Mapped[str] = mapped_column(ForeignKey("network_events.id"), unique=True, nullable=False)
    customer_id: Mapped[str] = mapped_column(ForeignKey("customers.id"), nullable=False)
    service_id: Mapped[str | None] = mapped_column(ForeignKey("services.id"))
    assigned_technician_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    severity: Mapped[str] = mapped_column(String(30), nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="open", server_default=text("'open'"), nullable=False)
    summary: Mapped[str] = mapped_column(String(255), nullable=False)
    # TMFORCE field-operations metadata. Nullable so non-TMFORCE tickets remain valid.
    tm_ticket_no: Mapped[str | None] = mapped_column(String(60), unique=True)
    ctt_activity_id: Mapped[str | None] = mapped_column(String(60))
    login_id: Mapped[str | None] = mapped_column(String(60))
    ticket_category: Mapped[str | None] = mapped_column(String(60))
    ticket_created_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    staff_code: Mapped[str | None] = mapped_column(String(20))


class EntityFactSheet(Base):
    """Retrievable per-entity fact group, mirroring the knowledge chunk index.

    One row per ``(entity_type, entity_id, group_key)``. ``content`` is the
    rendered, secret-free field block that is embedded for retrieval; sensitive
    fields live only in ``EntityFact`` and never enter ``content``.
    """

    __tablename__ = "entity_fact_sheets"
    __table_args__ = (UniqueConstraint("entity_type", "entity_id", "group_key", name="uq_fact_sheet_entity_group"),)
    id: Mapped[str] = mapped_column(String(160), primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(20), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    group_key: Mapped[str] = mapped_column(String(40), nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(Settings().embedding_dimensions))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class EntityFact(Base):
    """Typed field value for an entity, used for exact display and lookup."""

    __tablename__ = "entity_facts"
    __table_args__ = (UniqueConstraint("entity_type", "entity_id", "field_key", name="uq_fact_entity_field"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    entity_type: Mapped[str] = mapped_column(String(20), nullable=False)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False)
    group_key: Mapped[str] = mapped_column(String(40), nullable=False)
    field_key: Mapped[str] = mapped_column(String(60), nullable=False)
    label: Mapped[str] = mapped_column(String(120), nullable=False)
    value_text: Mapped[str | None] = mapped_column(Text)
    value_number: Mapped[float | None] = mapped_column(Float)
    is_sensitive: Mapped[bool] = mapped_column(Boolean, default=False, server_default=text("false"), nullable=False)
    source_updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"
    __table_args__ = (UniqueConstraint("document_key", "version", name="uq_document_version"),)
    id: Mapped[str] = mapped_column(String(120), primary_key=True)
    document_key: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[str] = mapped_column(String(40), nullable=False)
    version: Mapped[str] = mapped_column(String(40), nullable=False)


class KnowledgeChunk(Base):
    __tablename__ = "knowledge_chunks"
    __table_args__ = (UniqueConstraint("document_id", "section", name="uq_chunk_document_section"),)
    id: Mapped[str] = mapped_column(String(160), primary_key=True)
    document_id: Mapped[str] = mapped_column(ForeignKey("knowledge_documents.id"), nullable=False)
    section: Mapped[str] = mapped_column(String(160), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(Settings().embedding_dimensions))


class AssistantSession(Base):
    __tablename__ = "assistant_sessions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    ticket_id: Mapped[str] = mapped_column(ForeignKey("tickets.id"), nullable=False)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AssistantMessage(Base):
    __tablename__ = "assistant_messages"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    session_id: Mapped[str] = mapped_column(ForeignKey("assistant_sessions.id"), nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    citations: Mapped[list] = mapped_column(JSON, default=list, server_default=text("'[]'"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ToolExecution(Base):
    __tablename__ = "tool_executions"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    ticket_id: Mapped[str] = mapped_column(ForeignKey("tickets.id"), nullable=False)
    actor_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)
    parameters: Mapped[dict] = mapped_column(JSON, default=dict, server_default=text("'{}'"), nullable=False)
    outcome: Mapped[str] = mapped_column(String(40), nullable=False)
    message: Mapped[str | None] = mapped_column(String(400))
    correlation_id: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AuditEvent(Base):
    __tablename__ = "audit_events"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    actor_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"))
    ticket_id: Mapped[str | None] = mapped_column(ForeignKey("tickets.id"))
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    details: Mapped[dict] = mapped_column(JSON, default=dict, server_default=text("'{}'"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
