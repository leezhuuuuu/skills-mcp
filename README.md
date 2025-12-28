# Skills MCP

[![PyPI version](https://img.shields.io/pypi/v/skills-mcp.svg)](https://pypi.org/project/skills-mcp/)
[![License](https://img.shields.io/pypi/l/skills-mcp.svg)](LICENSE)
[![Python Versions](https://img.shields.io/pypi/pyversions/skills-mcp.svg)](https://pypi.org/project/skills-mcp/)

The **Package Manager for AI Agents**.

Skills MCP connects your LLM Agent (like Claude Desktop or Claude Code) to a global registry of capabilities. It allows your Agent to autonomously discover, install, and learn new skills to solve complex tasks.

> **Thin MCP, Fat Agent Philosophy:** This tool handles the delivery of code and instructions, empowering the Agent to execute them using its own environment (e.g., `uv`, `bash`).

---

## 🚀 Features

- **Search:** Find skills for specific tasks (e.g., "pdf", "excel", "diagram").
- **Install:** One-click download and installation to your local machine (`~/.skills`).
- **Learn:** Provides the Agent with the exact file structure and `SKILL.md` instructions.
- **Dependency Management:** Works seamlessly with `uv` to let Agents self-manage Python environments without polluting your system.

---

## 📦 Installation

The recommended way to install is via `uv` (a fast Python package manager). It ensures the tool runs in an isolated environment.

### Prerequisites
- Python 3.10+
- `uv` (Recommended)

```bash
# 1. Install uv (if you haven't already)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Install Skills MCP globally
uv tool install skills-mcp
```

*(Alternatively, you can use `pip`, but we strongly recommend `uv` to avoid dependency conflicts.)*

---

## ⚙️ Configuration

### 🖥️ Claude Desktop (GUI)

To use Skills MCP with the Claude Desktop app, update your configuration file:

- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Add the following entry:

```json
{
  "mcpServers": {
    "skills": {
      "command": "uv",
      "args": ["tool", "run", "skills-mcp"],
      "env": {
        "SKILLS_ROOT": "/Users/YOUR_USERNAME/.skills",
        "SKILLS_REGISTRY_URL": "https://skills.leezhu.cn/api/v1"
      }
    }
  }
}
```
*Tip: Replace `/Users/YOUR_USERNAME` with your actual home directory path.*

### ⌨️ Claude Code (CLI)

If you are using the `claude` command-line tool, you can install the MCP server directly via the CLI:

```bash
# Add the MCP server
claude mcp add skills -- uv tool run skills-mcp
```

**Note on Configuration:**
Claude Code inherits environment variables from your shell. To set custom configurations (like a private registry URL), export them in your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
export SKILLS_REGISTRY_URL="https://your-private-registry.com/api/v1"
```

### Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SKILLS_ROOT` | Where skills are installed locally. | `~/.skills` |
| `SKILLS_REGISTRY_URL` | The API endpoint of the skills registry. | `https://skills.leezhu.cn/api/v1` |
| `SKILLS_API_KEY` | (Optional) Token for private registries. | `None` |

---

## 💡 Usage Guide (for Agents)

Once installed, you can ask Claude to do things like:

1.  **Discovery:**
    > "Search for a skill that can split Excel files."
    *(Claude calls `skills_search`)*

2.  **Acquisition:**
    > "Install the excel-pro skill."
    *(Claude calls `skills_install`)*

3.  **Execution:**
    > "Read the instructions for excel-pro and split this file."
    *(Claude calls `skills_get_details`, reads the `SKILL.md`, installs dependencies via `uv`, and runs the script)*

---

## 🛠️ Development

### Setup

```bash
git clone https://github.com/leezhuuuuu/skills-mcp.git
cd skills-mcp

# Install dependencies
uv sync
```

### Running Locally (StdIO Mode)

```bash
# Direct run
uv run skills-mcp
```

---

## 🤝 Contributing

We welcome contributions! Please feel free to submit a Pull Request.

1.  Fork the repository.
2.  Create your feature branch.
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
