"""Tests for the Operator Correction Integration (Autonomous Learning Loop - WHAT-0019).

Coverage:
- drivers.knowledge_accrual_skill.record_operator_correction (skill layer)
- kernel.daemon_knowledge_accrual.enforce_reflection_hook operator-correction branch
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
# record_operator_correction — skill layer
# ---------------------------------------------------------------------------

class TestRecordOperatorCorrection:
    """Tests for drivers.knowledge_accrual_skill.record_operator_correction."""

    def test_creates_retro_file(self, tmp_path):
        retro_path = tmp_path / "audit" / "retro-42.md"
        with patch("drivers.knowledge_accrual_skill.TelemetryDaemon") as MockDaemon:
            MockDaemon.return_value.log_event = MagicMock()
            from drivers import knowledge_accrual_skill
            knowledge_accrual_skill.record_operator_correction(
                issue_id="42",
                insight="The operator corrected the prompt structure.",
                retro_path=str(retro_path),
            )
        assert retro_path.exists()
        content = retro_path.read_text()
        assert "Node 42" in content
        assert "The operator corrected the prompt structure." in content

    def test_emits_operator_correction_telemetry_event(self, tmp_path):
        retro_path = tmp_path / "audit" / "retro-42.md"
        captured = []

        class FakeDaemon:
            def log_event(self, **kwargs):
                captured.append(kwargs)

        with patch("drivers.knowledge_accrual_skill.TelemetryDaemon", return_value=FakeDaemon()):
            from drivers import knowledge_accrual_skill
            knowledge_accrual_skill.record_operator_correction(
                issue_id="42",
                insight="Some correction.",
                retro_path=str(retro_path),
            )

        assert len(captured) == 1
        evt = captured[0]
        assert evt["event"].upper() == "OPERATOR_CORRECTION"
        assert evt["node_id"] == "42"
        assert evt["stage"] == "reflect"
        assert evt["metadata"]["status"] == "operator_correction"

    def test_raises_on_empty_issue_id(self, tmp_path):
        from drivers import knowledge_accrual_skill
        with pytest.raises(ValueError, match="issue_id"):
            knowledge_accrual_skill.record_operator_correction(
                issue_id="",
                insight="Some insight.",
                retro_path=str(tmp_path / "retro-.md"),
            )


# ---------------------------------------------------------------------------
# enforce_reflection_hook — daemon layer
# ---------------------------------------------------------------------------

class TestEnforceReflectionHookOperatorCorrection:
    """Tests for kernel.daemon_knowledge_accrual.enforce_reflection_hook triggering on OPERATOR_CORRECTION."""

    @patch("subprocess.run")
    def test_blocks_if_operator_correction_but_no_retro(self, mock_run, tmp_path):
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        artifacts_dir = repo_root / "artifacts"
        artifacts_dir.mkdir()
        telemetry_path = artifacts_dir / "telemetry.jsonl"

        # Log an OPERATOR_CORRECTION
        _write_telemetry(str(telemetry_path), [
            {"node_id": "42", "event": "OPERATOR_CORRECTION", "metadata": {"status": "operator_correction"}}
        ])

        from kernel import daemon_knowledge_accrual
        # No retro file exists, should block
        with pytest.raises(Exception, match="REFLECTION BLOCKED: Node 42 experienced execution failures"):
            daemon_knowledge_accrual.enforce_reflection_hook(
                issue_id="42",
                repo_root=str(repo_root)
            )

    @patch("subprocess.run")
    def test_passes_if_operator_correction_and_retro_exists(self, mock_run, tmp_path):
        # mock gh output
        mock_run.return_value.stdout = "[]"
        
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        artifacts_dir = repo_root / "artifacts"
        artifacts_dir.mkdir()
        audit_dir = artifacts_dir / "audit"
        audit_dir.mkdir()
        
        telemetry_path = artifacts_dir / "telemetry.jsonl"
        retro_path = audit_dir / "retro-42.md"

        # Log an OPERATOR_CORRECTION
        _write_telemetry(str(telemetry_path), [
            {"node_id": "42", "event": "OPERATOR_CORRECTION", "metadata": {"status": "operator_correction"}}
        ])
        
        # Create retro file
        retro_path.write_text("retro content")

        from kernel import daemon_knowledge_accrual
        # Should not raise exception
        daemon_knowledge_accrual.enforce_reflection_hook(
            issue_id="42",
            repo_root=str(repo_root)
        )
