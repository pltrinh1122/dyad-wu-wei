"""Tests for the Positive Feedback Integration (Node 974).

Coverage:
- drivers.knowledge_accrual_skill.record_positive_feedback (skill layer)
- kernel.daemon_knowledge_accrual.enforce_reflection_hook positive-feedback branch
"""

import json
import os
import pytest
from unittest.mock import patch, MagicMock


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write_telemetry(path: str, events: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for e in events:
            f.write(json.dumps(e) + "\n")


# ---------------------------------------------------------------------------
# record_positive_feedback — skill layer
# ---------------------------------------------------------------------------

class TestRecordPositiveFeedback:
    """Tests for drivers.knowledge_accrual_skill.record_positive_feedback."""

    def test_creates_reaffirm_file(self, tmp_path):
        reaffirm_path = tmp_path / "audit" / "reaffirm-42.md"
        with patch("drivers.knowledge_accrual_skill.TelemetryDaemon") as MockDaemon:
            MockDaemon.return_value.log_event = MagicMock()
            from drivers import knowledge_accrual_skill
            knowledge_accrual_skill.record_positive_feedback(
                issue_id="42",
                insight="Structured retro surfacing works reliably.",
                reaffirm_path=str(reaffirm_path),
            )
        assert reaffirm_path.exists()
        content = reaffirm_path.read_text()
        assert "Node 42" in content
        assert "Structured retro surfacing works reliably." in content
        assert "SG-0005" in content

    def test_emits_positive_feedback_telemetry_event(self, tmp_path):
        reaffirm_path = tmp_path / "audit" / "reaffirm-42.md"
        captured = []

        class FakeDaemon:
            def log_event(self, **kwargs):
                captured.append(kwargs)

        with patch("drivers.knowledge_accrual_skill.TelemetryDaemon", return_value=FakeDaemon()):
            from drivers import knowledge_accrual_skill
            knowledge_accrual_skill.record_positive_feedback(
                issue_id="42",
                insight="Some good pattern.",
                reaffirm_path=str(reaffirm_path),
            )

        assert len(captured) == 1
        evt = captured[0]
        assert evt["event"].upper() == "POSITIVE_FEEDBACK"
        assert evt["node_id"] == "42"
        assert evt["stage"] == "reflect"
        assert evt["metadata"]["status"] == "positive_feedback"

    def test_creates_parent_dirs(self, tmp_path):
        nested = tmp_path / "deeply" / "nested" / "audit" / "reaffirm-99.md"
        with patch("drivers.knowledge_accrual_skill.TelemetryDaemon") as MockDaemon:
            MockDaemon.return_value.log_event = MagicMock()
            from drivers import knowledge_accrual_skill
            knowledge_accrual_skill.record_positive_feedback(
                issue_id="99",
                insight="Nested path creation works.",
                reaffirm_path=str(nested),
            )
        assert nested.exists()

    def test_raises_on_empty_issue_id(self, tmp_path):
        from drivers import knowledge_accrual_skill
        with pytest.raises((ValueError, SystemExit), match="issue_id"):
            knowledge_accrual_skill.record_positive_feedback(
                issue_id="",
                insight="Some insight.",
                reaffirm_path=str(tmp_path / "reaffirm-.md"),
            )

    def test_raises_on_empty_insight(self, tmp_path):
        from drivers import knowledge_accrual_skill
        with pytest.raises((ValueError, SystemExit), match="insight"):
            knowledge_accrual_skill.record_positive_feedback(
                issue_id="42",
                insight="   ",
                reaffirm_path=str(tmp_path / "reaffirm-42.md"),
            )

    def test_insight_truncated_in_telemetry_at_200_chars(self, tmp_path):
        """Telemetry ledger should not contain unbounded insight strings."""
        reaffirm_path = tmp_path / "audit" / "reaffirm-7.md"
        captured = []

        class FakeDaemon:
            def log_event(self, **kwargs):
                captured.append(kwargs)

        long_insight = "A" * 500
        with patch("drivers.knowledge_accrual_skill.TelemetryDaemon", return_value=FakeDaemon()):
            from drivers import knowledge_accrual_skill
            knowledge_accrual_skill.record_positive_feedback(
                issue_id="7",
                insight=long_insight,
                reaffirm_path=str(reaffirm_path),
            )

        assert len(captured[0]["metadata"]["insight_summary"]) == 200

    def test_reaffirm_file_contains_timestamp(self, tmp_path):
        reaffirm_path = tmp_path / "reaffirm-5.md"
        with patch("drivers.knowledge_accrual_skill.TelemetryDaemon") as MockDaemon:
            MockDaemon.return_value.log_event = MagicMock()
            from drivers import knowledge_accrual_skill
            knowledge_accrual_skill.record_positive_feedback(
                issue_id="5",
                insight="Timestamped.",
                reaffirm_path=str(reaffirm_path),
            )
        content = reaffirm_path.read_text()
        # Timestamp should be in ISO-8601 format
        import re
        assert re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", content)


# ---------------------------------------------------------------------------
# enforce_reflection_hook — positive feedback branch
# ---------------------------------------------------------------------------

class TestEnforceReflectionHookPositiveFeedback:
    """Tests for the positive-feedback gate in daemon_knowledge_accrual.enforce_reflection_hook."""

    def _make_telemetry(self, tmp_path, issue_id, event_type, status):
        tel = tmp_path / "artifacts" / "telemetry.jsonl"
        tel.parent.mkdir(parents=True, exist_ok=True)
        _write_telemetry(str(tel), [
            {"node_id": issue_id, "event": event_type, "metadata": {"status": status}},
        ])
        return str(tmp_path)

    def test_passes_when_no_positive_feedback_in_telemetry(self, tmp_path):
        """No POSITIVE_FEEDBACK event → gate does not block."""
        (tmp_path / "artifacts").mkdir(parents=True)
        # No telemetry file at all
        from kernel import daemon_knowledge_accrual
        # Should not raise
        daemon_knowledge_accrual.enforce_reflection_hook("42", str(tmp_path))

    def test_blocks_when_positive_feedback_but_no_reaffirm_file(self, tmp_path):
        """POSITIVE_FEEDBACK event exists but reaffirm file absent → raises."""
        repo_root = self._make_telemetry(tmp_path, "42", "POSITIVE_FEEDBACK", "positive_feedback")
        (tmp_path / "artifacts" / "audit").mkdir(parents=True, exist_ok=True)

        from kernel import daemon_knowledge_accrual
        with pytest.raises((Exception, SystemExit), match="reaffirm-42.md"):
            daemon_knowledge_accrual.enforce_reflection_hook("42", repo_root)

    def test_passes_when_positive_feedback_and_reaffirm_file_exists(self, tmp_path):
        """POSITIVE_FEEDBACK event + reaffirm file present → passes."""
        repo_root = self._make_telemetry(tmp_path, "42", "POSITIVE_FEEDBACK", "positive_feedback")
        audit_dir = tmp_path / "artifacts" / "audit"
        audit_dir.mkdir(parents=True, exist_ok=True)
        (audit_dir / "reaffirm-42.md").write_text("# Reaffirm")

        from kernel import daemon_knowledge_accrual
        # Should not raise
        daemon_knowledge_accrual.enforce_reflection_hook("42", repo_root)

    def test_status_field_also_triggers_gate(self, tmp_path):
        """metadata.status == 'positive_feedback' (without POSITIVE_FEEDBACK event) also triggers."""
        repo_root = self._make_telemetry(tmp_path, "55", "SOME_OTHER_EVENT", "positive_feedback")
        (tmp_path / "artifacts" / "audit").mkdir(parents=True, exist_ok=True)

        from kernel import daemon_knowledge_accrual
        with pytest.raises((Exception, SystemExit), match="reaffirm-55.md"):
            daemon_knowledge_accrual.enforce_reflection_hook("55", repo_root)

    def test_gate_not_triggered_for_different_node_id(self, tmp_path):
        """Positive feedback for node 99 must not block node 42."""
        repo_root = self._make_telemetry(tmp_path, "99", "POSITIVE_FEEDBACK", "positive_feedback")
        (tmp_path / "artifacts" / "audit").mkdir(parents=True, exist_ok=True)

        from kernel import daemon_knowledge_accrual
        # Node 42 has no positive feedback; should pass
        daemon_knowledge_accrual.enforce_reflection_hook("42", repo_root)
