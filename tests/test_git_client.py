import pytest
from unittest.mock import MagicMock
from skills import git_client

def test_git_add(mock_subprocess):
    git_client.add(["file1.txt", "file2.txt"])
    mock_subprocess.assert_called_once_with(["git", "add", "file1.txt", "file2.txt"], check=True)

def test_git_add_empty(mock_subprocess):
    git_client.add([])
    mock_subprocess.assert_not_called()

def test_git_commit(mock_subprocess):
    git_client.commit("Commit msg")
    mock_subprocess.assert_called_once_with(["git", "commit", "-m", "Commit msg"], check=True)

def test_git_push_default(mock_subprocess):
    git_client.push("feature-branch")
    mock_subprocess.assert_called_once_with(["git", "push", "-u", "origin", "feature-branch"], check=True)

def test_git_push_force(mock_subprocess):
    git_client.push("feature-branch", force=True)
    mock_subprocess.assert_called_once_with(["git", "push", "-f"], check=True)

def test_git_restore(mock_subprocess):
    git_client.restore(["file1.txt"])
    mock_subprocess.assert_called_once_with(["git", "restore", "file1.txt"], check=True)

def test_git_restore_empty(mock_subprocess):
    git_client.restore([])
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
    mock_subprocess.assert_called_once_with(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, check=True)

def test_git_get_commit_hash(mock_subprocess):
    mock_subprocess.return_value.stdout = "abcdef123456\n"
    commit = git_client.get_commit_hash("HEAD")
    assert commit == "abcdef123456"
    mock_subprocess.assert_called_once_with(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)

def test_git_branch_delete(mock_subprocess):
    git_client.branch_delete("node-branch")
    mock_subprocess.assert_called_once_with(["git", "branch", "-D", "node-branch"], check=True)

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

