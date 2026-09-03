"""Connection management handlers for Basecamp."""
from __future__ import annotations
import json
import uuid
from imperal_sdk import ActionResult
from app import chat
from schemas import ConnectParams, ConnectionIdParams, ConnectionList, ConnectionRecord
from basecamp_client import BasecampClient

_SECRET = "basecamp_connections"

def _mask(key: str) -> str:
    return key[:4] + "..." + key[-4:] if len(key) > 8 else "***"

async def _load_conns(ctx) -> list[dict]:
    raw = await ctx.secrets.get(_SECRET)
    if not raw:
        return []
    try:
        val = json.loads(raw)
        return val if isinstance(val, list) else []
    except Exception:
        return []

async def _save_conns(ctx, conns: list[dict]) -> None:
    await ctx.secrets.set(_SECRET, json.dumps(conns))

async def connect_basecamp(params: ConnectParams, ctx) -> ActionResult:
    client = BasecampClient(api_key=params.api_key, base_url=params.base_url)
    res = await client.test_auth()
    conns = await _load_conns(ctx)
    conn_id = str(uuid.uuid4())[:8]
    record = {
        "id": conn_id,
        "label": params.label or f"Basecamp ({conn_id})",
        "api_key": params.api_key,
        "base_url": client.base_url,
        "is_active": len(conns) == 0
    }
    conns.append(record)
    await _save_conns(ctx, conns)
    return ActionResult.ok(
        f"Connected Basecamp ({record['label']})",
        data={"id": conn_id, "label": record["label"], "status": res.get("status", "ok")}
    )

async def list_connections(ctx) -> ActionResult:
    conns = await _load_conns(ctx)
    items = [
        ConnectionRecord(
            id=c["id"],
            label=c.get("label", ""),
            masked_key=_mask(c.get("api_key", "")),
            base_url=c.get("base_url", ""),
            is_active=c.get("is_active", False)
        )
        for c in conns
    ]
    return ActionResult.ok(f"Found {len(items)} connections", data=ConnectionList(connections=items, total=len(items)).dict())

async def disconnect_basecamp(params: ConnectionIdParams, ctx) -> ActionResult:
    conns = await _load_conns(ctx)
    if not conns:
        return ActionResult.error("No connections to disconnect.")
    target_id = params.connection_id or conns[0]["id"]
    conns = [c for c in conns if c["id"] != target_id]
    if conns and not any(c.get("is_active") for c in conns):
        conns[0]["is_active"] = True
    await _save_conns(ctx, conns)
    return ActionResult.ok(f"Disconnected Basecamp connection {target_id}", data={"id": target_id})
