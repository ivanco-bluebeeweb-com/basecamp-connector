"""Resource operation handlers for Basecamp Connector."""
from __future__ import annotations
from imperal_sdk import ActionResult
from app import chat
from handlers_connection import resolve_client
from schemas import (
    ListProjectsParams, GetProjectParams, CreateProjectParams,
    ListTodosParams, CreateTodoParams, CompleteTodoParams, UncompleteTodoParams,
    ListMessagesParams, PostMessageParams, ListWebhooksParams, CreateWebhookParams,
    AuditHealthParams, ProjectList, ProjectRecord, TodoList, TodoRecord,
    MessageList, MessageRecord, WebhookList, WebhookRecord, HealthAuditResult
)

@chat.function(
    "list_projects",
    "List Basecamp projects.",
    action_type="read",
    chain_callable=True,
    data_model=ProjectList
)
async def list_projects(ctx, params: ListProjectsParams) -> ActionResult:
    """List Basecamp projects."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_projects(status=params.status, page=params.page)
        return ActionResult.success(
            ProjectList(projects=items, count=len(items)),
            summary=f"Retrieved {len(items)} projects."
        )
    except Exception as e:
        return ActionResult.error(f"Error listing projects: {e}")

@chat.function(
    "get_project",
    "Read details of a Basecamp project.",
    action_type="read",
    chain_callable=True,
    data_model=ProjectRecord
)
async def get_project(ctx, params: GetProjectParams) -> ActionResult:
    """Read a Basecamp project by ID."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.get_project(params.project_id)
        return ActionResult.success(
            ProjectRecord(id=item.get("id", params.project_id), name=item.get("name", ""), description=item.get("description", ""), status=item.get("status", "active")),
            summary=f"Retrieved project: {item.get('name')}"
        )
    except Exception as e:
        return ActionResult.error(f"Error reading project: {e}")

@chat.function(
    "create_project",
    "Create a new Basecamp project.",
    action_type="write",
    chain_callable=True,
    event="basecamp-connector.create_project",
    effects=["create:project"],
    data_model=ProjectRecord
)
async def create_project(ctx, params: CreateProjectParams) -> ActionResult:
    """Create a new Basecamp project."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.create_project(name=params.name, description=params.description)
        return ActionResult.success(
            ProjectRecord(id=item.get("id", 0), name=item.get("name", params.name), description=item.get("description", params.description or ""), status="active"),
            summary=f"Created project: {params.name}"
        )
    except Exception as e:
        return ActionResult.error(f"Error creating project: {e}")

@chat.function(
    "list_todos",
    "List to-dos in a Basecamp project.",
    action_type="read",
    chain_callable=True,
    data_model=TodoList
)
async def list_todos(ctx, params: ListTodosParams) -> ActionResult:
    """List to-dos in a Basecamp project."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_todos(project_id=params.project_id, todolist_id=params.todolist_id)
        return ActionResult.success(
            TodoList(todos=items, count=len(items)),
            summary=f"Retrieved {len(items)} to-dos."
        )
    except Exception as e:
        return ActionResult.error(f"Error listing to-dos: {e}")

@chat.function(
    "create_todo",
    "Create a new to-do item in Basecamp.",
    action_type="write",
    chain_callable=True,
    event="basecamp-connector.create_todo",
    effects=["create:todo"],
    data_model=TodoRecord
)
async def create_todo(ctx, params: CreateTodoParams) -> ActionResult:
    """Create a new to-do item in Basecamp."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.create_todo(project_id=params.project_id, todolist_id=params.todolist_id, content=params.content, due_on=params.due_on)
        return ActionResult.success(
            TodoRecord(id=item.get("id", 0), content=item.get("content", params.content), completed=item.get("completed", False), due_on=item.get("due_on", params.due_on)),
            summary=f"Created to-do: {params.content}"
        )
    except Exception as e:
        return ActionResult.error(f"Error creating to-do: {e}")

@chat.function(
    "complete_todo",
    "Mark a Basecamp to-do as completed.",
    action_type="write",
    chain_callable=True,
    event="basecamp-connector.complete_todo",
    effects=["update:todo"],
    data_model=TodoRecord
)
async def complete_todo(ctx, params: CompleteTodoParams) -> ActionResult:
    """Mark a Basecamp to-do as completed."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.complete_todo(project_id=params.project_id, todo_id=params.todo_id)
        return ActionResult.success(
            TodoRecord(id=params.todo_id, content=item.get("content", ""), completed=True),
            summary=f"Completed to-do {params.todo_id}"
        )
    except Exception as e:
        return ActionResult.error(f"Error completing to-do: {e}")

