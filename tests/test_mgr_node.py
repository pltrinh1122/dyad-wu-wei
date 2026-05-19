import pytest
from unittest.mock import patch, MagicMock
from orchestrator.mgr_node import reflect_node, sync_and_clean_node, plan_start_node, plan_finish_node, checkout_node

@patch('orchestrator.node_lifecycle.TerminalNode._validate_orthogonal_scope')
@patch('orchestrator.node_lifecycle.github_client')
def test_plan_start_node(mock_gh, mock_validate):
    mock_gh.get_issue_labels.return_value = ["backlog"]
    
    plan_start_node("100")
    
    mock_validate.assert_called_once()
    mock_gh.add_label.assert_called_once_with("100", "status: in-progress")

@patch('orchestrator.node_lifecycle.github_client')
def test_plan_start_node_locked(mock_gh):
    mock_gh.get_issue_labels.return_value = ["status: in-progress"]
    
    with pytest.raises(Exception, match="Node #100 is already in progress by another thread!"):
        plan_start_node("100")
        
@patch('orchestrator.node_lifecycle.github_client.get_open_issues')
@patch('orchestrator.node_lifecycle.github_client.get_issue_details')
def test_orthogonal_scope_validation(mock_details, mock_issues):
    from orchestrator.node_lifecycle import TerminalNode
    node = TerminalNode("100")
    
    mock_details.return_value = {
        "title": "Node 100: Activity: Do work",
        "body": "## Goal\nDo some work\n"
    }
    
    mock_issues.return_value = [
        {"number": 100, "title": "Node 100: Activity: Do work", "body": "## Goal\nDo some work\n"},
        {"number": 101, "title": "Node 101: Activity: Do other work", "body": "## Goal\nDo some work\n"}
    ]
    
    with pytest.raises(Exception, match="Orthogonal Scope Violation: Node 100 has an identical goal footprint to Node 101"):
        node._validate_orthogonal_scope()

    mock_issues.return_value = [
        {"number": 100, "title": "Node 100: Activity: Do work", "body": "## Goal\nDo some work\n"},
        {"number": 101, "title": "Node 101: Activity: Do work", "body": "## Goal\nDo some other work\n"}
    ]
    
    with pytest.raises(Exception, match="Orthogonal Scope Violation: Node 100 has an identical title footprint to Node 101"):
        node._validate_orthogonal_scope()

@patch('orchestrator.node_lifecycle.subprocess.run')
@patch('orchestrator.node_lifecycle.github_client')
def test_plan_finish_node(mock_gh, mock_run):
    mock_result = MagicMock()
    mock_result.stdout = '{"title": "Probe: Test Title"}'
    mock_run.return_value = mock_result
    
    result = plan_finish_node("100", "Test Body")
    
    assert result == "https://github.com/pltrinh1122/agent-antigravity/issues/100"
    mock_gh.rename_issue_title.assert_called_once_with("100", "Node 100: Probe: Test Title")
    mock_gh.update_issue_body.assert_called_once_with("100", "Test Body")

@patch('orchestrator.node_lifecycle.subprocess.run')
@patch('orchestrator.node_lifecycle.github_client')
@patch('orchestrator.node_lifecycle.os.makedirs')
def test_checkout_node(mock_makedirs, mock_gh, mock_run):
    checkout_node("157", "node/157-test")
    
    mock_gh.add_label.assert_called_once_with("157", "status: in-progress")
    
    mock_run.assert_called_once()
    assert mock_run.call_args[0][0] == ["git", "worktree", "add", "-b", "node/157-test", ".worktrees/node/157-test", "main"]

@patch('orchestrator.node_lifecycle.github_client')
@patch('orchestrator.node_lifecycle.frontier_editor')
@patch('orchestrator.node_lifecycle.subprocess.run')
@patch('skills.nba_evaluator.evaluate')
def test_reflect_node(mock_evaluate, mock_run, mock_fe, mock_gh):
    mock_evaluate.return_value = {
        "mode": "path_switching",
        "active_path": "Path 181: Configurable Sense Hooks",
        "recommended": [],
        "message": ""
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
        branch_name="node/1-test-branch"
    )
    
    mock_gh.close_issue.assert_any_call("100", "Node completed via Flow-State Manager. Moving to PR.")
    mock_gh.close_issue.assert_any_call("181", "Path Invariant Enforced: Automatically closed because the final child Activity has been completed.")
    mock_fe.set_active_path.assert_called_once_with("/tmp/dummy.md", "None")
    mock_fe.complete_active_node.assert_called_once_with("/tmp/dummy.md", "Node 1: Test", "It worked", ["[x] Good"])
    
    assert mock_run.call_count == 3
    call_args = [call[0][0] for call in mock_run.call_args_list]
    assert call_args[0] == ["git", "add", "."]
    assert call_args[1] == ["git", "commit", "-m", "Test commit"]
    assert call_args[2] == ["git", "push", "-u", "origin", "node/1-test-branch"]
    
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

