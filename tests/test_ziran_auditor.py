import os
import yaml
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
