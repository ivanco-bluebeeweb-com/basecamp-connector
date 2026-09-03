"""Pydantic schemas for Basecamp Connector."""
from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field

class ConnectParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Production.")
    api_key: str = Field(description="Basecamp API Key or Bearer Token.")
    base_url: str = Field(default="", description="Optional custom base URL or instance domain.")

class ConnectionIdParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier (empty uses active connection).")

class ResourceIdParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    resource_id: str = Field(description="Unique ID of the Basecamp resource.")

class ListResourcesParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    limit: int = Field(default=50, description="Maximum number of items to return (1-100).")
    cursor: str = Field(default="", description="Cursor for pagination.")

class ConnectionRecord(BaseModel):
    id: str
    label: str
    masked_key: str
    base_url: str
    is_active: bool

class ConnectionList(BaseModel):
    connections: list[ConnectionRecord]
    total: int

class AccountOverview(BaseModel):
    status: str
    base_url: str
    details: dict[str, Any]

class HealthReport(BaseModel):
    status: str
    connected: bool
    latency_ms: float
    message: str

class ResourceRecord(BaseModel):
    id: str
    name: str
    status: str

class ResourceList(BaseModel):
    items: list[ResourceRecord]
    total: int
    next_cursor: Optional[str] = None
