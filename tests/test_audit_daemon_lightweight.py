import pytest
from unittest.mock import patch, MagicMock
from drivers.audit_daemon import main

@patch("drivers.audit_daemon.load_config")
@patch("drivers.audit_daemon.get_current_branch")
@patch("drivers.audit_daemon.load_state")
@patch("drivers.audit_daemon.save_state")
@patch("drivers.audit_daemon.RULE_REGISTRY")
def test_main_lightweight_filtering(mock_registry, mock_save, mock_load, mock_get_branch, mock_config):
    mock_config.return_value = {
        "audit_branches": ["main"],
        "rules": [
            {"id": "heavy1", "type": "dummy_type", "lightweight": False},
            {"id": "light1", "type": "dummy_type", "lightweight": True},
            {"id": "heavy2", "type": "dummy_type"}
        ]
    }
    mock_get_branch.return_value = "main"
    mock_load.return_value = {}
    
    mock_evaluator = MagicMock()
    mock_evaluator.return_value = (False, {})
    mock_registry.get.return_value = mock_evaluator
    
    main(["--lightweight"])
    
    # Only light1 should be evaluated
    assert mock_evaluator.call_count == 1
    args, _ = mock_evaluator.call_args
    assert args[0]["id"] == "light1"
