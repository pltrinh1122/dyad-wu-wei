import os
import subprocess
import json
import yaml
import tempfile
import argparse
import sys
from drivers import github_client
from drivers.issue_factory import render_template

class BacklogDaemon:
    """Kernel daemon for GitHub Backlog operations."""
    
    def __init__(self, repository: str = "pltrinh1122/dyad-wu-wei"):
        self.repository = repository
        workspace_dir = os.environ.get("SPAO_WORKSPACE_DIR")
        if workspace_dir:
            from drivers.github_client import _resolve_gh_repo
            resolved = _resolve_gh_repo()
            if resolved:
                self.repository = resolved

    def load_node_taxonomy(self) -> dict:
        """Loads the domain-specific node taxonomy from dyad-wu-wei.yml."""
        from drivers import path_resolver
        workspace_path = path_resolver.resolve_workspace_path("dyad-wu-wei.yml")
        if os.path.exists(workspace_path):
            config_path = workspace_path
        else:
            config_path = path_resolver.resolve_core_path("dyad-wu-wei.yml")
            
        if not os.path.exists(config_path):
            return {
                "terminal": ["activity", "discovery"],
                "non_terminal": ["path"]
            }
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config.get("node_taxonomy", {
            "terminal": ["activity", "discovery"],
            "non_terminal": ["path"]
        })

    def list(self, label: str = "backlog") -> dict[str, list[dict]]:
        """Returns open backlog paths grouped by active strategic goals and unmapped paths, with dependencies resolved."""
        import re
        from kernel.daemon_strategic import load_ledger
        
        # 1. Fetch all open issues in a single request
        open_issues = github_client.get_open_issues()
        
        # 2. Path Filtering: isolate issues containing the 'path' label
        path_issues = []
        for issue in open_issues:
            labels = [l.get("name").lower() for l in issue.get("labels", []) if isinstance(l, dict) and "name" in l]
            # Also support string labels if mocked as list of strings
            labels += [l.lower() for l in issue.get("labels", []) if isinstance(l, str)]
            if "path" in labels:
                # Resolve dependencies from issue body
                body = issue.get("body") or ""
                deps = []
                dep_match = re.search(r"## Depends On\s*\n+([^\n#]+)", body, re.IGNORECASE)
                if dep_match:
                    dep_content = dep_match.group(1).strip()
                    if dep_content.upper() != "TBD" and dep_content:
                        deps = re.findall(r"\d+", dep_content)
                issue["dependencies"] = deps
                path_issues.append(issue)
                
        # 3. Load Strategic intent ledger
        ledger = load_ledger()
        goals = ledger.get("strategic_goals", [])
        active_goals = [g for g in goals if g.get("status") == "Active"]
        
        path_by_id = {str(issue["number"]): issue for issue in path_issues}
        mapped_ids = set()
        
        grouped = {}
        # 4. Group by active prioritized goals
        for goal in active_goals:
            goal_id = goal.get("id")
            goal_title = goal.get("title")
            header = f"🎯 [{goal_id}] {goal_title}"
            
            prioritized = goal.get("prioritized_paths", [])
            goal_paths = []
            for p_id in prioritized:
                p_id_str = str(p_id)
                if p_id_str in path_by_id:
                    goal_paths.append(path_by_id[p_id_str])
                    mapped_ids.add(p_id_str)
            grouped[header] = goal_paths
            
        # 5. Group remaining paths under Backlog / Unmapped
        unmapped_paths = []
        for issue in path_issues:
            issue_id_str = str(issue["number"])
            if issue_id_str not in mapped_ids:
                unmapped_paths.append(issue)
        
        grouped["📋 [Backlog / Unmapped]"] = unmapped_paths
        return grouped

    def add(self, node_type: str, title: str, goal: str, path_id: str = None, depends_on: str = None) -> str:
        """Creates a GH issue based on whether the node type maps to a Terminal or Non-Terminal Base Class."""
        node_type_lower = node_type.lower()
        taxonomy = self.load_node_taxonomy()
        
        is_terminal = node_type_lower in taxonomy.get("terminal", [])
        is_non_terminal = node_type_lower in taxonomy.get("non_terminal", [])
        
        if not is_terminal and not is_non_terminal:
            valid_types = taxonomy.get("terminal", []) + taxonomy.get("non_terminal", [])
            raise ValueError(f"Error: Invalid node type '{node_type}'. Must be one of: {', '.join(valid_types)}")
            
        if is_terminal and not path_id:
            raise ValueError("Terminal nodes (Activities and Discoveries) must belong to a parent Path. Please provide a path_id.")
            
        if is_terminal and path_id:
            try:
                path_details = github_client.get_issue_details(path_id)
                if not path_details:
                    raise ValueError(f"Parent Path issue {path_id} does not exist.")
                if path_details.get("state") != "OPEN":
                    raise ValueError(f"Parent Path issue {path_id} is already closed.")
                path_title = path_details.get("title", "")
                if not path_title.lower().startswith("path"):
                    raise ValueError(f"Parent issue {path_id} is not classified as a Path.")
            except ValueError:
                raise
            except Exception:
                pass

        from kernel.title_utils import clean_node_title
        # Strip any accidentally prepended predictive IDs or redundant prefixes from the user title
        cleaned_title = clean_node_title(title)
        formatted_title = f"{node_type.capitalize()}: {cleaned_title}"

        # Idempotency duplicate check
        try:
            open_issues = github_client.get_open_issues()
            for issue in open_issues:
                curr_title = issue.get("title", "")
                clean_curr = clean_node_title(curr_title)
                if clean_curr.lower() == cleaned_title.lower():
                    print(f"Warning: Reusing existing issue for {node_type} '{cleaned_title}'")
                    return f"https://github.com/{self.repository}/issues/{issue['number']}"
        except Exception:
            pass

        if is_non_terminal:
            kwargs = {"goal": goal}
            body = render_template("path_tracker", kwargs)
            issue_url = github_client.create_issue(formatted_title, body)
        else:
            kwargs = {
                "goal": goal,
                "changes": "TBD",
                "pre_requisites": "TBD",
                "post_requisites": "TBD",
                "depends_on": depends_on if depends_on else "TBD"
            }
            body = render_template("backlog_issue", kwargs)
            issue_url = github_client.create_issue(formatted_title, body)
                
        issue_id = issue_url.split("/")[-1]
        
        # Apply labels from node.yml
        try:
            from drivers import path_resolver
            node_yml = path_resolver.load_node_yml()
            status_config = node_yml.get("node_attributes", {}).get("status", {})
            class_config = node_yml.get("node_attributes", {}).get("classification", {})
            
            backlog_label = class_config.get("backlog", "backlog")
            todo_label = status_config.get("todo", "status: todo")
            
            github_client.add_label(issue_id, backlog_label)
            if is_terminal:
                github_client.add_label(issue_id, todo_label)
            if is_non_terminal:
                github_client.add_label(issue_id, "path")
        except Exception:
            github_client.add_label(issue_id, "backlog")
            if is_terminal:
                github_client.add_label(issue_id, "status: todo")
            if is_non_terminal:
                github_client.add_label(issue_id, "path")

        if is_terminal and path_id:
            path_details = github_client.get_issue_details(path_id)
            path_body = path_details.get("body", "")
            
            checkbox_line = f"- [ ] Node {issue_id}: {formatted_title}"
            if depends_on:
                checkbox_line += f" [Depends: {depends_on}]"
                
            if "## Meta-Index" in path_body:
                path_body += f"\n{checkbox_line}"
            else:
                path_body += f"\n\n## Meta-Index\n{checkbox_line}"
                
            github_client.update_issue_body(path_id, path_body)

        # Frontier Auto-Registration
        try:
            from kernel import agent_frontier
            from drivers import path_resolver
            workspace_dir = os.environ.get("SPAO_WORKSPACE_DIR")
            if workspace_dir:
                frontier_file = os.path.join(workspace_dir, "artifacts", "frontier_state.md")
            else:
                frontier_file = path_resolver.resolve_workspace_path("artifacts/frontier_state.md")
            if os.path.exists(frontier_file):
                agent_frontier.register_backlog_node(frontier_file, issue_id, formatted_title, goal)
        except Exception as e:
            print(f"Warning: Failed to auto-register node in frontier: {e}")

        if is_non_terminal:
            # 1. Discovery: Harmonization scoping
            align_url = self.add(
                node_type="discovery",
                title=f"Harmonize - {title}",
                goal=f"Harmonize on the philosophical and technical intent for {title}.",
                path_id=issue_id
            )
            align_id = align_url.split("/")[-1]

            # 2. Discovery: Plan
            plan_url = self.add(
                node_type="discovery",
                title=f"Plan - {title}",
                goal=f"Technical design and proposed changes for {title}.",
                path_id=issue_id,
                depends_on=align_id
            )
            plan_id = plan_url.split("/")[-1]

            # 3. Reflect Node
            self.add(
                node_type="activity",
                title=f"Reflect - {title}",
                goal=f"Final reflection and path closure for {title}.",
                path_id=issue_id,
                depends_on=plan_id
            )
        
        return issue_url

    def view(self, issue_id: str) -> dict:
        """Returns details for a specific issue."""
        return github_client.get_issue_details(issue_id)

    def edit(self, issue_id: str, new_body: str) -> None:
        """Updates an existing issue body."""
        github_client.update_issue_body(issue_id, new_body)

    def check_off_meta_index(self, path_id: str, node_id: str) -> None:
        """Finds the node in the parent Path's Meta-Index and marks it as completed."""
        try:
            data = github_client.get_issue_details(path_id)
            body = data.get("body", "")
            
            import re
            pattern = re.compile(r"-\s+\[\s*\]\s+Node\s+" + str(node_id) + r":", re.IGNORECASE)
            
            if pattern.search(body):
                new_body = pattern.sub(f"- [x] Node {node_id}:", body)
                github_client.update_issue_body(str(path_id), new_body)
        except Exception as e:
            print(f"Warning: Failed to check off Meta-Index for Node {node_id} in Path {path_id}: {e}")

    def uncheck_meta_index(self, path_id: str, node_id: str) -> None:
        """Finds the node in the parent Path's Meta-Index and marks it as uncompleted."""
        try:
            data = github_client.get_issue_details(path_id)
            body = data.get("body", "")
            
            import re
            pattern = re.compile(r"-\s+\[x\]\s+Node\s+" + str(node_id) + r":", re.IGNORECASE)
            
            if pattern.search(body):
                new_body = pattern.sub(f"- [ ] Node {node_id}:", body)
                github_client.update_issue_body(str(path_id), new_body)
        except Exception as e:
            print(f"Warning: Failed to uncheck Meta-Index for Node {node_id} in Path {path_id}: {e}")

