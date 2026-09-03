"""Connection lifecycle handlers for Basecamp Connector."""
from __future__ import annotations
import json, uuid
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    ConnectBasecampParams, DisconnectBasecampParams, NoParams,
    ConnectionList, BasecampConnection, ConnectResult, DisconnectResult
)
from basecamp_client import BasecampClient

SECRET_KEY = "basecamp_connections"

async def _load_connections(ctx) -> list[dict]:
    raw = await ctx.secrets.get(SECRET_KEY)
    if not raw:
        return []
    try:
        return json.loads(raw)
    except Exception:
        return []

async def _save_connections(ctx, connections: list[dict]) -> None:
    await ctx.secrets.set(SECRET_KEY, json.dumps(connections))

async def resolve_client(ctx, connection_id: str = "") -> BasecampClient:
    connections = await _load_connections(ctx)
    if not connections:
        raise ValueError("No Basecamp connections found. Please connect an account first.")
    if connection_id:
        for c in connections:
            if c.get("id") == connection_id:
                return BasecampClient(account_id=c["account_id"], access_token=c["access_token"])
        raise ValueError(f"Connection ID {connection_id} not found.")
    c = connections[0]
    return BasecampClient(account_id=c["account_id"], access_token=c["access_token"])

@chat.function(
    "connect_basecamp",
    "Connect your own Basecamp account by saving Account ID and OAuth Bearer token.",
    action_type="write",
    chain_callable=True,
    event="basecamp-connector.connect_basecamp",
    effects=["create:connection"],
    data_model=ConnectResult
)
async def connect_basecamp(ctx, params: ConnectBasecampParams) -> ActionResult:
    """Connect a Basecamp account after verifying credentials."""
    client = BasecampClient(account_id=params.account_id, access_token=params.access_token)
    if not await client.verify():
        return ActionResult.error("Failed to verify Basecamp connection with provided credentials.")
    connections = await _load_connections(ctx)
    conn_id = str(uuid.uuid4())
    entry = {
        "id": conn_id,
        "label": params.label or f"Basecamp ({params.account_id})",
        "account_id": params.account_id,
        "access_token": params.access_token
    }
    connections.append(entry)
    await _save_connections(ctx, connections)
    return ActionResult.success(
        ConnectResult(id=conn_id, label=entry["label"], account_id=params.account_id),
        summary=f"Connected Basecamp account {params.account_id}."
    )

@chat.function(
    "list_connections",
    "List connected Basecamp accounts without exposing credentials.",
    action_type="read",
    chain_callable=True,
    data_model=ConnectionList
)
async def list_connections(ctx, params: NoParams) -> ActionResult:
    """List connected Basecamp accounts."""
    connections = await _load_connections(ctx)
    return ActionResult.success(
        ConnectionList(connections=[
            BasecampConnection(id=c.get("id", ""), label=c.get("label", ""), account_id=c.get("account_id", ""))
            for c in connections
        ]),
        summary=f"Found {len(connections)} Basecamp connection(s)."
    )

@chat.function(
    "disconnect_basecamp",
    "Disconnect a Basecamp account.",
    action_type="write",
    chain_callable=True,
    event="basecamp-connector.disconnect_basecamp",
    effects=["delete:connection"],
    data_model=DisconnectResult
)
async def disconnect_basecamp(ctx, params: DisconnectBasecampParams) -> ActionResult:
    """Disconnect a Basecamp account by ID."""
    connections = await _load_connections(ctx)
    remaining = [c for c in connections if c.get("id") != params.connection_id]
    if len(remaining) == len(connections):
        return ActionResult.error(f"Connection {params.connection_id} not found.")
    await _save_connections(ctx, remaining)
    return ActionResult.success(
        DisconnectResult(removed_connection_id=params.connection_id),
        summary=f"Disconnected Basecamp account {params.connection_id}."
    )
