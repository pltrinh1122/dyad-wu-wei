import pytest
from unittest.mock import patch, MagicMock
from kernel.daemon_backlog import BacklogDaemon

@pytest.fixture(autouse=True)
def mock_register_backlog_node():
    with patch('kernel.agent_frontier.register_backlog_node') as mock_reg:
        yield mock_reg


def test_backlog_list(mock_backlog_gh):
    with patch('kernel.daemon_strategic.load_ledger') as mock_load:
        mock_load.return_value = {
            "strategic_goals": [
                {
                    "id": "SG-0001",
                    "title": "Goal 1",
                    "status": "Active",
                    "prioritized_paths": [100]
                }
            ]
        }
        mock_backlog_gh.get_open_issues.return_value = [
            {
                "number": 100,
                "title": "Path 100: Prioritized Path",
                "body": "## Goal\nTest goal\n## Depends On\n200",
                "labels": [{"name": "path"}]
            },
            {
                "number": 300,
                "title": "Path 300: Unmapped Path",
                "body": "## Goal\nTest goal 2",
                "labels": [{"name": "path"}]
            }
        ]
        
        daemon = BacklogDaemon()
        result = daemon.list()
        
        assert "🎯 [SG-0001] Goal 1" in result
        assert len(result["🎯 [SG-0001] Goal 1"]) == 1
        assert result["🎯 [SG-0001] Goal 1"][0]["number"] == 100
        assert result["🎯 [SG-0001] Goal 1"][0]["dependencies"] == ["200"]
        
        assert "📋 [Backlog / Unmapped]" in result
        assert len(result["📋 [Backlog / Unmapped]"]) == 1
        assert result["📋 [Backlog / Unmapped]"][0]["number"] == 300

@patch('kernel.daemon_backlog.render_template')
def test_backlog_add(mock_render, mock_backlog_gh):
    mock_backlog_gh.create_issue.return_value = "https://github.com/pltrinh1122/agent-antigravity/issues/31"
    mock_backlog_gh.get_issue_details.return_value = {
        "title": "Path 10: Parent Path Title",
        "state": "OPEN",
        "body": "Path body\n## Meta-Index\n- [x] Node 30"
    }
    mock_render.return_value = "Rendered Template Body"

    daemon = BacklogDaemon()
    url = daemon.add("discovery", "Future Work Item", "Description of work", path_id="10")

    assert url == "https://github.com/pltrinh1122/agent-antigravity/issues/31"
    mock_backlog_gh.create_issue.assert_called_once()
    # Now labels are fetched dynamically or defaults to status: todo, backlog
    mock_backlog_gh.add_label.assert_any_call("31", "backlog")
    mock_backlog_gh.add_label.assert_any_call("31", "status: todo")
    mock_backlog_gh.rename_issue_title.assert_called_once_with("31", "Discovery 31: Future Work Item")
    mock_backlog_gh.update_issue_body.assert_called_once()
    
    mock_render.assert_called_once_with("backlog_issue", {
        "goal": "Description of work",
        "changes": "TBD",
        "pre_requisites": "TBD",
        "post_requisites": "TBD",
        "depends_on": "TBD"
    })

def test_backlog_add_missing_path():
    daemon = BacklogDaemon()
    with pytest.raises(ValueError, match="Terminal nodes \\(Activities and Discoveries\\) must belong to a parent Path"):
        daemon.add("discovery", "Title", "Goal")

def test_backlog_add_invalid_path_cases(mock_backlog_gh):
    daemon = BacklogDaemon()
    
    # Case 1: Parent Path doesn't exist
    mock_backlog_gh.get_issue_details.return_value = None
    with pytest.raises(ValueError, match="Parent Path issue 10 does not exist"):
        daemon.add("discovery", "Title", "Goal", path_id="10")
        
    # Case 2: Parent Path is closed
    mock_backlog_gh.get_issue_details.return_value = {
        "title": "Path 10: Closed Path",
        "state": "CLOSED"
    }
    with pytest.raises(ValueError, match="Parent Path issue 10 is already closed"):
        daemon.add("discovery", "Title", "Goal", path_id="10")
        
    # Case 3: Parent issue is not a Path
    mock_backlog_gh.get_issue_details.return_value = {
        "title": "Discovery 10: Harmonize - title",
        "state": "OPEN"
    }
    with pytest.raises(ValueError, match="Parent issue 10 is not classified as a Path"):
        daemon.add("discovery", "Title", "Goal", path_id="10")

def test_backlog_add_duplicate(mock_backlog_gh):
    mock_backlog_gh.get_open_issues.return_value = [
        {"number": 200, "title": "Discovery 200: Existing Title"}
    ]
    mock_backlog_gh.get_issue_details.return_value = {
        "title": "Path 10: Parent Path Title",
        "state": "OPEN",
        "body": "## Meta-Index"
    }
    
    daemon = BacklogDaemon()
    url = daemon.add("discovery", "Existing Title", "Goal", path_id="10")
    
    assert "200" in url
    mock_backlog_gh.create_issue.assert_not_called()

