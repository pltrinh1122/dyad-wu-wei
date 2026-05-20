import pytest
from unittest.mock import patch, mock_open, MagicMock
from orchestrator.mgr_telemetry import TelemetryManager, SynthesisEngine
import json
import os
from datetime import datetime, timezone, timedelta

def test_log_event():
    with patch("os.makedirs"):
        with patch("skills.file_locker.lock_file"):
            with patch("builtins.open", mock_open()) as mocked_file:
                with patch.dict("os.environ", {"SPAO_TELEMETRY_NO_TEST_SAFETY": "1"}):
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
        assert "No telemetry data available" in tm.generate_report()

def test_synthesis_engine():
    events = [
        {"timestamp": "2026-05-20T00:00:00Z", "stage": "PLAN", "event": "START", "node_id": "1"},
        {"timestamp": "2026-05-20T02:00:00Z", "stage": "PLAN", "event": "FINISH", "node_id": "1"}, # 2 hours (Bottleneck)
        {"timestamp": "2026-05-20T03:00:00Z", "stage": "SENSE", "event": "START", "node_id": None},
        {"timestamp": "2026-05-20T03:01:00Z", "stage": "SENSE", "event": "FINISH", "node_id": None}, # 1 min (Healthy)
    ]
    engine = SynthesisEngine(events)
    metrics = engine.calculate_metrics()
    
    assert len(metrics) == 2
    
    plan_metric = next(m for m in metrics if m["stage"] == "PLAN")
    assert plan_metric["duration"] == timedelta(hours=2)
    assert plan_metric["is_bottleneck"] is True
    
    sense_metric = next(m for m in metrics if m["stage"] == "SENSE")
    assert sense_metric["duration"] == timedelta(minutes=1)
    assert sense_metric["is_bottleneck"] is False

def test_generate_report_with_bottleneck():
    events = [
        {"timestamp": "2026-05-20T00:00:00Z", "stage": "PLAN", "event": "START", "node_id": "1"},
        {"timestamp": "2026-05-20T02:00:00Z", "stage": "PLAN", "event": "FINISH", "node_id": "1"},
    ]
    fake_data = "\n".join([json.dumps(e) for e in events]) + "\n"
    
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=fake_data)):
            tm = TelemetryManager(ledger_path="/tmp/test.jsonl")
            report = tm.generate_report()
            assert "⚠️ BOTTLENECK" in report
            assert "🚨 Bottleneck Alerts" in report
            assert "**Node #1** stalled in **PLAN** phase for 2:00:00" in report

def test_ledger_anchoring():
    with patch("skills.git_client.get_git_common_dir") as mock_common:
        mock_common.return_value = "/repo/root/.git"
        with patch.dict("os.environ", {"SPAO_TELEMETRY_NO_TEST_SAFETY": "1"}):
            tm = TelemetryManager()
            assert tm.ledger_path == "/repo/root/artifacts/telemetry.jsonl"
        mock_common.assert_called_once()

def test_ledger_anchoring_worktree():
    with patch("skills.git_client.get_git_common_dir") as mock_common, \
         patch("skills.git_client.get_show_toplevel") as mock_toplevel:
        # git-common-dir is relative in worktrees sometimes
        mock_common.return_value = ".git"
        mock_toplevel.return_value = "/repo/root"
        with patch.dict("os.environ", {"SPAO_TELEMETRY_NO_TEST_SAFETY": "1"}):
            tm = TelemetryManager()
            assert tm.ledger_path == "/repo/root/artifacts/telemetry.jsonl"
        mock_common.assert_called_once()
        mock_toplevel.assert_called_once()

def test_ledger_anchoring_fallback():
    with patch("skills.git_client.get_git_common_dir") as mock_common:
        from subprocess import CalledProcessError
        mock_common.side_effect = CalledProcessError(1, "git")
        with patch.dict("os.environ", {"SPAO_TELEMETRY_NO_TEST_SAFETY": "1"}):
            tm = TelemetryManager()
            assert os.path.isabs(tm.ledger_path)
            assert tm.ledger_path.endswith("artifacts/telemetry.jsonl")

