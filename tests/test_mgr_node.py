import pytest
from unittest.mock import patch, MagicMock
from orchestrator.mgr_node import plan_start_node, plan_finish_node, checkout_node, reflect_node

@patch('orchestrator.mgr_telemetry.TelemetryManager')
@patch('orchestrator.node_lifecycle.TelemetryManager')
@patch('orchestrator.node_lifecycle.github_client')
@patch('orchestrator.node_lifecycle.frontier_editor')
@patch('orchestrator.node_lifecycle.mgr_backlog')
@patch('orchestrator.node_lifecycle.subprocess.run')
def test_plan_start_node(mock_run, mock_backlog, mock_fe, mock_gh, mock_tm_lifecycle, mock_tm_telemetry):
    mock_gh.get_issue_labels.return_value = []
    mock_gh.get_issue_details.return_value = {"title": "Test Title"}
    mock_fe.read_active_node.return_value = "None"
    
    plan_start_node("157")
    
    mock_gh.add_label.assert_called_with("157", "status: in-progress")
    mock_fe.append_active_node.assert_called_once()

@patch('orchestrator.node_lifecycle.github_client')
@patch('orchestrator.node_lifecycle.frontier_editor')
def test_plan_start_node_locked(mock_fe, mock_gh):
    mock_gh.get_issue_labels.return_value = ["status: in-progress"]
    mock_fe.read_active_node.return_value = "None"
    with pytest.raises(Exception, match="already in progress"):
        plan_start_node("157")

@patch('orchestrator.mgr_telemetry.TelemetryManager')
@patch('orchestrator.node_lifecycle.TelemetryManager')
@patch('orchestrator.node_lifecycle.github_client')
@patch('orchestrator.node_lifecycle.frontier_editor')
@patch('orchestrator.node_lifecycle.subprocess.run')
def test_checkout_node(mock_run, mock_fe, mock_gh, mock_tm_lifecycle, mock_tm_telemetry):
    mock_fe.read_active_node.return_value = "None"
    checkout_node("157", "node/157-test-branch")
    mock_gh.add_label.assert_called_with("157", "status: in-progress")
    mock_run.assert_called()

@patch('orchestrator.mgr_telemetry.TelemetryManager')
@patch('orchestrator.node_lifecycle.TelemetryManager')
@patch('orchestrator.node_lifecycle.github_client')
@patch('orchestrator.node_lifecycle.frontier_editor')
@patch('orchestrator.node_lifecycle.mgr_backlog')
@patch('orchestrator.node_lifecycle.subprocess.run')
@patch('orchestrator.node_lifecycle.mgr_nba')
def test_reflect_node(mock_nba, mock_run, mock_backlog, mock_fe, mock_gh, mock_tm_lifecycle, mock_tm_telemetry):
    mock_nba.NBAManager.return_value.evaluate.return_value = {
        "type": "path_switching",
        "recommendations": []
    }
    mock_fe.read_active_path.return_value = "Path 181: Configurable Sense Hooks"
    mock_fe.extract_path_id.return_value = "181"
    
    reflect_node(
        frontier_file="/tmp/dummy.md",
        issue_id="100",
        node_name="Node 1: Test",
        learnings="It worked",
        invariants=["[x] Good"],
        commit_msg="Test commit",
        branch_name="node/100-test-branch"
    )

    mock_gh.close_issue.assert_any_call("100", "Node completed via Flow-State Manager. Moving to PR.")
    mock_gh.close_issue.assert_any_call("181", "Path Invariant Enforced: Automatically closed because the final child Activity has been completed.")
    mock_fe.set_active_path.assert_called_once_with("/tmp/dummy.md", "None")
    mock_fe.complete_active_node.assert_called_once_with("/tmp/dummy.md", "Node 1: Test", "It worked", ["[x] Good"], clear_pointers=True)