@patch('orchestrator.mgr_node.github_client.get_open_prs', return_value=[])
@patch('orchestrator.mgr_node.github_client.get_merged_prs', return_value=[{"headRefName": "node/2-test"}])
@patch('orchestrator.mgr_node.HookManager')
@patch('orchestrator.mgr_node.subprocess.run')
def test_sync_and_clean_node(mock_run, mock_hm, mock_get_merged_prs, mock_get_open_prs):
    mock_result = MagicMock()
    mock_result.stdout = "main\nnode/1-test\nold-branch\nnode/2-test\n"
    mock_run.return_value = mock_result
    
    sync_and_clean_node()
    
    call_args = [call[0][0] for call in mock_run.call_args_list]
    assert ["git", "switch", "main"] in call_args
    assert ["git", "pull", "--prune", "origin", "main"] in call_args
    assert ["git", "branch", "--merged"] in call_args
    assert ["git", "worktree", "prune"] in call_args
    assert ["git", "branch", "-D", "node/1-test"] in call_args
    assert ["git", "branch", "-D", "old-branch"] in call_args
    assert ["git", "branch", "-D", "node/2-test"] in call_args
    
    mock_hm.return_value.execute_all.assert_called_once()
    mock_get_merged_prs.assert_called_once_with(limit=50)
    mock_get_open_prs.assert_called_once()

@patch('orchestrator.mgr_node.github_client.get_open_prs')
def test_sync_and_clean_node_with_open_prs(mock_get_open_prs):
    mock_get_open_prs.return_value = [{"number": 123, "headRefName": "node/123-test", "title": "Test PR", "url": "http"}]
    
    with pytest.raises(Exception, match="WIP-N=1 Violation: Cannot initiate SENSE phase while PRs are still open: #123 \\(node/123-test\\)"):
        sync_and_clean_node()
    
    mock_get_open_prs.assert_called_once()

def test_is_verbose():
    from orchestrator.mgr_node import is_verbose
    import os

    with patch.dict(os.environ, {}, clear=True):
        assert not is_verbose()

    with patch.dict(os.environ, {"SPAO_VERBOSE": "1"}):
        assert is_verbose()

    with patch.dict(os.environ, {"SPOA_VERBOSE": "true"}):
        assert is_verbose()

def test_log_stage_advancement(capsys):
    from orchestrator.node_lifecycle import log_stage_advancement
    import os

    with patch.dict(os.environ, {}, clear=True):
        log_stage_advancement("sense", "Testing", "Details")
        captured = capsys.readouterr()
        assert not captured.out

    with patch.dict(os.environ, {"SPAO_VERBOSE": "1"}):
        log_stage_advancement("sense", "Initiating testing", "Aesthetic checks")
        captured = capsys.readouterr()
        assert "SPAO Loop Stage" in captured.out
        assert "🔍 SENSE" in captured.out
        assert "Initiating testing" in captured.out
        assert "Aesthetic checks" in captured.out

@patch("orchestrator.mgr_node.BaseNode")
def test_cmd_set_status(mock_base_node):
    from orchestrator.mgr_node import cmd_set_status
    args = MagicMock()
    args.issue_id = "123"
    args.status_key = "todo"
    
    cmd_set_status(args)
    mock_base_node.assert_called_once_with("123")
    mock_base_node.return_value.set_status.assert_called_once_with("todo")

@patch("orchestrator.mgr_node.BaseNode")
def test_cmd_set_classification(mock_base_node):
    from orchestrator.mgr_node import cmd_set_classification
    args = MagicMock()
    args.issue_id = "123"
    args.classification_key = "backlog"
    
    cmd_set_classification(args)
    mock_base_node.assert_called_once_with("123")
    mock_base_node.return_value.set_classification.assert_called_once_with("backlog")
