# WHAT-0033: CI Hardening — Technical Specification for Hermetic gh Fixture Stub

## Overview
**Path**: #368 — Probe Path: CI Hardening — Remediate and Prevent Live GitHub API Calls in Test Suite
**Plan Node**: #370
**Implements decisions from**: WHY-0032

---

## Scope

Two concrete changes to be implemented in Activity node #371:

1. **`tests/fixtures/gh`** — hermetic shell stub replacing the real `gh` CLI in tests
2. **`tests/test_bash_wrappers.py`** — inject `tests/fixtures/` into `PATH` for all tests

---

## 1. `tests/fixtures/gh` — Stub Shell Script

New executable at `tests/fixtures/gh`. Intercepts all `gh` subcommand patterns
used by `bin/backlog`, `bin/node`, `bin/prompt`, and `bin/rt`.

### Canned response contract

```bash
#!/usr/bin/env bash
# Hermetic gh CLI stub for SPAO test suite.
# Returns minimal valid JSON for every gh subcommand pattern the wrappers use.
# EXIT 0 always — no network calls, no auth required.

case "$*" in

  # bin/backlog list → daemon_backlog → get_open_issues()
  "issue list --state open --limit 100 --json number,title,body")
    echo '[{"number":1,"title":"Path 1: Test Path","body":"## Goal\nTest goal."}]'
    ;;

  # _verify_state_purity / _validate_orthogonal_scope → get_issue_details()
  issue\ view\ *\ --json\ number,title,body)
    NUM=$(echo "$@" | grep -oE '[0-9]+' | head -1)
    echo "{\"number\":$NUM,\"title\":\"Test Issue $NUM\",\"body\":\"## Goal\\nTest.\"}"
    ;;

  # State checks: gh issue view N --json state
  issue\ view\ *\ --json\ state)
    echo '{"state":"OPEN"}'
    ;;

  # Close issue
  issue\ close\ *)
    echo "Issue closed." >&2
    ;;

  # Add comment
  issue\ comment\ *)
    echo "Comment added." >&2
    ;;

  # Reopen issue
  issue\ reopen\ *)
    echo "Issue reopened." >&2
    ;;

  # PR create
  "pr create"*)
    echo "https://github.com/pltrinh1122/dz-cil/pull/999"
    ;;

  # PR list (open PRs check in sync)
  "pr list --state open --json number,title,headRefName")
    echo '[]'
    ;;

  # GraphQL (gh_graph_skill)
  "api graphql"*)
    echo '{"data":{}}'
    ;;

  # Fallback — unknown subcommand, exit 0 silently
  *)
    echo "gh stub: unhandled: $*" >&2
    exit 0
    ;;
esac
exit 0
```

### Key properties
- Always exits 0
- No network calls, no `GITHUB_TOKEN` required
- Covers all patterns currently exercised by `test_bash_wrappers.py`
- Unknown subcommands warn to stderr but still exit 0 (non-fatal)

---

## 2. `tests/test_bash_wrappers.py` — PATH Injection

Add a **session-scoped pytest fixture** that prepends `tests/fixtures/` to `PATH`
before any test in the module runs:

```python
import os
import pytest

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

@pytest.fixture(autouse=True, scope="module")
def stub_gh_cli():
    """Prepend tests/fixtures/ to PATH so the stub gh replaces the real one."""
    original_path = os.environ.get("PATH", "")
    os.environ["PATH"] = FIXTURES_DIR + os.pathsep + original_path
    yield
    os.environ["PATH"] = original_path
```

Placement: insert immediately after the existing imports block (before the first
test function).

---

## 3. Files Changed

| File | Change type | Notes |
|---|---|---|
| `tests/fixtures/gh` | **NEW** | Hermetic stub; must be `chmod +x` |
| `tests/test_bash_wrappers.py` | **MODIFY** | Add `stub_gh_cli` autouse fixture |

No other files require modification. No production code changes.

---

## 4. Verification Plan

### Automated
```bash
spao test                        # all tests must pass locally
bash -n tests/fixtures/gh        # shell syntax check
```

### CI verification
- Push Activity node #371 branch → CI must show green on `test` job
- Confirm `test_backlog_list_subcommand` passes specifically

### Regression check
- Run `spao test` before and after — test count must stay at 112+ (no tests removed)

---

## 5. Feedforward Invariants

- `[ ]` `tests/fixtures/gh` created and `chmod +x`
- `[ ]` `stub_gh_cli` autouse fixture added to `test_bash_wrappers.py`
- `[ ]` `spao test` passes locally (112+ tests)
- `[ ]` CI green on node #371 PR (no CI waiver needed)
- `[ ]` PR #367 CI re-triggered and also goes green after fix lands on main
- `[ ]` Changes delivered via PR from node/371 branch — no hotfixes
