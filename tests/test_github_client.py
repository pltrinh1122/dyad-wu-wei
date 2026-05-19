import pytest
from unittest.mock import patch, MagicMock
from skills.github_client import create_issue, close_issue, reopen_issue, update_issue_body, create_pull_request, list_issues_by_label, add_to_backlog, get_issue_labels, add_label, remove_label, get_open_prs

@patch('skills.github_client.subprocess.run')
@patch('skills.github_client.tempfile.NamedTemporaryFile')
def test_create_issue(mock_tempfile, mock_run):
    mock_result = MagicMock()
    mock_result.stdout = "https://github.com/pltrinh1122/agent-antigravity/issues/99"
    mock_result.returncode = 0
    mock_run.return_value = mock_result
    
    mock_file = MagicMock()
    mock_file.name = "/tmp/fake.md"
    mock_tempfile.return_value.__enter__.return_value = mock_file
    
    issue_url = create_issue("Test Title", "Test Body")
    
    assert issue_url == "https://github.com/pltrinh1122/agent-antigravity/issues/99"
    mock_file.write.assert_called_once_with("Test Body")
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args == ["gh", "issue", "create", "--title", "Test Title", "-F", "/tmp/fake.md"]

@patch('skills.github_client.subprocess.run')
def test_close_issue(mock_run):
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_run.return_value = mock_result

    close_issue("99", "Closing comment")
    
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args == ["gh", "issue", "close", "99", "-c", "Closing comment"]

@patch('skills.github_client.subprocess.run')
def test_reopen_issue(mock_run):
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_run.return_value = mock_result

    reopen_issue("99")
    
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args == ["gh", "issue", "reopen", "99"]

@patch('skills.github_client.subprocess.run')
@patch('skills.github_client.tempfile.NamedTemporaryFile')
def test_update_issue_body(mock_tempfile, mock_run):
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_run.return_value = mock_result

    mock_file = MagicMock()
    mock_file.name = "/tmp/fake.md"
    mock_tempfile.return_value.__enter__.return_value = mock_file
    
    update_issue_body("99", "New Body")
    
    mock_file.write.assert_called_once_with("New Body")
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args == ["gh", "issue", "edit", "99", "--body-file", "/tmp/fake.md"]

@patch('skills.github_client.subprocess.run')
@patch('skills.github_client.tempfile.NamedTemporaryFile')
def test_create_pull_request(mock_tempfile, mock_run):
    mock_result = MagicMock()
    mock_result.stdout = "https://github.com/pltrinh1122/agent-antigravity/pull/99"
    mock_result.returncode = 0
    mock_run.return_value = mock_result
    
    mock_file = MagicMock()
    mock_file.name = "/tmp/fake_pr.md"
    mock_tempfile.return_value.__enter__.return_value = mock_file
    
    pr_url = create_pull_request("Test PR Title", "Test PR Body")
    
    assert pr_url == "https://github.com/pltrinh1122/agent-antigravity/pull/99"
    mock_file.write.assert_called_once_with("Test PR Body")
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args == ["gh", "pr", "create", "--title", "Test PR Title", "-F", "/tmp/fake_pr.md"]

@patch('skills.github_client.subprocess.run')
def test_list_issues_by_label(mock_run):
    mock_list_result = MagicMock()
    mock_list_result.stdout = '[{"number": 31, "title": "Backlog Item", "url": "https://github.com/org/repo/issues/31"}]'
    
    mock_view_result = MagicMock()
    mock_view_result.stdout = '{"state": "OPEN"}'

    mock_run.side_effect = [mock_list_result, mock_view_result]

    items = list_issues_by_label("backlog")

    assert len(items) == 1
    assert items[0]["number"] == 31
    assert items[0]["title"] == "Backlog Item"
    
    assert mock_run.call_count == 2
    list_args = mock_run.call_args_list[0][0][0]
    assert list_args == ["gh", "issue", "list", "--label", "backlog", "--state", "open",
                    "--json", "number,title,url"]
                    
    view_args = mock_run.call_args_list[1][0][0]
    assert view_args == ["gh", "issue", "view", "31", "--json", "state"]

@patch('skills.github_client.subprocess.run')
def test_list_issues_by_label_empty(mock_run):
    mock_result = MagicMock()
    mock_result.stdout = ""
    mock_run.return_value = mock_result

    items = list_issues_by_label("backlog")
    assert items == []

