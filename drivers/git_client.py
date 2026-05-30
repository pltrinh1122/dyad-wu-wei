import os
import subprocess
from kernel.daemon_telemetry import record_execution

def _run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    if kwargs.get("cwd") is None:
        workspace_dir = os.environ.get("SPAO_WORKSPACE_DIR")
        if workspace_dir:
            kwargs["cwd"] = workspace_dir
    return subprocess.run(cmd, **kwargs)

from kernel.daemon_telemetry import record_execution

@record_execution(stage="skill")
def add(files: list[str], cwd: str | None = None) -> None:
    """Stages files for commit."""
    if not files:
        return
    _run(["git", "add"] + files, check=True, cwd=cwd)

@record_execution(stage="skill")
def checkout_b(branch: str, cwd: str | None = None) -> None:
    """Creates a new branch and switches to it."""
    _run(["git", "checkout", "-b", branch], check=True, cwd=cwd)

@record_execution(stage="skill")
def switch(branch: str, cwd: str | None = None) -> None:
    """Switches to an existing branch."""
    _run(["git", "switch", branch], check=True, cwd=cwd)

@record_execution(stage="skill")
def commit(message: str, cwd: str | None = None) -> None:
    """Commits staged changes."""
    _run(["git", "commit", "-m", message], check=True, cwd=cwd)

@record_execution(stage="skill")
def push(branch: str, force: bool = False, cwd: str | None = None) -> None:
    """Pushes local commits to origin."""
    cmd = ["git", "push"]
    if force:
        cmd.append("-f")
    else:
        cmd.extend(["-u", "origin", branch])
    _run(cmd, check=True, cwd=cwd)

@record_execution(stage="skill")
def restore(files: list[str], staged: bool = False, cwd: str | None = None) -> None:
    """Restores specified modified files."""
    if not files:
        return
    cmd = ["git", "restore"]
    if staged:
        cmd.append("--staged")
    _run(cmd + files, check=True, cwd=cwd)

@record_execution(stage="skill")
def rebase(target: str = "origin/main", cwd: str | None = None) -> None:
    """Rebases the current branch onto target, ensuring conflict-free push."""
    _run(["git", "rebase", target], check=True, cwd=cwd)


@record_execution(stage="skill")
def rebase_with_conflict_resolution(target: str = "origin/main", cwd: str | None = None) -> None:
    """Rebases the current branch onto target with automatic resolution of deterministic conflicts.

    Deterministic auto-resolvable patterns:
    - ``artifacts/frontier_state.yml.sha256``: regenerated from the merged
      ``frontier_state.yml`` via SHA-256 so it is always correct post-merge.

    Any remaining conflicts are surfaced as a clear error that aborts the rebase
    and lists the conflicting files so the operator can act.

    Args:
        target: The rebase target ref (default: ``origin/main``).
        cwd:    Working directory for git operations (e.g. a worktree path).
    """
    import hashlib

    # Known files whose conflicts can be resolved deterministically.
    SHA256_CHECKSUM_FILE = "artifacts/frontier_state.yml.sha256"
    SHA256_SOURCE_FILE   = "artifacts/frontier_state.yml"

    res = _run(["git", "rebase", target], capture_output=True, text=True, cwd=cwd)
    if res.returncode == 0:
        # Clean rebase — nothing to do.
        return

    # Rebase failed — inspect the conflict list.
    conflict_res = _run(
        ["git", "diff", "--name-only", "--diff-filter=U"],
        capture_output=True, text=True, cwd=cwd,
    )
    conflicted_files = [f.strip() for f in conflict_res.stdout.splitlines() if f.strip()]

    unresolved = []
    for conflict_file in conflicted_files:
        if conflict_file == SHA256_CHECKSUM_FILE:
            # Auto-resolve: regenerate the SHA-256 from the merged source file.
            root = cwd or "."
            source_path = os.path.join(root, SHA256_SOURCE_FILE)
            dest_path   = os.path.join(root, SHA256_CHECKSUM_FILE)
            if os.path.exists(source_path):
                with open(source_path, "rb") as f:
                    digest = hashlib.sha256(f.read()).hexdigest()
                with open(dest_path, "w") as f:
                    f.write(digest + "\n")
                _run(["git", "add", SHA256_CHECKSUM_FILE], check=True, cwd=cwd)
                print(
                    f"[🔧 AUTO-RESOLVE] Regenerated {SHA256_CHECKSUM_FILE} "
                    f"from {SHA256_SOURCE_FILE} (SHA-256: {digest[:12]}...)"
                )
            else:
                unresolved.append(conflict_file)
        else:
            unresolved.append(conflict_file)

    if unresolved:
        # Abort the rebase so the worktree is not left in a broken state.
        _run(["git", "rebase", "--abort"], cwd=cwd)
        raise Exception(
            f"Reflection Blocked (WHY-0083): Branch has unresolved merge conflicts "
            f"with '{target}'. Auto-resolution could not handle: {unresolved}. "
            f"You must resolve these conflicts locally before reflecting."
        )

    # All conflicts resolved — continue the rebase.
    continue_env = {**os.environ, "GIT_EDITOR": "true"}
    cont_res = _run(
        ["git", "rebase", "--continue"],
        capture_output=True, text=True, env=continue_env, cwd=cwd,
    )
    if cont_res.returncode != 0:
        _run(["git", "rebase", "--abort"], cwd=cwd)
        raise Exception(
            f"Reflection Blocked (WHY-0083): Rebase --continue failed after "
            f"auto-resolution of deterministic conflicts. "
            f"stderr: {cont_res.stderr.strip()}"
        )


@record_execution(stage="skill")
def status_porcelain(cwd: str | None = None) -> str:
    """Returns git status in porcelain format."""
    res = _run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True, cwd=cwd)
    return res.stdout

