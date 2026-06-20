"""
GitHub Graph Skill
==================
A pure, stateless skill for parsing and analyzing the dependency graph 
materialized in GitHub Issue bodies (Meta-Indices).
"""

import re
import subprocess
import json

class DAGValidationError(Exception):
    """Raised when dependency graph validation fails."""
    pass

def fetch_path_data(path_id: str, repository: str = "pltrinh1122/dyad-wu-wei") -> str:
    """Fetches the issue body for a given Path ID."""
    result = subprocess.run(
        ["gh", "issue", "view", str(path_id), "--repo", repository, "--json", "body"],
        capture_output=True, text=True, check=True
    )
    data = json.loads(result.stdout.strip() or "{}")
    return data.get("body", "")

def validate_dag(nodes: dict) -> None:
    """
    Validates a dependency graph for referential integrity, self-dependency, 
    and acyclicity (cycle detection).
    
    Raises:
      DAGValidationError
    """
    for u, data in nodes.items():
        for v in data["depends"]:
            if v not in nodes:
                raise DAGValidationError(f"Referential Integrity Violation: Node {u} depends on non-existent Node {v}")
            if u == v:
                raise DAGValidationError(f"Self-Dependency Violation: Node {u} cannot depend on itself")
                
    # Cycle detection via DFS
    state = {}  # 0: unvisited, 1: visiting, 2: visited
    parent = {}
    
    def dfs(u):
        state[u] = 1  # visiting
        for v in nodes[u]["depends"]:
            if state.get(v, 0) == 1:
                # Cycle detected. Reconstruct path.
                cycle = [v]
                curr = u
                while curr != v:
                    cycle.append(curr)
                    curr = parent[curr]
                cycle.append(v)
                cycle.reverse()
                path_str = " -> ".join(cycle)
                raise DAGValidationError(f"Cycle Detected: {path_str}")
            elif state.get(v, 0) == 0:
                parent[v] = u
                dfs(v)
        state[u] = 2  # visited

    for node in nodes:
        if state.get(node, 0) == 0:
            dfs(node)

def parse_meta_index(body: str) -> dict:
    """
    Parses a markdown Meta-Index into a dependency graph.
    
    Returns a dict mapping Node ID (str) to:
      {
        "completed": bool,
        "depends": list[str],
        "title": str
      }
    """
    nodes = {}
    # Handle both real newlines and literal \n characters that might appear from JSON parsing
    body = body.replace("\\n", "\n")
    
    # Pre-process to merge wrapped lines. If a line doesn't start with '- [', it's likely a continuation.
    merged_lines = []
    for line in body.splitlines():
        if re.match(r'^\s*-\s+\[', line):
            merged_lines.append(line)
        elif merged_lines and line.strip():
            merged_lines[-1] = merged_lines[-1] + " " + line.strip()
            
    pattern = re.compile(
        r"^\s*-\s+\[([xX /])\]\s+(?:Node|Activity|Discovery|Path|#)?\s*(\d+):?\s*(.*?)(?:\s*\[Depends:\s*(.*?)\s*\])?\s*$",
        re.IGNORECASE
    )
    
    for line in merged_lines:
        line_stripped = line.strip()
        match = pattern.match(line_stripped)
        if match:
            status_char = match.group(1).lower()
            nid = match.group(2)
            title = match.group(3).strip()
            dep_str = match.group(4)
            
            depends = []
            if dep_str is not None:
                # Split and clean whitespace
                depends = [d.strip() for d in dep_str.split(",") if d.strip()]
                
            nodes[nid] = {
                "completed": status_char == "x",
                "in_progress": status_char == "/",
                "depends": depends,
                "title": title
            }
            
    # Validate the graph before returning
    validate_dag(nodes)
    return nodes

def get_ready_nodes(nodes: dict) -> list[str]:
    """
    Returns a list of Node IDs that are incomplete and whose 
    dependencies are all satisfied (completed).
    """
    incomplete_ids = {nid for nid, data in nodes.items() if not data["completed"]}
    
    # --- DIRECT GITHUB API STATE CHECKS ---
    # To fix orphan path generation, if a node is incomplete in markdown,
    # we verify its actual state via the GitHub API.
    from drivers import github_client
    actually_completed = set()
    for nid in list(incomplete_ids):
        try:
            details = github_client.get_issue_details(nid)
            if details.get("state", "").upper() == "CLOSED":
                actually_completed.add(nid)
                nodes[nid]["completed"] = True
                nodes[nid]["in_progress"] = False
        except Exception:
            pass
            
    incomplete_ids = incomplete_ids - actually_completed
    # ----------------------------------------
    
    ready_ids = []
    for nid in incomplete_ids:
        deps = nodes[nid]["depends"]
        
        # Terminal Reflect Invariant
        if "reflect" in nodes[nid].get("title", "").lower() and len(incomplete_ids) > 1:
            continue
            
        # A node is ready if none of its dependencies are in the incomplete list AND the node itself is not in-progress
        if not any(dep in incomplete_ids for dep in deps) and not nodes[nid].get("in_progress", False):
            ready_ids.append(nid)
    
    # Sort by numeric ID to ensure deterministic order
    return sorted(ready_ids, key=int)

def get_next_nodes(body: str) -> list[dict]:
    """
    High-level primitive that parses a Meta-Index and returns 
    the full details of the next unblocked nodes.
    """
    nodes = parse_meta_index(body)
    ready_ids = get_ready_nodes(nodes)
    
    return [
        {"id": nid, "title": nodes[nid]["title"]}
        for nid in ready_ids
    ]
