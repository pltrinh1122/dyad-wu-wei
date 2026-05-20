import os
import tempfile
import yaml
import pytest
from unittest import mock
from orchestrator.node_lifecycle import load_node_status_config, load_node_classification_config, BaseNode, TerminalNode

def test_load_node_status_config_success():
    mock_yaml_content = {
        "node_attributes": {
            "status": {
                "in_progress": "status: in-progress"
            },
            "classification": {
                "backlog": "backlog"
            }
        }
    }
    with mock.patch("os.path.exists", return_value=True):
        with mock.patch("builtins.open", mock.mock_open(read_data=yaml.dump(mock_yaml_content))):
            status_config = load_node_status_config()
            assert status_config.get("in_progress") == "status: in-progress"

            class_config = load_node_classification_config()
            assert class_config.get("backlog") == "backlog"

def test_load_node_status_config_not_found():
    with mock.patch("os.path.exists", return_value=False):
        status_config = load_node_status_config()
        assert status_config == {}

        class_config = load_node_classification_config()
        assert class_config == {}

@mock.patch("orchestrator.node_lifecycle.load_node_status_config")
@mock.patch("orchestrator.node_lifecycle.github_client.add_label")
def test_base_node_set_status(mock_add_label, mock_load_config):
    mock_load_config.return_value = {"in_progress": "status: in-progress"}
    node = BaseNode("100")
    node.set_status("in_progress")
    mock_add_label.assert_called_once_with("100", "status: in-progress")

@mock.patch("orchestrator.node_lifecycle.load_node_status_config")
def test_base_node_set_status_invalid(mock_load_config):
    mock_load_config.return_value = {"in_progress": "status: in-progress"}
    node = BaseNode("100")
    with pytest.raises(ValueError, match="Status key 'invalid' is not defined in node.yml"):
        node.set_status("invalid")

@mock.patch("orchestrator.node_lifecycle.load_node_classification_config")
@mock.patch("orchestrator.node_lifecycle.github_client.add_label")
def test_base_node_set_classification(mock_add_label, mock_load_config):
    mock_load_config.return_value = {"backlog": "backlog"}
    node = BaseNode("100")
    node.set_classification("backlog")
    mock_add_label.assert_called_once_with("100", "backlog")

@mock.patch("orchestrator.node_lifecycle.load_node_classification_config")
def test_base_node_set_classification_invalid(mock_load_config):
    mock_load_config.return_value = {"backlog": "backlog"}
    node = BaseNode("100")
    with pytest.raises(ValueError, match="Classification key 'invalid' is not defined in node.yml"):
        node.set_classification("invalid")

@mock.patch("orchestrator.node_lifecycle.github_client.get_issue_labels")
def test_base_node_metadata_properties(mock_get_labels):
    mock_get_labels.return_value = ["loop:spao", "area:metasystem", "kind:infra"]
    node = BaseNode("390")
    assert node.loop == "spao"
    assert node.area == "metasystem"
    assert node.kind == "infra"

@mock.patch("orchestrator.node_lifecycle.github_client.get_issue_labels")
def test_get_worktree_path(mock_get_labels):
    # SPAO loop
    mock_get_labels.return_value = ["loop:spao"]
    node = BaseNode("390")
    assert node.get_worktree_path("node/390-test") == os.path.join(".worktrees", "spao", "node/390-test")

    # SDLC loop
    mock_get_labels.return_value = ["loop:sdlc"]
    node = BaseNode("390")
    assert node.get_worktree_path("node/390-test") == os.path.join(".worktrees", "sdlc", "node/390-test")

    # Default loop
    mock_get_labels.return_value = []
    node = BaseNode("390")
    assert node.get_worktree_path("node/390-test") == os.path.join(".worktrees", "node/390-test")

@mock.patch("orchestrator.node_lifecycle.github_client.get_issue_labels")
@mock.patch("subprocess.run")
def test_validate_spao_purity_success(mock_run, mock_get_labels):
    mock_get_labels.return_value = ["loop:spao"]
    mock_run.return_value = mock.MagicMock(returncode=0, stdout="kb/WHAT-0034.md\nartifacts/frontier_state.md\nGEMINI.md")
    
    node = TerminalNode("390")
    # Should not raise any exception
    node._validate_spao_purity()

@mock.patch("orchestrator.node_lifecycle.github_client.get_issue_labels")
@mock.patch("subprocess.run")
def test_validate_spao_purity_failure(mock_run, mock_get_labels):
    mock_get_labels.return_value = ["loop:spao"]
    mock_run.return_value = mock.MagicMock(returncode=0, stdout="skills/path_resolver.py\nkb/WHAT-0034.md")
    
    node = TerminalNode("390")
    with pytest.raises(Exception, match="SPAO PR Purity Violation"):
        node._validate_spao_purity()

@mock.patch("orchestrator.node_lifecycle.github_client.get_issue_labels")
@mock.patch("subprocess.run")
@mock.patch("orchestrator.node_lifecycle.github_client.get_issue_details")
def test_plan_finish_spec_check_failure(mock_get_details, mock_run, mock_get_labels):
    mock_get_details.return_value = {"title": "Probe 386: Plan - Test Issue", "body": "Goal"}
    mock_get_labels.return_value = []
    mock_run.return_value = mock.MagicMock(returncode=0, stdout="skills/path_resolver.py")
    
    node = TerminalNode("390")
    with pytest.raises(Exception, match="SPEC file violation"):
        node.plan_finish("dummy body")

