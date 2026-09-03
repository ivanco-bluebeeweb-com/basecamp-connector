"""HTTP client for Basecamp 3 API."""
from __future__ import annotations
import httpx
from typing import Any

class BasecampClient:
    def __init__(self, account_id: str, access_token: str):
        self.account_id = account_id.strip()
        self.access_token = access_token.strip()
        self.base_url = f"https://3.basecampapi.com/{self.account_id}"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "User-Agent": "Imperal-Cloud-OS (integrations@imperal.io)"
        }
        self.timeout = httpx.Timeout(30.0, connect=10.0)

    async def verify(self) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/projects.json", headers=self.headers)
            if resp.status_code in (200, 201):
                return {"status": "ok", "project_count": len(resp.json())}
            resp.raise_for_status()
            return resp.json()

    async def list_projects(self, status: str = "active", page: int = 1) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            params = {"status": status, "page": page} if status != "active" else {"page": page}
            resp = await client.get(f"{self.base_url}/projects.json", headers=self.headers, params=params)
            resp.raise_for_status()
            return resp.json()

    async def get_project(self, project_id: int) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/projects/{project_id}.json", headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    async def create_project(self, name: str, description: str = "") -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            payload = {"name": name, "description": description}
            resp = await client.post(f"{self.base_url}/projects.json", headers=self.headers, json=payload)
            resp.raise_for_status()
            return resp.json()

    async def list_todos(self, project_id: int, todolist_id: int, status: str = "active") -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            params = {"status": status}
            resp = await client.get(f"{self.base_url}/buckets/{project_id}/todolists/{todolist_id}/todos.json", headers=self.headers, params=params)
            resp.raise_for_status()
            return resp.json()

    async def create_todo(self, project_id: int, todolist_id: int, content: str, description: str = "", due_on: str = "", assignee_ids: list[int] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            payload: dict[str, Any] = {"content": content, "description": description}
            if due_on:
                payload["due_on"] = due_on
            if assignee_ids:
                payload["assignee_ids"] = assignee_ids
            resp = await client.post(f"{self.base_url}/buckets/{project_id}/todolists/{todolist_id}/todos.json", headers=self.headers, json=payload)
            resp.raise_for_status()
            return resp.json()

    async def complete_todo(self, project_id: int, todo_id: int) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(f"{self.base_url}/buckets/{project_id}/todos/{todo_id}/completion.json", headers=self.headers)
            resp.raise_for_status()
            return resp.json() if resp.text else {"status": "completed", "id": todo_id}

    async def uncomplete_todo(self, project_id: int, todo_id: int) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.delete(f"{self.base_url}/buckets/{project_id}/todos/{todo_id}/completion.json", headers=self.headers)
            resp.raise_for_status()
            return resp.json() if resp.text else {"status": "uncompleted", "id": todo_id}

    async def list_messages(self, project_id: int, message_board_id: int, page: int = 1) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/buckets/{project_id}/message_boards/{message_board_id}/messages.json", headers=self.headers, params={"page": page})
            resp.raise_for_status()
            return resp.json()

    async def post_message(self, project_id: int, message_board_id: int, subject: str, content: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            payload = {"subject": subject, "content": content, "status": "active"}
            resp = await client.post(f"{self.base_url}/buckets/{project_id}/message_boards/{message_board_id}/messages.json", headers=self.headers, json=payload)
            resp.raise_for_status()
            return resp.json()

    async def list_webhooks(self, project_id: int) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.get(f"{self.base_url}/buckets/{project_id}/webhooks.json", headers=self.headers)
            resp.raise_for_status()
            return resp.json()

    async def create_webhook(self, project_id: int, payload_url: str, types: list[str] | None = None) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            payload: dict[str, Any] = {"payload_url": payload_url, "active": True}
            if types:
                payload["types"] = types
            resp = await client.post(f"{self.base_url}/buckets/{project_id}/webhooks.json", headers=self.headers, json=payload)
            resp.raise_for_status()
            return resp.json()
