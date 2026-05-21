import subprocess
from orchestrator.mgr_telemetry import record_execution

@record_execution(stage="skill")
def add(files: list[str], cwd: str | None = None) -> None:
    """Stages files for commit."""
    if not files:
        return
    subprocess.run(["git", "add"] + files, check=True, cwd=cwd)

@record_execution(stage="skill")
def commit(message: str, cwd: str | None = None) -> None:
    """Commits staged changes."""
    subprocess.run(["git", "commit", "-m", message], check=True, cwd=cwd)

@record_execution(stage="skill")
def push(branch: str, force: bool = False, cwd: str | None = None) -> None:
    """Pushes local commits to origin."""
    cmd = ["git", "push"]
    if force:
        cmd.append("-f")
    else:
        cmd.extend(["-u", "origin", branch])
    subprocess.run(cmd, check=True, cwd=cwd)

@record_execution(stage="skill")
def restore(files: list[str], staged: bool = False, cwd: str | None = None) -> None:
    """Restores specified modified files."""
    if not files:
        return
    cmd = ["git", "restore"]
    if staged:
        cmd.append("--staged")
    subprocess.run(cmd + files, check=True, cwd=cwd)

@record_execution(stage="skill")
def status_porcelain(cwd: str | None = None) -> str:
    """Returns git status in porcelain format."""
    res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True, cwd=cwd)
    return res.stdout

@record_execution(stage="skill")
def diff_names(branch: str, cwd: str | None = None) -> list[str]:
    """Returns list of files modified against specified branch."""
    res = subprocess.run(["git", "diff", "--name-only", branch], capture_output=True, text=True, check=True, cwd=cwd)
    return [f.strip() for f in res.stdout.splitlines() if f.strip()]

@record_execution(stage="skill")
def reset_hard(cwd: str | None = None) -> None:
    """Performs a hard reset to HEAD~1."""
    subprocess.run(["git", "reset", "--hard", "HEAD~1"], check=True, cwd=cwd)

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
def get_current_branch(cwd: str | None = None) -> str:
    """Returns the current branch name, resolving detached HEAD at origin/main or main as 'main'."""
    res = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True, cwd=cwd)
    branch = res.stdout.strip()
    if not branch:
        try:
            head_commit = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True, cwd=cwd).stdout.strip()
            origin_main_commit = subprocess.run(["git", "rev-parse", "origin/main"], capture_output=True, text=True, check=True, cwd=cwd).stdout.strip()
            main_commit = subprocess.run(["git", "rev-parse", "main"], capture_output=True, text=True, check=True, cwd=cwd).stdout.strip()
            if head_commit in (origin_main_commit, main_commit):
                return "main"
        except Exception:
            pass
    return branch

@record_execution(stage="skill")
def fetch(remote: str = "origin", prune: bool = True, cwd: str | None = None) -> None:
    """Fetches updates from the remote repository."""
    cmd = ["git", "fetch"]
    if prune:
        cmd.append("--prune")
    cmd.append(remote)
    subprocess.run(cmd, check=True, cwd=cwd)

@record_execution(stage="skill")
def get_commit_hash(revision: str = "HEAD") -> str:
    """Returns the commit hash for the specified revision."""
    res = subprocess.run(["git", "rev-parse", revision], capture_output=True, text=True, check=True)
    return res.stdout.strip()

@record_execution(stage="skill")
def branch_delete(branch: str) -> None:
    """Deletes a local branch."""
    try:
        subprocess.run(["git", "branch", "-D", branch], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        stderr = getattr(e, "stderr", "") or ""
        if "used by worktree" in stderr:
            print(f"Warning: Cannot delete branch '{branch}' because it is currently used by another worktree.")
        elif "not found" in stderr:
            pass  # It's already deleted
        else:
            raise e

@record_execution(stage="skill")
def switch(branch: str, detach: bool = False) -> None:
    """Switches to the specified branch, optionally detaching HEAD."""
    cmd = ["git", "switch"]
    if detach:
        cmd.append("--detach")
    cmd.append(branch)
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        if not detach:
            # Fall back to detached HEAD if the branch is locked in another worktree
            subprocess.run(["git", "switch", "--detach", branch], check=True)
        else:
            raise e

@record_execution(stage="skill")
def pull(remote: str, branch: str, prune: bool = False) -> None:
    """Pulls commits from remote repository branch."""
    cmd = ["git", "pull"]
    if prune:
        cmd.append("--prune")
    cmd.extend([remote, branch])
    subprocess.run(cmd, check=True)

@record_execution(stage="skill")
def list_merged_branches() -> list[str]:
    """Returns a list of local branches that have been merged into HEAD."""
    res = subprocess.run(["git", "branch", "--merged"], capture_output=True, text=True, check=True)
    return [b.strip().strip("* ") for b in res.stdout.splitlines() if b.strip()]

@record_execution(stage="skill")
def list_local_branches() -> list[str]:
    """Returns a list of all local branch names."""
    res = subprocess.run(["git", "branch", "--format", "%(refname:short)"], capture_output=True, text=True, check=True)
    return [b.strip() for b in res.stdout.splitlines() if b.strip()]

@record_execution(stage="skill")
def worktree_prune() -> None:
    """Prunes stale git worktrees."""
    subprocess.run(["git", "worktree", "prune"], check=False)

def get_git_common_dir() -> str:
    """Returns the .git directory path (git-common-dir)."""
    res = subprocess.run(["git", "rev-parse", "--git-common-dir"], capture_output=True, text=True, check=True)
    return res.stdout.strip()

@record_execution(stage="skill")
def tag(version: str, message: str) -> None:
    """Creates an annotated git tag."""
    subprocess.run(["git", "tag", "-a", version, "-m", message], check=True)

@record_execution(stage="skill")
def tag_push(version: str) -> None:
    """Pushes a specific tag to origin."""
    subprocess.run(["git", "push", "origin", version], check=True)

def get_show_toplevel() -> str:
    """Returns the primary repository root directory."""
    res = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
    return res.stdout.strip()

