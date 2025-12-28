import httpx
from typing import Optional, Dict, Any, Iterator
from .config import config

class RegistryClient:
    def __init__(self):
        self.base_url = config.registry_url
        self.headers = {
            "User-Agent": "skills-mcp/0.1.0"
        }
        if config.api_key:
            self.headers["Authorization"] = f"Bearer {config.api_key}"

    def search(self, query: str = "", page: int = 1, limit: int = 20) -> Dict[str, Any]:
        """Search skills from the registry."""
        params = {"q": query, "page": page, "limit": limit}
        try:
            resp = httpx.get(f"{self.base_url}/skills", params=params, headers=self.headers, timeout=10.0)
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise PermissionError("Registry authentication failed. Check SKILLS_API_KEY.")
            raise RuntimeError(f"Registry error: {e.response.text}")
        except httpx.RequestError as e:
            raise RuntimeError(f"Network error connecting to registry: {str(e)}")

    def download(self, name: str) -> Iterator[bytes]:
        """Download skill zip stream."""
        url = f"{self.base_url}/download/{name}"
        try:
            # Note: We use a context manager in the caller, so we return a stream here
            # But httpx streams need to be closed.
            # Let's implement a wrapper for simplicity.
            pass
        except Exception:
            raise
