"""Connection lifecycle handlers for Basecamp Connector."""
from __future__ import annotations
import json
import uuid
from imperal_sdk import ActionResult
from basecamp_client import BasecampClient
from schemas import ConnectBasecampParams, ConnectionIdParams, ConnectionList, ConnectionRecord

SECRET_KEY = "basecamp_connections"

def _mask(token: str) -> str:
    return f"{token[:4]}...{token[-4:]}" if len(token) > 8 else "***"

async def _load_conns(ctx) -> list[dict]:
    raw = await ctx.secrets.get(SECRET_KEY)
    if not raw:
        return []
    try:
        data = json.loads(raw)
        return data if isinstance(data, list) else []
    except Exception:
        return []

async def _save_conns(ctx, conns: list[dict]) -> None:
    await ctx.secrets.set(SECRET_KEY, json.dumps(conns))

async def resolve_client(ctx, connection_id: str = "") -> BasecampClient:
    conns = await _load_conns(ctx)
    if not conns:
        raise ValueError("No Basecamp connections configured. Connect an account first.")
    target = None
    if connection_id:
        for c in conns:
            if c["id"] == connection_id:
                target = c
                break
        if not target:
            raise ValueError(f"Connection {connection_id} not found.")
    else:
        target = conns[0]
    return BasecampClient(account_id=target["account_id"], access_token=target["access_token"])

async def connect_basecamp(params: ConnectBasecampParams, ctx) -> ActionResult:
    client = BasecampClient(account_id=params.account_id, access_token=params.access_token)
    try:
        ver = await client.verify()
    except Exception as e:
        return ActionResult.error(f"Failed to connect Basecamp account: {e}")

    conn_id = f"bc_{uuid.uuid4().hex[:8]}"
    label = params.label.strip() or f"Basecamp ({params.account_id})"
    conns = await _load_conns(ctx)
    conns.append({
        "id": conn_id,
        "label": label,
        "account_id": params.account_id,
        "access_token": params.access_token
    })
    await _save_conns(ctx, conns)
    return ActionResult.ok({
        "connection_id": conn_id,
        "label": label,
        "account_id": params.account_id,
        "status": "connected",
        "verification": ver
    }, summary=f"Basecamp account {params.account_id} connected successfully.")

async def list_connections(params: dict, ctx) -> ActionResult:
    conns = await _load_conns(ctx)
    records = [
        ConnectionRecord(
            id=c["id"],
            label=c["label"],
            account_id=c["account_id"],
            masked_token=_mask(c["access_token"]),
            is_active=True
        ) for c in conns
    ]
    return ActionResult.ok(ConnectionList(connections=records, total=len(records)).model_dump(), summary=f"Found {len(records)} connection(s).")

async def disconnect_basecamp(params: ConnectionIdParams, ctx) -> ActionResult:
    conns = await _load_conns(ctx)
    if not conns:
        return ActionResult.error("No connections to disconnect.")
    target_id = params.connection_id or conns[0]["id"]
    new_conns = [c for c in conns if c["id"] != target_id]
    if len(new_conns) == len(conns):
        return ActionResult.error(f"Connection {target_id} not found.")
    await _save_conns(ctx, new_conns)
    return ActionResult.ok({"status": "disconnected", "connection_id": target_id}, summary=f"Basecamp connection {target_id} disconnected.")
