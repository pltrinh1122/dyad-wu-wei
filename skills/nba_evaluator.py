"""
NBA Evaluator Skill
===================
A pure, stateless skill that determines the Next-Best-Action (NBA) for the operator.

Two-tier logic:
  1. Current Path Continuation: If a Path is active in frontier_state.md, look for
     pending backlog issues linked to that Path and recommend the next Activity within it.
  2. Path Switching: If the current Path has no pending work, fall back to the global
     backlog and surface the highest-priority item across all pending nodes.
"""

import os
import re
import subprocess
from skills import gh_graph_skill


def _get_frontier_path(frontier_file: str | None = None) -> str:
    if frontier_file:
        return frontier_file
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(repo_dir, "artifacts", "frontier_state.md")


def get_active_path(frontier_file: str | None = None) -> str | None:
    """
    Reads frontier_state.md to determine the active Path node (non-terminal).
    Returns the Path title string if found, else None.
    """
    from skills.frontier_editor import read_active_path
    path = _get_frontier_path(frontier_file)
    active_path = read_active_path(path)
    if active_path and re.match(r"^Path \d+:", active_path, re.IGNORECASE):
        return active_path
    return None


def get_backlog_items(repository: str) -> list[dict]:
    """
    Queries GitHub for issues with the 'backlog' label from the given repository.
    Returns a list of dicts with 'number', 'title', 'url'.
    """
    result = subprocess.run(
        ["gh", "issue", "list",
         "--repo", repository,
         "--label", "backlog",
         "--json", "number,title,url",
         "--limit", "100"],
        capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        return []
    import json
    try:
        return json.loads(result.stdout.strip())
    except (json.JSONDecodeError, ValueError):
        return []


def evaluate(repository: str, frontier_file: str | None = None) -> dict:
    """
    Runs the two-tier NBA evaluation.

    Returns a dict:
      {
        "mode": "path_continuation" | "path_switching",
        "active_path": str | None,
        "recommended": list[dict],   # ordered list of {'number', 'title', 'url'}
        "message": str
      }
    """
    active_path = get_active_path(frontier_file)
    backlog = get_backlog_items(repository)

    if active_path:
        # Extract numeric ID from active path, e.g. "Path 181: Configurable Sense Hooks" -> 181
        path_number_match = re.search(r"Path (\d+):", active_path, re.IGNORECASE)
        path_number = int(path_number_match.group(1)) if path_number_match else None

        related = []
        if path_number:
            try:
                body = gh_graph_skill.fetch_path_data(path_number, repository)
                nodes = gh_graph_skill.parse_meta_index(body)
                ready_ids = gh_graph_skill.get_ready_nodes(nodes)
                
                for item in backlog:
                    item_num = str(item.get("number", ""))
                    if item_num in ready_ids:
                        related.append(item)
            except Exception:
                pass

        if related:
            return {
                "mode": "path_continuation",
                "active_path": active_path,
                "recommended": related[:3],
                "message": f"Continuing active {active_path}\n\n\033[1;31m🛑 SENSE PHASE COMPLETE. \033[0m\n\033[1;33mTHE SENSE-GATE INVARIANT IS ACTIVE.\nYOU MUST HALT EXECUTION AND AWAIT EXPLICIT OPERATOR APPROVAL BEFORE CALLING plan-start.\033[0m"
            }

    # Path Switching fallback: surface top backlog items globally
    return {
        "mode": "path_switching",
        "active_path": active_path,
        "recommended": backlog[:3],
        "message": "No pending work in current Path. Recommending next best from global backlog.\n\n\033[1;31m🛑 SENSE PHASE COMPLETE. \033[0m\n\033[1;33mTHE SENSE-GATE INVARIANT IS ACTIVE.\nYOU MUST HALT EXECUTION AND AWAIT EXPLICIT OPERATOR APPROVAL BEFORE CALLING plan-start.\033[0m"
    }
