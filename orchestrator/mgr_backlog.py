import os
import subprocess
import json
import yaml
import tempfile
from skills import github_client
from skills.issue_factory import render_template

class BacklogManager:
    """Orchestrator for GitHub Backlog operations."""
    
    def __init__(self, repository: str = "pltrinh1122/agent-antigravity"):
        self.repository = repository

    def load_node_taxonomy(self) -> dict:
        """Loads the domain-specific node taxonomy from antigravity.yml."""
        config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "antigravity.yml")
        if not os.path.exists(config_path):
            return {
                "terminal": ["activity", "probe"],
                "non_terminal": ["path"]
            }
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        return config.get("node_taxonomy", {
            "terminal": ["activity", "probe"],
            "non_terminal": ["path"]
        })

    def list(self, label: str = "backlog") -> list[dict]:
        """Returns a list of open issues matching the given label, verified via strong consistency."""
        issues = github_client.list_issues_by_label(label)
        return issues

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
            raise ValueError("Terminal nodes (Activities and Probes) must belong to a parent Path. Please provide a path_id.")
            
        formatted_title = f"{node_type.capitalize()}: {title}"
        if is_non_terminal:
            kwargs = {"goal": goal}
            body = render_template("path_tracker", kwargs)
            issue_url = github_client.create_issue(formatted_title, body)
            github_client.add_label(issue_url.split("/")[-1], "backlog")
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
            github_client.add_label(issue_url.split("/")[-1], "backlog")
                
        issue_id = issue_url.split("/")[-1]
        new_title = f"{node_type.capitalize()} {issue_id}: {title}"
        github_client.rename_issue_title(issue_id, new_title)
        
        if is_terminal and path_id:
            path_details = github_client.get_issue_details(path_id)
            path_body = path_details.get("body", "")
            
            checkbox_line = f"- [ ] Node {issue_id}: {new_title}"
            if depends_on:
                checkbox_line += f" [Depends: {depends_on}]"
                
            if "## Meta-Index" in path_body:
                path_body += f"\n{checkbox_line}"
            else:
                path_body += f"\n\n## Meta-Index\n{checkbox_line}"
                
            github_client.update_issue_body(path_id, path_body)
        
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

def main():
    import argparse
    import sys
    
    parser = argparse.ArgumentParser(description="Antigravity Backlog Manager")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    
    # list
    parser_list = subparsers.add_parser("list", help="List backlog items")
    parser_list.add_argument("--label", default="backlog", help="Label to filter by")
    
    # new
    parser_new = subparsers.add_parser("new", help="Add a new item to the backlog")
    parser_new.add_argument("type", help="Node type (path, activity, probe)")
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
    manager = BacklogManager()
    
    if args.subcommand == "list":
        items = manager.list(args.label)
        if items:
            print(f"\n📋 Backlog ({len(items)} item(s) pending):")
            for item in items:
                print(f"  {item['title']}")
            print()
        else:
            print("Backlog is empty.")
            
    elif args.subcommand == "new":
        try:
            url = manager.add(args.type, args.title, args.goal, path_id=args.path, depends_on=args.depends)
            print(url)
        except Exception as e:
            print(str(e))
            sys.exit(1)
            
    elif args.subcommand == "view":
        data = manager.view(args.issue_id)
        print('='*40)
        print(f"Issue #{args.issue_id}: {data['title']} [OPEN]")
        print('='*40)
        print(data['body'])
        print('='*40)
        
    elif args.subcommand == "edit":
        manager.edit(args.issue_id, args.new_body)

if __name__ == "__main__":
    main()
