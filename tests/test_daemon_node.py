import pytest
from unittest.mock import MagicMock, patch
from kernel.daemon_node import plan_start_node, plan_finish_node, checkout_node, reflect_node, sync_and_clean_node


def test_plan_start_node(mock_gh, mock_fe, mock_telemetry, mock_backlog, mock_subprocess):
    # Setup
    mock_gh.get_issue_labels.return_value = []
    mock_gh.get_issue_details.return_value = {"title": "Test Title"}
    mock_fe.read_active_node.return_value = "None"
    mock_gh.get_open_prs.return_value = []
    
    # Act
    plan_start_node("157")
    
    # Assert
    mock_gh.add_label.assert_called_with("157", "status: in-progress")
    mock_fe.append_active_node.assert_called_once()

def test_plan_start_node_locked(mock_gh, mock_fe):
    # Setup
    mock_gh.get_issue_labels.return_value = ["status: in-progress"]
    mock_fe.read_active_node.return_value = "None"
    mock_gh.get_open_prs.return_value = []
    
    # Act & Assert
    with pytest.raises(Exception, match="already in progress"):
        plan_start_node("157")

def test_checkout_node(mock_gh, mock_fe, mock_telemetry, mock_subprocess):
    # Setup
    mock_fe.read_active_node.return_value = "None"
    mock_gh.get_open_prs.return_value = []
    
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
    mock_gh.close_issue.assert_any_call("100", "Node completed via Node Lifecycle Daemon. Moving to PR.")
    mock_gh.close_issue.assert_any_call("181", "Path Invariant Enforced: Automatically closed because the final child Activity has been completed.")
    mock_fe.set_active_path.assert_called_once_with("/tmp/dummy.md", "None")
    mock_fe.complete_active_node.assert_called_once_with("/tmp/dummy.md", "Node 1: Test", "It worked", ["[x] Good"], clear_pointers=True)


def test_sync_and_clean_node_order():
    daemon = MagicMock()
    with patch("kernel.daemon_node.git_client") as mock_git, \
         patch("kernel.daemon_node.github_client") as mock_gh, \
         patch("kernel.daemon_node.subprocess") as mock_sub, \
         patch("kernel.daemon_node.HookDaemon") as mock_hook, \
         patch("kernel.daemon_node.get_local_worktrees", return_value=[]), \
         patch("kernel.daemon_node.os.path.exists", return_value=False):
        
        daemon.attach_mock(mock_git, 'git')
        daemon.attach_mock(mock_gh, 'gh')
        
        mock_git.list_merged_branches.return_value = []
        mock_git.list_local_branches.return_value = []
        
        sync_and_clean_node()
        
        calls = daemon.mock_calls
        filtered_calls = [
            (call[0], call[1], call[2]) for call in calls 
            if call[0] in ('git.fetch', 'git.switch', 'gh.get_open_prs')
        ]
        
        # Local Mode: should switch but NOT fetch or get open prs
        assert filtered_calls == [
            ('git.switch', ('origin/main',), {'detach': True})
        ]

