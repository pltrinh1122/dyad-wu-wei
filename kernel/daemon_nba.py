import os
import json
import subprocess
from drivers import github_client
from kernel import agent_frontier
from drivers import gh_graph_skill

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
        from drivers import path_resolver
        if not os.path.isabs(frontier_file):
            frontier_file = path_resolver.resolve_workspace_path(frontier_file)
        active_path_str = agent_frontier.read_active_path(frontier_file)
        active_id = None
        if active_path_str:
            active_id = agent_frontier.extract_path_id(active_path_str)
            
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
            
            # Reorder backlog_items based on active strategic goals
            prioritized_ids = []
            from kernel import daemon_strategic
            yaml_path = daemon_strategic.get_ledger_path()
            if os.path.exists(yaml_path):
                import yaml
                try:
                    with open(yaml_path, "r") as f:
                        data = yaml.safe_load(f) or {}
                    goals = data.get("strategic_goals", [])
                    for goal in goals:
                        if goal.get("status") == "Active":
                            prioritized_ids.extend([str(pid) for pid in goal.get("prioritized_paths", [])])
                except Exception as e:
                    print(f"Warning: Failed to load/parse strategic intent ledger: {e}")
            
            if prioritized_ids:
                prioritized_set = set(prioritized_ids)
                matched_items = []
                unmatched_items = []
                for item in backlog_items:
                    num_str = str(item.get("number", ""))
                    if num_str in prioritized_set:
                        matched_items.append(item)
                    else:
                        unmatched_items.append(item)
                
                matched_items.sort(key=lambda x: prioritized_ids.index(str(x.get("number", ""))))
                backlog_items = matched_items + unmatched_items

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
