import os
import json
import pytest
from unittest.mock import patch, MagicMock, mock_open

from kernel.daemon_knowledge_accrual import (
    get_repo_root,
    run_kb_check,
    enforce_reflection_hook,
    inject_contextual_rules
)

def test_get_repo_root():
    with patch("drivers.path_resolver.get_workspace_dir", return_value="/mock/workspace"):
        assert get_repo_root() == "/mock/workspace"

def test_run_kb_check_fallback_diff():
    # Test lines 29-34: if diff HEAD fails, use diff
    with patch("subprocess.run") as mock_run, \
         patch("drivers.knowledge_accrual_skill.check_kb_conflicts", return_value=[]):
        
        # First call fails, second call succeeds
        def run_side_effect(cmd, *args, **kwargs):
            m = MagicMock()
            if cmd == ["git", "diff", "HEAD"]:
                m.returncode = 1
                m.stdout = ""
            else:
                m.returncode = 0
                m.stdout = "diff text"
            return m
            
        mock_run.side_effect = run_side_effect
        assert run_kb_check("/mock/repo", strict=True) is True

def test_enforce_reflection_hook_worktree_retro():
    # Lines 85-87
    mock_telemetry = '{"node_id": "544", "event": "FAILURE", "metadata": {"error": "some failure"}}\n'
    with patch("builtins.open", mock_open(read_data=mock_telemetry)):
        def mock_exists(path):
            if "telemetry.jsonl" in path:
                return True
            if "retro-544.md" in path and "worktree_mock" in path:
                return True
            return False
            
        with patch("os.path.exists", mock_exists), \
             patch("subprocess.run") as mock_run:
            mock_res = MagicMock()
            mock_res.returncode = 0
            mock_res.stdout = '[{"number": 123, "title": "surfaced"}]'
            mock_run.return_value = mock_res
            enforce_reflection_hook("544", "/mock/repo", worktree_root="/mock/repo/worktree_mock")

def test_enforce_reflection_hook_frontier_path_match():
    # Lines 122-131
    mock_telemetry = '{"node_id": "544", "event": "FAILURE", "metadata": {"error": "some failure"}}\n'
    
    mock_frontier = """
nodes:
  - name: Path 809
  - name: Node 544
"""
    with patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open()) as mock_file, \
         patch("kernel.daemon_backlog.BacklogDaemon.add") as mock_add, \
         patch("subprocess.run") as mock_run:
         
        def open_side_effect(path, *args, **kwargs):
            if "telemetry.jsonl" in path:
                return mock_open(read_data=mock_telemetry).return_value
            if "frontier_state.yml" in path:
                return mock_open(read_data=mock_frontier).return_value
            return mock_open().return_value
            
        mock_file.side_effect = open_side_effect
        
        mock_res = MagicMock()
        mock_res.returncode = 0
        mock_res.stdout = "[]"
        mock_run.return_value = mock_res
        
        enforce_reflection_hook("544", "/mock/repo")
        mock_add.assert_called_once()
        assert mock_add.call_args[1]["path_id"] == "809"

def test_enforce_reflection_hook_fallback_active_path():
    # Lines 145-147
    mock_telemetry = '{"node_id": "544", "event": "FAILURE", "metadata": {"error": "some failure"}}\n'
    
    with patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data=mock_telemetry)), \
         patch("kernel.daemon_backlog.BacklogDaemon.add") as mock_add, \
         patch("subprocess.run") as mock_run, \
         patch("drivers.github_client.list_issues_by_label", return_value=[]), \
         patch("kernel.agent_frontier.read_active_path", return_value="current_active_path: 999"), \
         patch("kernel.agent_frontier.extract_path_id", return_value="999"):
         
        mock_res = MagicMock()
        mock_res.returncode = 0
        mock_res.stdout = "[]"
        mock_run.return_value = mock_res
        
        enforce_reflection_hook("544", "/mock/repo")
        mock_add.assert_called_once()
        assert mock_add.call_args[1]["path_id"] == "999"

def test_enforce_reflection_hook_exception():
    # Line 165-166
    mock_telemetry = '{"node_id": "544", "event": "FAILURE", "metadata": {"error": "some failure"}}\n'
    
    with patch("builtins.open", mock_open(read_data=mock_telemetry)), \
         patch("os.path.exists", return_value=True), \
         patch("subprocess.run", side_effect=Exception("gh error")):
         
        enforce_reflection_hook("544", "/mock/repo")
        # Should catch and print warning, not crash

def test_inject_contextual_rules_gemini_missing():
    # Line 215
    with patch("os.path.exists", return_value=False), \
         patch("drivers.knowledge_accrual_skill.build_contextual_prompt_injection", return_value="inj"):
        inject_contextual_rules("/mock/repo")

def test_inject_contextual_rules_gemini_exception():
    # Line 209
    with patch("os.path.exists", return_value=True), \
         patch("kernel.agent_frontier.read_active_path", return_value="current_active_path: 999"), \
         patch("builtins.open", side_effect=Exception("Read error")), \
         patch("drivers.knowledge_accrual_skill.build_contextual_prompt_injection", return_value="inj"):
        with pytest.raises((Exception, SystemExit), match="Read error"):
            inject_contextual_rules("/mock/repo")