@record_execution(stage="skill")
def diff_names(branch: str, cwd: str | None = None) -> list[str]:
    """Returns list of files modified against specified branch."""
    res = _run(["git", "diff", "--name-only", branch], capture_output=True, text=True, check=True, cwd=cwd)
    return [f.strip() for f in res.stdout.splitlines() if f.strip()]

def get_staged_files(cwd: str | None = None) -> list[str]:
    """Returns list of currently staged files."""
    res = _run(["git", "diff", "--name-only", "--cached"], capture_output=True, text=True, check=True, cwd=cwd)
    return [f.strip() for f in res.stdout.splitlines() if f.strip()]

@record_execution(stage="skill")
def reset_hard(cwd: str | None = None) -> None:
    """Performs a hard reset to HEAD~1."""
    _run(["git", "reset", "--hard", "HEAD~1"], check=True, cwd=cwd)

@record_execution(stage="skill")
def worktree_add(branch: str, path: str, base: str = "main") -> None:
    """Adds a new git worktree, cleaning up pre-existing branches safely if needed."""
    try:
        res = _run(["git", "show-ref", "--verify", f"refs/heads/{branch}"], check=False)
        if res.returncode == 0:
            _run(["git", "branch", "-D", branch], check=True)
    except Exception:
        pass
    _run(["git", "worktree", "add", "-b", branch, path, base], check=True)

@record_execution(stage="skill")
def worktree_remove(path: str, force: bool = False) -> None:
    """Removes a git worktree."""
    cmd = ["git", "worktree", "remove"]
    if force:
        cmd.append("-f")
    cmd.append(path)
    _run(cmd, check=True)

@record_execution(stage="skill")
def get_current_branch(cwd: str | None = None) -> str:
    """Returns the current branch name, resolving detached HEAD at origin/main or main as 'main'."""
    res = _run(["git", "branch", "--show-current"], capture_output=True, text=True, check=True, cwd=cwd)
    branch = res.stdout.strip()
    if not branch:
        try:
            head_commit = _run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True, cwd=cwd).stdout.strip()
            origin_main_commit = _run(["git", "rev-parse", "origin/main"], capture_output=True, text=True, check=True, cwd=cwd).stdout.strip()
            main_commit = _run(["git", "rev-parse", "main"], capture_output=True, text=True, check=True, cwd=cwd).stdout.strip()
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
    _run(cmd, check=True, cwd=cwd)

@record_execution(stage="skill")
def get_commit_hash(revision: str = "HEAD") -> str:
    """Returns the commit hash for the specified revision."""
    res = _run(["git", "rev-parse", revision], capture_output=True, text=True, check=True)
    return res.stdout.strip()

@record_execution(stage="skill")
def branch_delete(branch: str) -> None:
    """Deletes a local branch."""
    try:
        _run(["git", "branch", "-D", branch], check=True, capture_output=True, text=True)
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
        _run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        if not detach:
            # Fall back to detached HEAD if the branch is locked in another worktree
            _run(["git", "switch", "--detach", branch], check=True)
        else:
            raise e

@record_execution(stage="skill")
def pull(remote: str, branch: str, prune: bool = False) -> None:
    """Pulls commits from remote repository branch."""
    cmd = ["git", "pull"]
    if prune:
        cmd.append("--prune")
    cmd.extend([remote, branch])
    _run(cmd, check=True)

@record_execution(stage="skill")
def list_merged_branches() -> list[str]:
    """Returns a list of local branches that have been merged into HEAD."""
    res = _run(["git", "branch", "--merged"], capture_output=True, text=True, check=True)
    branches = []
    for line in res.stdout.splitlines():
        line = line.strip().lstrip("*+ ")
        if line and not line.startswith("(") and "detached" not in line:
            branches.append(line)
    return branches

@record_execution(stage="skill")
def list_local_branches() -> list[str]:
    """Returns a list of all local branch names."""
    res = _run(["git", "branch", "--format", "%(refname:short)"], capture_output=True, text=True, check=True)
    branches = []
    for line in res.stdout.splitlines():
        line = line.strip()
        if line and not line.startswith("(") and "detached" not in line:
            branches.append(line)
    return branches

@record_execution(stage="skill")
def worktree_prune() -> None:
    """Prunes stale git worktrees."""
    _run(["git", "worktree", "prune"], check=False)

def get_git_common_dir() -> str:
    """Returns the .git directory path (git-common-dir)."""
    res = _run(["git", "rev-parse", "--git-common-dir"], capture_output=True, text=True, check=True)
    return res.stdout.strip()

@record_execution(stage="skill")
def tag(version: str, message: str) -> None:
    """Creates an annotated git tag."""
    _run(["git", "tag", "-a", version, "-m", message], check=True)

@record_execution(stage="skill")
def tag_push(version: str) -> None:
    """Pushes a specific tag to origin."""
    _run(["git", "push", "origin", version], check=True)

def get_show_toplevel() -> str:
    """Returns the primary repository root directory."""
    res = _run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
    return res.stdout.strip()

@record_execution(stage="skill")
def check_merge_conflicts(target: str = "origin/main", cwd: str | None = None) -> bool:
    """Returns True if merging the target into HEAD would result in conflicts, False otherwise."""
    res = _run(["git", "merge-tree", "--write-tree", "HEAD", target], capture_output=True, text=True, cwd=cwd)
    if res.returncode == 1:
        return True
    elif res.returncode == 0:
        return False
    else:
        res.check_returncode() # Will raise CalledProcessError
        return False # Fallback

@record_execution(stage="skill")
def clone(url: str, path: str, cwd: str | None = None) -> None:
    """Clones a repository to the specified path."""
    _run(["git", "clone", url, path], check=True, cwd=cwd)
