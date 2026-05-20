import pytest
from unittest.mock import patch, MagicMock
from orchestrator.mgr_backlog import BacklogManager

@patch('skills.github_client.list_issues_by_label')
def test_backlog_list(mock_list):
    mock_list.return_value = [{"number": 31, "title": "Backlog Item", "url": "https://..."}]
    manager = BacklogManager()
    items = manager.list("backlog")
    assert len(items) == 1
    assert items[0]["number"] == 31
    mock_list.assert_called_once_with("backlog")

@patch('skills.github_client.create_issue')
@patch('skills.github_client.add_label')
@patch('skills.github_client.rename_issue_title')
@patch('skills.github_client.get_issue_details')
@patch('skills.github_client.update_issue_body')
@patch('orchestrator.mgr_backlog.render_template')
def test_backlog_add(mock_render, mock_update, mock_details, mock_rename, mock_label, mock_create):
    mock_create.return_value = "https://github.com/pltrinh1122/agent-antigravity/issues/31"
    mock_details.return_value = {"body": "Path body\n## Meta-Index\n- [x] Node 30"}
    mock_render.return_value = "Rendered Template Body"

    manager = BacklogManager()
    url = manager.add("probe", "Future Work Item", "Description of work", path_id="10")

    assert url == "https://github.com/pltrinh1122/agent-antigravity/issues/31"
    mock_create.assert_called_once()
    mock_label.assert_called_once_with("31", "backlog")
    mock_rename.assert_called_once_with("31", "Probe 31: Future Work Item")
    mock_update.assert_called_once()
    
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

@patch('skills.github_client.get_issue_details')
@patch('skills.github_client.update_issue_body')
def test_check_off_meta_index(mock_update, mock_details):
    mock_details.return_value = {"body": "## Meta-Index\n- [ ] Node 229: Title [Depends: 228]\n- [ ] Node 230: Title"}
    
    manager = BacklogManager()
    manager.check_off_meta_index("213", "229")

    mock_details.assert_called_once_with("213")
    mock_update.assert_called_once_with("213", "## Meta-Index\n- [x] Node 229: Title [Depends: 228]\n- [ ] Node 230: Title")
