"""
GitHub Graph Skill
==================
A pure, stateless skill for parsing and analyzing the dependency graph 
materialized in GitHub Issue bodies (Meta-Indices).
"""

import re
import subprocess
import json

def fetch_path_data(path_id: str, repository: str = "pltrinh1122/agent-antigravity") -> str:
    """Fetches the issue body for a given Path ID."""
    result = subprocess.run(
        ["gh", "issue", "view", str(path_id), "--repo", repository, "--json", "body"],
        capture_output=True, text=True, check=True
    )
    data = json.loads(result.stdout.strip() or "{}")
    return data.get("body", "")

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
    for line in body.splitlines():
        line = line.strip()
        # Matches: - [x] Node 123: Title
        # Matches: - [ ] Activity 456: Title
        # Matches: - [/] Probe 789: Title
        status_match = re.match(r"-\s+\[([xX /])\]\s+(?:Node|Activity|Probe|Path)?\s*(\d+):?\s*(.*)", line, re.IGNORECASE)
        if status_match:
            status_char = status_match.group(1).lower()
            nid = status_match.group(2)
            title = status_match.group(3).strip()
            
            # Remove trailing dependency annotations from title if present
            title = re.sub(r"\s*\[Depends:.*?\]\s*$", "", title)
            
            depends = []
            dep_match = re.search(r"\[Depends:\s*(.*?)\]", line, re.IGNORECASE)
            if dep_match:
                depends = [d.strip() for d in dep_match.group(1).split(",")]
            
            nodes[nid] = {
                "completed": status_char == "x",
                "depends": depends,
                "title": title
            }
    return nodes

def get_ready_nodes(nodes: dict) -> list[str]:
    """
    Returns a list of Node IDs that are incomplete and whose 
    dependencies are all satisfied (completed).
    """
    incomplete_ids = {nid for nid, data in nodes.items() if not data["completed"]}
    ready_ids = []
    for nid in incomplete_ids:
        deps = nodes[nid]["depends"]
        # A node is ready if none of its dependencies are in the incomplete list
        if not any(dep in incomplete_ids for dep in deps):
            ready_ids.append(nid)
    
    # Sort by numeric ID to ensure deterministic order
    return sorted(ready_ids, key=int)
