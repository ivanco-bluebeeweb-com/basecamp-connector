"""Extension declaration, capabilities, health check for Basecamp Connector."""
from __future__ import annotations
import json
from imperal_sdk import ChatExtension, Extension

ext = Extension(
    "basecamp-connector",
    version="0.1.0",
    display_name="Basecamp",
    icon="icon.svg",
    capabilities=["basecamp:manage"],
    description="Official Imperal connector for Basecamp (C25. Project & Work Management). Manage operations securely."
)

chat = ChatExtension(ext)

@ext.health_check
async def health_check(ctx) -> dict:
    raw = await ctx.secrets.get("basecamp_connections")
    try:
        count = len(json.loads(raw)) if raw else 0
    except Exception:
        count = 0
    return {
        "healthy": True,
        "detail": f"{count} Basecamp connection(s) configured." if count else "Not connected yet."
    }
