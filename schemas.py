"""Pydantic schemas for Basecamp Connector."""
from __future__ import annotations
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class NoParams(BaseModel):
    """Empty parameter model."""
    pass

class ConnectBasecampParams(BaseModel):
    label: str = Field(default="", description="Connection label")
    account_id: str = Field(..., description="Basecamp Account ID")
    access_token: str = Field(..., description="Basecamp OAuth Bearer token")

class DisconnectBasecampParams(BaseModel):
    connection_id: str = Field(..., description="Connection ID to remove")

class ListProjectsParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID")
    status: Optional[str] = Field(default="active", description="Filter by status: active, archived, trashed")
    page: int = Field(default=1, description="Page number")

class GetProjectParams(BaseModel):
    project_id: int = Field(..., description="Basecamp Project ID")
    connection_id: str = Field(default="", description="Optional connection ID")

class CreateProjectParams(BaseModel):
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(default="", description="Project description")
    connection_id: str = Field(default="", description="Optional connection ID")

class ListTodosParams(BaseModel):
    project_id: int = Field(..., description="Basecamp Project ID")
    todolist_id: Optional[int] = Field(default=None, description="Optional To-do List ID")
    connection_id: str = Field(default="", description="Optional connection ID")

class CreateTodoParams(BaseModel):
    project_id: int = Field(..., description="Basecamp Project ID")
    todolist_id: int = Field(..., description="To-do List ID")
    content: str = Field(..., description="To-do item content")
    due_on: Optional[str] = Field(default=None, description="Due date (YYYY-MM-DD)")
    connection_id: str = Field(default="", description="Optional connection ID")

class CompleteTodoParams(BaseModel):
    project_id: int = Field(..., description="Basecamp Project ID")
    todo_id: int = Field(..., description="To-do ID")
    connection_id: str = Field(default="", description="Optional connection ID")

class UncompleteTodoParams(BaseModel):
    project_id: int = Field(..., description="Basecamp Project ID")
    todo_id: int = Field(..., description="To-do ID")
    connection_id: str = Field(default="", description="Optional connection ID")

class ListMessagesParams(BaseModel):
    project_id: int = Field(..., description="Basecamp Project ID")
    connection_id: str = Field(default="", description="Optional connection ID")

class PostMessageParams(BaseModel):
    project_id: int = Field(..., description="Basecamp Project ID")
    subject: str = Field(..., description="Message subject")
    content: str = Field(..., description="Message body HTML or text")
    connection_id: str = Field(default="", description="Optional connection ID")

class ListWebhooksParams(BaseModel):
    project_id: int = Field(..., description="Basecamp Project ID")
    connection_id: str = Field(default="", description="Optional connection ID")

class CreateWebhookParams(BaseModel):
    project_id: int = Field(..., description="Basecamp Project ID")
    payload_url: str = Field(..., description="Target webhook URL")
    types: Optional[List[str]] = Field(default=None, description="Event types to subscribe to")
    connection_id: str = Field(default="", description="Optional connection ID")

class AuditHealthParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID")

# Return Models for typed ActionResult
class BasecampConnection(BaseModel):
    id: str
    label: str
    account_id: str

class ConnectionList(BaseModel):
    connections: List[BasecampConnection] = Field(default_factory=list)

class ConnectResult(BaseModel):
    id: str
    label: str
    account_id: str

class DisconnectResult(BaseModel):
    removed_connection_id: str

class ProjectRecord(BaseModel):
    id: int
    name: str
    description: Optional[str] = ""
    status: Optional[str] = "active"

class ProjectList(BaseModel):
    projects: List[Dict[str, Any]] = Field(default_factory=list)
    count: int

class TodoRecord(BaseModel):
    id: int
    content: str
    completed: bool = False
    due_on: Optional[str] = None

class TodoList(BaseModel):
    todos: List[Dict[str, Any]] = Field(default_factory=list)
    count: int

class MessageRecord(BaseModel):
    id: int
    subject: str
    content: Optional[str] = ""

class MessageList(BaseModel):
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    count: int

class WebhookRecord(BaseModel):
    id: int
    payload_url: str

class WebhookList(BaseModel):
    webhooks: List[Dict[str, Any]] = Field(default_factory=list)
    count: int

class HealthAuditResult(BaseModel):
    status: str
    projects_count: int
    detail: str
