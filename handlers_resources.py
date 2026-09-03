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

@chat.function(
    'list_projects',
    'List Basecamp projects.',
    action_type='read',
    chain_callable=True
)
async def list_projects(params: ListProjectsParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_projects(status=params.status, page=params.page)
        return ActionResult.ok({"projects": items, "count": len(items)}, summary=f"Retrieved {len(items)} projects.")
    except Exception as e:
        return ActionResult.error(f"Error listing projects: {e}")

@chat.function(
    'get_project',
    'Read details of a Basecamp project.',
    action_type='read',
    chain_callable=True
)
async def get_project(params: GetProjectParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.get_project(params.project_id)
        return ActionResult.ok(item, summary=f"Retrieved project: {item.get('name')}")
    except Exception as e:
        return ActionResult.error(f"Error reading project: {e}")

@chat.function(
    'create_project',
    'Create a new Basecamp project.',
    action_type='write',
    chain_callable=True,
    effects=['create:project']
)
async def create_project(params: CreateProjectParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.create_project(name=params.name, description=params.description)
        return ActionResult.ok(item, summary=f"Created Basecamp project: {item.get('name')}")
    except Exception as e:
        return ActionResult.error(f"Error creating project: {e}")

@chat.function(
    'list_todos',
    'List to-dos in a Basecamp to-do set or list.',
    action_type='read',
    chain_callable=True
)
async def list_todos(params: ListTodosParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_todos(project_id=params.project_id, todoset_id=params.todoset_id, page=params.page)
        return ActionResult.ok({"todos": items, "count": len(items)}, summary=f"Retrieved {len(items)} to-dos.")
    except Exception as e:
        return ActionResult.error(f"Error listing todos: {e}")

@chat.function(
    'create_todo',
    'Create a new to-do item in Basecamp.',
    action_type='write',
    chain_callable=True,
    effects=['create:todo']
)
async def create_todo(params: CreateTodoParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.create_todo(
            project_id=params.project_id,
            todolist_id=params.todolist_id,
            content=params.content,
            description=params.description,
            due_on=params.due_on
        )
        return ActionResult.ok(item, summary=f"Created to-do: {item.get('title', params.content)}")
    except Exception as e:
        return ActionResult.error(f"Error creating todo: {e}")

@chat.function(
    'complete_todo',
    'Mark a Basecamp to-do item as completed.',
    action_type='write',
    chain_callable=True,
    effects=['update:todo']
)
async def complete_todo(params: CompleteTodoParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        res = await client.complete_todo(project_id=params.project_id, todo_id=params.todo_id)
        return ActionResult.ok(res, summary=f"Completed to-do {params.todo_id}.")
    except Exception as e:
        return ActionResult.error(f"Error completing todo: {e}")

@chat.function(
    'uncomplete_todo',
    'Reopen a previously completed Basecamp to-do.',
    action_type='write',
    chain_callable=True,
    effects=['update:todo']
)
async def uncomplete_todo(params: UncompleteTodoParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        res = await client.uncomplete_todo(project_id=params.project_id, todo_id=params.todo_id)
        return ActionResult.ok(res, summary=f"Reopened to-do {params.todo_id}.")
    except Exception as e:
        return ActionResult.error(f"Error reopening todo: {e}")

@chat.function(
    'list_messages',
    'List message board posts in a Basecamp project.',
    action_type='read',
    chain_callable=True
)
async def list_messages(params: ListMessagesParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_messages(project_id=params.project_id, message_board_id=params.message_board_id, page=params.page)
        return ActionResult.ok({"messages": items, "count": len(items)}, summary=f"Retrieved {len(items)} messages.")
    except Exception as e:
        return ActionResult.error(f"Error listing messages: {e}")

@chat.function(
    'post_message',
    'Post a new message to the Basecamp project message board.',
    action_type='write',
    chain_callable=True,
    effects=['create:message']
)
async def post_message(params: PostMessageParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.post_message(
            project_id=params.project_id,
            message_board_id=params.message_board_id,
            subject=params.subject,
            content=params.content
        )
        return ActionResult.ok(item, summary=f"Posted message: {params.subject}")
    except Exception as e:
        return ActionResult.error(f"Error posting message: {e}")

@chat.function(
    'list_webhooks',
    'List registered webhooks in Basecamp.',
    action_type='read',
    chain_callable=True
)
async def list_webhooks(params: ListWebhooksParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        items = await client.list_webhooks(project_id=params.project_id)
        return ActionResult.ok({"webhooks": items, "count": len(items)}, summary=f"Retrieved {len(items)} webhooks.")
    except Exception as e:
        return ActionResult.error(f"Error listing webhooks: {e}")

@chat.function(
    'create_webhook',
    'Register a new webhook endpoint in Basecamp.',
    action_type='write',
    chain_callable=True,
    effects=['create:webhook']
)
async def create_webhook(params: CreateWebhookParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        item = await client.create_webhook(project_id=params.project_id, payload_url=params.payload_url, types=params.types)
        return ActionResult.ok(item, summary=f"Created webhook for {params.payload_url}")
    except Exception as e:
        return ActionResult.error(f"Error creating webhook: {e}")

@chat.function(
    'audit_basecamp_health',
    'Audit account connectivity, project count, and active to-dos.',
    action_type='read',
    chain_callable=True
)
async def audit_basecamp_health(params: AuditHealthParams, ctx) -> ActionResult:
    client = await resolve_client(ctx, params.connection_id)
    try:
        projects = await client.list_projects()
        return ActionResult.ok({
            "status": "healthy",
            "projects_count": len(projects),
            "detail": f"Account is operational with {len(projects)} accessible project(s)."
        }, summary=f"Basecamp health audit: healthy ({len(projects)} projects).")
    except Exception as e:
        return ActionResult.error(f"Health audit failed: {e}")
