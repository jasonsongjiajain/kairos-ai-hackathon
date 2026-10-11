from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

CREDENTIAL_KEYS = (
    "onu_password",
    "ppp_password",
    "wifi_password",
    "password",
    "passphrase",
    "credential",
    "secret",
)
REDACTED_PLACEHOLDER = "[redacted]"


def redact_details(details: dict | None) -> dict:
    """Return a copy of a detail mapping with credential-shaped values masked."""
    if not details:
        return {}
    return {
        key: REDACTED_PLACEHOLDER if key.lower() in CREDENTIAL_KEYS else value
        for key, value in details.items()
    }


def find_credential(details: dict | None) -> tuple[str, str] | None:
    """Return the first credential-shaped key/value pair, or None when absent."""
    if not details:
        return None
    for key in CREDENTIAL_KEYS:
        value = details.get(key)
        if isinstance(value, str) and value:
            return key, value
    return None


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


class TicketRead(ORMModel):
    id: str
    source_event_id: str
    customer_id: str
    service_id: str | None = None
    assigned_technician_id: str
    severity: str
    status: str
    summary: str


class AssignedTicketRead(TicketRead):
    customer_ref: str
    customer_name: str
    service_type: str | None = None
    service_ref: str | None = None


class CustomerRead(ORMModel):
    id: str
    customer_ref: str
    name: str
    address: str
    is_demo: bool


class ServiceRead(ORMModel):
    id: str
    service_type: str
    service_ref: str
    status: str
    details: dict

    @field_validator("details")
    @classmethod
    def _redact_credentials(cls, value: dict) -> dict:
        return redact_details(value)


class DeviceRead(ORMModel):
    id: str
    device_ref: str
    device_type: str
    name: str
    status: str
    credential_available: bool = False


class TicketDetailRead(ORMModel):
    ticket: TicketRead
    assigned_technician_name: str
    customer: CustomerRead
    services: list[ServiceRead]
    devices: list[DeviceRead]


class CustomerDetailRead(ORMModel):
    customer: CustomerRead
    services: list[ServiceRead]
    devices: list[DeviceRead]


class TopologyNodeRead(ORMModel):
    device_id: str
    device_ref: str
    device_type: str
    name: str
    status: str
    service_id: str | None = None
    service_ref: str | None = None


class TopologyEdgeRead(ORMModel):
    source_device_id: str
    target_device_id: str
    service_id: str | None = None
    service_ref: str | None = None


class TopologyPathRead(ORMModel):
    ticket_id: str
    service_id: str | None = None
    service_ref: str | None = None
    nodes: list[TopologyNodeRead]
    edges: list[TopologyEdgeRead]


class CredentialRevealRead(ORMModel):
    device_id: str
    device_ref: str
    credential_type: str
    credential: str
