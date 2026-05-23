import subprocess
import tempfile
import json
from kernel.mgr_telemetry import record_execution

@record_execution(stage="skill")
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

@record_execution(stage="skill")
def close_issue(issue_id: str, comment_body: str) -> None:
    """Closes a GH issue with a final comment."""
    subprocess.run(
        ["gh", "issue", "close", str(issue_id), "-c", comment_body],
        check=True
    )
    try:
        labels = get_issue_labels(issue_id)
        for label in labels:
            if label.startswith("status:"):
                remove_label(issue_id, label)
    except Exception:
        pass

def reopen_issue(issue_id: str) -> None:
    """Reopens a closed GH issue."""
    subprocess.run(
        ["gh", "issue", "reopen", str(issue_id)],
        check=True
    )

@record_execution(stage="skill")
def update_issue_body(issue_id: str, new_body: str) -> None:
    """Updates an existing issue body using a temp file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=True) as temp_file:
        temp_file.write(new_body)
        temp_file.flush()
        
        subprocess.run(
            ["gh", "issue", "edit", str(issue_id), "--body-file", temp_file.name],
            check=True
        )


@record_execution(stage="skill")
def list_issues_by_label(label: str) -> list[dict]:
    """Returns a list of open issues matching the given label.
    
    Each item is a dict with 'number', 'title', and 'url' keys.
    Returns an empty list if no issues are found.
    """
    result = subprocess.run(
        ["gh", "issue", "list", "--label", label, "--state", "open",
         "--json", "number,title,url,state"],
        capture_output=True, text=True, check=True
    )
    import json
    issues = json.loads(result.stdout.strip() or "[]")
    
    valid_issues = []
    for issue in issues:
        if issue.get("state") == "OPEN":
            valid_issues.append({
                "number": issue["number"],
                "title": issue["title"],
                "url": issue["url"]
            })
            
    return valid_issues

def get_open_issues() -> list[dict]:
    """Returns a list of open issues in the repository.
    
    Each item is a dict with 'number', 'title', and 'body' keys.
    """
    result = subprocess.run(
        ["gh", "issue", "list", "--state", "open", "--limit", "100", "--json", "number,title,body"],
        capture_output=True, text=True, check=True
    )
    import json
    return json.loads(result.stdout.strip() or "[]")

@record_execution(stage="skill")
def get_issue_details(issue_id: str) -> dict:
    """Returns details for a specific issue."""
    result = subprocess.run(
        ["gh", "issue", "view", str(issue_id), "--json", "number,title,body,state"],
        capture_output=True, text=True, check=True
    )
    import json
    return json.loads(result.stdout.strip() or "{}")

def rename_issue_title(issue_id: str, new_title: str) -> None:
    """Renames an existing GH issue's title."""
    subprocess.run(
        ["gh", "issue", "edit", str(issue_id), "--title", new_title],
        check=True
    )


@record_execution(stage="skill")
def create_pull_request(title: str, body: str, head: str = None) -> str:
    """Creates a PR using gh pr create, or returns the existing PR URL if it already exists for the head branch."""
    if not head:
        res = subprocess.run(
            ["git", "symbolic-ref", "--short", "HEAD"],
            capture_output=True, text=True
        )
        if res.returncode == 0:
            head = res.stdout.strip()

    if head:
        chk_res = subprocess.run(
            ["gh", "pr", "list", "--head", head, "--state", "open", "--json", "url"],
            capture_output=True, text=True, check=True
        )
        prs = json.loads(chk_res.stdout.strip() or "[]")
        if prs and isinstance(prs, list) and len(prs) > 0:
            return prs[0]["url"]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=True) as temp_file:
        temp_file.write(body)
        temp_file.flush()
        
        cmd = ["gh", "pr", "create", "--title", title, "-F", temp_file.name]
        if head:
            cmd += ["--head", head]
        result = subprocess.run(
            cmd,
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

def get_merged_prs(limit: int = 50) -> list[dict]:
    """Returns a list of recently merged PRs for the repository.
    
    Each item is a dict with 'headRefName'.
    """
    result = subprocess.run(
        ["gh", "pr", "list", "--state", "merged", "--limit", str(limit), "--json", "headRefName"],
        capture_output=True, text=True, check=True
    )
    import json
    return json.loads(result.stdout.strip() or "[]")

def merge_pull_request(pr_number: int, method: str = "squash") -> None:
    """Merges a pull request using the specified method."""
    subprocess.run(
        ["gh", "pr", "merge", str(pr_number), f"--{method}", "--delete-branch"],
        check=True
    )

def close_pull_request(pr_number: int) -> None:
    """Closes a pull request without merging."""
    subprocess.run(
        ["gh", "pr", "close", str(pr_number)],
        check=True
    )
