import os
import json
import pytest
from drivers.exhaust_logger import ExhaustLogger

def test_dump_transient_exhaust(tmp_path, monkeypatch):
    # Mock os.getcwd to use tmp_path so we don't pollute the actual repo
    monkeypatch.setattr(os, "getcwd", lambda: str(tmp_path))
    
    guard_name = "test_guard"
    payload = {"error_code": 401, "reason": "Unauthorized"}
    message = "The API call failed."
    
    artifact_path = ExhaustLogger.dump_transient_exhaust(guard_name, payload, message)
    
    assert os.path.exists(artifact_path)
    assert artifact_path.endswith(".json")
    assert f"exhaust_{guard_name}_" in artifact_path
    
    with open(artifact_path, "r") as f:
        data = json.load(f)
        
    assert data["guard"] == guard_name
    assert data["message"] == message
    assert data["payload"] == payload
    assert "timestamp" in data

def test_clear_historical_exhaust(tmp_path, monkeypatch):
    monkeypatch.setattr(os, "getcwd", lambda: str(tmp_path))
    
    guard_name = "test_guard"
    other_guard = "other_guard"
    
    # Create files
    path1 = ExhaustLogger.dump_transient_exhaust(guard_name, {}, "error 1")
    path2 = ExhaustLogger.dump_transient_exhaust(guard_name, {}, "error 2")
    path3 = ExhaustLogger.dump_transient_exhaust(other_guard, {}, "error 3")
    
    assert os.path.exists(path1)
    assert os.path.exists(path2)
    assert os.path.exists(path3)
    
    # Clear for test_guard
    ExhaustLogger.clear_historical_exhaust(guard_name)
    
    assert not os.path.exists(path1)
    assert not os.path.exists(path2)
    assert os.path.exists(path3)  # Other guard's exhaust should remain
