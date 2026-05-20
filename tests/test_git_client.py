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
