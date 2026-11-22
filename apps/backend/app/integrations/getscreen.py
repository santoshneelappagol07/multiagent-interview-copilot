import httpx
from typing import Dict, Any, List
import logging

logger = logging.getLogger("ai_voice_copilot.integrations.getscreen")

class GetscreenClient:
    """
    Optional integration with Getscreen.me HTTP REST API
    Used for device querying and session auditing.
    (Note: Audio capture is handled via loopback of whatever plays on the local system)
    """
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.base_url = "https://api.getscreen.me/v1"

    def is_configured(self) -> bool:
        return bool(self.api_key)

    async def list_devices(self) -> List[Dict[str, Any]]:
        if not self.is_configured():
            return []
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    f"{self.base_url}/devices",
                    headers={"X-Api-Key": self.api_key},
                    timeout=5.0
                )
                if resp.status_code == 200:
                    return resp.json().get("data", [])
        except Exception as e:
            logger.error(f"Failed to query Getscreen devices: {e}")
        return []

getscreen_client = GetscreenClient()
