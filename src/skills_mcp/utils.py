import os
from pathlib import Path

# 强制过滤的黑名单
IGNORED_DIRS = {
    ".git", ".svn", ".hg", ".idea", ".vscode",
    ".venv", "venv", "env", "node_modules",
    "__pycache__", "dist", "build", "target",
    "bin", "obj"
}

IGNORED_FILES = {
    ".DS_Store", "Thumbs.db"
}

IGNORED_EXTENSIONS = {
    ".pyc", ".pyo", ".pyd", ".so", ".dll", ".dylib", ".exe", ".class"
}

def generate_tree(root_path: Path) -> str:
    """Generates a visual file tree string, filtering out noise."""
    output = []

    # Walk the directory
    for dirpath, dirnames, filenames in os.walk(root_path):
        # 1. In-place filtering of directories to prevent recursion into ignored dirs
        dirnames[:] = [d for d in dirnames if d not in IGNORED_DIRS and not d.startswith(".")]

        rel_path = Path(dirpath).relative_to(root_path)

        if rel_path == Path("."):
            level = 0
        else:
            level = len(rel_path.parts)
            indent = "  " * (level - 1)
            output.append(f"{indent}- {rel_path.name}/")

        sub_indent = "  " * level
        for f in sorted(filenames):
            if f in IGNORED_FILES or f.startswith("."):
                continue
            if any(f.endswith(ext) for ext in IGNORED_EXTENSIONS):
                continue

            output.append(f"{sub_indent}- {f}")

    return "\n".join(output)
