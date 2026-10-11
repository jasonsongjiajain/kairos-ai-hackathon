from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class DemoEventRead(ORMModel):
    id: str
    source_event_id: str
    event_type: str
    processed_at: datetime | None
