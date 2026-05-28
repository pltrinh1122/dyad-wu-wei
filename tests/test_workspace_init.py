import os
import sys
import subprocess
from unittest import mock
import pytest
from kernel import daemon_workspace
from kernel.node_lifecycle import BaseNode, TerminalNode

@mock.patch("kernel.daemon_workspace.git_client.clone")
@mock.patch("kernel.daemon_workspace.path_resolver.get_core_dir")
@mock.patch("kernel.daemon_workspace.subprocess.check_call")
@mock.patch("kernel.daemon_workspace.subprocess.check_output")
@mock.patch("venv.create")
def test_daemon_workspace_init(mock_venv_create, mock_check_output, mock_check_call, mock_get_core_dir, mock_clone, tmp_path):
    # Setup mock core dir
    core_dir = tmp_path / "core"
    core_dir.mkdir()
    mock_get_core_dir.return_value = str(core_dir)
    
    # Create empty parent gitignore
    gitignore = core_dir / ".gitignore"
    gitignore.touch()
    
    mock_check_output.return_value = b"2026-05-25T00:00:00Z\n"
    
    # Call init_workspace
    repo_url = "https://github.com/operator/repo"
    daemon_workspace.init_workspace(repo_url)
    
    workspace_path = core_dir / ".workspace"
    
    # Assert clone was called
    mock_clone.assert_called_once_with(repo_url, str(workspace_path))
    
    # Assert directories created
    assert (workspace_path / "kb").is_dir()
    assert (workspace_path / "artifacts").is_dir()
    
    # Assert GEMINI.md created
    gemini_md = workspace_path / "GEMINI.md"
    assert gemini_md.is_file()
    assert "Workspace Mode" in gemini_md.read_text()
    
    # Assert venv created and dependencies installed
    mock_venv_create.assert_called_once_with(str(workspace_path / ".venv"), with_pip=True)
    assert mock_check_call.call_count >= 2
    
    # Assert parent gitignore updated
    assert "\n.workspace/\n" in gitignore.read_text()
    
    # Assert child gitignore created
    child_gitignore = workspace_path / ".gitignore"
    assert child_gitignore.is_file()
    
    # Assert config saved
    config_file = core_dir / "artifacts" / "active_workspace.json"
    assert config_file.is_file()

@mock.patch("kernel.daemon_workspace.git_client.clone")
@mock.patch("kernel.daemon_workspace.path_resolver.get_core_dir")
@mock.patch("kernel.daemon_workspace.subprocess.check_call")
@mock.patch("kernel.daemon_workspace.subprocess.check_output")
@mock.patch("venv.create")
def test_daemon_workspace_init_custom_target(mock_venv_create, mock_check_output, mock_check_call, mock_get_core_dir, mock_clone, tmp_path):
    core_dir = tmp_path / "core"
    core_dir.mkdir()
    mock_get_core_dir.return_value = str(core_dir)
    mock_check_output.return_value = b"2026-05-25T00:00:00Z\n"
    
    custom_target = tmp_path / "custom_workspace"
    repo_url = "https://github.com/operator/repo"
    
    daemon_workspace.init_workspace(repo_url, target_dir=str(custom_target))
    
    mock_clone.assert_called_once_with(repo_url, str(custom_target))
    assert (custom_target / "kb").is_dir()
    assert (custom_target / "artifacts").is_dir()
    assert (custom_target / "GEMINI.md").is_file()

@mock.patch("kernel.node_lifecycle.github_client.get_issue_labels")
def test_node_lifecycle_workspace_redirection(mock_get_labels):
    mock_env = {"SPAO_WORKSPACE_DIR": "/tmp/workspace_dir"}
    mock_get_labels.return_value = ["loop:spao"]
    node = BaseNode("390")
    
    with mock.patch.dict(os.environ, mock_env):
        worktree_path = node.get_worktree_path("node/390-test")
        assert worktree_path == os.path.join("/tmp/workspace_dir", ".worktrees", "node/390-test")


@mock.patch("kernel.node_lifecycle.github_client.is_branch_merged_on_github")
@mock.patch("kernel.node_lifecycle.git_client.worktree_remove")
@mock.patch("kernel.node_lifecycle.git_client.branch_delete")
@mock.patch("os.path.exists")
def test_node_lifecycle_clean_if_merged_workspace(mock_exists, mock_branch_delete, mock_worktree_remove, mock_is_merged):
    mock_env = {"SPAO_WORKSPACE_DIR": "/tmp/workspace_dir"}
    mock_exists.return_value = True
    mock_is_merged.return_value = True
    
    with mock.patch.dict(os.environ, mock_env):
        TerminalNode.clean_if_merged("node/390-test")
        
        expected_path = os.path.join("/tmp/workspace_dir", ".worktrees", "node/390-test")
        mock_worktree_remove.assert_called_once_with(expected_path, force=True)
        mock_branch_delete.assert_called_once_with("node/390-test")
