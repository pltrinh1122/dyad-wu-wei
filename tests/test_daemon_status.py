import os
import sys
from unittest.mock import patch, MagicMock

from kernel.daemon_status import get_prompt_backlog_size, main

def test_get_prompt_backlog_size(tmp_path):
    repo_root = str(tmp_path)
    artifacts_dir = os.path.join(repo_root, "artifacts")
    os.makedirs(artifacts_dir)
    yaml_path = os.path.join(artifacts_dir, "prompt_backlog.yml")
    
    with open(yaml_path, "w") as f:
        f.write("prompts:\n  - msg: 1\n  - msg: 2\n")
        
    assert get_prompt_backlog_size(repo_root) == 2

@patch("kernel.daemon_status.get_current_branch")
@patch("kernel.daemon_status.get_open_prs")
@patch("kernel.daemon_status.read_active_path")
@patch("kernel.daemon_status.read_active_node")
def test_main(mock_node, mock_path, mock_prs, mock_branch, capsys):
    mock_node.return_value = "805"
    mock_path.return_value = "802"
    mock_branch.return_value = "node/805-status-dashboard"
    mock_prs.return_value = [{"number": 1, "title": "Test PR", "url": "http"}]
    
    with patch("kernel.daemon_status.repo_root", "/tmp"):
        with patch("os.path.exists", return_value=True):
            main()
            
    captured = capsys.readouterr()
    assert "Active Path : 802" in captured.out
    assert "Active Node : 805" in captured.out
    assert "WIP Branch  : node/805-status-dashboard" in captured.out
    assert "Open PRs    : 1" in captured.out
    assert "- #1: Test PR" in captured.out
