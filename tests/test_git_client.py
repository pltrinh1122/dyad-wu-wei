import pytest
from unittest.mock import MagicMock
from drivers import git_client

def test_git_add(mock_subprocess):
    git_client.add(["file1.txt", "file2.txt"], cwd="/some/dir")
    mock_subprocess.assert_called_once_with(["git", "add", "file1.txt", "file2.txt"], check=True, cwd="/some/dir")

def test_git_add_empty(mock_subprocess):
    git_client.add([], cwd="/some/dir")
    mock_subprocess.assert_not_called()

def test_git_commit(mock_subprocess):
    git_client.commit("Commit msg", cwd="/some/dir")
    mock_subprocess.assert_called_once_with(["git", "commit", "-m", "Commit msg"], check=True, cwd="/some/dir")

def test_git_push_default(mock_subprocess):
    git_client.push("feature-branch", cwd="/some/dir")
    mock_subprocess.assert_called_once_with(["git", "push", "-u", "origin", "feature-branch"], check=True, cwd="/some/dir")

def test_git_push_force(mock_subprocess):
    git_client.push("feature-branch", force=True, cwd="/some/dir")
    mock_subprocess.assert_called_once_with(["git", "push", "-f"], check=True, cwd="/some/dir")

def test_git_restore(mock_subprocess):
    git_client.restore(["file1.txt"], cwd="/some/dir")
    mock_subprocess.assert_called_once_with(["git", "restore", "file1.txt"], check=True, cwd="/some/dir")

def test_git_restore_staged(mock_subprocess):
    git_client.restore(["file1.txt"], staged=True, cwd="/some/dir")
    mock_subprocess.assert_called_once_with(["git", "restore", "--staged", "file1.txt"], check=True, cwd="/some/dir")

def test_git_restore_empty(mock_subprocess):
    git_client.restore([], cwd="/some/dir")
    mock_subprocess.assert_not_called()

def test_git_worktree_add(mock_subprocess):
    git_client.worktree_add("node-branch", ".worktrees/node-branch", "main")
    mock_subprocess.assert_called_once_with(["git", "worktree", "add", "-b", "node-branch", ".worktrees/node-branch", "main"], check=True)

def test_git_worktree_remove_default(mock_subprocess):
    git_client.worktree_remove(".worktrees/node-branch")
    mock_subprocess.assert_called_once_with(["git", "worktree", "remove", ".worktrees/node-branch"], check=True)

def test_git_worktree_remove_force(mock_subprocess):
    git_client.worktree_remove(".worktrees/node-branch", force=True)
    mock_subprocess.assert_called_once_with(["git", "worktree", "remove", "-f", ".worktrees/node-branch"], check=True)

def test_git_get_current_branch(mock_subprocess):
    mock_subprocess.return_value.stdout = "main\n"
    branch = git_client.get_current_branch()
    assert branch == "main"
    mock_subprocess.assert_called_once_with(["git", "branch", "--show-current"], capture_output=True, text=True, check=True, cwd=None)

def test_git_get_commit_hash(mock_subprocess):
    mock_subprocess.return_value.stdout = "abcdef123456\n"
    commit = git_client.get_commit_hash("HEAD")
    assert commit == "abcdef123456"
    mock_subprocess.assert_called_once_with(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)

def test_git_branch_delete(mock_subprocess):
    git_client.branch_delete("node-branch")
    mock_subprocess.assert_called_once_with(["git", "branch", "-D", "node-branch"], check=True, capture_output=True, text=True)

def test_git_branch_delete_in_use(mock_subprocess):
    import subprocess
    error = subprocess.CalledProcessError(1, ["git", "branch", "-D", "node-branch"])
    error.stderr = "error: cannot delete branch 'node-branch' used by worktree at '/path'"
    mock_subprocess.side_effect = error
    git_client.branch_delete("node-branch")

def test_git_branch_delete_not_found(mock_subprocess):
    import subprocess
    error = subprocess.CalledProcessError(1, ["git", "branch", "-D", "node-branch"])
    error.stderr = "error: branch 'node-branch' not found"
    mock_subprocess.side_effect = error
    git_client.branch_delete("node-branch")

def test_git_branch_delete_other_error(mock_subprocess):
    import subprocess
    error = subprocess.CalledProcessError(1, ["git", "branch", "-D", "node-branch"])
    error.stderr = "fatal: some other error"
    mock_subprocess.side_effect = error
    with pytest.raises(subprocess.CalledProcessError):
        git_client.branch_delete("node-branch")

