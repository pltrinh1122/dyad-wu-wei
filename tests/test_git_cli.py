import sys
import pytest
from unittest.mock import patch, MagicMock
from skills import git_cli

@patch("sys.argv", ["bin/git", "add", "file.txt"])
@patch("skills.git_client.add")
def test_cli_add(mock_add):
    git_cli.main()
    mock_add.assert_called_once_with(["file.txt"])

@patch("sys.argv", ["bin/git", "commit", "-m", "Commit message"])
@patch("skills.git_client.commit")
def test_cli_commit(mock_commit):
    git_cli.main()
    mock_commit.assert_called_once_with("Commit message")

@patch("sys.argv", ["bin/git", "push", "feature-branch"])
@patch("skills.git_client.push")
def test_cli_push_explicit(mock_push):
    git_cli.main()
    mock_push.assert_called_once_with("feature-branch", force=False)

@patch("sys.argv", ["bin/git", "push", "-f"])
@patch("skills.git_client.get_current_branch", return_value="main")
@patch("skills.git_client.push")
def test_cli_push_implicit_force(mock_push, mock_get_current):
    git_cli.main()
    mock_push.assert_called_once_with("main", force=True)

@patch("sys.argv", ["bin/git", "restore", "file.txt"])
@patch("skills.git_client.restore")
def test_cli_restore(mock_restore):
    git_cli.main()
    mock_restore.assert_called_once_with(["file.txt"])

@patch("sys.argv", ["bin/git", "worktree", "add", "node-branch", ".worktrees/node-branch"])
@patch("skills.git_client.worktree_add")
def test_cli_worktree_add(mock_wt_add):
    git_cli.main()
    mock_wt_add.assert_called_once_with("node-branch", ".worktrees/node-branch", "main")

@patch("sys.argv", ["bin/git", "worktree", "remove", ".worktrees/node-branch", "-f"])
@patch("skills.git_client.worktree_remove")
def test_cli_worktree_remove(mock_wt_remove):
    git_cli.main()
    mock_wt_remove.assert_called_once_with(".worktrees/node-branch", force=True)
