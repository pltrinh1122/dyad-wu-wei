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

@patch('orchestrator.sense_hooks.HookManager._load_config', return_value=[])
@patch('orchestrator.mgr_prompt.list_prompts')
def test_execute_prompt_queue_hook(mock_list_prompts, mock_load_config):
    hm = HookManager("fake.yml")
    config = {"location": "custom/path.yml"}
    
    hm.execute_prompt_queue_hook(config)
    
    mock_list_prompts.assert_called_once_with(all_prompts=False, backlog_file="custom/path.yml")
    
@patch('orchestrator.sense_hooks.HookManager._load_config', return_value=[])
@patch('orchestrator.mgr_prompt.list_prompts')
def test_execute_prompt_queue_hook_default(mock_list_prompts, mock_load_config):
    hm = HookManager("fake.yml")
    config = {}
    
    hm.execute_prompt_queue_hook(config)
    
    mock_list_prompts.assert_called_once_with(all_prompts=False, backlog_file="artifacts/prompt_backlog.yml")

@patch('orchestrator.sense_hooks.HookManager._load_config', return_value=[])
@patch('orchestrator.mgr_nba.NBAManager.evaluate')
def test_execute_next_best_action_hook(mock_evaluate, mock_load_config, capsys):
    mock_evaluate.return_value = {
        "type": "path_continuation",
        "path_id": "181",
        "path_title": "Configurable Sense Hooks",
        "recommendations": [{"number": 189, "title": "Activity 189: NBA Skill"}]
    }
    hm = HookManager("fake.yml")
    hm.execute_next_best_action_hook({"repository": "owner/repo"})
    mock_evaluate.assert_called_once_with(frontier_file="artifacts/frontier_state.md")
    out = capsys.readouterr().out
    assert "Next-Best-Action" in out
    assert "#189" in out
    assert "Configurable Sense Hooks" in out

@patch('orchestrator.sense_hooks.HookManager._load_config', return_value=[])
@patch('orchestrator.mgr_nba.NBAManager.evaluate')
def test_execute_next_best_action_hook_empty(mock_evaluate, mock_load_config, capsys):
    mock_evaluate.return_value = {
        "type": "path_switching",
        "recommendations": []
    }
    hm = HookManager("fake.yml")
    hm.execute_next_best_action_hook({})
    out = capsys.readouterr().out
    assert "Global backlog empty" in out