def test_sync_and_clean_node_remote_mode():
    daemon = MagicMock()
    backlog_content = """
prompts:
  - id: p-123
    timestamp: '2026-05-23T21:00:00Z'
    text: '[NOTIFICATION] Sluice Gate Opened: PR for Node 878'
    status: pending
"""
    from unittest.mock import mock_open
    with patch("kernel.daemon_node.git_client") as mock_git, \
         patch("kernel.daemon_node.github_client") as mock_gh, \
         patch("kernel.daemon_node.subprocess") as mock_sub, \
         patch("kernel.daemon_node.HookDaemon") as mock_hook, \
         patch("kernel.daemon_node.os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data=backlog_content.encode('utf-8'))), \
         patch("kernel.daemon_node.process_prompts") as mock_process, \
         patch("kernel.daemon_node.clean_prompts") as mock_clean:
        
        daemon.attach_mock(mock_git, 'git')
        daemon.attach_mock(mock_gh, 'gh')
        
        mock_gh.get_open_prs.return_value = []
        mock_gh.get_merged_prs.return_value = []
        mock_git.list_merged_branches.return_value = []
        mock_git.list_local_branches.return_value = []
        
        sync_and_clean_node()
        
        calls = daemon.mock_calls
        filtered_calls = [
            (call[0], call[1], call[2]) for call in calls 
            if call[0] in ('git.fetch', 'git.switch', 'gh.get_open_prs')
        ]
        
        # Remote Mode: should fetch, switch, and query get_open_prs
        assert filtered_calls == [
            ('git.fetch', ('origin',), {'prune': True}),
            ('git.switch', ('origin/main',), {'detach': True}),
            ('gh.get_open_prs', (), {})
        ]
        mock_process.assert_called_once_with("p-123", resolution_context="sync")
        mock_clean.assert_called_once()

def test_sync_and_clean_node_wip_violation():
    with patch("kernel.daemon_node.git_client"), \
         patch("kernel.daemon_node.github_client"), \
         patch("kernel.daemon_node.subprocess"), \
         patch("kernel.daemon_node.HookDaemon"), \
         patch("kernel.daemon_node.get_local_worktrees") as mock_wt, \
         patch("kernel.daemon_node.os.path.exists", return_value=False):
        
        mock_wt.return_value = [{"number": 123, "url": "local:node/123-some-branch"}]
        
        with pytest.raises(Exception, match="WIP-N=1 Violation"):
            sync_and_clean_node()
            
    backlog_content = "prompts:\n  - id: p-123\n    text: '[NOTIFICATION] Sluice Gate Opened: PR for Node 878'\n    status: pending"
    from unittest.mock import mock_open
    with patch("kernel.daemon_node.git_client"), \
         patch("kernel.daemon_node.github_client") as mock_gh, \
         patch("kernel.daemon_node.subprocess"), \
         patch("kernel.daemon_node.HookDaemon"), \
         patch("kernel.daemon_node.os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data=backlog_content.encode('utf-8'))):
        
        mock_gh.get_open_prs.return_value = [{"number": 123, "headRefName": "some-branch"}]
        
        with pytest.raises(Exception, match="WIP-N=1 Violation"):
            sync_and_clean_node()

def test_sync_and_clean_node_rom_drift(capsys):
    from unittest.mock import mock_open
    with patch("kernel.daemon_node.git_client"), \
         patch("kernel.daemon_node.github_client") as mock_gh, \
         patch("kernel.daemon_node.os.path.exists") as mock_exists, \
         patch("builtins.open") as mock_file, \
         patch("kernel.daemon_node.hashlib.sha256") as mock_sha256, \
         patch("kernel.daemon_node.HookDaemon"), \
         patch("kernel.daemon_node.get_local_worktrees", return_value=[]):
        
        def exists_side_effect(path):
            if "prompt_backlog" in path:
                return False
            return True
        mock_exists.side_effect = exists_side_effect
        
        mock_file.return_value = mock_open(read_data=b"data")()
        
        mock_hash1 = MagicMock()
        mock_hash1.hexdigest.return_value = "hash1"
        mock_hash2 = MagicMock()
        mock_hash2.hexdigest.return_value = "hash2"
        mock_sha256.side_effect = [mock_hash1, mock_hash2]
        
        with pytest.raises(Exception, match="CRITICAL ROM DRIFT DETECTED"):
            sync_and_clean_node()


def test_cmd_retro_compile():
    args = MagicMock()
    args.retro_command = "compile"
    args.start_path = "860"
    args.end_path = "860"
    args.output_path = None
    
    with patch("kernel.daemon_retro.RetroCompiler") as mock_compiler_cls:
        from kernel.daemon_node import cmd_retro
        cmd_retro(args)
        
        mock_compiler_cls.assert_called_once_with("860", "860")
        mock_compiler_cls.return_value.compile.assert_called_once_with(None)

def test_cmd_retro_list(capsys):
    args = MagicMock()
    args.retro_command = "list"
    
    with patch("glob.glob") as mock_glob:
        mock_glob.return_value = ["artifacts/retrospective_path_860_860.md"]
        from kernel.daemon_node import cmd_retro
        cmd_retro(args)
        
        captured = capsys.readouterr()
        assert "retrospective_path_860_860.md" in captured.out

def test_cmd_retro_view():
    args = MagicMock()
    args.retro_command = "view"
    args.start_path = "860"
    args.end_path = None
    
    from unittest.mock import mock_open
    with patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data="retro contents")):
        from kernel.daemon_node import cmd_retro
        with patch("builtins.print") as mock_print:
            cmd_retro(args)
            mock_print.assert_called_once_with("retro contents")


def test_cmd_retro_attach(tmp_path):
    """Happy path: retro attach stages, commits, and pushes the retro file."""
    retro_file = tmp_path / "retro-806.md"
    retro_file.write_text("# Retro 806\nTest retro content.\n")

    args = MagicMock()
    args.retro_command = "attach"
    args.issue_id = "806"
    args.retro_file = str(retro_file)
    args.branch_name = "node/806-implement-bin-node-retro-attach"

    with patch("kernel.node_lifecycle.TerminalNode.retro_attach", return_value=str(retro_file)) as mock_attach:
        from kernel.daemon_node import cmd_retro
        cmd_retro(args)
        mock_attach.assert_called_once_with(str(retro_file), "node/806-implement-bin-node-retro-attach")


def test_retro_attach_file_not_found(tmp_path):
    """Error case: retro_attach raises FileNotFoundError for a missing retro file."""
    import pytest
    from kernel.node_lifecycle import TerminalNode

    with patch("drivers.path_resolver.get_workspace_dir", return_value=str(tmp_path)), \
         patch("kernel.node_lifecycle.TerminalNode.get_worktree_path", return_value=str(tmp_path)):
        node = TerminalNode("806")
        with pytest.raises(FileNotFoundError, match="does not exist"):
            node.retro_attach("artifacts/audit/retro-806-nonexistent.md", "node/806-test")

