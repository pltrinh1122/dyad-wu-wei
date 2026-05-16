import pytest
from unittest.mock import patch
from skills.flow_state_manager import plan_node, reflect_node

@patch('skills.flow_state_manager.github_client')
def test_plan_node(mock_gh):
    mock_gh.create_issue.return_value = "https://github.com/org/repo/issues/100"
    
    result = plan_node("Test Title", "Test Body")
    
    assert result == "https://github.com/org/repo/issues/100"
    mock_gh.create_issue.assert_called_once_with("Test Title", "Test Body")

@patch('skills.flow_state_manager.github_client')
@patch('skills.flow_state_manager.frontier_editor')
@patch('skills.flow_state_manager.subprocess.run')
def test_reflect_node(mock_run, mock_fe, mock_gh):
    reflect_node(
        frontier_file="/tmp/dummy.md",
        issue_id="100",
        node_name="Node 1: Test",
        learnings="It worked",
        invariants=["[x] Good"],
        commit_msg="Test commit"
    )
    
    # Verify GitHub closed
    mock_gh.close_issue.assert_called_once_with("100", "Node completed via Flow-State Manager.")
    
    # Verify Frontier updated
    mock_fe.complete_active_node.assert_called_once_with("/tmp/dummy.md", "Node 1: Test", "It worked", ["[x] Good"])
    
    # Verify Git commands
    assert mock_run.call_count == 3
    
    call_args = [call[0][0] for call in mock_run.call_args_list]
    assert call_args[0] == ["git", "add", "."]
    assert call_args[1] == ["git", "commit", "-m", "Test commit"]
    assert call_args[2] == ["git", "push", "origin", "main"]
