import os
import yaml
import re
from drivers import github_client
from drivers import path_resolver
from kernel import agent_frontier
from kernel import daemon_strategic

class NBADaemon:
    """Manages the Next-Best-Rub (NBR) orchestration logic."""
    
    def __init__(self, repository: str = None):
        self.repository = repository
        
    def evaluate(self, frontier_file: str, local_mode: bool = False) -> dict:
        """Evaluates the current state and returns the Next-Best-Rub (NBR) recommendations.
        
        Logic:
        1. Fetch all issues labeled 'status: todo' (Staging Area).
        2. Score them against active strategic goals in strategic_intent.yml.
        3. Return the top 5 issues as recommendations.
        """
        locked_node_ids = set()
        try:
            if not os.path.isabs(frontier_file):
                frontier_file = path_resolver.resolve_workspace_path(frontier_file)
            state = agent_frontier.load_state(frontier_file)
            agents = state.get("active_agents", {})
            for agent_name, agent_data in agents.items():
                active_node = agent_data.get("current_active_node")
                if active_node:
                    match = re.search(r"(?:Node |#)(\d+)", active_node)
                    if match:
                        locked_node_ids.add(str(match.group(1)))
        except Exception:
            pass

        try:
            if local_mode:
                staging_items = []
            else:
                staging_items = github_client.list_issues_by_label("status: todo")
                if not staging_items:
                    staging_items = github_client.list_issues_by_label("staging")

            # Filter out locked items
            staging_items = [i for i in staging_items if str(i.get("number", "")) not in locked_node_ids]

            # Read strategic goals
            active_keywords = []
            yaml_path = daemon_strategic.get_ledger_path()
            if os.path.exists(yaml_path):
                with open(yaml_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                goals = data.get("strategic_goals", [])
                for goal in goals:
                    if goal.get("status") == "Active":
                        text = (goal.get("title", "") + " " + goal.get("collaborative_gap", "")).lower()
                        words = re.findall(r'\b\w{4,}\b', text)
                        active_keywords.extend(words)
            
            keyword_set = set(active_keywords)

            def score_issue(item):
                score = 0
                text = (item.get("title", "") + " " + item.get("body", "")).lower()
                words = re.findall(r'\b\w{4,}\b', text)
                for w in words:
                    if w in keyword_set:
                        score += 1
                return score

            scored_items = []
            for item in staging_items:
                scored_items.append((score_issue(item), item))

            scored_items.sort(key=lambda x: (-x[0], x[1].get("number", 0)))
            
            top_items = [x[1] for x in scored_items[:5]]

            return {
                "type": "next_best_rub",
                "recommendations": top_items
            }

        except Exception as e:
            print(f"Error: Failed to evaluate Next-Best-Rub: {e}")
            return {
                "type": "error",
                "message": str(e)
            }