def test_git_switch(mock_subprocess):
    git_client.switch("main")
    mock_subprocess.assert_called_once_with(["git", "switch", "main"], check=True)

def test_git_pull_default(mock_subprocess):
    git_client.pull("origin", "main")
    mock_subprocess.assert_called_once_with(["git", "pull", "origin", "main"], check=True)

def test_git_pull_prune(mock_subprocess):
    git_client.pull("origin", "main", prune=True)
    mock_subprocess.assert_called_once_with(["git", "pull", "--prune", "origin", "main"], check=True)

def test_git_list_merged_branches(mock_subprocess):
    mock_subprocess.return_value.stdout = "  main\n* current-branch\n  merged-branch\n"
    branches = git_client.list_merged_branches()
    assert branches == ["main", "current-branch", "merged-branch"]
    mock_subprocess.assert_called_once_with(["git", "branch", "--merged"], capture_output=True, text=True, check=True)

def test_git_list_local_branches(mock_subprocess):
    mock_subprocess.return_value.stdout = "main\nfeature-1\n"
    branches = git_client.list_local_branches()
    assert branches == ["main", "feature-1"]
    mock_subprocess.assert_called_once_with(["git", "branch", "--format", "%(refname:short)"], capture_output=True, text=True, check=True)

def test_git_worktree_prune(mock_subprocess):
    git_client.worktree_prune()
    mock_subprocess.assert_called_once_with(["git", "worktree", "prune"], check=False)

def test_git_get_git_common_dir(mock_subprocess):
    mock_subprocess.return_value.stdout = ".git\n"
    res = git_client.get_git_common_dir()
    assert res == ".git"
    mock_subprocess.assert_called_once_with(["git", "rev-parse", "--git-common-dir"], capture_output=True, text=True, check=True)

def test_git_get_show_toplevel(mock_subprocess):
    mock_subprocess.return_value.stdout = "/path/to/repo\n"
    res = git_client.get_show_toplevel()
    assert res == "/path/to/repo"
    mock_subprocess.assert_called_once_with(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)

def test_git_status_porcelain(mock_subprocess):
    mock_subprocess.return_value.stdout = "M file1.txt\n?? file2.txt\n"
    res = git_client.status_porcelain(cwd="/some/dir")
    assert res == "M file1.txt\n?? file2.txt\n"
    mock_subprocess.assert_called_once_with(["git", "status", "--porcelain"], capture_output=True, text=True, check=True, cwd="/some/dir")

def test_git_diff_names(mock_subprocess):
    mock_subprocess.return_value.stdout = "file1.txt\nfile2.txt\n"
    res = git_client.diff_names("main", cwd="/some/dir")
    assert res == ["file1.txt", "file2.txt"]
    mock_subprocess.assert_called_once_with(["git", "diff", "--name-only", "main"], capture_output=True, text=True, check=True, cwd="/some/dir")

def test_git_reset_hard(mock_subprocess):
    git_client.reset_hard(cwd="/some/dir")
    mock_subprocess.assert_called_once_with(["git", "reset", "--hard", "HEAD~1"], check=True, cwd="/some/dir")

def test_git_switch_fallback(mock_subprocess):
    import subprocess
    # First call fails, second call (fallback) succeeds
    mock_subprocess.side_effect = [
        subprocess.CalledProcessError(128, ["git", "switch", "main"]),
        MagicMock(returncode=0, stdout="success")
    ]
    git_client.switch("main")
    assert mock_subprocess.call_count == 2
    mock_subprocess.assert_any_call(["git", "switch", "main"], check=True)
    mock_subprocess.assert_any_call(["git", "switch", "--detach", "main"], check=True)

def test_git_switch_detach(mock_subprocess):
    git_client.switch("main", detach=True)
    mock_subprocess.assert_called_once_with(["git", "switch", "--detach", "main"], check=True)

def test_git_get_current_branch_detached(mock_subprocess):
    # Simulating detached HEAD pointing to origin/main
    show_current_res = MagicMock(stdout="\n")
    head_res = MagicMock(stdout="hash123\n")
    origin_main_res = MagicMock(stdout="hash123\n")
    main_res = MagicMock(stdout="hash456\n")
    
    mock_subprocess.side_effect = [show_current_res, head_res, origin_main_res, main_res]
    
    branch = git_client.get_current_branch()
    assert branch == "main"
    assert mock_subprocess.call_count == 4
    mock_subprocess.assert_any_call(["git", "branch", "--show-current"], capture_output=True, text=True, check=True, cwd=None)
    mock_subprocess.assert_any_call(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True, cwd=None)
    mock_subprocess.assert_any_call(["git", "rev-parse", "origin/main"], capture_output=True, text=True, check=True, cwd=None)
    mock_subprocess.assert_any_call(["git", "rev-parse", "main"], capture_output=True, text=True, check=True, cwd=None)

