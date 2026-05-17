import pytest
from unittest.mock import patch, MagicMock
from orchestrator.flow_state_manager import plan_node, reflect_node, sync_and_clean_node

@patch('orchestrator.flow_state_manager.subprocess.run')
@patch('orchestrator.flow_state_manager.github_client')
def test_plan_node(mock_gh, mock_run):
    mock_result = MagicMock()
    mock_result.stdout = '{"title": "Probe: Test Title"}'
    mock_run.return_value = mock_result
    
    result = plan_node("100", "Test Body")
    
    assert result == "https://github.com/pltrinh1122/agent-antigravity/issues/100"
    mock_gh.rename_issue_title.assert_called_once_with("100", "Node 100: Probe: Test Title")
    mock_gh.update_issue_body.assert_called_once_with("100", "Test Body")

@patch('orchestrator.flow_state_manager.github_client')
@patch('orchestrator.flow_state_manager.frontier_editor')
@patch('orchestrator.flow_state_manager.subprocess.run')
def test_reflect_node(mock_run, mock_fe, mock_gh):
    reflect_node(
        frontier_file="/tmp/dummy.md",
        issue_id="100",
        node_name="Node 1: Test",
        learnings="It worked",
        invariants=["[x] Good"],
        commit_msg="Test commit",
        branch_name="node/1-test-branch"
    )
    
    # Verify GitHub closed
    mock_gh.close_issue.assert_called_once_with("100", "Node completed via Flow-State Manager. Moving to PR.")
    
    # Verify Frontier updated
    mock_fe.complete_active_node.assert_called_once_with("/tmp/dummy.md", "Node 1: Test", "It worked", ["[x] Good"])
    
    # Verify Git commands
    assert mock_run.call_count == 3
    
    call_args = [call[0][0] for call in mock_run.call_args_list]
    assert call_args[0] == ["git", "add", "."]
    assert call_args[1] == ["git", "commit", "-m", "Test commit"]
    assert call_args[2] == ["git", "push", "-u", "origin", "node/1-test-branch"]
    
    # Verify PR created
    mock_gh.create_pull_request.assert_called_once_with("Node 1: Test", "Resolves #100\n\nIt worked")

def test_reflect_node_invalid_branch():
    with pytest.raises(ValueError):
        reflect_node(
            frontier_file="/tmp/dummy.md",
            issue_id="100",
            node_name="Node 1: Test",
            learnings="It worked",
            invariants=["[x] Good"],
            commit_msg="Test commit",
            branch_name="invalid_branch_name"
        )

@patch('orchestrator.flow_state_manager.github_client.list_issues_by_label', return_value=[])
@patch('orchestrator.flow_state_manager.subprocess.run')
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

def test_is_verbose():
    """Verifies that is_verbose evaluates the correct environment variables."""
    from orchestrator.flow_state_manager import is_verbose
    import os

    # Standard / silent mode
    with patch.dict(os.environ, {}, clear=True):
        assert not is_verbose()

    # SPAO_VERBOSE enabled
    with patch.dict(os.environ, {"SPAO_VERBOSE": "1"}):
        assert is_verbose()

    # SPOA_VERBOSE enabled (operator fallback spelling)
    with patch.dict(os.environ, {"SPOA_VERBOSE": "true"}):
        assert is_verbose()

def test_log_stage_advancement(capsys):
    """Verifies that log_stage_advancement outputs content only when verbose is active."""
    from orchestrator.flow_state_manager import log_stage_advancement
    import os

    # Verify standard (silent) mode prints nothing
    with patch.dict(os.environ, {}, clear=True):
        log_stage_advancement("sense", "Testing", "Details")
        captured = capsys.readouterr()
        assert not captured.out

    # Verify verbose prints beautiful Stage banner
    with patch.dict(os.environ, {"SPAO_VERBOSE": "1"}):
        log_stage_advancement("sense", "Initiating testing", "Aesthetic checks")
        captured = capsys.readouterr()
        assert "SPAO Loop Stage" in captured.out
        assert "🔍 SENSE" in captured.out
        assert "Initiating testing" in captured.out
        assert "Aesthetic checks" in captured.out

