import os
from pathlib import Path

# Defaults
DEFAULT_REGISTRY_URL = "https://skills.leezhu.cn/api/v1"
DEFAULT_ROOT = Path.home() / ".skills"

class Config:
    def __init__(self):
        # 1. Skills Root Directory
        root_env = os.getenv("SKILLS_ROOT")
        if root_env:
            self.root_dir = Path(root_env).expanduser().resolve()
        else:
            self.root_dir = DEFAULT_ROOT

        # Ensure directory exists
        self.root_dir.mkdir(parents=True, exist_ok=True)

        # 2. Registry URL
        url_env = os.getenv("SKILLS_REGISTRY_URL")
        self.registry_url = url_env.rstrip("/") if url_env else DEFAULT_REGISTRY_URL

        # 3. Auth Token
        self.api_key = os.getenv("SKILLS_API_KEY")

config = Config()
