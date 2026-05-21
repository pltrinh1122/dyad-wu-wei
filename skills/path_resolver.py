import os
import yaml
from skills import git_client

def get_core_dir() -> str:
    """Returns the absolute path to the SPAO installation/core codebase directory."""
    # This file resides in <core_dir>/skills/path_resolver.py
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_workspace_dir() -> str:
    """Returns the absolute path to the active project workspace root directory."""
    env_workspace = os.environ.get("SPAO_WORKSPACE_DIR")
    if env_workspace:
        return os.path.abspath(env_workspace)
        
    try:
        toplevel = git_client.get_show_toplevel()
        if toplevel:
            return os.path.abspath(toplevel)
    except Exception:
        pass
        
    return os.path.abspath(os.getcwd())

def resolve_workspace_path(*paths: str) -> str:
    """Resolves an absolute path relative to the active target workspace root."""
    return os.path.join(get_workspace_dir(), *paths)

def resolve_core_path(*paths: str) -> str:
    """Resolves an absolute path relative to the SPAO core installation directory."""
    return os.path.join(get_core_dir(), *paths)

def load_node_yml() -> dict:
    """Loads node.yml from workspace directory, falling back to core directory if missing."""
    workspace_path = resolve_workspace_path("node.yml")
    if os.path.exists(workspace_path):
        target_path = workspace_path
    else:
        target_path = resolve_core_path("node.yml")
        
    if not os.path.exists(target_path):
        return {}
        
    with open(target_path, "r") as f:
        config = yaml.safe_load(f) or {}
    return config

def resolve_agent_id() -> str | None:
    """Dynamically resolves the active agent persona identity."""
    # 1. Check if SPAO_AGENT_ID exists in the environment
    agent_id = os.environ.get("SPAO_AGENT_ID")
    if agent_id:
        return agent_id
        
    # 2. Fallback to parsing the workspace directory basename
    try:
        workspace_dir = get_workspace_dir()
        basename = os.path.basename(workspace_dir)
        if basename.lower().startswith("agent-"):
            normalized = basename.lower().replace("_", "-")
            if normalized.endswith("-auto"):
                normalized = normalized[:-5]
            return normalized
    except Exception:
        pass
        
    return None

def load_antigravity_yml() -> dict:
    """Loads antigravity.yml from workspace directory, falling back to core directory if missing."""
    workspace_path = resolve_workspace_path("antigravity.yml")
    if os.path.exists(workspace_path):
        target_path = workspace_path
    else:
        target_path = resolve_core_path("antigravity.yml")
        
    if not os.path.exists(target_path):
        return {}
        
    with open(target_path, "r") as f:
        config = yaml.safe_load(f) or {}
        
    resolved_id = resolve_agent_id()
    if resolved_id:
        config["agent_id"] = resolved_id
        
    return config

