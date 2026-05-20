import pytest
from unittest.mock import MagicMock, patch
import os

_FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

@pytest.fixture(autouse=True, scope="session")
def stub_gh_cli():
    """Inject tests/fixtures/ into PATH at the session level to redirect all gh calls."""
    original_path = os.environ.get("PATH", "")
    os.environ["PATH"] = _FIXTURES_DIR + os.pathsep + original_path
    yield
    os.environ["PATH"] = original_path


@pytest.fixture
def mock_gh():
    """Provides a centralized mock for github_client."""
    with patch("orchestrator.node_lifecycle.github_client") as m:
        m.get_issue_details.return_value = {"title": "Dummy Issue", "body": "## Goal\nDummy Goal"}
        m.list_issues_by_label.return_value = []
        yield m

@pytest.fixture
def mock_fe():
    """Provides a centralized mock for mgr_frontier."""
    with patch("orchestrator.node_lifecycle.mgr_frontier") as m:
        m.read_active_node.return_value = "None"
        m.read_active_path.return_value = "None"
        yield m

@pytest.fixture
def mock_telemetry():
    """Provides a centralized mock for TelemetryManager."""
    with patch("orchestrator.mgr_telemetry.TelemetryManager") as m:
        instance = m.return_value
        yield instance

@pytest.fixture
def mock_subprocess():
    """Provides a centralized mock for subprocess.run."""
    with patch("subprocess.run") as m:
        m.return_value = MagicMock(returncode=0, stdout="success")
        yield m

@pytest.fixture
def mock_backlog():
    """Provides a centralized mock for mgr_backlog."""
    with patch("orchestrator.node_lifecycle.mgr_backlog") as m:
        yield m

@pytest.fixture
def mock_nba():
    """Provides a centralized mock for mgr_nba."""
    with patch("orchestrator.node_lifecycle.mgr_nba") as m:
        instance = m.NBAManager.return_value
        instance.evaluate.return_value = {"type": "path_switching", "recommendations": []}
        yield m

@pytest.fixture
def mock_backlog_gh():
    """Provides a centralized mock for github_client inside mgr_backlog."""
    with patch("orchestrator.mgr_backlog.github_client") as m:
        yield m

@pytest.fixture
def mock_tempfile():
    """Provides a centralized mock for tempfile.NamedTemporaryFile."""
    with patch("tempfile.NamedTemporaryFile") as m:
        mock_file = MagicMock()
        mock_file.name = "/tmp/fake_temp_file"
        m.return_value.__enter__.return_value = mock_file
        yield m, mock_file

@pytest.fixture
def temp_workspace(tmp_path):
    """Sets up a temporary workspace with basic frontier files."""
    frontier = tmp_path / "frontier_state.md"
    frontier.write_text("# Agentic Frontier State\n\n## Current Active Node\nNone\n")
    
    antigravity_yml = tmp_path / "antigravity.yml"
    antigravity_yml.write_text("nodes:\n  Activity: { status: Act }\n")
    
    return {
        "frontier": str(frontier),
        "antigravity_yml": str(antigravity_yml),
        "root": str(tmp_path)
    }
