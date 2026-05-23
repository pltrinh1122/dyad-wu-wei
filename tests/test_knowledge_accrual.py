import os
import json
import pytest
from unittest.mock import patch, MagicMock, mock_open

from drivers.knowledge_accrual_skill import (
    parse_test_failure_diagnostics,
    check_kb_conflicts,
    synthesize_rule,
    build_contextual_prompt_injection
)
from kernel.daemon_knowledge_accrual import (
    run_kb_check,
    enforce_reflection_hook,
    inject_contextual_rules
)
from drivers.audit_daemon import evaluate_lexical_guard


def test_parse_test_failure_diagnostics():
    pytest_output = """
============================= test session starts ==============================
collected 1 item

tests/test_dummy.py F                                                     [100%]

=================================== FAILURES ===================================
__________________________________ test_dummy __________________________________

    def test_dummy():
>       raise ValueError("This is a test error message")
E       ValueError: This is a test error message

tests/test_dummy.py:10: ValueError
=========================== short test summary info ============================
    """
    failures = parse_test_failure_diagnostics(pytest_output)
    assert len(failures) == 1
    assert failures[0]["test_name"] == "test_dummy"
    assert failures[0]["file_path"] == "tests/test_dummy.py"
    assert failures[0]["line_number"] == 10
    assert failures[0]["error_type"] == "ValueError"
    assert failures[0]["error_message"] == "This is a test error message"


def test_check_kb_conflicts_forbidden_words():
    term1 = "ep" + "ic"
    term2 = "sp" + "ike"
    diff_text = f"""
diff --git a/kb/test.md b/kb/test.md
index 123456..7890ab 100644
--- a/kb/test.md
+++ b/kb/test.md
@@ -1,3 +1,4 @@
 # Test
+This is an {term1} transition and {term2} task.
 """
    conflicts = check_kb_conflicts(diff_text)
    assert len(conflicts) > 0
    assert any(term1 in c for c in conflicts)


def test_check_kb_conflicts_forbidden_commands():
    diff_text = """
diff --git a/kb/test.md b/kb/test.md
index 123456..7890ab 100644
--- a/kb/test.md
+++ b/kb/test.md
@@ -1,3 +1,4 @@
 # Test
+To do this, run git checkout main.
+Or run gh pr create.
 """
    conflicts = check_kb_conflicts(diff_text)
    assert len(conflicts) == 2
    assert any("git checkout" in c for c in conflicts)
    assert any("gh pr" in c for c in conflicts)


def test_check_kb_conflicts_clean():
    diff_text = """
diff --git a/kb/test.md b/kb/test.md
index 123456..7890ab 100644
--- a/kb/test.md
+++ b/kb/test.md
@@ -1,3 +1,4 @@
 # Test
+This is a clean path and discovery task.
 """
    conflicts = check_kb_conflicts(diff_text)
    assert len(conflicts) == 0


def test_synthesize_rule():
    failure = {
        "test_name": "test_dummy",
        "error_message": "forbidden word 'legacy_term' detected"
    }
    rule = synthesize_rule(failure)
    assert rule is not None
    assert rule["type"] == "lexical_guard"
    assert "legacy_term" in rule["pattern"]
    assert rule["alert_level"] == "FAILURE"

def test_synthesize_rule_constraints():
    # Length constraint
    assert synthesize_rule({"error_message": "forbidden term 'a'"}) is None
    assert synthesize_rule({"error_message": "forbidden term '123'"}) is None
    
    # Generic word blacklist
    assert synthesize_rule({"error_message": "forbidden term 'path'"}) is None
    assert synthesize_rule({"error_message": "forbidden term 'THE'"}) is None
    
    # Path constraint
    assert synthesize_rule({"error_message": "forbidden term '/absolute/path/file.py'"}) is None



