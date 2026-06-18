import pytest
from unittest.mock import patch, mock_open, MagicMock
from kernel.daemon_telemetry import TelemetryDaemon, SynthesisEngine
import json
import os
from datetime import datetime, timezone, timedelta

def test_log_event():
    with patch("os.makedirs"):
        with patch("drivers.file_locker.lock_file"):
            with patch("builtins.open", mock_open()) as mocked_file:
                with patch.dict("os.environ", {"SPAO_TELEMETRY_NO_TEST_SAFETY": "1"}):
                    tm = TelemetryDaemon(ledger_path="/tmp/test.jsonl")
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
        tm = TelemetryDaemon(ledger_path="/tmp/test.jsonl")
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
            tm = TelemetryDaemon(ledger_path="/tmp/test.jsonl")
            report = tm.generate_report()
            assert "⚠️ BOTTLENECK" in report
            assert "🚨 Bottleneck Alerts" in report
            assert "**Node #1** stalled in **PLAN** phase for 2:00:00" in report

def test_ledger_anchoring():
    with patch("drivers.path_resolver.resolve_workspace_path") as mock_resolve:
        mock_resolve.return_value = "/repo/root/artifacts/telemetry.jsonl"
        with patch.dict("os.environ", {"SPAO_TELEMETRY_NO_TEST_SAFETY": "1"}, clear=False):
            if "SPAO_PERSONA_ID" in os.environ:
                del os.environ["SPAO_PERSONA_ID"]
            tm = TelemetryDaemon()
            assert tm.ledger_path == "/repo/root/artifacts/telemetry.jsonl"
        mock_resolve.assert_called_with("artifacts", "telemetry.jsonl")

def test_ledger_anchoring_persona():
    with patch("drivers.path_resolver.resolve_workspace_path") as mock_resolve:
        mock_resolve.return_value = "/repo/root/artifacts/telemetry_test_persona.jsonl"
        with patch.dict("os.environ", {"SPAO_TELEMETRY_NO_TEST_SAFETY": "1", "SPAO_PERSONA_ID": "test_persona"}, clear=False):
            tm = TelemetryDaemon()
            assert tm.ledger_path == "/repo/root/artifacts/telemetry_test_persona.jsonl"
        mock_resolve.assert_called_with("artifacts", "telemetry_test_persona.jsonl")
