import shutil
import zipfile
import io
import httpx
from pathlib import Path
from typing import List, Dict, Optional

from .config import config
from .utils import generate_tree
from .api import RegistryClient

client = RegistryClient()

def get_installed_skills() -> List[Dict[str, str]]:
    """List local skills."""
    skills = []
    if not config.root_dir.exists():
        return []

    for item in config.root_dir.iterdir():
        if item.is_dir() and (item / "SKILL.md").exists():
            skills.append({
                "name": item.name,
                "path": str(item)
            })
    return skills

def is_installed(name: str) -> bool:
    return (config.root_dir / name / "SKILL.md").exists()

def get_details(name: str) -> Dict[str, str]:
    target_dir = config.root_dir / name
    if not target_dir.exists():
        raise FileNotFoundError(f"Skill '{name}' is not installed locally.")

    skill_md = target_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"Corrupted skill '{name}': SKILL.md missing.")

    return {
        "path": str(target_dir),
        "tree": generate_tree(target_dir),
        "instruction": skill_md.read_text(encoding="utf-8")
    }

def install_skill(name: str, force: bool = False) -> str:
    target_dir = config.root_dir / name

    if target_dir.exists():
        if not force:
            return f"Skill '{name}' is already installed at {target_dir}."
        else:
            shutil.rmtree(target_dir)

    # Download logic
    url = f"{client.base_url}/download/{name}"

    try:
        with httpx.stream("GET", url, headers=client.headers, timeout=30.0) as resp:
            if resp.status_code == 404:
                raise RuntimeError(f"Skill '{name}' not found in registry.")
            resp.raise_for_status()

            # Download full content to memory (assuming zip files are small < 50MB)
            # For larger files, we should use a temporary file.
            data = io.BytesIO()
            for chunk in resp.iter_bytes():
                data.write(chunk)

            with zipfile.ZipFile(data) as zf:
                # Security Check: Prevent Zip Slip
                for member in zf.namelist():
                    if ".." in member or member.startswith("/"):
                        raise RuntimeError("Malicious zip file detected.")

                # 1. 检查是否存在顶层目录嵌套
                # 改进后的判定逻辑：只要 SKILL.md 是在子目录里，就认为是嵌套的
                skill_md_path = next((f for f in zf.namelist() if f.endswith("SKILL.md")), None)

                if skill_md_path and "/" in skill_md_path:
                    # 例如 "docx/SKILL.md"
                    prefix = skill_md_path.split("/SKILL.md")[0] + "/"
                    is_nested = True
                else:
                    prefix = ""
                    is_nested = False

                target_dir.mkdir(parents=True, exist_ok=True)

                if is_nested:
                    # 智能解压：去掉第一层目录
                    for member in zf.infolist():
                        if member.filename == prefix: continue # 跳过顶层目录本身
                        
                        # 去掉前缀
                        new_name = member.filename[len(prefix):]
                        if not new_name: continue
                        
                        target_path = target_dir / new_name
                        
                        if member.is_dir():
                            target_path.mkdir(parents=True, exist_ok=True)
                        else:
                            target_path.parent.mkdir(parents=True, exist_ok=True)
                            with zf.open(member, "r") as source, open(target_path, "wb") as target:
                                shutil.copyfileobj(source, target)
                else:
                    # 直接解压
                    zf.extractall(target_dir)
                
                # 最后的完整性检查
                if not (target_dir / "SKILL.md").exists():
                     # 回滚
                     shutil.rmtree(target_dir)
                     raise RuntimeError("Invalid skill package: missing SKILL.md after extraction.")

    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"Download failed: {e.response.text}")
    except Exception as e:
        # Cleanup partial install
        if target_dir.exists():
            shutil.rmtree(target_dir)
        raise e

    return f"Successfully installed '{name}' to {target_dir}."