@chat.function(
    "uncomplete_todo",
    "Reopen a completed Basecamp to-do.",
    action_type="write",
    chain_callable=True,
    event="basecamp-connector.uncomplete_todo",
    effects=["update:todo"],
    data_model=TodoRecord
)
async def uncomplete_todo(ctx, params: UncompleteTodoParams) -> ActionResult:
    """Reopen a completed Basecamp to-do."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.uncomplete_todo(project_id=params.project_id, todo_id=params.todo_id)
        return ActionResult.success(
            TodoRecord(id=params.todo_id, content=item.get("content", ""), completed=False),
            summary=f"Reopened to-do {params.todo_id}"
        )
    except Exception as e:
        return ActionResult.error(f"Error reopening to-do: {e}")

@chat.function(
    "list_messages",
    "List messages posted to a Basecamp project board.",
    action_type="read",
    chain_callable=True,
    data_model=MessageList
)
async def list_messages(ctx, params: ListMessagesParams) -> ActionResult:
    """List messages posted to a Basecamp project board."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_messages(project_id=params.project_id)
        return ActionResult.success(
            MessageList(messages=items, count=len(items)),
            summary=f"Retrieved {len(items)} messages."
        )
    except Exception as e:
        return ActionResult.error(f"Error listing messages: {e}")

@chat.function(
    "post_message",
    "Post a new message to a Basecamp project board.",
    action_type="write",
    chain_callable=True,
    event="basecamp-connector.post_message",
    effects=["create:message"],
    data_model=MessageRecord
)
async def post_message(ctx, params: PostMessageParams) -> ActionResult:
    """Post a new message to a Basecamp project board."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.post_message(project_id=params.project_id, subject=params.subject, content=params.content)
        return ActionResult.success(
            MessageRecord(id=item.get("id", 0), subject=item.get("subject", params.subject), content=item.get("content", params.content)),
            summary=f"Posted message: {params.subject}"
        )
    except Exception as e:
        return ActionResult.error(f"Error posting message: {e}")

@chat.function(
    "list_webhooks",
    "List registered webhooks in Basecamp.",
    action_type="read",
    chain_callable=True,
    data_model=WebhookList
)
async def list_webhooks(ctx, params: ListWebhooksParams) -> ActionResult:
    """List registered webhooks in Basecamp."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_webhooks(project_id=params.project_id)
        return ActionResult.success(
            WebhookList(webhooks=items, count=len(items)),
            summary=f"Retrieved {len(items)} webhooks."
        )
    except Exception as e:
        return ActionResult.error(f"Error listing webhooks: {e}")

@chat.function(
    "create_webhook",
    "Register a new webhook endpoint in Basecamp.",
    action_type="write",
    chain_callable=True,
    event="basecamp-connector.create_webhook",
    effects=["create:webhook"],
    data_model=WebhookRecord
)
async def create_webhook(ctx, params: CreateWebhookParams) -> ActionResult:
    """Register a new webhook endpoint in Basecamp."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.create_webhook(project_id=params.project_id, payload_url=params.payload_url, types=params.types)
        return ActionResult.success(
            WebhookRecord(id=item.get("id", 0), payload_url=item.get("payload_url", params.payload_url)),
            summary=f"Created webhook for {params.payload_url}"
        )
    except Exception as e:
        return ActionResult.error(f"Error creating webhook: {e}")

@chat.function(
    "audit_basecamp_health",
    "Audit account connectivity, project count, and active to-dos.",
    action_type="read",
    chain_callable=True,
    data_model=HealthAuditResult
)
async def audit_basecamp_health(ctx, params: AuditHealthParams) -> ActionResult:
    """Audit account connectivity and project count."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        projects = await client.list_projects()
        return ActionResult.success(
            HealthAuditResult(
                status="healthy",
                projects_count=len(projects),
                detail=f"Account is operational with {len(projects)} accessible project(s)."
            ),
            summary=f"Basecamp health audit: healthy ({len(projects)} projects)."
        )
    except Exception as e:
        return ActionResult.error(f"Health audit failed: {e}")