def test_build_contextual_prompt_injection():
    mock_yaml = """
strategic_goals:
  - id: SG-0005
    prioritized_paths:
      - 541
"""
    with patch("builtins.open", mock_open(read_data=mock_yaml)), \
         patch("os.path.exists", return_value=True), \
         patch("os.listdir", return_value=["SG-0005.md"]):
             
        # Mock file read for SG-0005.md
        def mock_file_open(filename, *args, **kwargs):
            if "SG-0005.md" in filename:
                return mock_open(read_data="Rules for SG-0005").return_value
            return mock_open(read_data=mock_yaml).return_value
            
        with patch("builtins.open", mock_file_open):
            injection = build_contextual_prompt_injection("541", "/mock/kb")
            assert "Rules for SG-0005" in injection
            assert "<!-- CONTEXTUAL_ROM_INJECTION_START -->" in injection


def test_run_kb_check_success():
    with patch("subprocess.run") as mock_run, \
         patch("drivers.knowledge_accrual_skill.check_kb_conflicts", return_value=[]):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "diff text"
        mock_run.return_value = mock_result
        
        assert run_kb_check("/mock/repo", strict=True) is True


def test_run_kb_check_failure():
    with patch("subprocess.run") as mock_run, \
         patch("drivers.knowledge_accrual_skill.check_kb_conflicts", return_value=["conflict"]):
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "diff text"
        mock_run.return_value = mock_result
        
        with pytest.raises(Exception, match="KB Conflict Check Failed"):
            run_kb_check("/mock/repo", strict=True)


def test_enforce_reflection_hook_no_failures():
    # Telemetry shows no failure events, reflection hook should pass
    mock_telemetry = '{"node_id": "544", "event": "SUCCESS", "metadata": {}}\n'
    with patch("builtins.open", mock_open(read_data=mock_telemetry)), \
         patch("os.path.exists", return_value=True):
        
        # Should not raise exception
        enforce_reflection_hook("544", "/mock/repo")


def test_enforce_reflection_hook_with_failures_and_retro():
    mock_telemetry = '{"node_id": "544", "event": "FAILURE", "metadata": {"error": "some failure"}}\n'
    with patch("builtins.open", mock_open(read_data=mock_telemetry)), \
         patch("os.path.exists", return_value=True):
        
        # Mock that retro-544.md exists
        # enforce_reflection_hook checks os.path.exists for retro_path
        def mock_exists(path):
            if "retro-544.md" in path or "telemetry.jsonl" in path:
                return True
            return False
            
        with patch("os.path.exists", mock_exists):
            # Should not raise exception because retro exists
            enforce_reflection_hook("544", "/mock/repo")


def test_enforce_reflection_hook_with_failures_no_retro():
    mock_telemetry = '{"node_id": "544", "event": "FAILURE", "metadata": {"error": "some failure"}}\n'
    with patch("builtins.open", mock_open(read_data=mock_telemetry)):
        
        def mock_exists(path):
            if "telemetry.jsonl" in path:
                return True
            # retro file does not exist
            return False
            
        with patch("os.path.exists", mock_exists):
            with pytest.raises(Exception, match="REFLECTION BLOCKED"):
                enforce_reflection_hook("544", "/mock/repo")


def test_inject_contextual_rules():
    mock_frontier = "current_active_path: 541\n"
    mock_gemini = "Some instructions\n<!-- CONTEXTUAL_ROM_INJECTION_START -->\n<!-- CONTEXTUAL_ROM_INJECTION_END -->\n"
    
    with patch("os.path.exists", return_value=True), \
         patch("builtins.open", mock_open()) as mock_file, \
         patch("drivers.knowledge_accrual_skill.build_contextual_prompt_injection", return_value="<!-- CONTEXTUAL_ROM_INJECTION_START -->\nInjected Content\n<!-- CONTEXTUAL_ROM_INJECTION_END -->") as mock_inject:
             
        # Mock file reads and writes
        file_handles = [
            mock_open(read_data=mock_frontier).return_value, # frontier_state.yml
            mock_open(read_data=mock_gemini).return_value,   # GEMINI.md read
            mock_open().return_value                         # GEMINI.md write
        ]
        mock_file.side_effect = file_handles
        
        inject_contextual_rules("/mock/repo")
        
        # Verify that GEMINI.md is written with the injected content
        write_call = file_handles[2].write
        write_call.assert_called_once()
        written_data = write_call.call_args[0][0]
        assert "Injected Content" in written_data


