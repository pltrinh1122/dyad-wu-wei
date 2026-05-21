import pytest
from unittest.mock import MagicMock, patch
from orchestrator.mgr_node import plan_start_node, plan_finish_node, checkout_node, reflect_node, sync_and_clean_node


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


def test_sync_and_clean_node_order():
    manager = MagicMock()
    with patch("orchestrator.mgr_node.git_client") as mock_git, \
         patch("orchestrator.mgr_node.github_client") as mock_gh, \
         patch("orchestrator.mgr_node.subprocess") as mock_sub, \
         patch("orchestrator.mgr_node.HookManager") as mock_hook:
        
        manager.attach_mock(mock_git, 'git')
        manager.attach_mock(mock_gh, 'gh')
        
        mock_gh.get_open_prs.return_value = []
        mock_git.list_merged_branches.return_value = []
        mock_git.list_local_branches.return_value = []
        
        sync_and_clean_node()
        
        calls = manager.mock_calls
        filtered_calls = [
            (call[0], call[1], call[2]) for call in calls 
            if call[0] in ('git.fetch', 'git.switch', 'gh.get_open_prs')
        ]
        
        assert filtered_calls == [
            ('git.fetch', ('origin',), {'prune': True}),
            ('git.switch', ('origin/main',), {'detach': True}),
            ('gh.get_open_prs', (), {})
        ]


def test_sync_and_clean_node_wip_violation():
    manager = MagicMock()
    with patch("orchestrator.mgr_node.git_client") as mock_git, \
         patch("orchestrator.mgr_node.github_client") as mock_gh, \
         patch("orchestrator.mgr_node.subprocess") as mock_sub, \
         patch("orchestrator.mgr_node.HookManager") as mock_hook:
        
        manager.attach_mock(mock_git, 'git')
        manager.attach_mock(mock_gh, 'gh')
        
        mock_gh.get_open_prs.return_value = [{"number": 123, "headRefName": "some-branch"}]
        
        with pytest.raises(Exception, match="WIP-N=1 Violation"):
            sync_and_clean_node()
            
        calls = manager.mock_calls
        filtered_calls = [
            (call[0], call[1], call[2]) for call in calls 
            if call[0] in ('git.fetch', 'git.switch', 'gh.get_open_prs')
        ]
        
        assert filtered_calls == [
            ('git.fetch', ('origin',), {'prune': True}),
            ('git.switch', ('origin/main',), {'detach': True}),
            ('gh.get_open_prs', (), {})
        ]