@patch('kernel.agent_frontier.register_backlog_node')
@patch('kernel.daemon_backlog.render_template')
def test_backlog_add_frontier_registration(mock_render, mock_register, mock_backlog_gh):
    mock_backlog_gh.create_issue.return_value = "https://github.com/pltrinh1122/agent-antigravity/issues/100"
    mock_backlog_gh.get_issue_details.return_value = {
        "title": "Path 10: Parent Path Title",
        "state": "OPEN",
        "body": "## Meta-Index"
    }
    mock_render.return_value = "Rendered Template Body"

    daemon = BacklogDaemon()
    daemon.add("discovery", "New Title", "Goal", path_id="10")
    
    mock_register.assert_called_once()

def test_check_off_meta_index(mock_backlog_gh):
    mock_backlog_gh.get_issue_details.return_value = {"body": "## Meta-Index\n- [ ] Node 229: Title [Depends: 228]\n- [ ] Node 230: Title"}
    
    daemon = BacklogDaemon()
    daemon.check_off_meta_index("213", "229")

    mock_backlog_gh.get_issue_details.assert_called_once_with("213")
    mock_backlog_gh.update_issue_body.assert_called_once_with("213", "## Meta-Index\n- [x] Node 229: Title [Depends: 228]\n- [ ] Node 230: Title")

@patch('kernel.daemon_backlog.render_template')
def test_backlog_add_path(mock_render, mock_backlog_gh):
    mock_backlog_gh.create_issue.side_effect = [
        "https://github.com/pltrinh1122/agent-antigravity/issues/100",
        "https://github.com/pltrinh1122/agent-antigravity/issues/101",
        "https://github.com/pltrinh1122/agent-antigravity/issues/102",
        "https://github.com/pltrinh1122/agent-antigravity/issues/103"
    ]
    mock_backlog_gh.get_issue_details.return_value = {
        "title": "Path 100: New Path Title",
        "state": "OPEN",
        "body": "## Meta-Index"
    }
    mock_render.return_value = "Rendered Template Body"

    daemon = BacklogDaemon()
    url = daemon.add("path", "New Path Title", "Macro goal")

    assert url == "https://github.com/pltrinh1122/agent-antigravity/issues/100"
    assert mock_backlog_gh.create_issue.call_count == 4
    # Labels added for each issue (both backlog and status: todo for terminals, and path for path)
    assert mock_backlog_gh.add_label.call_count == 8 # 2 (Path: backlog, path) + 2*3 (Align, Plan, Reflect)
    mock_backlog_gh.add_label.assert_any_call("100", "path")
    mock_backlog_gh.rename_issue_title.assert_any_call("103", "Activity 103: Reflect - New Path Title")

def test_backlog_cli_list(mock_backlog_gh, capsys):
    from kernel.daemon_backlog import main
    import sys
    
    with patch('kernel.daemon_strategic.load_ledger') as mock_load:
        mock_load.return_value = {
            "strategic_goals": [
                {
                    "id": "SG-0001",
                    "title": "Goal 1",
                    "status": "Active",
                    "prioritized_paths": [100]
                }
            ]
        }
        mock_backlog_gh.get_open_issues.return_value = [
            {
                "number": 100,
                "title": "Path 100: Prioritized Path",
                "body": "## Goal\nTest goal\n## Depends On\n200",
                "labels": [{"name": "path"}]
            },
            {
                "number": 300,
                "title": "Path 300: Unmapped Path",
                "body": "## Goal\nTest goal 2",
                "labels": [{"name": "path"}]
            }
        ]
        
        with patch.object(sys, 'argv', ['daemon_backlog', 'list']):
            main()
            captured = capsys.readouterr()
            expected_output = "\n🎯 [SG-0001] Goal 1\n  Path 100: Prioritized Path [Depends: 200]\n\n📋 [Backlog / Unmapped]\n  Path 300: Unmapped Path\n\n"
            assert captured.out == expected_output

def test_backlog_workspace_isolation(tmp_path):
    import os
    workspace_dir = tmp_path / "child_workspace"
    workspace_dir.mkdir()
    
    # Create child artifacts/ frontier state path
    artifacts_dir = workspace_dir / "artifacts"
    artifacts_dir.mkdir()
    frontier_file = artifacts_dir / "frontier_state.md"
    frontier_file.touch()
    
    # Set config path in env
    mock_env = {"SPAO_WORKSPACE_DIR": str(workspace_dir)}
    
    with patch.dict(os.environ, mock_env), \
         patch("kernel.agent_frontier.register_backlog_node") as mock_register, \
         patch("drivers.github_client.create_issue", return_value="https://github.com/pltrinh1122/agent-antigravity/issues/100"), \
         patch("drivers.github_client.get_issue_details", return_value={"title": "Path 10: Parent Path Title", "state": "OPEN", "body": "## Meta-Index"}), \
         patch("drivers.github_client.get_open_issues", return_value=[]), \
         patch("drivers.github_client.add_label"), \
         patch("drivers.github_client.rename_issue_title"), \
         patch("drivers.github_client.update_issue_body"):
         
        daemon = BacklogDaemon()
        daemon.add("discovery", "Workspace Work Item", "Description of work", path_id="10")
        
        # Verify that register_backlog_node was called with frontier_file in the workspace
        mock_register.assert_called_once()
        args, kwargs = mock_register.call_args
        assert args[0] == str(frontier_file)

