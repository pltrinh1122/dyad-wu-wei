import os
import json
import pytest
from unittest.mock import patch, MagicMock, mock_open

from skills.audit_daemon import (
    evaluate_node_completion_threshold,
    evaluate_file_modified,
    main
)

def test_evaluate_node_completion_threshold():
    rule = {
        "id": "test-rule",
        "type": "node_completion_threshold",
        "threshold": 2,
        "alert_level": "NOTIFICATION",
        "prompt_message": "Threshold reached: {current}"
    }
    
    state = {"last_count": 5}
    
    mock_frontier = "Some content\n- **Status**: Completed\n- **Status**: Completed\n- **Status**: Completed\n- **Status**: Completed\n- **Status**: Completed\n- **Status**: Completed\n- **Status**: Completed"
    # That's 7 completed nodes
    
    with patch("pathlib.Path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data=mock_frontier)), \
         patch("skills.audit_daemon.inject_prompt") as mock_inject:
             
        triggered, new_state = evaluate_node_completion_threshold(rule, state.copy())
        
        assert triggered is True
        assert new_state["last_count"] == 7
        mock_inject.assert_called_once_with("[NOTIFICATION] Threshold reached: 7")

def test_evaluate_node_completion_threshold_not_reached():
    rule = {
        "id": "test-rule",
        "threshold": 5
    }
    state = {"last_count": 5}
    mock_frontier = "- **Status**: Completed\n" * 7
    # 7 completed, threshold is 5, so we need 5+5=10. Current is 7.
    
    with patch("pathlib.Path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data=mock_frontier)), \
         patch("skills.audit_daemon.inject_prompt") as mock_inject:
             
        triggered, new_state = evaluate_node_completion_threshold(rule, state.copy())
        
        assert triggered is False
        assert new_state["last_count"] == 5
        mock_inject.assert_not_called()

def test_evaluate_file_modified():
    rule = {
        "id": "file-rule",
        "type": "file_modified",
        "file": "req.txt",
        "alert_level": "FAILURE",
        "prompt_message": "File changed"
    }
    state = {"last_hash": "old_hash"}
    
    with patch("skills.audit_daemon.subprocess.run") as mock_run, \
         patch("skills.audit_daemon.inject_prompt") as mock_inject:
             
        mock_result = MagicMock()
        mock_result.stdout = "new_hash\n"
        mock_run.return_value = mock_result
        
        triggered, new_state = evaluate_file_modified(rule, state.copy())
        
        assert triggered is True
        assert new_state["last_hash"] == "new_hash"
        mock_inject.assert_called_once_with("[FAILURE] File changed")

def test_evaluate_file_modified_initial_run():
    rule = {
        "id": "file-rule",
        "file": "req.txt",
        "prompt_message": "File changed"
    }
    state = {} # First run
    
    with patch("skills.audit_daemon.subprocess.run") as mock_run, \
         patch("skills.audit_daemon.inject_prompt") as mock_inject:
             
        mock_result = MagicMock()
        mock_result.stdout = "new_hash\n"
        mock_run.return_value = mock_result
        
        triggered, new_state = evaluate_file_modified(rule, state.copy())
        
        # Should initialize but NOT trigger prompt
        assert triggered is True # Means state changed and we should save
        assert new_state["last_hash"] == "new_hash"
        mock_inject.assert_not_called()

@patch("skills.audit_daemon.load_config")
@patch("skills.audit_daemon.get_current_branch")
@patch("skills.audit_daemon.load_state")
@patch("skills.audit_daemon.save_state")
def test_main_ignores_unconfigured_branch(mock_save, mock_load, mock_get_branch, mock_config):
    mock_config.return_value = {
        "audit_branches": ["main"]
    }
    mock_get_branch.return_value = "feature-branch"
    
    main()
    
    mock_load.assert_not_called()
    mock_save.assert_not_called()

@patch("skills.audit_daemon.load_config")
@patch("skills.audit_daemon.get_current_branch")
@patch("skills.audit_daemon.load_state")
@patch("skills.audit_daemon.save_state")
@patch("skills.audit_daemon.RULE_REGISTRY")
def test_main_processes_rules(mock_registry, mock_save, mock_load, mock_get_branch, mock_config):
    mock_config.return_value = {
        "audit_branches": ["main"],
        "rules": [
            {"id": "rule1", "type": "dummy_type"}
        ]
    }
    mock_get_branch.return_value = "main"
    mock_load.return_value = {"rule1": {"last_val": "a"}}
    
    mock_evaluator = MagicMock()
    mock_evaluator.return_value = (True, {"last_val": "b"})
    mock_registry.get.return_value = mock_evaluator
    
    main()
    
    mock_evaluator.assert_called_once()
    mock_save.assert_called_once_with({"rule1": {"last_val": "b"}})
