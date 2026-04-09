"""
NanoClaw ADK Agent — root agent definition.

Loaded by `adk api_server`. Reads persona from AGENT.md,
configures MCP tools (nanoclaw IPC), and exposes specialist
sub-agents from the Specialists section of the persona.
"""

import os
import re
from pathlib import Path

from google.adk.agents import LlmAgent

# --- Configuration from environment ---

MODEL = os.environ.get("NANOCLAW_MODEL", "gemini-2.5-flash")
MCP_SERVER_PATH = os.environ.get("NANOCLAW_MCP_SERVER", "")
CHAT_JID = os.environ.get("NANOCLAW_CHAT_JID", "")
GROUP_FOLDER = os.environ.get("NANOCLAW_GROUP_FOLDER", "")
IS_MAIN = os.environ.get("NANOCLAW_IS_MAIN", "0")
WORKSPACE = os.environ.get("NANOCLAW_WORKSPACE", "/workspace/group")


# --- Load persona from AGENT.md ---

def load_persona() -> str:
    """Load agent persona from AGENT.md, falling back to GEMINI.md."""
    for name in ["AGENT.md", "GEMINI.md", "CLAUDE.md"]:
        persona_path = Path(WORKSPACE) / name
        if persona_path.exists():
            return persona_path.read_text()
    return "You are a helpful assistant."


def load_global_persona() -> str:
    """Load global persona if available."""
    for name in ["AGENT.md", "GEMINI.md", "CLAUDE.md"]:
        path = Path("/workspace/global") / name
        if path.exists():
            return path.read_text()
    return ""


def parse_specialists(persona: str) -> list:
    """Parse specialist definitions from ## Specialists section."""
    specialists = []
    section = re.search(
        r"## Specialists\s*\n([\s\S]*?)(?=\n## |\Z)", persona, re.IGNORECASE
    )
    if not section:
        return specialists

    headings = list(
        re.finditer(r"###\s+(\w+)\s*\n([\s\S]*?)(?=\n###\s|\Z)", section.group(1))
    )
    for match in headings:
        name = match.group(1).lower()
        instruction = match.group(2).strip()
        if not instruction or name in ("how", "when"):
            continue
        specialists.append(
            LlmAgent(
                name=name,
                model=MODEL,
                instruction=instruction,
                description=f"{name.title()} specialist agent",
            )
        )
    return specialists


# --- Build tools ---

def build_tools() -> list:
    """Configure MCP tools for the NanoClaw IPC server."""
    tools = []
    if not MCP_SERVER_PATH:
        return tools

    mcp_env = {
        "NANOCLAW_CHAT_JID": CHAT_JID,
        "NANOCLAW_GROUP_FOLDER": GROUP_FOLDER,
        "NANOCLAW_IS_MAIN": IS_MAIN,
        "NANOCLAW_RUNTIME": "gemini",
        "NANOCLAW_MODEL": MODEL,
    }

    try:
        # Try newer ADK API first (google-adk >= 1.0)
        from google.adk.tools.mcp_tool import MCPToolset
        from mcp import StdioServerParameters
        tools.append(
            MCPToolset(
                connection_params=StdioServerParameters(
                    command="node",
                    args=[MCP_SERVER_PATH],
                    env=mcp_env,
                )
            )
        )
    except (ImportError, TypeError):
        try:
            # Try older ADK API (McpToolset + StdioConnectionParams)
            from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams
            tools.append(
                McpToolset(
                    connection_params=StdioConnectionParams(
                        command="node",
                        args=[MCP_SERVER_PATH],
                        env=mcp_env,
                    )
                )
            )
        except Exception as e:
            print(f"[nanoclaw_agent] Warning: Could not configure MCP tools: {e}")

    return tools


# --- Assemble the root agent ---

persona = load_persona()
global_persona = load_global_persona()
full_instruction = f"{global_persona}\n\n---\n\n{persona}" if global_persona else persona

specialists = parse_specialists(persona)

agent_kwargs = dict(
    name="nanoclaw",
    model=MODEL,
    instruction=full_instruction,
    description="NanoClaw personal assistant",
    tools=build_tools(),
)
if specialists:
    agent_kwargs["sub_agents"] = specialists

root_agent = LlmAgent(**agent_kwargs)