@patch('skills.github_client.subprocess.run')
@patch('skills.github_client.tempfile.NamedTemporaryFile')
@patch('skills.github_client.render_template')
def test_add_to_backlog(mock_render, mock_tempfile, mock_run):
    mock_result_create = MagicMock()
    mock_result_create.stdout = "https://github.com/pltrinh1122/agent-antigravity/issues/31"
    
    mock_result_rename = MagicMock()
    mock_result_rename.stdout = ""

    mock_result_view = MagicMock()
    mock_result_view.stdout = '{"body": "Path body\\n## Meta-Index\\n- [x] Node 30"}'
    
    mock_result_edit = MagicMock()
    mock_result_edit.stdout = ""

    mock_run.side_effect = [mock_result_create, mock_result_rename, mock_result_view, mock_result_edit]

    mock_file = MagicMock()
    mock_file.name = "/tmp/fake_backlog.md"
    mock_tempfile.return_value.__enter__.return_value = mock_file
    
    mock_render.return_value = "Rendered Template Body"

    url = add_to_backlog("probe", "Future Work Item", "Description of work", path_id="10")

    assert url == "https://github.com/pltrinh1122/agent-antigravity/issues/31"
    mock_file.write.assert_any_call("Rendered Template Body")
    
    assert mock_run.call_count == 4
    
    # Check first call (create)
    create_args = mock_run.call_args_list[0][0][0]
    assert create_args == ["gh", "issue", "create", "--title", "Probe: Future Work Item",
                    "-F", "/tmp/fake_backlog.md", "--label", "backlog"]
                    
    # Check second call (edit/rename)
    edit_args = mock_run.call_args_list[1][0][0]
    assert edit_args == ["gh", "issue", "edit", "31", "--title", "Probe 31: Future Work Item"]
    
    # Check third call (view path)
    view_args = mock_run.call_args_list[2][0][0]
    assert view_args == ["gh", "issue", "view", "10", "--json", "body"]
    
    # Check fourth call (edit path)
    update_args = mock_run.call_args_list[3][0][0]
    assert update_args == ["gh", "issue", "edit", "10", "--body-file", mock_file.name]
    
    mock_render.assert_called_once_with("backlog_issue", {
        "goal": "Description of work",
        "changes": "TBD",
        "pre_requisites": "TBD",
        "post_requisites": "TBD",
        "depends_on": "TBD"
    })

def test_add_to_backlog_missing_path():
    with pytest.raises(ValueError, match="Terminal nodes \\(Activities and Probes\\) must belong to a parent Path"):
        add_to_backlog("probe", "Title", "Goal")

@patch('skills.github_client.subprocess.run')
def test_get_issue_labels(mock_run):
    mock_result = MagicMock()
    mock_result.stdout = '{"labels": [{"name": "status: in-progress"}, {"name": "backlog"}]}'
    mock_run.return_value = mock_result

    labels = get_issue_labels("145")

    assert labels == ["status: in-progress", "backlog"]
    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args == ["gh", "issue", "view", "145", "--json", "labels"]

@patch('skills.github_client.subprocess.run')
def test_add_label(mock_run):
    mock_result = MagicMock()
    mock_run.return_value = mock_result

    add_label("145", "status: in-progress")

    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args == ["gh", "issue", "edit", "145", "--add-label", "status: in-progress"]

@patch('skills.github_client.subprocess.run')
def test_remove_label(mock_run):
    mock_result = MagicMock()
    mock_run.return_value = mock_result

    remove_label("145", "backlog")

    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args == ["gh", "issue", "edit", "145", "--remove-label", "backlog"]

@patch('skills.github_client.subprocess.run')
def test_get_open_prs(mock_run):
    mock_result = MagicMock()
    mock_result.stdout = '[{"number": 123, "title": "Test PR", "headRefName": "node/123-test", "url": "https://..."}]'
    mock_run.return_value = mock_result

    prs = get_open_prs()

    assert len(prs) == 1
    assert prs[0]["number"] == 123
    assert prs[0]["headRefName"] == "node/123-test"

    mock_run.assert_called_once()
    args = mock_run.call_args[0][0]
    assert args == ["gh", "pr", "list", "--state", "open", "--json", "number,title,headRefName,url"]

@patch('skills.github_client.subprocess.run')
@patch('skills.github_client.update_issue_body')
def test_check_off_meta_index(mock_update, mock_run):
    mock_result = MagicMock()
    mock_result.stdout = '{"body": "## Meta-Index\\n- [ ] Node 229: Title [Depends: 228]\\n- [ ] Node 230: Title"}'
    mock_result.returncode = 0
    mock_run.return_value = mock_result

    from skills.github_client import check_off_meta_index
    check_off_meta_index("213", "229")

    mock_run.assert_called_once()
    mock_update.assert_called_once_with("213", "## Meta-Index\n- [x] Node 229: Title [Depends: 228]\n- [ ] Node 230: Title")

@patch('skills.github_client.subprocess.run')
@patch('skills.github_client.update_issue_body')
def test_check_off_meta_index_not_found(mock_update, mock_run):
    mock_result = MagicMock()
    mock_result.stdout = '{"body": "## Meta-Index\\n- [ ] Node 230: Title"}'
    mock_result.returncode = 0
    mock_run.return_value = mock_result

    from skills.github_client import check_off_meta_index
    check_off_meta_index("213", "229")

    mock_run.assert_called_once()
    mock_update.assert_not_called()
