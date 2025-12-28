from typing import Optional
from mcp.server.fastmcp import FastMCP
from pydantic import Field

from . import api, local

# Initialize FastMCP
mcp = FastMCP("skills")

@mcp.tool()
def skills_search(
    query: str = Field(description="Search keywords"),
    page: int = Field(default=1, description="Page number"),
    limit: int = Field(default=10, description="Items per page")
) -> str:
    """
    Search the global skills registry for available capabilities.
    Use this when you don't have a tool for a specific task.
    """
    client = api.RegistryClient()
    try:
        results = client.search(query, page, limit)

        # Format for LLM
        # 优先取 "skills"，为了兼容性也 fallback 到 "items"
        items = results.get("skills", results.get("items", []))
        if not items:
            return "No skills found matching your query."

        output = [f"Found {len(items)} skills (Page {page}):"]
        for item in items:
            output.append(f"- {item['name']} (v{item.get('version', '?')}): {item['description']}")

        return "\n".join(output)
    except Exception as e:
        return f"Error searching skills: {str(e)}"

@mcp.tool()
def skills_list() -> str:
    """List all locally installed skills."""
    try:
        skills = local.get_installed_skills()
        if not skills:
            return "No skills installed locally."

        output = ["Installed Skills:"]
        for s in skills:
            output.append(f"- {s['name']} ({s['path']})")
        return "\n".join(output)
    except Exception as e:
        return f"Error listing skills: {str(e)}"

@mcp.tool()
def skills_install(
    name: str = Field(description="Exact name of the skill"),
    force: bool = Field(default=False, description="Overwrite if exists")
) -> str:
    """Download and install a skill to the local environment."""
    try:
        return local.install_skill(name, force)
    except Exception as e:
        return f"Installation failed: {str(e)}"

@mcp.tool()
def skills_get_details(
    name: str = Field(description="Name of the installed skill")
) -> str:
    """
    Read the instruction manual (SKILL.md) and file structure of a locally installed skill.
    Use this to learn how to use a skill after installing it.
    """
    try:
        details = local.get_details(name)
        return f"""# Skill: {name}
Path: {details['path']}

## File Structure
```
{details['tree']}
```

## Instructions
{details['instruction']}
"""
    except Exception as e:
        return f"Error getting details: {str(e)}"

def main():
    mcp.run()

if __name__ == "__main__":
    main()
