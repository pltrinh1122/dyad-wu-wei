import pytest
import os
import yaml
from unittest.mock import patch, mock_open
from kernel.agent_frontier import dispatch_active_node

def test_dispatch_active_node_success(tmp_path):
    # Setup mock frontier state
    state_file = tmp_path / "frontier_state.yml"
    state_data = {
        "active_agents": {
            "frontier": {
                "current_active_path": "Path: Test",
                "current_active_node": "Node 123: Test"
            }
        }
    }
    with open(state_file, "w") as f:
        yaml.dump(state_data, f)
        
    # Act
    dispatch_active_node(str(state_file), "123", "frontier", "research")
    
    # Assert
    with open(state_file, "r") as f:
        updated_state = yaml.safe_load(f)
        
    assert updated_state["active_agents"]["frontier"]["current_active_node"] is None
    assert updated_state["active_agents"]["research"]["current_active_node"] == "Node 123: Test"
    assert updated_state["active_agents"]["research"]["current_active_path"] == "Path: Test"

def test_dispatch_active_node_failure(tmp_path):
    state_file = tmp_path / "frontier_state.yml"
    state_data = {
        "active_agents": {
            "frontier": {
                "current_active_path": "Path: Test",
                "current_active_node": "Node 999: Test"
            }
        }
    }
    with open(state_file, "w") as f:
        yaml.dump(state_data, f)
        
    # Act & Assert
    with pytest.raises(ValueError, match="not currently locked"):
        dispatch_active_node(str(state_file), "123", "frontier", "research")
