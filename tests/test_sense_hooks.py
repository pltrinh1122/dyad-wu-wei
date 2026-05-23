import pytest
from unittest.mock import patch, mock_open, MagicMock
from kernel.sense_hooks import HookDaemon
import yaml

def test_hook_manager_load_config():
    fake_config = {"sense_hooks": [{"type": "prompt_queue"}, {"type": "next_best_action"}]}
    fake_yaml = yaml.dump(fake_config)
    
    with patch("os.path.exists", return_value=True):
        with patch("builtins.open", mock_open(read_data=fake_yaml)):
            hm = HookDaemon("fake.yml")
            assert len(hm.hooks) == 2
            assert hm.hooks[0]["type"] == "prompt_queue"
            assert hm.hooks[1]["type"] == "next_best_action"

@patch.object(HookDaemon, 'execute_prompt_queue_hook')
@patch.object(HookDaemon, 'execute_next_best_action_hook')
def test_execute_all(mock_nba, mock_pq):
    hm = HookDaemon("fake.yml")
    hm.hooks = [
        {"type": "prompt_queue", "location": "a"},
        {"type": "next_best_action", "repository": "b"},
        {"type": "unknown"}
    ]
    
    hm.execute_all()
    
    mock_pq.assert_called_once_with({"type": "prompt_queue", "location": "a"})
    mock_nba.assert_called_once_with({"type": "next_best_action", "repository": "b"}, local_mode=False)

@patch('kernel.sense_hooks.HookDaemon._load_config', return_value=[])
@patch('kernel.daemon_prompt.list_prompts')
def test_execute_prompt_queue_hook(mock_list_prompts, mock_load_config):
    hm = HookDaemon("fake.yml")
    config = {"location": "custom/path.yml"}
    
    hm.execute_prompt_queue_hook(config)
    
    mock_list_prompts.assert_called_once_with(all_prompts=False, backlog_file="custom/path.yml")
    
@patch('kernel.sense_hooks.HookDaemon._load_config', return_value=[])
@patch('kernel.daemon_prompt.list_prompts')
def test_execute_prompt_queue_hook_default(mock_list_prompts, mock_load_config):
    hm = HookDaemon("fake.yml")
    config = {}
    
    hm.execute_prompt_queue_hook(config)
    
    mock_list_prompts.assert_called_once_with(all_prompts=False, backlog_file="artifacts/prompt_backlog.yml")

@patch('kernel.sense_hooks.HookDaemon._load_config', return_value=[])
@patch('kernel.daemon_nba.NBADaemon.evaluate')
def test_execute_next_best_action_hook(mock_evaluate, mock_load_config, capsys):
    mock_evaluate.return_value = {
        "type": "path_continuation",
        "path_id": "181",
        "path_title": "Configurable Sense Hooks",
        "recommendations": [{"number": 189, "title": "Activity 189: NBA Skill"}]
    }
    hm = HookDaemon("fake.yml")
    hm.execute_next_best_action_hook({"repository": "owner/repo"})
    mock_evaluate.assert_called_once_with(frontier_file="artifacts/frontier_state.md", local_mode=False)
    out = capsys.readouterr().out
    assert "Next-Best-Action" in out
    assert "#189" in out
    assert "Configurable Sense Hooks" in out
    assert "┌─" in out
    assert "└─" in out

@patch('kernel.sense_hooks.HookDaemon._load_config', return_value=[])
@patch('kernel.daemon_nba.NBADaemon.evaluate')
def test_execute_next_best_action_hook_empty(mock_evaluate, mock_load_config, capsys):
    mock_evaluate.return_value = {
        "type": "path_switching",
        "recommendations": []
    }
    hm = HookDaemon("fake.yml")
    hm.execute_next_best_action_hook({})
    mock_evaluate.assert_called_once_with(frontier_file="artifacts/frontier_state.md", local_mode=False)
    out = capsys.readouterr().out
    assert "Global backlog empty" in out
    assert "┌─" in out
