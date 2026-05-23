import os
import yaml
import json
import pytest
import pytest
from kernel import ziran_auditor

@pytest.fixture
def mock_repo_root(tmp_path):
    return str(tmp_path)

def test_read_ledger_empty(mock_repo_root):
    data = ziran_auditor.read_ledger(mock_repo_root)
    assert data == {"primitives": {}}

def test_write_and_read_ledger(mock_repo_root):
    test_data = {
        "primitives": {
            "SG-0005": {"state": "Active", "gradient": "Turbulent", "confidence": 0.4}
        }
    }
    ziran_auditor.write_ledger(mock_repo_root, test_data)
    data = ziran_auditor.read_ledger(mock_repo_root)
    assert data == test_data

def test_mutate_primitive_new(mock_repo_root):
    ziran_auditor.mutate_primitive(mock_repo_root, "WHAT-0077", "Active", "Laminar", 1.0)
    data = ziran_auditor.read_ledger(mock_repo_root)
    assert "WHAT-0077" in data["primitives"]
    assert data["primitives"]["WHAT-0077"]["state"] == "Active"
    assert data["primitives"]["WHAT-0077"]["gradient"] == "Laminar"
    assert data["primitives"]["WHAT-0077"]["confidence"] == 1.0

def test_mutate_primitive_existing(mock_repo_root):
    ziran_auditor.mutate_primitive(mock_repo_root, "WHAT-0077", "Active", "Laminar", 1.0)
    ziran_auditor.mutate_primitive(mock_repo_root, "WHAT-0077", "Active", "Turbulent", 0.5)
    data = ziran_auditor.read_ledger(mock_repo_root)
    assert data["primitives"]["WHAT-0077"]["gradient"] == "Turbulent"
    assert data["primitives"]["WHAT-0077"]["confidence"] == 0.5

def test_parse_telemetry_missing(mock_repo_root):
    events = ziran_auditor.parse_telemetry(mock_repo_root)
    assert events == {}

def test_parse_telemetry_valid(mock_repo_root):
    telemetry_dir = os.path.join(mock_repo_root, "artifacts", "telemetry")
    os.makedirs(telemetry_dir, exist_ok=True)
    events_file = os.path.join(telemetry_dir, "events.jsonl")
    
    with open(events_file, "w", encoding="utf-8") as f:
        f.write('{"kb_target": "SG-0001", "status": "Laminar"}\n')
        f.write('{"kb_target": "SG-0001", "status": "Turbulent"}\n')
        f.write('invalid json\n')
        f.write('{"kb_target": "SG-0002", "status": "Laminar"}\n')
        
    events = ziran_auditor.parse_telemetry(mock_repo_root)
    assert len(events["SG-0001"]) == 2
    assert len(events["SG-0002"]) == 1

def test_calculate_gradient():
    assert ziran_auditor.calculate_gradient(10, 0) == 1.0
    assert ziran_auditor.calculate_gradient(0, 10) == 0.0
    assert ziran_auditor.calculate_gradient(5, 5) == 0.5
    assert ziran_auditor.calculate_gradient(0, 0) == 1.0

def test_evaluate_and_apply_gradients(mock_repo_root):
    # Setup telemetry
    telemetry_dir = os.path.join(mock_repo_root, "artifacts", "telemetry")
    os.makedirs(telemetry_dir, exist_ok=True)
    events_file = os.path.join(telemetry_dir, "events.jsonl")
    
    with open(events_file, "w", encoding="utf-8") as f:
        # SG-0001: 10 Laminar -> 1.0 (Laminar promotion)
        for _ in range(10): f.write('{"kb_target": "SG-0001", "status": "Laminar"}\n')
        # SG-0002: 6 Turbulent, 4 Laminar -> 0.4 (Turbulent demotion)
        for _ in range(4): f.write('{"kb_target": "SG-0002", "status": "Laminar"}\n')
        for _ in range(6): f.write('{"kb_target": "SG-0002", "status": "Turbulent"}\n')
        # SG-0003: 8 Laminar, 2 Turbulent -> 0.8 (No change, remains whatever it was)
        for _ in range(8): f.write('{"kb_target": "SG-0003", "status": "Laminar"}\n')
        for _ in range(2): f.write('{"kb_target": "SG-0003", "status": "Turbulent"}\n')
        
    # Setup initial ledger state
    initial_ledger = {
        "primitives": {
            "SG-0003": {"state": "Active", "gradient": "Turbulent", "confidence": 0.1}
        }
    }
    ziran_auditor.write_ledger(mock_repo_root, initial_ledger)
    
    # Evaluate
    ziran_auditor.evaluate_and_apply_gradients(mock_repo_root)
    
    ledger = ziran_auditor.read_ledger(mock_repo_root)
    # SG-0001 promoted to Laminar
    assert ledger["primitives"]["SG-0001"]["gradient"] == "Laminar"
    assert ledger["primitives"]["SG-0001"]["confidence"] == 1.0
    
    # SG-0002 demoted to Turbulent
    assert ledger["primitives"]["SG-0002"]["gradient"] == "Turbulent"
    assert ledger["primitives"]["SG-0002"]["confidence"] == 1.0
    
    # SG-0003 should remain Turbulent because 0.8 is not > 0.9 or < 0.6
    assert ledger["primitives"]["SG-0003"]["gradient"] == "Turbulent"
    # But wait, evaluate_and_apply_gradients doesn't write anything if new_gradient is None!
    # So confidence won't update for SG-0003 right now, which matches our logic.
    assert ledger["primitives"]["SG-0003"]["confidence"] == 0.1
