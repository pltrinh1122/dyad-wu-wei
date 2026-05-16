import pytest
from unittest.mock import patch, MagicMock
from skills.github_client import create_issue, close_issue, update_issue_body

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
