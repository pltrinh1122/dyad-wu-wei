import os
import re
import yaml
from drivers import git_client

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

def resolve_agent_id() -> str:
    """Dynamically resolves the identity of the executing agent at runtime."""
    # 1. Environment Variable
    env_agent_id = os.environ.get("SPAO_AGENT_ID")
    if env_agent_id:
        return env_agent_id
        
    def _resolve_from_path(path: str) -> str | None:
        basename = os.path.basename(path)
        if not basename:
            return None
        sanitized = basename.lower().replace("_", "-")
        if sanitized.endswith("-auto"):
            sanitized = sanitized[:-5]
        if re.match(r"^agent-[a-z0-9]+$", sanitized):
            return sanitized
        return None

    # 2. Directory Path Fallback
    # Check workspace_dir and all its parent directories (most specific first)
    current = os.path.abspath(get_workspace_dir())
    while True:
        agent_id = _resolve_from_path(current)
        if agent_id:
            return agent_id
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent

    # 3. Default / None Fallback
    return None

def load_antigravity_yml() -> dict:
    """Loads antigravity.yml from workspace directory, falling back to core directory if missing."""
    workspace_path = resolve_workspace_path("antigravity.yml")
    if os.path.exists(workspace_path):
        target_path = workspace_path
    else:
        target_path = resolve_core_path("antigravity.yml")
        
    if not os.path.exists(target_path):
        config = {}
    else:
        with open(target_path, "r") as f:
            config = yaml.safe_load(f) or {}
            
    # Inject resolved agent_id dynamically
    config["agent_id"] = resolve_agent_id()
    return config

