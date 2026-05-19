import json
from unittest.mock import patch, MagicMock
from skills.nba_evaluator import get_active_path, get_backlog_items, evaluate


@patch('skills.frontier_editor.read_active_node', return_value="Path 181: Configurable Sense Hooks")
def test_get_active_path_returns_path(mock_read):
    result = get_active_path("/fake/frontier.md")
    assert result == "Path 181: Configurable Sense Hooks"


@patch('skills.frontier_editor.read_active_node', return_value="Activity 189: NBA Skill")
def test_get_active_path_returns_none_for_activity(mock_read):
    result = get_active_path("/fake/frontier.md")
    assert result is None


@patch('skills.frontier_editor.read_active_node', return_value="")
def test_get_active_path_empty(mock_read):
    result = get_active_path("/fake/frontier.md")
    assert result is None


@patch('subprocess.run')
def test_get_backlog_items(mock_run):
    fake_data = [{"number": 181, "title": "Path 181: Configurable Sense Hooks", "url": "http://example.com"}]
    mock_run.return_value = MagicMock(returncode=0, stdout=json.dumps(fake_data))
    result = get_backlog_items("owner/repo")
    assert len(result) == 1
    assert result[0]["number"] == 181


@patch('subprocess.run')
def test_get_backlog_items_gh_failure(mock_run):
    mock_run.return_value = MagicMock(returncode=1, stdout="")
    result = get_backlog_items("owner/repo")
    assert result == []


@patch('skills.nba_evaluator.get_active_path', return_value="Path 181: Configurable Sense Hooks")
@patch('skills.nba_evaluator.get_backlog_items')
def test_evaluate_path_continuation(mock_backlog, mock_path):
    mock_backlog.return_value = [
        {"number": 187, "title": "Activity 187: Prompt Queue Hook", "url": "http"},
        {"number": 189, "title": "Activity 189: NBA Skill", "url": "http"},
    ]
    result = evaluate(repository="owner/repo", frontier_file="/fake/frontier.md")
    assert result["mode"] == "path_continuation"
    assert result["active_path"] == "Path 181: Configurable Sense Hooks"
    assert len(result["recommended"]) == 2


@patch('skills.nba_evaluator.get_active_path', return_value=None)
@patch('skills.nba_evaluator.get_backlog_items')
def test_evaluate_path_switching(mock_backlog, mock_path):
    mock_backlog.return_value = [
        {"number": 118, "title": "Probe 118: Parallel Processing", "url": "http"},
    ]
    result = evaluate(repository="owner/repo")
    assert result["mode"] == "path_switching"
    assert result["active_path"] is None
    assert result["recommended"][0]["number"] == 118


@patch('skills.nba_evaluator.get_active_path', return_value="Path 181: Configurable Sense Hooks")
@patch('skills.nba_evaluator.get_backlog_items')
def test_evaluate_falls_back_when_no_related_activities(mock_backlog, mock_path):
    # Only items that aren't Activities numerically after 181
    mock_backlog.return_value = [
        {"number": 118, "title": "Probe 118: Parallel Processing", "url": "http"},
    ]
    result = evaluate(repository="owner/repo", frontier_file="/fake/frontier.md")
    # No related activities found -> falls back to path_switching
    assert result["mode"] == "path_switching"
