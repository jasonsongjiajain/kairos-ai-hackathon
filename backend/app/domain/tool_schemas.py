from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class ToolCatalogItemRead(BaseModel):
    name: str
    description: str
    kind: str
    requires_confirmation: bool


class ToolProposeRequest(BaseModel):
    tool_name: str = Field(min_length=1, max_length=60)
    model_proposal: dict | None = None
    device_id: str = Field(min_length=1, max_length=64)
    parameters: dict = Field(default_factory=dict)


class AgentToolProposeRequest(BaseModel):
    question: str = Field(min_length=1, max_length=1000)
    device_id: str = Field(min_length=1, max_length=64)



class ToolProposalRead(BaseModel):
    id: str
    ticket_id: str
    tool_name: str
    device_id: str
    device_ref: str
    kind: str
    requires_confirmation: bool
    parameters: dict
    status: str
    summary: str
    confirmation_id: str
    created_at: datetime


class ToolConfirmRequest(BaseModel):
    confirmation_id: str = Field(min_length=1, max_length=120)


class ToolExecutionRead(BaseModel):
    id: str
    ticket_id: str
    tool_name: str
    device_id: str
    device_ref: str
    status: str
    message: str
    correlation_id: str
    executed_at: datetime


class AuditEventRead(BaseModel):
    id: str
    event_type: str
    actor_id: str | None
    actor_name: str | None
    ticket_id: str | None
    details: dict
    created_at: datetime
