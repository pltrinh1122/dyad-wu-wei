import pytest
from unittest.mock import patch, mock_open
import json
import yaml
import os
from kernel.daemon_retro import RetroCompiler

def test_load_nodes_and_paths():
    fake_frontier = {
        "nodes": [
            {"name": "Node 404: S" + "pike Path: Strategic Intent Tracking"},
            {"name": "Node 405: Discovery 405: Harmonize - Strategic Intent Tracking"},
            {"name": "Node 412: Path 412: Verify Goals"},
            {"name": "Node 413: Discovery 413: Harmonize - Verify Goals"},
            {"name": "Node 420: Path 420: TBD"},
        ]
    }
    fake_yaml = yaml.dump(fake_frontier)

    with patch("builtins.open", mock_open(read_data=fake_yaml)):
        with patch("os.path.exists", return_value=True):
            compiler = RetroCompiler(404, 412, frontier_path="/dummy/frontier.yml")
            target_nodes, mapping = compiler.load_nodes_and_paths()
            
            # Nodes for Path 404 (404, 405) and Path 412 (412, 413) should be included.
            # Path 420 (node 420) should not be included.
            assert "404" in target_nodes
            assert "405" in target_nodes
            assert "412" in target_nodes
            assert "413" in target_nodes
            assert "420" not in target_nodes
            
            assert mapping["405"] == 404
            assert mapping["413"] == 412

def test_process_telemetry():
    fake_telemetry = [
        {"timestamp": "2026-05-20T00:00:00.000000Z", "node_id": "404", "stage": "PLAN", "event": "START", "metadata": {"function": "plan_start"}},
        {"timestamp": "2026-05-20T00:01:00.000000Z", "node_id": "404", "stage": "PLAN", "event": "FINISH", "metadata": {"function": "plan_start", "status": "success", "duration_sec": 60.0}},
        # Node 405 events
        {"timestamp": "2026-05-20T00:02:00.000000Z", "node_id": "405", "stage": "ACT", "event": "START", "metadata": {"function": "checkout"}},
        {"timestamp": "2026-05-20T00:04:00.000000Z", "node_id": "405", "stage": "ACT", "event": "FINISH", "metadata": {"function": "checkout", "status": "success", "duration_sec": 120.0}},
        # API call
        {"timestamp": "2026-05-20T00:03:00.000000Z", "node_id": "405", "stage": "SKILL", "domain": "drivers", "event": "FINISH", "metadata": {"function": "get_issue_details", "duration_sec": 0.5}},
        # Error event (Close call)
        {"timestamp": "2026-05-20T00:03:30.000000Z", "node_id": "405", "stage": "PLAN", "event": "FINISH", "metadata": {"function": "plan_finish", "status": "error", "error": "SPEC file violation: A corresponding WHAT- specification file must exist"}},
    ]
    fake_log = "\n".join([json.dumps(e) for e in fake_telemetry]) + "\n"

    with patch("builtins.open", mock_open(read_data=fake_log)):
        with patch("os.path.exists", return_value=True):
            compiler = RetroCompiler(404, 404, telemetry_path="/dummy/telemetry.jsonl")
            metrics = compiler.process_telemetry({"404", "405"})
            
            assert metrics["api_count"] == 1
            assert metrics["avg_api_latency"] == "0.500s"
            # Anomaly classification assertion
            assert len(metrics["anomalies"][2]) == 1 # SPEC file violation is Tier 2 Close Call
            assert "SPEC file violation" in metrics["anomalies"][2][0]

def test_compile():
    fake_yaml = yaml.dump({"nodes": [{"name": "Node 404: Path 404: Test"}]})
    fake_telemetry = json.dumps({"timestamp": "2026-05-20T00:00:00Z", "node_id": "404", "stage": "PLAN", "event": "START"}) + "\n"
    fake_template = "# Retrospective - {assessment_title}\n{timeline_events}\n{tier1_mishaps}\n{tier2_close_calls}\n{tier3_precursors}\n{tier4_calibrations}\n| Execution Time (Avg/Node) | | | |\n| GitHub API Latency (Avg) | | | |\n| Active Worktrees / Local Size | | | |\n| Duplicate File Lock Contention | | | |"

    files = {
        "/dummy/frontier.yml": fake_yaml,
        "/dummy/telemetry.jsonl": fake_telemetry,
        "kb/templates/shar_retrospective.md": fake_template
    }

    import io
    written_data = []

    class MockFile(io.StringIO):
        def __init__(self, content="", mode="r"):
            super().__init__(content)
            self.mode = mode
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            if "w" in self.mode:
                written_data.append(self.getvalue())
            super().__exit__(exc_type, exc_val, exc_tb)

    def custom_open(path, mode="r", *args, **kwargs):
        if "w" in mode:
            return MockFile(mode=mode)
        if path in files:
            return MockFile(files[path], mode=mode)
        raise FileNotFoundError(f"Mock file not found: {path}")

    with patch("builtins.open", side_effect=custom_open):
        with patch("os.path.exists", return_value=True):
            with patch("os.makedirs"):
                compiler = RetroCompiler(404, 404, telemetry_path="/dummy/telemetry.jsonl", frontier_path="/dummy/frontier.yml")
                compiler.compile("/dummy/output.md")
                
                assert len(written_data) == 1
                assert "Paths 404 to 404" in written_data[0]
