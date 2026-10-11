from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DemoEventRead(ORMModel):
    id: str
    source_event_id: str
    event_type: str
    processed_at: datetime | None


class PendingEventRead(ORMModel):
    id: str
    source_event_id: str
    event_type: str
    device_id: str
    device_ref: str
    device_name: str
    device_status: str
    service_id: str | None = None
    service_ref: str | None = None
    payload: dict
    received_at: datetime


class ProcessedTicketRead(ORMModel):
    id: str
    source_event_id: str
    customer_id: str
    service_id: str | None = None
    assigned_technician_id: str
    severity: str
    status: str
    summary: str


class ProcessEventResponse(ORMModel):
    ticket: ProcessedTicketRead
    created: bool
    duplicate: bool
    source_event_id: str
    assigned_technician_name: str
