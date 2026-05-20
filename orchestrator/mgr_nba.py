import os
import json
import subprocess
from skills import github_client
from orchestrator import mgr_frontier
from skills import gh_graph_skill

class NBAManager:
    """Manages the Next-Best-Action (NBA) orchestration logic."""
    
    def __init__(self, repository: str = None):
        self.repository = repository
        
    def evaluate(self, frontier_file: str) -> dict:
        """Evaluates the current state and returns the Next-Best-Action recommendations.
        
        Logic:
        1. Try to find the Current Active Path from the frontier.
        2. If active path exists, check its Meta-Index for pending children.
        3. If pending children found -> Path Continuation.
        4. If no active path OR no pending children -> Path Switching (Global Backlog).
        """
        from skills import path_resolver
        if not os.path.isabs(frontier_file):
            frontier_file = path_resolver.resolve_workspace_path(frontier_file)
        active_path_str = mgr_frontier.read_active_path(frontier_file)
        active_id = None
        if active_path_str:
            active_id = mgr_frontier.extract_path_id(active_path_str)
            
        if active_id:
            # Tier 1: Path Continuation
            try:
                path_details = github_client.get_issue_details(active_id)
                path_body = path_details.get("body", "")
                
                next_nodes = gh_graph_skill.get_next_nodes(path_body)
                if next_nodes:
                    return {
                        "type": "path_continuation",
                        "path_id": active_id,
                        "path_title": path_details.get("title", f"Path {active_id}"),
                        "recommendations": next_nodes
                    }
            except Exception as e:
                # Log error and fallback to Path Switching
                print(f"Warning: Failed to evaluate active Path {active_id}: {e}")
                
        # Tier 2: Path Switching / Global Backlog
        try:
            backlog_items = github_client.list_issues_by_label("backlog")
            # Filter out non-terminal nodes (Paths) from global recommendation? 
            # Or include them as "Switch to Path"?
            # For now, include all as recommendations.
            return {
                "type": "path_switching",
                "recommendations": backlog_items[:5] # Limit to top 5
            }
        except Exception as e:
            print(f"Error: Failed to fetch global backlog: {e}")
            return {
                "type": "error",
                "message": str(e)
            }
