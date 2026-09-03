"""Connection handlers for Basecamp Connector."""
from __future__ import annotations
import json
import uuid
from imperal_sdk import ActionResult
from app import chat
from schemas import ConnectBasecampParams, ConnectionIdParams, ConnectionRecord, ConnectionList
from basecamp_client import BasecampClient

_SECRET = "basecamp_connections"

async def _load_connections(ctx) -> list[dict]:
    raw = await ctx.secrets.get(_SECRET)
    if not raw:
        return []
    try:
        data = json.loads(raw)
    except Exception:
        return []
    return data if isinstance(data, list) else []

async def _save_connections(ctx, conns: list[dict]) -> None:
    await ctx.secrets.set(_SECRET, json.dumps(conns))

async def resolve_connection(ctx, connection_id: str = "") -> dict | None:
    conns = await _load_connections(ctx)
    if not conns:
        return None
    if not connection_id:
        for c in conns:
            if c.get("is_active"):
                return c
        return conns[0]
    for c in conns:
        if c.get("id") == connection_id:
            return c
    return None

async def resolve_client(ctx, connection_id: str = "") -> BasecampClient:
    conn = await resolve_connection(ctx, connection_id)
    if not conn:
        raise ValueError("No Basecamp account connected. Please connect one first.")
    return BasecampClient(account_id=conn["account_id"], access_token=conn["access_token"])

@chat.function("connect_basecamp", action_type="write", description="Connect a Basecamp workspace by saving account ID and OAuth token.")
async def connect_basecamp(params: ConnectBasecampParams, ctx) -> ActionResult[ConnectionRecord]:
    client = BasecampClient(account_id=params.account_id, access_token=params.access_token)
    await client.verify()
    conns = await _load_connections(ctx)
    cid = f"conn_{uuid.uuid4().hex[:8]}"
    record = {
        "id": cid,
        "label": params.label or f"Basecamp Account {params.account_id}",
        "account_id": params.account_id,
        "access_token": params.access_token,
        "is_active": True
    }
    for c in conns:
        c["is_active"] = False
    conns.append(record)
    await _save_connections(ctx, conns)
    return ActionResult.ok(
        ConnectionRecord(
            id=record["id"],
            label=record["label"],
            masked_key=f"••••{params.access_token[-4:]}",
            base_url=f"https://3.basecampapi.com/{params.account_id}",
            is_active=True
        ),
        summary=f"Connected Basecamp account {params.account_id} successfully."
    )

@chat.function("list_connections", action_type="read", description="List connected Basecamp workspaces.")
async def list_connections(ctx) -> ActionResult[ConnectionList]:
    conns = await _load_connections(ctx)
    records = [
        ConnectionRecord(
            id=c["id"],
            label=c.get("label", ""),
            masked_key=f"••••{c['access_token'][-4:]}" if c.get("access_token") else "",
            base_url=f"https://3.basecampapi.com/{c.get('account_id', '')}",
            is_active=c.get("is_active", False)
        )
        for c in conns
    ]
    return ActionResult.ok(ConnectionList(connections=records, total=len(records)), summary=f"Found {len(records)} connection(s).")

@chat.function("disconnect_basecamp", action_type="write", description="Disconnect a Basecamp workspace.")
async def disconnect_basecamp(params: ConnectionIdParams, ctx) -> ActionResult:
    conns = await _load_connections(ctx)
    target = params.connection_id
    if not target:
        for c in conns:
            if c.get("is_active"):
                target = c.get("id")
                break
    conns = [c for c in conns if c.get("id") != target]
    if conns and not any(c.get("is_active") for c in conns):
        conns[0]["is_active"] = True
    await _save_connections(ctx, conns)
    return ActionResult.ok({"disconnected": target}, summary="Basecamp account disconnected.")