def test_git_fetch_default(mock_subprocess):
    git_client.fetch()
    mock_subprocess.assert_called_once_with(["git", "fetch", "--prune", "origin"], check=True, cwd=None)

def test_git_fetch_custom(mock_subprocess):
    git_client.fetch(remote="upstream", prune=False, cwd="/some/dir")
    mock_subprocess.assert_called_once_with(["git", "fetch", "upstream"], check=True, cwd="/some/dir")


# --- Tests for rebase_with_conflict_resolution ---

def test_rebase_with_conflict_resolution_clean(mock_subprocess):
    """Clean rebase: no conflicts — function returns without extra calls."""
    mock_subprocess.return_value = MagicMock(returncode=0, stdout="", stderr="")
    git_client.rebase_with_conflict_resolution("origin/main", cwd="/repo")
    # Only one subprocess call: the initial rebase
    mock_subprocess.assert_called_once_with(
        ["git", "rebase", "origin/main"], capture_output=True, text=True, cwd="/repo"
    )


def test_rebase_with_conflict_resolution_sha256_autoresolve(tmp_path):
    """SHA256 conflict: auto-regenerates checksum file and continues rebase successfully."""
    import hashlib
    import subprocess
    from unittest.mock import patch, call, MagicMock

    # Set up filesystem: a source yml and conflicted sha256 file
    artifacts_dir = tmp_path / "artifacts"
    artifacts_dir.mkdir()
    frontier_yml = artifacts_dir / "frontier_state.yml"
    frontier_yml.write_text("active_node: none\n")
    frontier_sha = artifacts_dir / "frontier_state.yml.sha256"
    frontier_sha.write_text("<<<<<<< HEAD\nold_hash\n=======\nnew_hash\n>>>>>>> origin/main\n")

    expected_digest = hashlib.sha256(b"active_node: none\n").hexdigest()

    call_log = []

    def fake_run(cmd, **kwargs):
        call_log.append(cmd)
        mock = MagicMock()
        if cmd == ["git", "rebase", "origin/main"]:
            mock.returncode = 1
            mock.stdout = ""
            mock.stderr = "CONFLICT"
        elif cmd == ["git", "diff", "--name-only", "--diff-filter=U"]:
            mock.returncode = 0
            mock.stdout = "artifacts/frontier_state.yml.sha256\n"
        elif cmd == ["git", "add", "artifacts/frontier_state.yml.sha256"]:
            mock.returncode = 0
        elif cmd == ["git", "rebase", "--continue"]:
            mock.returncode = 0
            mock.stdout = "Applied patch."
            mock.stderr = ""
        return mock

    with patch("drivers.git_client._run", side_effect=fake_run):
        git_client.rebase_with_conflict_resolution("origin/main", cwd=str(tmp_path))

    # Verify the checksum was regenerated correctly
    assert frontier_sha.read_text().strip() == expected_digest
    assert ["git", "rebase", "--continue"] in call_log


def test_rebase_with_conflict_resolution_unresolvable(tmp_path):
    """Unresolvable conflict: rebase is aborted and a clear error is raised."""
    from unittest.mock import patch, MagicMock

    call_log = []

    def fake_run(cmd, **kwargs):
        call_log.append(cmd)
        mock = MagicMock()
        if cmd == ["git", "rebase", "origin/main"]:
            mock.returncode = 1
            mock.stdout = ""
            mock.stderr = "CONFLICT"
        elif cmd == ["git", "diff", "--name-only", "--diff-filter=U"]:
            mock.returncode = 0
            mock.stdout = "kernel/some_code.py\n"
        elif cmd == ["git", "rebase", "--abort"]:
            mock.returncode = 0
        return mock

    with patch("drivers.git_client._run", side_effect=fake_run):
        with pytest.raises(Exception, match="Auto-resolution could not handle"):
            git_client.rebase_with_conflict_resolution("origin/main", cwd=str(tmp_path))

    assert ["git", "rebase", "--abort"] in call_log

