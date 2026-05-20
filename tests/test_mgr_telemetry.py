import pytest
from unittest.mock import patch, mock_open
from orchestrator.mgr_telemetry import TelemetryManager
import json
import os

def test_log_event():
    with patch("os.makedirs"):
        with patch("skills.file_locker.lock_file"):
            with patch("builtins.open", mock_open()) as mocked_file:
                tm = TelemetryManager(ledger_path="/tmp/test.jsonl")
                tm.log_event(stage="plan", event="start", node_id="264", metadata={"test": "data"})
                
                # Check if write was called
                mocked_file().write.assert_called_once()
                written_data = json.loads(mocked_file().write.call_args[0][0])
                assert written_data["stage"] == "PLAN"
                assert written_data["event"] == "START"
                assert written_data["node_id"] == "264"
                assert written_data["metadata"]["test"] == "data"
                assert "timestamp" in written_data

def test_generate_report_empty():
    with patch("os.path.exists", return_value=False):
        tm = TelemetryManager(ledger_path="/tmp/test.jsonl")
        assert tm.generate_report() == "No telemetry data available."

def test_generate_report_with_data():
    fake_data = json.dumps({"timestamp": "2026-05-20T00:00:00Z", "stage": "PLAN", "event": "START"}) + "\n"
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=fake_data)):
            tm = TelemetryManager(ledger_path="/tmp/test.jsonl")
            report = tm.generate_report()
            assert "# SPAO Operational Health Report" in report
            assert "Total Observation Points: 1" in report
