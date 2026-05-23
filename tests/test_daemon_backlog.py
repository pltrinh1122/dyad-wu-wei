import pytest
from unittest.mock import patch, MagicMock
from kernel.daemon_backlog import BacklogDaemon

@pytest.fixture(autouse=True)
def mock_register_backlog_node():
    with patch('kernel.agent_frontier.register_backlog_node') as mock_reg:
        yield mock_reg


def test_backlog_list(mock_backlog_gh):
    mock_backlog_gh.list_issues_by_label.return_value = [{"number": 31, "title": "Backlog Item", "url": "https://..."}]
    daemon = BacklogDaemon()
    items = daemon.list("backlog")
    assert len(items) == 1
    assert items[0]["number"] == 31
    mock_backlog_gh.list_issues_by_label.assert_called_once_with("backlog")

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
    url = daemon.add("probe", "Future Work Item", "Description of work", path_id="10")

    assert url == "https://github.com/pltrinh1122/agent-antigravity/issues/31"
    mock_backlog_gh.create_issue.assert_called_once()
    # Now labels are fetched dynamically or defaults to status: todo, backlog
    mock_backlog_gh.add_label.assert_any_call("31", "backlog")
    mock_backlog_gh.add_label.assert_any_call("31", "status: todo")
    mock_backlog_gh.rename_issue_title.assert_called_once_with("31", "Probe 31: Future Work Item")
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
    with pytest.raises(ValueError, match="Terminal nodes \\(Activities and Probes\\) must belong to a parent Path"):
        daemon.add("probe", "Title", "Goal")

def test_backlog_add_invalid_path_cases(mock_backlog_gh):
    daemon = BacklogDaemon()
    
    # Case 1: Parent Path doesn't exist
    mock_backlog_gh.get_issue_details.return_value = None
    with pytest.raises(ValueError, match="Parent Path issue 10 does not exist"):
        daemon.add("probe", "Title", "Goal", path_id="10")
        
    # Case 2: Parent Path is closed
    mock_backlog_gh.get_issue_details.return_value = {
        "title": "Path 10: Closed Path",
        "state": "CLOSED"
    }
    with pytest.raises(ValueError, match="Parent Path issue 10 is already closed"):
        daemon.add("probe", "Title", "Goal", path_id="10")
        
    # Case 3: Parent issue is not a Path
    mock_backlog_gh.get_issue_details.return_value = {
        "title": "Probe 10: Align - title",
        "state": "OPEN"
    }
    with pytest.raises(ValueError, match="Parent issue 10 is not classified as a Path"):
        daemon.add("probe", "Title", "Goal", path_id="10")

def test_backlog_add_duplicate(mock_backlog_gh):
    mock_backlog_gh.get_open_issues.return_value = [
        {"number": 200, "title": "Probe 200: Existing Title"}
    ]
    mock_backlog_gh.get_issue_details.return_value = {
        "title": "Path 10: Parent Path Title",
        "state": "OPEN",
        "body": "## Meta-Index"
    }
    
    daemon = BacklogDaemon()
    url = daemon.add("probe", "Existing Title", "Goal", path_id="10")
    
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
    daemon.add("probe", "New Title", "Goal", path_id="10")
    
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
    assert mock_backlog_gh.rename_issue_title.call_count == 4
    
    mock_backlog_gh.rename_issue_title.assert_any_call("100", "Path 100: New Path Title")
    mock_backlog_gh.rename_issue_title.assert_any_call("101", "Probe 101: Align - New Path Title")
    mock_backlog_gh.rename_issue_title.assert_any_call("102", "Probe 102: Plan - New Path Title")
    mock_backlog_gh.rename_issue_title.assert_any_call("103", "Activity 103: Reflect - New Path Title")
