import pytest
from unittest.mock import patch, MagicMock
from skills.flow_state_manager import plan_node, reflect_node, sync_and_clean_node

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
        commit_msg="Test commit",
        branch_name="node/1-test-branch",
        pr_title="PR Title"
    )
    
    # Verify GitHub closed
    mock_gh.close_issue.assert_called_once_with("100", "Node completed via Flow-State Manager. Moving to PR.")
    
    # Verify Frontier updated
    mock_fe.complete_active_node.assert_called_once_with("/tmp/dummy.md", "Node 1: Test", "It worked", ["[x] Good"])
    
    # Verify Git commands
    assert mock_run.call_count == 4
    
    call_args = [call[0][0] for call in mock_run.call_args_list]
    assert call_args[0] == ["git", "checkout", "-b", "node/1-test-branch"]
    assert call_args[1] == ["git", "add", "."]
    assert call_args[2] == ["git", "commit", "-m", "Test commit"]
    assert call_args[3] == ["git", "push", "-u", "origin", "node/1-test-branch"]
    
    # Verify PR created
    mock_gh.create_pull_request.assert_called_once_with("PR Title", "Resolves #100\n\nIt worked")

def test_reflect_node_invalid_branch():
    with pytest.raises(ValueError):
        reflect_node(
            frontier_file="/tmp/dummy.md",
            issue_id="100",
            node_name="Node 1: Test",
            learnings="It worked",
            invariants=["[x] Good"],
            commit_msg="Test commit",
            branch_name="invalid_branch_name",
            pr_title="PR Title"
        )

@patch('skills.flow_state_manager.github_client.list_issues_by_label', return_value=[])
@patch('skills.flow_state_manager.subprocess.run')
def test_sync_and_clean_node(mock_run, mock_list):
    mock_result = MagicMock()
    mock_result.stdout = "  main\n* node/1-test\n  old-branch\n"
    mock_run.return_value = mock_result
    
    sync_and_clean_node()
    
    # It should run switch, pull, list merged, then delete 'node/1-test' and 'old-branch'
    call_args = [call[0][0] for call in mock_run.call_args_list]
    assert ["git", "switch", "main"] in call_args
    assert ["git", "pull", "--prune", "origin", "main"] in call_args
    assert ["git", "branch", "--merged"] in call_args
    assert ["git", "branch", "-d", "node/1-test"] in call_args
    assert ["git", "branch", "-d", "old-branch"] in call_args
    mock_list.assert_called_once_with("backlog")
