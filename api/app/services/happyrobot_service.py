import httpx
import logging
from typing import Any, Optional
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

class HappyRobotClient:
    def __init__(self):
        self.api_key = settings.happyrobot_api_key
        self.base_url = settings.happyrobot_base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.client = httpx.AsyncClient(headers=self.headers, timeout=30.0)

    async def close(self):
        await self.client.aclose()

    async def _get(self, path: str) -> Optional[dict]:
        if not self.api_key:
            return None
        try:
            url = f"{self.base_url}{path}"
            resp = await self.client.get(url)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            logger.warning(f"HappyRobot API GET {path} failed: {e}")
            return None

    async def list_workflows(self) -> list[dict]:
        data = await self._get("/workflows")
        if data and "workflows" in data:
            return data["workflows"]
        if data and isinstance(data, list):
            return data
        return []

    async def list_runs(self, workflow_id: str, limit: int = 100) -> list[dict]:
        data = await self._get(f"/workflows/{workflow_id}/runs?limit={limit}")
        if data and "runs" in data:
            return data["runs"]
        if data and isinstance(data, list):
            return data
        return []

    async def get_run(self, run_id: str) -> Optional[dict]:
        return await self._get(f"/runs/{run_id}")

    async def get_run_nodes(self, run_id: str) -> list[dict]:
        data = await self._get(f"/runs/{run_id}/nodes")
        if data and "nodes" in data:
            return data["nodes"]
        if data and isinstance(data, list):
            return data
        return []

    async def get_run_sessions(self, run_id: str) -> list[dict]:
        data = await self._get(f"/runs/{run_id}/sessions")
        if data and "sessions" in data:
            return data["sessions"]
        if data and isinstance(data, list):
            return data
        return []

    async def get_session_messages(self, session_id: str) -> list[dict]:
        data = await self._get(f"/sessions/{session_id}/messages")
        if data and "messages" in data:
            return data["messages"]
        if data and isinstance(data, list):
            return data
        return []

    async def get_run_output(self, run_id: str, output_id: str) -> Optional[dict]:
        return await self._get(f"/runs/{run_id}/outputs/{output_id}")

    async def get_workflow(self, workflow_id: str) -> Optional[dict]:
        return await self._get(f"/workflows/{workflow_id}")

    def is_configured(self) -> bool:
        return bool(self.api_key)

_hr_client: Optional[HappyRobotClient] = None

async def get_hr_client() -> HappyRobotClient:
    global _hr_client
    if _hr_client is None:
        _hr_client = HappyRobotClient()
    return _hr_client
