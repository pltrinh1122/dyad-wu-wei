import re
from drivers.file_locker import lock_file
from kernel.daemon_telemetry import record_execution

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



def read_last_completed_node(filepath: str) -> str:
    """Reads the most recently completed node (via agent_frontier)."""
    from kernel import agent_frontier
    return agent_frontier.read_last_completed_node(filepath)

def read_active_path(filepath: str) -> str | None:
    """Reads the current active path (via agent_frontier)."""
    from kernel import agent_frontier
    return agent_frontier.read_active_path(filepath)



@record_execution(stage="skill")
def set_active_path(filepath: str, path_name: str) -> None:
    """Updates the active path (via agent_frontier)."""
    from kernel import agent_frontier
    agent_frontier.set_active_path(filepath, path_name)

