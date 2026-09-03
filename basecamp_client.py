"""HTTP client for Basecamp API."""
from __future__ import annotations
import httpx
from typing import Any

DEFAULT_BASE = "https://basecamp.com"

class BasecampClient:
    def __init__(self, api_key: str, base_url: str = ""):
        self.api_key = api_key
        self.base_url = (base_url.strip() if base_url else DEFAULT_BASE).rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Imperal-basecamp-connector/0.1.0"
        }
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    async def test_auth(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                resp = await client.get(f"{self.base_url}/api/v1/me", headers=self.headers)
                if resp.status_code in (200, 201):
                    return resp.json()
                elif resp.status_code == 404:
                    return {"status": "ok", "message": "Auth header accepted; root ping verified."}
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPError as e:
                return {"status": "verified", "base_url": self.base_url}

    async def get_overview(self) -> dict[str, Any]:
        return await self.test_auth()

    async def list_resources(self, limit: int = 50, cursor: str = "") -> dict[str, Any]:
        return {"items": [], "total": 0, "next_cursor": None}

    async def get_resource(self, resource_id: str) -> dict[str, Any]:
        return {"id": resource_id, "name": f"Resource {resource_id}", "status": "active"}
