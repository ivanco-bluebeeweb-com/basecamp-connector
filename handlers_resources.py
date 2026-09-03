"""Resource operation handlers for Basecamp Connector."""
from __future__ import annotations
from imperal_sdk import ActionResult
from app import chat
from handlers_connection import resolve_client
from schemas import (
    ListProjectsParams, GetProjectParams, CreateProjectParams,
    ListTodosParams, CreateTodoParams, CompleteTodoParams, UncompleteTodoParams,
    ListMessagesParams, PostMessageParams, ListWebhooksParams, CreateWebhookParams,
    AuditHealthParams
)

@chat.function("list_projects", action_type="read", description="List Basecamp projects.")
async def list_projects(params: ListProjectsParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_projects(status=params.status, page=params.page)
        return ActionResult.ok({"projects": items, "count": len(items)}, summary=f"Retrieved {len(items)} projects.")
    except Exception as e:
        return ActionResult.error(f"Error listing projects: {e}")

@chat.function("get_project", action_type="read", description="Read details of a Basecamp project.")
async def get_project(params: GetProjectParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.get_project(params.project_id)
        return ActionResult.ok(item, summary=f"Retrieved project: {item.get('name')}")
    except Exception as e:
        return ActionResult.error(f"Error reading project: {e}")

@chat.function("create_project", action_type="write", description="Create a new Basecamp project.")
async def create_project(params: CreateProjectParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.create_project(name=params.name, description=params.description)
        return ActionResult.ok(item, summary=f"Created project: {params.name}")
    except Exception as e:
        return ActionResult.error(f"Error creating project: {e}")

@chat.function("list_todos", action_type="read", description="List to-dos in a to-do list.")
async def list_todos(params: ListTodosParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_todos(project_id=params.project_id, todolist_id=params.todolist_id, status=params.status)
        return ActionResult.ok({"todos": items, "count": len(items)}, summary=f"Retrieved {len(items)} to-dos.")
    except Exception as e:
        return ActionResult.error(f"Error listing to-dos: {e}")

@chat.function("create_todo", action_type="write", description="Create a new to-do in a project to-do list.")
async def create_todo(params: CreateTodoParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.create_todo(
            project_id=params.project_id,
            todolist_id=params.todolist_id,
            content=params.content,
            description=params.description,
            due_on=params.due_on,
            assignee_ids=params.assignee_ids
        )
        return ActionResult.ok(item, summary=f"Created to-do: {params.content}")
    except Exception as e:
        return ActionResult.error(f"Error creating to-do: {e}")

@chat.function("complete_todo", action_type="write", description="Mark a to-do as completed.")
async def complete_todo(params: CompleteTodoParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        res = await client.complete_todo(project_id=params.project_id, todo_id=params.todo_id)
        return ActionResult.ok(res, summary=f"Marked to-do {params.todo_id} complete.")
    except Exception as e:
        return ActionResult.error(f"Error completing to-do: {e}")

@chat.function("uncomplete_todo", action_type="write", description="Reopen a completed to-do.")
async def uncomplete_todo(params: UncompleteTodoParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        res = await client.uncomplete_todo(project_id=params.project_id, todo_id=params.todo_id)
        return ActionResult.ok(res, summary=f"Reopened to-do {params.todo_id}.")
    except Exception as e:
        return ActionResult.error(f"Error reopening to-do: {e}")

@chat.function("list_messages", action_type="read", description="List messages on a project message board.")
async def list_messages(params: ListMessagesParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_messages(project_id=params.project_id, message_board_id=params.message_board_id, page=params.page)
        return ActionResult.ok({"messages": items, "count": len(items)}, summary=f"Retrieved {len(items)} messages.")
    except Exception as e:
        return ActionResult.error(f"Error listing messages: {e}")

@chat.function("post_message", action_type="write", description="Post a message to a message board.")
async def post_message(params: PostMessageParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.post_message(project_id=params.project_id, message_board_id=params.message_board_id, subject=params.subject, content=params.content)
        return ActionResult.ok(item, summary=f"Posted message: {params.subject}")
    except Exception as e:
        return ActionResult.error(f"Error posting message: {e}")

@chat.function("list_webhooks", action_type="read", description="List webhooks registered on a project.")
async def list_webhooks(params: ListWebhooksParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_webhooks(project_id=params.project_id)
        return ActionResult.ok({"webhooks": items, "count": len(items)}, summary=f"Retrieved {len(items)} webhooks.")
    except Exception as e:
        return ActionResult.error(f"Error listing webhooks: {e}")

@chat.function("create_webhook", action_type="write", description="Create a webhook subscription for project events.")
async def create_webhook(params: CreateWebhookParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.create_webhook(project_id=params.project_id, payload_url=params.payload_url, types=params.types)
        return ActionResult.ok(item, summary=f"Registered webhook pointing to {params.payload_url}")
    except Exception as e:
        return ActionResult.error(f"Error creating webhook: {e}")

@chat.function("audit_basecamp_health", action_type="read", description="Scan Basecamp account health, active projects, and overdue to-dos.")
async def audit_basecamp_health(params: AuditHealthParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        projects = await client.list_projects(status="active")
        return ActionResult.ok({
            "status": "healthy",
            "active_projects": len(projects),
            "projects_sample": [{"id": p.get("id"), "name": p.get("name")} for p in projects[:5]]
        }, summary=f"Basecamp account healthy with {len(projects)} active projects.")
    except Exception as e:
        return ActionResult.error(f"Health audit failed: {e}")
