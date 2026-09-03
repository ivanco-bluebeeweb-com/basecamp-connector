"""Pydantic schemas for Basecamp Connector (Basecamp 3 API)."""
from __future__ import annotations
from typing import Any, Optional
from pydantic import BaseModel, Field

class ConnectBasecampParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Production Basecamp.")
    account_id: str = Field(description="Basecamp numeric account ID (found in URL: 3.basecampapi.com/{account_id}).")
    access_token: str = Field(description="OAuth 2.0 Bearer access token.")

class ConnectionIdParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier (empty uses active connection).")

class ListProjectsParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    status: str = Field(default="active", description="Filter by status: active, archived, or trashed.")
    page: int = Field(default=1, description="Page number for pagination.")

class GetProjectParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    project_id: int = Field(description="Project ID.")

class CreateProjectParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    name: str = Field(description="Project name.")
    description: str = Field(default="", description="Project description.")

class ListTodosParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    project_id: int = Field(description="Project ID.")
    todolist_id: int = Field(description="To-do list ID.")
    status: str = Field(default="active", description="Filter by status: active, completed, or trashed.")

class CreateTodoParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    project_id: int = Field(description="Project ID.")
    todolist_id: int = Field(description="To-do list ID where task is created.")
    content: str = Field(description="To-do title/content.")
    description: str = Field(default="", description="Additional details/notes (HTML supported).")
    due_on: str = Field(default="", description="Due date in YYYY-MM-DD format.")
    assignee_ids: list[int] = Field(default_factory=list, description="List of user IDs assigned to this to-do.")

class CompleteTodoParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    project_id: int = Field(description="Project ID.")
    todo_id: int = Field(description="To-do ID to complete.")

class UncompleteTodoParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    project_id: int = Field(description="Project ID.")
    todo_id: int = Field(description="To-do ID to uncomplete.")

class ListMessagesParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    project_id: int = Field(description="Project ID.")
    message_board_id: int = Field(description="Message board ID.")
    page: int = Field(default=1, description="Page number.")

class PostMessageParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    project_id: int = Field(description="Project ID.")
    message_board_id: int = Field(description="Message board ID.")
    subject: str = Field(description="Message subject.")
    content: str = Field(description="Message body content (HTML supported).")

class ListWebhooksParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    project_id: int = Field(description="Project ID.")

class CreateWebhookParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")
    project_id: int = Field(description="Project ID.")
    payload_url: str = Field(description="Target HTTPS callback URL.")
    types: list[str] = Field(default_factory=list, description="Event types to subscribe to (e.g. ['Todo', 'Comment']).")

class AuditHealthParams(BaseModel):
    connection_id: str = Field(default="", description="Connection identifier.")

class ConnectionRecord(BaseModel):
    id: str
    label: str
    account_id: str
    masked_token: str
    is_active: bool

class ConnectionList(BaseModel):
    connections: list[ConnectionRecord]
    total: int
