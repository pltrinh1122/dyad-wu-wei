import subprocess
import tempfile

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
