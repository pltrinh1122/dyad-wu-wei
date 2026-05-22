import pytest
from unittest.mock import patch, MagicMock
from drivers.infra_manager import start_daemon, stop_daemon, get_daemon_status

@patch('drivers.infra_manager.subprocess.run')
def test_start_daemon_systemd_user(mock_run):
    start_daemon("github-runner", daemon_type="systemd_user")
    mock_run.assert_called_once_with(["systemctl", "--user", "start", "github-runner"], check=True)

@patch('drivers.infra_manager.subprocess.run')
def test_stop_daemon_systemd_user(mock_run):
    stop_daemon("github-runner", daemon_type="systemd_user")
    mock_run.assert_called_once_with(["systemctl", "--user", "stop", "github-runner"], check=True)

@patch('drivers.infra_manager.subprocess.run')
def test_get_daemon_status_systemd_user(mock_run):
    mock_result = MagicMock()
    mock_result.stdout = "active\n"
    mock_run.return_value = mock_result
    
    status = get_daemon_status("github-runner", daemon_type="systemd_user")
    
    assert status == "active"
    mock_run.assert_called_once_with(["systemctl", "--user", "is-active", "github-runner"], capture_output=True, text=True)

def test_invalid_daemon_type():
    with pytest.raises(ValueError):
        start_daemon("github-runner", daemon_type="docker")
