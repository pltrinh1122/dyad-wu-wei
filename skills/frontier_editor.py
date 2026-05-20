import re
from skills.file_locker import lock_file
from orchestrator.mgr_telemetry import record_execution

def extract_path_id(path_str: str) -> str | None:
    """
    Extracts the numeric ID from a Path string.
    Supports formats like:
      - Path 181: Title
      - Title (#181)
      - 181
    """
    if not path_str:
        return None
    # Matches "Path 181:"
    match = re.search(r"Path (\d+):", path_str, re.IGNORECASE)
    if match:
        return match.group(1)
    # Matches "(#181)"
    match = re.search(r"\(#(\d+)\)", path_str)
    if match:
        return match.group(1)
    # Matches raw number
    match = re.match(r"^(\d+)$", path_str.strip())
    if match:
        return match.group(1)
    return None

def read_active_node(filepath: str) -> str:
    """Reads the current active node from the frontier state (via mgr_frontier)."""
    from orchestrator import mgr_frontier
    return mgr_frontier.read_active_node(filepath)

def read_last_completed_node(filepath: str) -> str:
    """Reads the most recently completed node (via mgr_frontier)."""
    from orchestrator import mgr_frontier
    return mgr_frontier.read_last_completed_node(filepath)

def read_active_path(filepath: str) -> str | None:
    """Reads the current active path (via mgr_frontier)."""
    from orchestrator import mgr_frontier
    return mgr_frontier.read_active_path(filepath)

@record_execution(stage="skill")
def complete_active_node(filepath: str, node_name: str, learnings: str, invariants: list[str], clear_pointers: bool = True) -> None:
    """Appends the completed node block (via mgr_frontier)."""
    from orchestrator import mgr_frontier
    mgr_frontier.complete_active_node(filepath, node_name, learnings, invariants, clear_pointers)

def set_active_node(filepath: str, node_name: str) -> None:
    """Updates the active node (via mgr_frontier)."""
    from orchestrator import mgr_frontier
    mgr_frontier.set_active_node(filepath, node_name)

@record_execution(stage="skill")
def set_active_path(filepath: str, path_name: str) -> None:
    """Updates the active path (via mgr_frontier)."""
    from orchestrator import mgr_frontier
    mgr_frontier.set_active_path(filepath, path_name)

def append_active_node(filepath: str, node_id: int, node_title: str, description: str, invariants: list[str]) -> None:
    """Appends a new active node block (via mgr_frontier)."""
    from orchestrator import mgr_frontier
    mgr_frontier.append_active_node(filepath, node_id, node_title, description, invariants)
