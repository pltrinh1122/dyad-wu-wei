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

@mock.patch("orchestrator.node_lifecycle.github_client.remove_label")
@mock.patch("orchestrator.node_lifecycle.github_client.get_issue_labels")
@mock.patch("orchestrator.node_lifecycle.load_node_status_config")
@mock.patch("orchestrator.node_lifecycle.github_client.add_label")
def test_base_node_set_status(mock_add_label, mock_load_config, mock_get_labels, mock_remove_label):
    mock_load_config.return_value = {
        "todo": "status: todo",
        "in_progress": "status: in-progress"
    }
    mock_get_labels.return_value = ["status: todo", "backlog"]
    
    node = BaseNode("100")
    node.set_status("in_progress")
    
    mock_add_label.assert_called_once_with("100", "status: in-progress")
    mock_remove_label.assert_called_once_with("100", "status: todo")

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

@mock.patch("orchestrator.node_lifecycle.git_client.diff_names")
@mock.patch("orchestrator.node_lifecycle.github_client.get_issue_labels")
def test_validate_spao_purity_success(mock_get_labels, mock_diff_names):
    mock_get_labels.return_value = ["loop:spao"]
    mock_diff_names.return_value = ["kb/WHAT-0034.md", "artifacts/frontier_state.md", "GEMINI.md"]
    
    node = TerminalNode("390")
    # Should not raise any exception
    node._validate_spao_purity(worktree_path="/some/dir")
    mock_diff_names.assert_called_once_with("main", cwd="/some/dir")

@mock.patch("orchestrator.node_lifecycle.git_client.diff_names")
@mock.patch("orchestrator.node_lifecycle.github_client.get_issue_labels")
def test_validate_spao_purity_failure(mock_get_labels, mock_diff_names):
    mock_get_labels.return_value = ["loop:spao"]
    mock_diff_names.return_value = ["skills/path_resolver.py", "kb/WHAT-0034.md"]
    
    node = TerminalNode("390")
    with pytest.raises(Exception, match="SPAO PR Purity Violation"):
        node._validate_spao_purity(worktree_path="/some/dir")
    mock_diff_names.assert_called_once_with("main", cwd="/some/dir")

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

@mock.patch("orchestrator.node_lifecycle.git_client")
@mock.patch("orchestrator.node_lifecycle.github_client")
@mock.patch("orchestrator.node_lifecycle.mgr_frontier")
@mock.patch("orchestrator.node_lifecycle.mgr_nba")
@mock.patch("orchestrator.node_lifecycle.TerminalNode.get_worktree_path")
def test_reflect_success(mock_get_worktree_path, mock_nba, mock_frontier, mock_gh, mock_git):
    mock_get_worktree_path.return_value = ".worktrees/node/390-test"
    mock_frontier.read_active_path.return_value = None
    mock_nba.NBAManager.return_value.evaluate.return_value = {"type": "continue"}
    mock_gh.get_issue_labels.return_value = []
    mock_git.get_git_common_dir.return_value = ".git"
    
    node = TerminalNode("390")
    
    with mock.patch("orchestrator.node_lifecycle.FlowTransaction") as mock_tx:
        node.reflect("frontier.md", "node-390", "learnings", ["invariants"], "commit-msg", "node/390-test", stage="all")
        
    expected_worktree = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(".git")), ".worktrees/node/390-test"))
    mock_git.add.assert_called_once_with(["."], cwd=expected_worktree)
    mock_git.commit.assert_called_once_with("commit-msg", cwd=expected_worktree)
    mock_git.push.assert_called_once_with("node/390-test", cwd=expected_worktree)

@mock.patch("orchestrator.node_lifecycle.github_client.get_issue_labels")
@mock.patch("orchestrator.node_lifecycle.FlowTransaction")
@mock.patch("orchestrator.node_lifecycle.load_node_status_config")
@mock.patch("orchestrator.node_lifecycle.github_client.get_issue_details")
@mock.patch("orchestrator.node_lifecycle.TerminalNode._verify_state_purity")
@mock.patch("orchestrator.node_lifecycle.TerminalNode._validate_orthogonal_scope")
@mock.patch("orchestrator.node_lifecycle.TerminalNode.set_status")
@mock.patch("orchestrator.node_lifecycle.mgr_frontier.append_active_node")
def test_plan_start_dependency_violation(mock_append, mock_set_status, mock_validate_scope, mock_verify_purity, mock_get_details, mock_load_config, mock_tx, mock_get_labels):
    mock_load_config.return_value = {"in_progress": "status: in-progress"}
    mock_get_labels.return_value = []
    
    def side_effect(issue_id):
        if str(issue_id) == "390":
            return {
                "title": "Probe 390: Plan - title",
                "body": "## Goal\nSome goal\n\n## Depends On\nNode 380",
                "state": "OPEN"
            }
        elif str(issue_id) == "380":
            return {
                "title": "Probe 380: Align - title",
                "body": "Some body",
                "state": "OPEN"
            }
        return {}
        
    mock_get_details.side_effect = side_effect
    
    node = TerminalNode("390")
    
    with pytest.raises(Exception, match="Dependency Violation: Node #390 depends on Node #380, which is still open"):
        node.plan_start("dummy_frontier.md")


@mock.patch("orchestrator.node_lifecycle.github_client.get_issue_labels")
@mock.patch("orchestrator.node_lifecycle.FlowTransaction")
@mock.patch("orchestrator.node_lifecycle.load_node_status_config")
@mock.patch("orchestrator.node_lifecycle.github_client.get_issue_details")
@mock.patch("orchestrator.node_lifecycle.TerminalNode._verify_state_purity")
@mock.patch("orchestrator.node_lifecycle.TerminalNode._validate_orthogonal_scope")
@mock.patch("orchestrator.node_lifecycle.TerminalNode.set_status")
@mock.patch("orchestrator.node_lifecycle.mgr_frontier.append_active_node")
def test_plan_start_dependency_satisfied(mock_append, mock_set_status, mock_validate_scope, mock_verify_purity, mock_get_details, mock_load_config, mock_tx, mock_get_labels):
    mock_load_config.return_value = {"in_progress": "status: in-progress"}
    mock_get_labels.return_value = []
    
    def side_effect(issue_id):
        if str(issue_id) == "390":
            return {
                "title": "Probe 390: Plan - title",
                "body": "## Goal\nSome goal\n\n## Depends On\nNode 380",
                "state": "OPEN"
            }
        elif str(issue_id) == "380":
            return {
                "title": "Probe 380: Align - title",
                "body": "Some body",
                "state": "CLOSED"
            }
        return {}
        
    mock_get_details.side_effect = side_effect
    
    node = TerminalNode("390")
    
    node.plan_start("dummy_frontier.md")
    mock_set_status.assert_called_with("in_progress")

