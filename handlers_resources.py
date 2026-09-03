"""Resource handlers for Basecamp."""
from __future__ import annotations
import time
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    ConnectionIdParams, ResourceIdParams, ListResourcesParams,
    AccountOverview, HealthReport, ResourceRecord, ResourceList
)
from handlers_connection import _load_conns
from basecamp_client import BasecampClient

async def _get_client(params, ctx):
    conns = await _load_conns(ctx)
    if not conns:
        return None, "No connected Basecamp account found. Please connect first."
    cid = getattr(params, "connection_id", "")
    target = None
    if cid:
        for c in conns:
            if c["id"] == cid:
                target = c
                break
    if not target:
        target = next((c for c in conns if c.get("is_active")), conns[0])
    return BasecampClient(api_key=target["api_key"], base_url=target.get("base_url", "")), None

async def get_overview(params: ConnectionIdParams, ctx) -> ActionResult:
    client, err = await _get_client(params, ctx)
    if err:
        return ActionResult.error(err)
    data = await client.get_overview()
    return ActionResult.ok(f"Basecamp overview retrieved", data=data)

async def audit_health(params: ConnectionIdParams, ctx) -> ActionResult:
    start = time.perf_counter()
    client, err = await _get_client(params, ctx)
    if err:
        return ActionResult.error(err)
    data = await client.test_auth()
    latency = round((time.perf_counter() - start) * 1000, 2)
    rep = HealthReport(
        status="healthy" if data.get("status") in ("ok", "verified") else "warning",
        connected=True,
        latency_ms=latency,
        message=f"Basecamp responsive in {latency}ms"
    )
    return ActionResult.ok(f"Basecamp health audit: {rep.status}", data=rep.dict())

async def list_resources(params: ListResourcesParams, ctx) -> ActionResult:
    client, err = await _get_client(params, ctx)
    if err:
        return ActionResult.error(err)
    data = await client.list_resources(limit=params.limit, cursor=params.cursor)
    return ActionResult.ok(f"Basecamp resources listed", data=data)

async def get_resource(params: ResourceIdParams, ctx) -> ActionResult:
    client, err = await _get_client(params, ctx)
    if err:
        return ActionResult.error(err)
    data = await client.get_resource(params.resource_id)
    return ActionResult.ok(f"Basecamp resource {params.resource_id} retrieved", data=data)
