"""Resource operation handlers for Basecamp Connector."""
from __future__ import annotations
from imperal_sdk import ActionResult
from handlers_connection import resolve_client
from schemas import (
    ListProjectsParams, GetProjectParams, CreateProjectParams,
    ListTodosParams, CreateTodoParams, CompleteTodoParams, UncompleteTodoParams,
    ListMessagesParams, PostMessageParams, ListWebhooksParams, CreateWebhookParams,
    AuditHealthParams
)

async def list_projects(params: ListProjectsParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_projects(status=params.status, page=params.page)
        return ActionResult.ok({"projects": items, "count": len(items)}, summary=f"Retrieved {len(items)} projects.")
    except Exception as e:
        return ActionResult.error(f"Error listing projects: {e}")

async def get_project(params: GetProjectParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.get_project(params.project_id)
        return ActionResult.ok(item, summary=f"Retrieved project: {item.get('name')}")
    except Exception as e:
        return ActionResult.error(f"Error reading project: {e}")

async def create_project(params: CreateProjectParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.create_project(name=params.name, description=params.description)
        return ActionResult.ok(item, summary=f"Created project: {params.name}")
    except Exception as e:
        return ActionResult.error(f"Error creating project: {e}")

async def list_todos(params: ListTodosParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_todos(project_id=params.project_id, todolist_id=params.todolist_id, status=params.status)
        return ActionResult.ok({"todos": items, "count": len(items)}, summary=f"Retrieved {len(items)} to-dos.")
    except Exception as e:
        return ActionResult.error(f"Error listing to-dos: {e}")

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

async def complete_todo(params: CompleteTodoParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        res = await client.complete_todo(project_id=params.project_id, todo_id=params.todo_id)
        return ActionResult.ok(res, summary=f"Marked to-do {params.todo_id} complete.")
    except Exception as e:
        return ActionResult.error(f"Error completing to-do: {e}")

async def uncomplete_todo(params: UncompleteTodoParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        res = await client.uncomplete_todo(project_id=params.project_id, todo_id=params.todo_id)
        return ActionResult.ok(res, summary=f"Reopened to-do {params.todo_id}.")
    except Exception as e:
        return ActionResult.error(f"Error reopening to-do: {e}")

async def list_messages(params: ListMessagesParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_messages(project_id=params.project_id, message_board_id=params.message_board_id, page=params.page)
        return ActionResult.ok({"messages": items, "count": len(items)}, summary=f"Retrieved {len(items)} messages.")
    except Exception as e:
        return ActionResult.error(f"Error listing messages: {e}")

async def post_message(params: PostMessageParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.post_message(project_id=params.project_id, message_board_id=params.message_board_id, subject=params.subject, content=params.content)
        return ActionResult.ok(item, summary=f"Posted message: {params.subject}")
    except Exception as e:
        return ActionResult.error(f"Error posting message: {e}")

async def list_webhooks(params: ListWebhooksParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_webhooks(project_id=params.project_id)
        return ActionResult.ok({"webhooks": items, "count": len(items)}, summary=f"Retrieved {len(items)} webhooks.")
    except Exception as e:
        return ActionResult.error(f"Error listing webhooks: {e}")

async def create_webhook(params: CreateWebhookParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.create_webhook(project_id=params.project_id, payload_url=params.payload_url, types=params.types)
        return ActionResult.ok(item, summary=f"Registered webhook pointing to {params.payload_url}")
    except Exception as e:
        return ActionResult.error(f"Error creating webhook: {e}")

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
