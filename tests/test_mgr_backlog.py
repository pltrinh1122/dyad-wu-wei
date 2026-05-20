import pytest
from unittest.mock import patch, MagicMock
from orchestrator.mgr_backlog import BacklogManager

def test_backlog_list(mock_backlog_gh):
    mock_backlog_gh.list_issues_by_label.return_value = [{"number": 31, "title": "Backlog Item", "url": "https://..."}]
    manager = BacklogManager()
    items = manager.list("backlog")
    assert len(items) == 1
    assert items[0]["number"] == 31
    mock_backlog_gh.list_issues_by_label.assert_called_once_with("backlog")

@patch('orchestrator.mgr_backlog.render_template')
def test_backlog_add(mock_render, mock_backlog_gh):
    mock_backlog_gh.create_issue.return_value = "https://github.com/pltrinh1122/agent-antigravity/issues/31"
    mock_backlog_gh.get_issue_details.return_value = {"body": "Path body\n## Meta-Index\n- [x] Node 30"}
    mock_render.return_value = "Rendered Template Body"

    manager = BacklogManager()
    url = manager.add("probe", "Future Work Item", "Description of work", path_id="10")

    assert url == "https://github.com/pltrinh1122/agent-antigravity/issues/31"
    mock_backlog_gh.create_issue.assert_called_once()
    mock_backlog_gh.add_label.assert_called_once_with("31", "backlog")
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
    manager = BacklogManager()
    with pytest.raises(ValueError, match="Terminal nodes \\(Activities and Probes\\) must belong to a parent Path"):
        manager.add("probe", "Title", "Goal")

def test_check_off_meta_index(mock_backlog_gh):
    mock_backlog_gh.get_issue_details.return_value = {"body": "## Meta-Index\n- [ ] Node 229: Title [Depends: 228]\n- [ ] Node 230: Title"}
    
    manager = BacklogManager()
    manager.check_off_meta_index("213", "229")

    mock_backlog_gh.get_issue_details.assert_called_once_with("213")
    mock_backlog_gh.update_issue_body.assert_called_once_with("213", "## Meta-Index\n- [x] Node 229: Title [Depends: 228]\n- [ ] Node 230: Title")

@patch('orchestrator.mgr_backlog.render_template')
def test_backlog_add_path(mock_render, mock_backlog_gh):
    mock_backlog_gh.create_issue.side_effect = [
        "https://github.com/pltrinh1122/agent-antigravity/issues/100",
        "https://github.com/pltrinh1122/agent-antigravity/issues/101",
        "https://github.com/pltrinh1122/agent-antigravity/issues/102",
        "https://github.com/pltrinh1122/agent-antigravity/issues/103"
    ]
    mock_backlog_gh.get_issue_details.return_value = {"body": "## Meta-Index"}
    mock_render.return_value = "Rendered Template Body"

    manager = BacklogManager()
    url = manager.add("path", "New Path Title", "Macro goal")

    assert url == "https://github.com/pltrinh1122/agent-antigravity/issues/100"
    assert mock_backlog_gh.create_issue.call_count == 4
    assert mock_backlog_gh.add_label.call_count == 4
    assert mock_backlog_gh.rename_issue_title.call_count == 4
    
    mock_backlog_gh.rename_issue_title.assert_any_call("100", "Path 100: New Path Title")
    mock_backlog_gh.rename_issue_title.assert_any_call("101", "Probe 101: Align - New Path Title")
    mock_backlog_gh.rename_issue_title.assert_any_call("102", "Probe 102: Plan - New Path Title")
    mock_backlog_gh.rename_issue_title.assert_any_call("103", "Activity 103: Reflect - New Path Title")
