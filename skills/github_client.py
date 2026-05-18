import subprocess
import tempfile
from skills.issue_factory import render_template

def create_issue(title: str, body: str) -> str:
    """Creates a GH issue safely using a temp file for the body."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=True) as temp_file:
        temp_file.write(body)
        temp_file.flush()
        
        result = subprocess.run(
            ["gh", "issue", "create", "--title", title, "-F", temp_file.name],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()

def close_issue(issue_id: str, comment_body: str) -> None:
    """Closes a GH issue with a final comment."""
    subprocess.run(
        ["gh", "issue", "close", str(issue_id), "-c", comment_body],
        check=True
    )

def update_issue_body(issue_id: str, new_body: str) -> None:
    """Updates an existing issue body using a temp file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=True) as temp_file:
        temp_file.write(new_body)
        temp_file.flush()
        
        subprocess.run(
            ["gh", "issue", "edit", str(issue_id), "--body-file", temp_file.name],
            check=True
        )

def create_pull_request(title: str, body: str) -> str:
    """Creates a Pull Request safely using a temp file for the body."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=True) as temp_file:
        temp_file.write(body)
        temp_file.flush()
        
        result = subprocess.run(
            ["gh", "pr", "create", "--title", title, "-F", temp_file.name],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()

def list_issues_by_label(label: str) -> list[dict]:
    """Returns a list of open issues matching the given label.
    
    Each item is a dict with 'number', 'title', and 'url' keys.
    Returns an empty list if no issues are found.
    """
    result = subprocess.run(
        ["gh", "issue", "list", "--label", label, "--state", "open",
         "--json", "number,title,url"],
        capture_output=True, text=True, check=True
    )
    import json
    issues = json.loads(result.stdout.strip() or "[]")
    
    valid_issues = []
    for issue in issues:
        view_res = subprocess.run(
            ["gh", "issue", "view", str(issue["number"]), "--json", "state"],
            capture_output=True, text=True, check=True
        )
        state_data = json.loads(view_res.stdout.strip() or "{}")
        if state_data.get("state") == "OPEN":
            valid_issues.append(issue)
            
    return valid_issues

def rename_issue_title(issue_id: str, new_title: str) -> None:
    """Renames an existing GH issue's title."""
    subprocess.run(
        ["gh", "issue", "edit", str(issue_id), "--title", new_title],
        check=True
    )

import yaml
import os

def load_node_taxonomy() -> dict:
    """Loads the domain-specific node taxonomy from antigravity.yml."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "antigravity.yml")
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

def add_to_backlog(node_type: str, title: str, goal: str) -> str:
    """Creates a GH issue based on whether the node type maps to a Terminal or Non-Terminal Base Class.
    
    Returns the URL of the created issue.
    """
    node_type_lower = node_type.lower()
    taxonomy = load_node_taxonomy()
    
    is_terminal = node_type_lower in taxonomy.get("terminal", [])
    is_non_terminal = node_type_lower in taxonomy.get("non_terminal", [])
    
    if not is_terminal and not is_non_terminal:
        valid_types = taxonomy.get("terminal", []) + taxonomy.get("non_terminal", [])
        raise ValueError(f"Error: Invalid node type '{node_type}'. Must be one of: {', '.join(valid_types)}")
        
    formatted_title = f"{node_type.capitalize()}: {title}"
    if is_non_terminal:
        kwargs = {"goal": goal}
        body = render_template("path_tracker", kwargs)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=True) as temp_file:
            temp_file.write(body)
            temp_file.flush()
            
            result = subprocess.run(
                ["gh", "issue", "create", "--title", formatted_title, "-F", temp_file.name],
                capture_output=True, text=True, check=True
            )
    else:
        kwargs = {
            "goal": goal,
            "changes": "TBD",
            "invariants": "TBD",
            "depends_on": "TBD"
        }
        body = render_template("backlog_issue", kwargs)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=True) as temp_file:
            temp_file.write(body)
            temp_file.flush()
            
            result = subprocess.run(
                ["gh", "issue", "create", "--title", formatted_title,
                 "-F", temp_file.name, "--label", "backlog"],
                capture_output=True, text=True, check=True
            )
            
    issue_url = result.stdout.strip()
    issue_id = issue_url.split("/")[-1]
    new_title = f"{node_type.capitalize()} {issue_id}: {title}"
    rename_issue_title(issue_id, new_title)
    
    return issue_url

def create_pull_request(title: str, body: str) -> str:
    """Creates a PR using gh pr create."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=True) as temp_file:
        temp_file.write(body)
        temp_file.flush()
        
        result = subprocess.run(
            ["gh", "pr", "create", "--title", title, "-F", temp_file.name],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()

def get_issue_labels(issue_id: str) -> list[str]:
    """Returns a list of label names for the given issue."""
    result = subprocess.run(
        ["gh", "issue", "view", str(issue_id), "--json", "labels"],
        capture_output=True, text=True, check=True
    )
    import json
    data = json.loads(result.stdout.strip() or "{}")
    labels = data.get("labels", [])
    return [label.get("name") for label in labels]

def add_label(issue_id: str, label: str) -> None:
    """Adds a label to the given issue."""
    try:
        subprocess.run(
            ["gh", "issue", "edit", str(issue_id), "--add-label", label],
            check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as e:
        if "not found" in e.stderr:
            subprocess.run(["gh", "label", "create", label, "--force"], check=True, capture_output=True)
            subprocess.run(
                ["gh", "issue", "edit", str(issue_id), "--add-label", label],
                check=True, capture_output=True
            )
        else:
            raise e

def remove_label(issue_id: str, label: str) -> None:
    """Removes a label from the given issue."""
    subprocess.run(
        ["gh", "issue", "edit", str(issue_id), "--remove-label", label],
        check=True
    )

def get_open_prs() -> list[dict]:
    """Returns a list of currently open PRs for the repository."""
    result = subprocess.run(
        ["gh", "pr", "list", "--state", "open", "--json", "number,title,headRefName,url"],
        capture_output=True, text=True, check=True
    )
    import json
    return json.loads(result.stdout.strip() or "[]")
