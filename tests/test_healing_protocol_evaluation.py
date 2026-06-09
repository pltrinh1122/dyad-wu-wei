import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from drivers.audit_daemon import evaluate_seizure_detection

def test_seizure_detection_no_failures():
    rule = {
        "id": "seizure_detector",
        "type": "seizure_detection",
        "threshold": 3,
        "alert_level": "FAILURE"
    }
    state = {"last_fail_count": 0}
    
    with patch("pathlib.Path.glob") as mock_glob, \
         patch("pathlib.Path.exists", return_value=True), \
         patch("drivers.audit_daemon.dispatch_alert") as mock_inject:
         
        mock_glob.return_value = []
        
        triggered, new_state = evaluate_seizure_detection(rule, state.copy())
        
        assert triggered is False
        assert new_state["last_fail_count"] == 0
        mock_inject.assert_not_called()

def test_seizure_detection_under_threshold():
    rule = {
        "id": "seizure_detector",
        "type": "seizure_detection",
        "threshold": 3,
        "alert_level": "FAILURE"
    }
    state = {"last_fail_count": 0}
    
    with patch("pathlib.Path.glob") as mock_glob, \
         patch("pathlib.Path.exists", return_value=True), \
         patch("drivers.audit_daemon.dispatch_alert") as mock_inject:
         
        mock_glob.return_value = [
            Path("test-fail-1.json"),
            Path("test-fail-2.json")
        ]
        
        triggered, new_state = evaluate_seizure_detection(rule, state.copy())
        
        assert triggered is False
        assert new_state["last_fail_count"] == 0
        mock_inject.assert_not_called()

def test_seizure_detection_recovery_reset():
    rule = {
        "id": "seizure_detector",
        "type": "seizure_detection",
        "threshold": 3,
        "alert_level": "FAILURE"
    }
    state = {"last_fail_count": 5}
    
    with patch("pathlib.Path.glob") as mock_glob, \
         patch("pathlib.Path.exists", return_value=True), \
         patch("drivers.audit_daemon.dispatch_alert") as mock_inject:
         
        mock_glob.return_value = [
            Path("test-fail-1.json"),
            Path("test-fail-2.json")
        ]
        
        triggered, new_state = evaluate_seizure_detection(rule, state.copy())
        
        assert triggered is True
        assert new_state["last_fail_count"] == 2
        mock_inject.assert_not_called()
