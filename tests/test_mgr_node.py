import pytest
from unittest.mock import MagicMock
from orchestrator.mgr_node import plan_start_node, plan_finish_node, checkout_node, reflect_node

def test_plan_start_node(mock_gh, mock_fe, mock_telemetry, mock_backlog, mock_subprocess):
    # Setup
    mock_gh.get_issue_labels.return_value = []
    mock_gh.get_issue_details.return_value = {"title": "Test Title"}
    mock_fe.read_active_node.return_value = "None"
    
    # Act
    plan_start_node("157")
    
    # Assert
    mock_gh.add_label.assert_called_with("157", "status: in-progress")
    mock_fe.append_active_node.assert_called_once()

def test_plan_start_node_locked(mock_gh, mock_fe):
    # Setup
    mock_gh.get_issue_labels.return_value = ["status: in-progress"]
    mock_fe.read_active_node.return_value = "None"
    
    # Act & Assert
    with pytest.raises(Exception, match="already in progress"):
        plan_start_node("157")

def test_checkout_node(mock_gh, mock_fe, mock_telemetry, mock_subprocess):
    # Setup
    mock_fe.read_active_node.return_value = "None"
    
    # Act
    checkout_node("157", "node/157-test-branch")
    
    # Assert
    mock_gh.add_label.assert_called_with("157", "status: in-progress")
    mock_subprocess.assert_called()

def test_reflect_node(mock_gh, mock_fe, mock_telemetry, mock_backlog, mock_subprocess, mock_nba):
    # Setup
    mock_fe.read_active_path.return_value = "Path 181: Configurable Sense Hooks"
    mock_fe.extract_path_id.return_value = "181"
    
    # Act
    reflect_node(
        frontier_file="/tmp/dummy.md",
        issue_id="100",
        node_name="Node 1: Test",
        learnings="It worked",
        invariants=["[x] Good"],
        commit_msg="Test commit",
        branch_name="node/100-test-branch"
    )

    # Assert
    mock_gh.close_issue.assert_any_call("100", "Node completed via Flow-State Manager. Moving to PR.")
    mock_gh.close_issue.assert_any_call("181", "Path Invariant Enforced: Automatically closed because the final child Activity has been completed.")
    mock_fe.set_active_path.assert_called_once_with("/tmp/dummy.md", "None")
    mock_fe.complete_active_node.assert_called_once_with("/tmp/dummy.md", "Node 1: Test", "It worked", ["[x] Good"], clear_pointers=True)
