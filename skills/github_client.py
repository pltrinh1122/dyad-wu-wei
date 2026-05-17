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
    return json.loads(result.stdout.strip() or "[]")

def rename_issue_title(issue_id: str, new_title: str) -> None:
    """Renames an existing GH issue's title."""
    subprocess.run(
        ["gh", "issue", "edit", str(issue_id), "--title", new_title],
        check=True
    )

def add_to_backlog(node_type: str, title: str, goal: str) -> str:
    """Creates a GH issue using the backlog_issue template and applies the 'backlog' label.
    
    Returns the URL of the created issue.
    """
    formatted_title = f"{node_type.capitalize()}: {title}"
    if node_type.lower() == "path":
        kwargs = {"goal": goal}
        body = render_template("path_tracker", kwargs)
        label = "meta"
    else:
        kwargs = {
            "goal": goal,
            "changes": "TBD",
            "invariants": "TBD",
            "depends_on": "TBD"
        }
        body = render_template("backlog_issue", kwargs)
        label = "backlog"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=True) as temp_file:
        temp_file.write(body)
        temp_file.flush()
        
        result = subprocess.run(
            ["gh", "issue", "create", "--title", formatted_title,
             "-F", temp_file.name, "--label", label],
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
