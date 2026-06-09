import os
import json
import subprocess
from drivers import github_client
from kernel import agent_frontier
from drivers import gh_graph_skill

class NBADaemon:
    """Manages the Next-Best-Action (NBA) orchestration logic."""
    
    def __init__(self, repository: str = None):
        self.repository = repository
        
    def evaluate(self, frontier_file: str, local_mode: bool = False) -> dict:
        """Evaluates the current state and returns the Next-Best-Action recommendations.
        
        Logic:
        1. Try to find the Current Active Path from the frontier.
        2. If active path exists, check its Meta-Index for pending children.
        3. If pending children found -> Path Continuation.
        4. If no active path OR no pending children -> Path Switching (Global Backlog).
        """
        import re
        from drivers import path_resolver
        if not os.path.isabs(frontier_file):
            frontier_file = path_resolver.resolve_workspace_path(frontier_file)
        active_path_str = agent_frontier.read_active_path(frontier_file)
        active_id = None
        if active_path_str:
            active_id = agent_frontier.extract_path_id(active_path_str)
            
        if active_id:
            if local_mode:
                # Local-First Path Continuation
                try:
                    state = agent_frontier.load_state(frontier_file)
                    
                    # Clean active path string to get core title
                    core_title = active_path_str.strip("*")
                    while True:
                        prev = core_title
                        core_title = re.sub(r"^(Node|Path|Discovery|Activity|Act|Harmonize|Plan|Reflect)\s*\d*:\s*", "", core_title, flags=re.IGNORECASE)
                        core_title = re.sub(r"^(Node|Path|Discovery|Activity|Act|Harmonize|Plan|Reflect)\s*\d*\s*-\s*", "", core_title, flags=re.IGNORECASE)
                        core_title = core_title.strip()
                        if core_title == prev:
                            break
                    
                    # Find child nodes in state
                    child_candidates = []
                    for n in state.get("nodes", []):
                        n_name = n.get("name", "")
                        if core_title in n_name and f"Path {active_id}" not in n_name:
                            # Reconstruct item
                            match = re.search(r"(?:Node |#)(\d+)", n_name)
                            if match:
                                issue_num = int(match.group(1))
                                title = n_name.split(":", 1)[1].strip()
                                child_candidates.append({
                                    "number": issue_num,
                                    "id": str(issue_num),
                                    "title": title,
                                    "status": n.get("status", "")
                                })
                    
                    # Group by subtype and status
                    harmonize_nodes = [n for n in child_candidates if "Harmonize" in n["title"]]
                    plan_nodes = [n for n in child_candidates if "Plan" in n["title"]]
                    reflect_nodes = [n for n in child_candidates if "Reflect" in n["title"]]
                    other_nodes = [n for n in child_candidates if n not in harmonize_nodes + plan_nodes + reflect_nodes]
                    
                    next_nodes = []
                    
                    # Lifecycle sequence: Harmonize -> Plan -> Others -> Reflect
                    uncompleted_harmonize = [n for n in harmonize_nodes if n["status"] != "Completed"]
                    uncompleted_plan = [n for n in plan_nodes if n["status"] != "Completed"]
                    uncompleted_others = [n for n in other_nodes if n["status"] != "Completed"]
                    uncompleted_reflect = [n for n in reflect_nodes if n["status"] != "Completed"]
                    
                    if uncompleted_harmonize:
                        next_nodes = uncompleted_harmonize
                    elif uncompleted_plan:
                        next_nodes = uncompleted_plan
                    elif uncompleted_others:
                        next_nodes = uncompleted_others
                    elif uncompleted_reflect:
                        next_nodes = uncompleted_reflect
                    
                    if next_nodes:
                        recs = [{"number": n["number"], "id": n["id"], "title": n["title"]} for n in next_nodes]
                        return {
                            "type": "path_continuation",
                            "path_id": active_id,
                            "path_title": active_path_str,
                            "recommendations": recs
                        }
                except Exception as e:
                    print(f"Warning: Failed to evaluate active Path {active_id} locally: {e}")
            else:
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
            if local_mode:
                state = agent_frontier.load_state(frontier_file)
                all_nodes = state.get("nodes", [])
                backlog_items = []
                
                active_ids = set()
                for n in all_nodes:
                    if n.get("status") not in ("Completed", "Backlog"):
                        match = re.search(r"(?:Node |#)(\d+)", n.get("name", ""))
                        if match:
                            active_ids.add(str(match.group(1)))

                from drivers import path_resolver
                import yaml
                repo_root = path_resolver.get_workspace_dir()
                global_backlog_path = os.path.join(repo_root, "artifacts", "global_backlog.yml")
                
                if os.path.exists(global_backlog_path):
                    with open(global_backlog_path, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f) or {}
                    backlog_items = data.get("backlog_items", [])
                
                for item in backlog_items:
                    item_id = str(item.get("number", ""))
                    if item_id in active_ids:
                        raise Exception(f"[CYBERNETIC STEERING VECTOR] Mutually Exclusive Residence Violation: Issue {item_id} is active but still exists in the global backlog cache. Purge it from global_backlog.yml.")
            else:
                backlog_items = github_client.list_issues_by_label("backlog")
                backlog_items = [item for item in backlog_items if "path" not in item.get("labels", [])]
            
            backlog_items.sort(key=lambda x: x.get("number", 0))
            
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
                # Filter prioritized paths to only include those with open
                # GitHub issues. Closed path issues = completed paths.
                try:
                    open_path_issues = github_client.list_issues_by_label("path")
                    open_path_ids = {str(i.get("number", "")) for i in open_path_issues}
                    prioritized_ids = [pid for pid in prioritized_ids if pid in open_path_ids]
                except Exception:
                    pass  # If API fails, proceed with unfiltered list
                
                # Build child_to_path map from open Path issues
                child_to_path = {}
                try:
                    import re
                    for p in open_path_issues:
                        pid = str(p.get("number", ""))
                        body = p.get("body", "")
                        # Support both `- [ ] Node 1914` and `- [ ] #1914` formats
                        matches = re.findall(r"-\s+\[\s*[xX ]?\s*\]\s+(?:(?:Node|Activity|Discovery)\s+|#)(\d+)\b", body, re.IGNORECASE)
                        for m in matches:
                            child_to_path[m] = pid
                except Exception:
                    pass

                prioritized_set = set(prioritized_ids)
                matched_items = []
                unmatched_items = []
                
                for item in backlog_items:
                    num_str = str(item.get("number", ""))
                    parent_id = child_to_path.get(num_str, "")
                    
                    if parent_id in prioritized_set:
                        matched_items.append((prioritized_ids.index(parent_id), item))
                    elif parent_id != "":
                        unmatched_items.append(item)
                    else:
                        unmatched_items.append(item)
                
                matched_items.sort(key=lambda x: (x[0], x[1].get("number", 0)))
                matched_items = [x[1] for x in matched_items]
                unmatched_items.sort(key=lambda x: x.get("number", 0))
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
