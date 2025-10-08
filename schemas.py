from pydantic import BaseModel, Field
from typing import Optional, Dict


class LogEntry(BaseModel):
    timestamp: Optional[str]
    level: str
    source: Optional[str]
    message: str
    meta: Optional[Dict] = Field(default_factory=dict)


class IngestResponse(BaseModel):
    id: str
    indexed: bool


