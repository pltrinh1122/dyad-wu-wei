"""Tests for drivers/support_client.py — full-cycle ticket tracking."""
import json
import pytest
from unittest.mock import patch, MagicMock

from drivers.support_client import (
    _labels_to_phase,
    file_support_ticket,
    get_ticket_status,
    list_support_tickets,
)


class TestLabelsToPhase:
    """Test the label-to-lifecycle-phase mapping per WHY-1372."""

    def test_closed_state_is_resolved(self):
        assert _labels_to_phase(["support", "backlog"], "CLOSED") == "✅ Resolved"

    def test_in_progress_label(self):
        assert _labels_to_phase(["support", "status: in-progress"], "OPEN") == "🔧 In Progress"

    def test_backlog_label(self):
        assert _labels_to_phase(["support", "backlog"], "OPEN") == "📋 Accepted / Queued"

    def test_triage_label(self):
        assert _labels_to_phase(["support", "status:triage"], "OPEN") == "🔍 Under Review"

    def test_no_lifecycle_labels_is_received(self):
        assert _labels_to_phase(["support", "external-project"], "OPEN") == "📥 Received"

    def test_empty_labels_is_received(self):
        assert _labels_to_phase([], "OPEN") == "📥 Received"


class TestFileTicket:
    """Test the file_support_ticket function."""

    def test_invalid_type_raises(self):
        with pytest.raises(ValueError, match="Invalid ticket type"):
            file_support_ticket("invalid", "fl", "test")

    @patch("drivers.support_client.subprocess.run")
    def test_file_creates_issue(self, mock_run):
        mock_run.return_value = MagicMock(stdout="https://github.com/test/1\n")
        url = file_support_ticket("bug", "fl", "Something broke")
        assert url == "https://github.com/test/1"
        mock_run.assert_called_once()
        cmd = mock_run.call_args[0][0]
        assert "gh" in cmd
        assert "issue" in cmd
        assert "create" in cmd

    @patch("drivers.support_client.subprocess.run")
    def test_file_includes_blocking_flag(self, mock_run):
        mock_run.return_value = MagicMock(stdout="https://github.com/test/2\n")
        file_support_ticket("escalation", "fl", "Blocked!", blocking=True)
        cmd_kwargs = mock_run.call_args
        body_idx = cmd_kwargs[0][0].index("--body") + 1
        body = cmd_kwargs[0][0][body_idx]
        assert "cannot proceed" in body


class TestGetTicketStatus:
    """Test the get_ticket_status function."""

    @patch("drivers.support_client.subprocess.run")
    def test_status_returns_structured_data(self, mock_run):
        mock_data = {
            "number": 1233,
            "title": "[SUPPORT] [fl] bug: test",
            "state": "OPEN",
            "labels": [{"name": "support"}, {"name": "backlog"}],
            "createdAt": "2026-05-29T10:00:00Z",
            "updatedAt": "2026-05-29T11:00:00Z",
            "comments": [],
            "url": "https://github.com/test/1233",
        }
        mock_run.return_value = MagicMock(stdout=json.dumps(mock_data))
        result = get_ticket_status(1233)

        assert result["number"] == 1233
        assert result["phase"] == "📋 Accepted / Queued"
        assert result["state"] == "OPEN"
        assert "support" in result["labels"]

    @patch("drivers.support_client.subprocess.run")
    def test_status_resolved_ticket(self, mock_run):
        mock_data = {
            "number": 42,
            "title": "[SUPPORT] [fl] bug: fixed",
            "state": "CLOSED",
            "labels": [{"name": "support"}, {"name": "backlog"}],
            "createdAt": "2026-05-29T10:00:00Z",
            "updatedAt": "2026-05-29T12:00:00Z",
            "comments": [{"author": {"login": "bot"}, "body": "## Remediation\n- **Fix**: commit abc123", "createdAt": "2026-05-29T12:00:00Z"}],
            "url": "https://github.com/test/42",
        }
        mock_run.return_value = MagicMock(stdout=json.dumps(mock_data))
        result = get_ticket_status(42)

        assert result["phase"] == "✅ Resolved"
        assert len(result["comments"]) == 1


class TestListTickets:
    """Test the list_support_tickets function."""

    @patch("drivers.support_client.subprocess.run")
    def test_list_returns_tickets(self, mock_run):
        mock_data = [
            {"number": 1, "title": "[SUPPORT] [fl] bug: a", "labels": [{"name": "support"}], "createdAt": "2026-05-29T10:00:00Z", "state": "OPEN"},
            {"number": 2, "title": "[SUPPORT] [acme] tooling: b", "labels": [{"name": "support"}, {"name": "backlog"}], "createdAt": "2026-05-29T11:00:00Z", "state": "OPEN"},
        ]
        mock_run.return_value = MagicMock(stdout=json.dumps(mock_data))
        result = list_support_tickets()
        assert len(result) == 2
        assert result[0]["phase"] == "📥 Received"
        assert result[1]["phase"] == "📋 Accepted / Queued"

    @patch("drivers.support_client.subprocess.run")
    def test_list_filters_by_project(self, mock_run):
        mock_data = [
            {"number": 1, "title": "[SUPPORT] [fl] bug: a", "labels": [{"name": "support"}], "createdAt": "2026-05-29T10:00:00Z", "state": "OPEN"},
            {"number": 2, "title": "[SUPPORT] [acme] tooling: b", "labels": [{"name": "support"}], "createdAt": "2026-05-29T11:00:00Z", "state": "OPEN"},
        ]
        mock_run.return_value = MagicMock(stdout=json.dumps(mock_data))
        result = list_support_tickets(project_filter="fl")
        assert len(result) == 1
        assert result[0]["number"] == 1

    @patch("drivers.support_client.subprocess.run")
    def test_list_empty(self, mock_run):
        mock_run.return_value = MagicMock(stdout="[]")
        result = list_support_tickets()
        assert result == []
