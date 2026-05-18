import pytest
from unittest.mock import patch, mock_open, MagicMock
from orchestrator.sense_hooks import HookManager
import yaml

def test_hook_manager_load_config():
    fake_config = {"sense_hooks": [{"type": "prompt_queue"}, {"type": "next_best_action"}]}
    fake_yaml = yaml.dump(fake_config)
    
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=fake_yaml)):
            hm = HookManager("fake.yml")
            assert len(hm.hooks) == 2
            assert hm.hooks[0]["type"] == "prompt_queue"
            assert hm.hooks[1]["type"] == "next_best_action"

@patch.object(HookManager, 'execute_prompt_queue_hook')
@patch.object(HookManager, 'execute_next_best_action_hook')
def test_execute_all(mock_nba, mock_pq):
    hm = HookManager("fake.yml")
    hm.hooks = [
        {"type": "prompt_queue", "location": "a"},
        {"type": "next_best_action", "repository": "b"},
        {"type": "unknown"}
    ]
    
    hm.execute_all()
    
    mock_pq.assert_called_once_with({"type": "prompt_queue", "location": "a"})
    mock_nba.assert_called_once_with({"type": "next_best_action", "repository": "b"})