from kernel.daemon_telemetry import record_execution

@record_execution(stage="sense")
def main():
    
    parser = argparse.ArgumentParser(description="Antigravity Backlog Daemon")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    
    # list
    parser_list = subparsers.add_parser("list", help="List backlog items")
    parser_list.add_argument("--label", default="backlog", help="Label to filter by")
    
    # new
    parser_new = subparsers.add_parser("new", help="Add a new item to the backlog")
    parser_new.add_argument("type", help="Node type (path, activity, discovery)")
    parser_new.add_argument("title", help="Issue title")
    parser_new.add_argument("goal", help="Issue goal")
    parser_new.add_argument("--path", help="Parent Path ID (required for terminal nodes)")
    parser_new.add_argument("--depends", help="Comma-separated list of dependent Issue IDs")
    
    # view
    parser_view = subparsers.add_parser("view", help="View a backlog item")
    parser_view.add_argument("issue_id", help="Issue ID to view")
    
    # edit
    parser_edit = subparsers.add_parser("edit", help="Edit a backlog item body")
    parser_edit.add_argument("issue_id", help="Issue ID to edit")
    parser_edit.add_argument("new_body", help="New body content")
    
    args = parser.parse_args()
    daemon = BacklogDaemon()
    
    if args.subcommand == "list":
        grouped_data = daemon.list(args.label)
        has_paths = any(len(paths) > 0 for paths in grouped_data.values())
        if has_paths:
            print()
            for header, paths in grouped_data.items():
                print(header)
                for path in paths:
                    dep_str = ""
                    if path.get("dependencies"):
                        dep_str = f" [Depends: {', '.join(path['dependencies'])}]"
                    print(f"  {path['title']}{dep_str}")
                print()
        else:
            print("Backlog is empty.")
            
    elif args.subcommand == "new":
        try:
            url = daemon.add(args.type, args.title, args.goal, path_id=args.path, depends_on=args.depends)
            print(url)
        except Exception as e:
            print(str(e))
            sys.exit(1)
            
    elif args.subcommand == "view":
        data = daemon.view(args.issue_id)
        print('='*40)
        state = data.get('state', 'UNKNOWN')
        print(f"Issue #{args.issue_id}: {data['title']} [{state}]")
        print('='*40)
        print(data['body'])
        print('='*40)
        
    elif args.subcommand == "edit":
        daemon.edit(args.issue_id, args.new_body)

if __name__ == "__main__":
    main()
