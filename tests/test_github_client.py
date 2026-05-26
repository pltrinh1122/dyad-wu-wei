import pytest
from unittest.mock import MagicMock
from drivers.github_client import create_issue, close_issue, reopen_issue, update_issue_body, create_pull_request, list_issues_by_label, get_issue_labels, add_label, remove_label, get_open_prs, get_open_issues, get_issue_details

def test_create_issue(mock_tempfile, mock_subprocess):
    mock_gh_cmd, mock_file = mock_tempfile
    mock_subprocess.return_value.stdout = "https://github.com/pltrinh1122/dz-cil/issues/99"
    
    issue_url = create_issue("Test Title", "Test Body")
    
    assert issue_url == "https://github.com/pltrinh1122/dz-cil/issues/99"
    mock_file.write.assert_called_once_with("Test Body")
    mock_subprocess.assert_called_once()
    args = mock_subprocess.call_args[0][0]
    assert "create" in args

def test_close_issue(mock_subprocess):
    mock_close = MagicMock(returncode=0)
    mock_labels = MagicMock(stdout='{"labels": [{"name": "status: in-progress"}]}', returncode=0)
    mock_remove = MagicMock(returncode=0)
    
    mock_subprocess.side_effect = [mock_close, mock_labels, mock_remove]
    
    close_issue("99", "Closing comment")
    
    assert mock_subprocess.call_count == 3
    close_args = mock_subprocess.call_args_list[0][0][0]
    assert "close" in close_args
    assert "99" in close_args
    
    view_args = mock_subprocess.call_args_list[1][0][0]
    assert "view" in view_args
    
    remove_args = mock_subprocess.call_args_list[2][0][0]
    assert "--remove-label" in remove_args
    assert "status: in-progress" in remove_args

def test_reopen_issue(mock_subprocess):
    reopen_issue("99")
    mock_subprocess.assert_called_once()
    args = mock_subprocess.call_args[0][0]
    assert "reopen" in args

def test_update_issue_body(mock_tempfile, mock_subprocess):
    mock_gh_cmd, mock_file = mock_tempfile
    update_issue_body("99", "New Body")
    mock_file.write.assert_called_once_with("New Body")
    mock_subprocess.assert_called_once()

def test_create_pull_request(mock_tempfile, mock_subprocess):
    mock_gh_cmd, mock_file = mock_tempfile
    
    mock_git_ref = MagicMock(returncode=0, stdout="node/294-test\n")
    mock_pr_list = MagicMock(returncode=0, stdout="[]\n")
    mock_pr_create = MagicMock(returncode=0, stdout="https://github.com/pltrinh1122/dz-cil/pull/99\n")
    
    mock_subprocess.side_effect = [mock_git_ref, mock_pr_list, mock_pr_create]
    
    pr_url = create_pull_request("Test PR Title", "Test PR Body")
    assert pr_url == "https://github.com/pltrinh1122/dz-cil/pull/99"
    mock_file.write.assert_called_once_with("Test PR Body")
    
    assert mock_subprocess.call_count == 3
    args0 = mock_subprocess.call_args_list[0][0][0]
    assert args0 == ["git", "symbolic-ref", "--short", "HEAD"]
    
    args1 = mock_subprocess.call_args_list[1][0][0]
    assert "pr" in args1
    assert "list" in args1
    assert "node/294-test" in args1
    
    args2 = mock_subprocess.call_args_list[2][0][0]
    assert "pr" in args2
    assert "create" in args2

def test_create_pull_request_already_exists(mock_tempfile, mock_subprocess):
    mock_gh_cmd, mock_file = mock_tempfile
    
    mock_git_ref = MagicMock(returncode=0, stdout="node/294-test\n")
    mock_pr_list = MagicMock(returncode=0, stdout='[{"url": "https://github.com/pltrinh1122/dz-cil/pull/99"}]\n')
    
    mock_subprocess.side_effect = [mock_git_ref, mock_pr_list]
    
    pr_url = create_pull_request("Test PR Title", "Test PR Body")
    assert pr_url == "https://github.com/pltrinh1122/dz-cil/pull/99"
    
    mock_file.write.assert_not_called()
    assert mock_subprocess.call_count == 2
    
    args0 = mock_subprocess.call_args_list[0][0][0]
    assert args0 == ["git", "symbolic-ref", "--short", "HEAD"]
    
    args1 = mock_subprocess.call_args_list[1][0][0]
    assert "pr" in args1
    assert "list" in args1
    assert "node/294-test" in args1

def test_create_pull_request_with_explicit_head(mock_tempfile, mock_subprocess):
    mock_gh_cmd, mock_file = mock_tempfile
    
    mock_pr_list = MagicMock(returncode=0, stdout="[]\n")
    mock_pr_create = MagicMock(returncode=0, stdout="https://github.com/pltrinh1122/dz-cil/pull/100\n")
    
    mock_subprocess.side_effect = [mock_pr_list, mock_pr_create]
    
    pr_url = create_pull_request("Test PR Title", "Test PR Body", head="custom-branch")
    assert pr_url == "https://github.com/pltrinh1122/dz-cil/pull/100"
    mock_file.write.assert_called_once_with("Test PR Body")
    
    assert mock_subprocess.call_count == 2
    args0 = mock_subprocess.call_args_list[0][0][0]
    assert "custom-branch" in args0
    args1 = mock_subprocess.call_args_list[1][0][0]
    assert "--head" in args1
    assert "custom-branch" in args1


def test_list_issues_by_label(mock_subprocess):
    mock_list_result = MagicMock(stdout='[{"number": 31, "title": "Backlog Item", "url": "https://...", "state": "OPEN"}]', returncode=0)
    mock_subprocess.side_effect = [mock_list_result]

    items = list_issues_by_label("backlog")
    assert len(items) == 1
    assert items[0]["number"] == 31
    assert mock_subprocess.call_count == 1

def test_get_issue_labels(mock_subprocess):
    mock_subprocess.return_value.stdout = '{"labels": [{"name": "status: in-progress"}, {"name": "backlog"}]}'
    labels = get_issue_labels("145")
    assert "status: in-progress" in labels

def test_add_label(mock_subprocess):
    add_label("145", "status: in-progress")
    mock_subprocess.assert_called_once()

def test_remove_label(mock_subprocess):
    remove_label("145", "backlog")
    mock_subprocess.assert_called_once()

def test_get_open_prs(mock_subprocess):
    # First call is the list, second is the view
    mock_subprocess.return_value.stdout = ""
    def side_effect(*args, **kwargs):
        class MockProc:
            returncode = 0
            stdout = ""
        mock_proc = MockProc()
        if "list" in args[0]:
            mock_proc.stdout = '[{"number": 123, "title": "Test PR", "headRefName": "node/123-test", "url": "https://..."}]'
        else:
            mock_proc.stdout = '{"state": "OPEN"}'
        return mock_proc
    
    mock_subprocess.side_effect = side_effect
    prs = get_open_prs()
    assert len(prs) == 1
def test_get_open_issues(mock_subprocess):
    mock_subprocess.return_value.stdout = '[{"number": 1, "title": "A", "body": "B", "labels": [{"name": "backlog"}]}]'
    issues = get_open_issues()
    assert len(issues) == 1

def test_get_issue_details(mock_subprocess):
    mock_subprocess.return_value.stdout = '{"number": 1, "title": "A", "body": "B"}'
    details = get_issue_details("1")
    assert details["title"] == "A"