def test_evaluate_lexical_guard():
    rule = {
        "id": "lexical-rule",
        "type": "lexical_guard",
        "pattern": "\\bforbidden_word\\b",
        "alert_level": "FAILURE",
        "prompt_message": "Detected forbidden word"
    }
    state = {}
    
    # Mock git status --porcelain returning modified file
    with patch("drivers.audit_daemon.subprocess.run") as mock_run, \
         patch("drivers.audit_daemon.inject_prompt") as mock_inject, \
         patch("pathlib.Path.exists", return_value=True), \
         patch("builtins.open", mock_open(read_data="This contains forbidden_word!")):
             
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = " M src/code.py\n"
        mock_run.return_value = mock_result
        
        triggered, new_state = evaluate_lexical_guard(rule, state.copy())
        
        assert triggered is True
        assert "src/code.py" in new_state["triggered_files"]
        mock_inject.assert_called_once_with("[FAILURE] Detected forbidden word")


def test_enforce_reflection_hook_surfacing():
    # Test case 1: Retrospective has not been surfaced yet. It should create a backlog issue.
    mock_telemetry = '{"node_id": "544", "event": "FAILURE", "metadata": {"error": "some failure"}}\n'
    
    with patch("builtins.open", mock_open(read_data=mock_telemetry)), \
         patch("os.path.exists", return_value=True), \
         patch("subprocess.run") as mock_run, \
         patch("kernel.daemon_backlog.BacklogDaemon.add") as mock_backlog_add, \
         patch("drivers.github_client.list_issues_by_label") as mock_list_issues:
        
        # Mock gh issue list --search returning empty (not surfaced yet)
        mock_gh_res = MagicMock()
        mock_gh_res.returncode = 0
        mock_gh_res.stdout = "[]"
        mock_run.return_value = mock_gh_res
        
        # Mock github path issues list
        mock_list_issues.return_value = [{"number": 809, "title": "Path 809: Test Path", "body": "- [ ] Node 544: Test Node (#544)"}]
        
        enforce_reflection_hook("544", "/mock/repo")
        
        # Verify that BacklogDaemon.add is called to create the backlog issue
        mock_backlog_add.assert_called_once_with(
            node_type="activity",
            title="Reflect - Synthesize Epistemic Retrospective retro-544.md",
            goal="Synthesize the epistemic learnings from the post-failure retrospective retro-544.md into the system's operational guidelines (the Dao).",
            path_id="809"
        )


def test_enforce_reflection_hook_already_surfaced():
    # Test case 2: Retrospective is already surfaced. It should not create a backlog issue.
    mock_telemetry = '{"node_id": "544", "event": "FAILURE", "metadata": {"error": "some failure"}}\n'
    
    with patch("builtins.open", mock_open(read_data=mock_telemetry)), \
         patch("os.path.exists", return_value=True), \
         patch("subprocess.run") as mock_run, \
         patch("kernel.daemon_backlog.BacklogDaemon.add") as mock_backlog_add:
        
        # Mock gh issue list --search returning existing issue
        mock_gh_res = MagicMock()
        mock_gh_res.returncode = 0
        mock_gh_res.stdout = '[{"number": 850, "title": "Reflect - Synthesize Epistemic Retrospective retro-544.md"}]'
        mock_run.return_value = mock_gh_res
        
        enforce_reflection_hook("544", "/mock/repo")
        
        # Verify that BacklogDaemon.add is NOT called
        mock_backlog_add.assert_not_called()

