import subprocess
from orchestrator.mgr_telemetry import record_execution

@record_execution(stage="skill")
def add(files: list[str]) -> None:
    """Stages files for commit."""
    if not files:
        return
    subprocess.run(["git", "add"] + files, check=True)

@record_execution(stage="skill")
def commit(message: str) -> None:
    """Commits staged changes."""
    subprocess.run(["git", "commit", "-m", message], check=True)

@record_execution(stage="skill")
def push(branch: str, force: bool = False) -> None:
    """Pushes local commits to origin."""
    cmd = ["git", "push"]
    if force:
        cmd.append("-f")
    else:
        cmd.extend(["-u", "origin", branch])
    subprocess.run(cmd, check=True)

@record_execution(stage="skill")
def restore(files: list[str]) -> None:
    """Restores specified modified files."""
    if not files:
        return
    subprocess.run(["git", "restore"] + files, check=True)

@record_execution(stage="skill")
def worktree_add(branch: str, path: str, base: str = "main") -> None:
    """Adds a new git worktree."""
    subprocess.run(["git", "worktree", "add", "-b", branch, path, base], check=True)

@record_execution(stage="skill")
def worktree_remove(path: str, force: bool = False) -> None:
    """Removes a git worktree."""
    cmd = ["git", "worktree", "remove"]
    if force:
        cmd.append("-f")
    cmd.append(path)
    subprocess.run(cmd, check=True)

@record_execution(stage="skill")
def get_current_branch() -> str:
    """Returns the current branch name."""
    res = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, check=True)
    return res.stdout.strip()

@record_execution(stage="skill")
def get_commit_hash(revision: str = "HEAD") -> str:
    """Returns the commit hash for the specified revision."""
    res = subprocess.run(["git", "rev-parse", revision], capture_output=True, text=True, check=True)
    return res.stdout.strip()

@record_execution(stage="skill")
def branch_delete(branch: str) -> None:
    """Deletes a local branch."""
    subprocess.run(["git", "branch", "-D", branch], check=True)
