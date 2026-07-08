import os
import sys
from unittest.mock import patch, MagicMock

from kernel.daemon_status import get_prompt_backlog_size, get_local_worktrees, main

@patch('drivers.github_client.list_issues_by_label')
def test_get_prompt_backlog_size(mock_list):
    mock_list.return_value = [{"number": 1}, {"number": 2}]
    assert get_prompt_backlog_size("/some/repo/root") == 2

def test_get_local_worktrees(tmp_path):
    repo_root = str(tmp_path)
    worktrees_dir = os.path.join(repo_root, ".worktrees")
    
    # Empty case
    assert get_local_worktrees(repo_root) == []
    
    # Create worktrees directory and subdirectories
    os.makedirs(os.path.join(worktrees_dir, "node", "805-implement-status-dashboard"))
    os.makedirs(os.path.join(worktrees_dir, "spao", "806-spao-rules"))
    os.makedirs(os.path.join(worktrees_dir, "sdlc", "807-sdlc-features"))
    os.makedirs(os.path.join(worktrees_dir, "other-worktree"))
    
    # Should be empty because .git file is missing
    assert get_local_worktrees(repo_root) == []
    
    # Create .git files
    with open(os.path.join(worktrees_dir, "node", "805-implement-status-dashboard", ".git"), "w") as f:
        f.write("gitdir: ...")
    with open(os.path.join(worktrees_dir, "spao", "806-spao-rules", ".git"), "w") as f:
        f.write("gitdir: ...")
    with open(os.path.join(worktrees_dir, "sdlc", "807-sdlc-features", ".git"), "w") as f:
        f.write("gitdir: ...")
    with open(os.path.join(worktrees_dir, "other-worktree", ".git"), "w") as f:
        f.write("gitdir: ...")
        
    result = get_local_worktrees(repo_root)
    assert len(result) == 4
    
    # They should be sorted numerically
    assert result[0]["number"] == 805
    assert result[0]["title"] == "Implement status dashboard"
    assert result[0]["url"] == "local:node/805-implement-status-dashboard"
    
    assert result[1]["number"] == 806
    assert result[1]["title"] == "Spao rules"
    assert result[1]["url"] == "local:spao/806-spao-rules"
    
    assert result[2]["number"] == 807
    assert result[2]["title"] == "Sdlc features"
    assert result[2]["url"] == "local:sdlc/807-sdlc-features"
    
    # The one directly under .worktrees
    assert result[3]["number"] == "?"
    assert result[3]["title"] == "Other worktree"
    assert result[3]["url"] == "local:other-worktree"

@patch("kernel.daemon_status.get_current_branch")
@patch("kernel.daemon_status.get_local_worktrees")
@patch("subprocess.run")
def test_main(mock_subprocess, mock_worktrees, mock_branch, capsys):
    mock_proc = MagicMock(returncode=0)
    mock_proc.stdout = "123\tstatus: in-progress\tTest Issue"
    mock_subprocess.return_value = mock_proc
    mock_branch.return_value = "node/805-status-dashboard"
    mock_worktrees.return_value = [{"number": 1, "title": "Test PR", "url": "local:node/1-test-pr"}]
    
    with patch("kernel.daemon_status.repo_root", "/tmp"):
        with patch("os.path.exists", return_value=True):
            main()
            
    captured = capsys.readouterr()
    assert "Active Nodes (In-Progress):" in captured.out
    assert "123\tstatus: in-progress\tTest Issue" in captured.out
    assert "WIP Branch  : node/805-status-dashboard" in captured.out
    assert "Local Worktrees: 1" in captured.out
    assert "- #1: Test PR" in captured.out

@patch("drivers.github_client.list_issues_by_label")
@patch("kernel.daemon_strategic.load_ledger")
@patch("drivers.github_client.get_issue_details")
def test_print_goal_progress_report(mock_details, mock_ledger, mock_list_issues, capsys):
    from kernel.daemon_status import print_goal_progress_report
    
    mock_ledger.return_value = {
        "strategic_goals": [
            {
                "id": "SG-0004",
                "title": "Test Goal",
                "status": "Active",
                "prioritized_paths": [916, 999]
            }
        ]
    }
    
    mock_list_issues.return_value = [
        {
            "number": 999,
            "title": "Path 999: Open Path",
            "labels": [{"name": "path"}]
        }
    ]
    
    mock_details.return_value = {
        "title": "Path 916: Completed Path"
    }
    
    print_goal_progress_report()
    
    captured = capsys.readouterr()
    assert "🎯 [SG-0004] Test Goal" in captured.out
    assert "[█████░░░░░] 50.0% (1/2)" in captured.out
    assert "[x] Path 916: Completed Path" in captured.out
    assert "[ ] Path 999: Open Path" in captured.out

def test_main_dispatcher_auto_lock(capsys, monkeypatch):
    import kernel.daemon_status
    import kernel.daemon_nba
    import subprocess
    
    monkeypatch.setattr(kernel.daemon_status, "get_current_branch", lambda cwd=None: "main")
    monkeypatch.setattr(kernel.daemon_status, "get_local_worktrees", lambda repo: [])
    
    mock_proc = MagicMock(returncode=0)
    # It first runs `gh issue list`, we should return empty for no active nodes
    def run_side_effect(*args, **kwargs):
        res = MagicMock(returncode=0)
        if "issue" in args[0]:
            res.stdout = ""
        else:
            res.stdout = "ℹ️  Auto-resolved SPAO_PERSONA_ID to 'agent-sg5' for Path #802"
        res.stderr = ""
        return res
    monkeypatch.setattr(subprocess, "run", run_side_effect)
    
    monkeypatch.setattr(kernel.daemon_nba.NBADaemon, "evaluate", lambda self, frontier_file, local_mode=False: {
        "type": "path_continuation",
        "recommendations": [{"id": 805, "title": "Act - Something"}]
    })
    
    with patch("kernel.daemon_status.repo_root", "/tmp"):
        with patch("os.path.exists", return_value=True):
            kernel.daemon_status.main()
            
    captured = capsys.readouterr()
    assert "[🤖 AUTONOMY] WIP=0 detected. Automatically acquiring lock for top NBA: Node 805..." in captured.out
    assert "[🤖 DISPATCH] NBA Auto-Locked for subagent agent-sg5. Main Agent MUST use invoke_subagent to dispatch this node." in captured.out
