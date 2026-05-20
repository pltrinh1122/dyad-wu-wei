# WHY-0032: CI Hardening — Bash Wrapper Tests Must Not Make Live GitHub API Calls

## Decision Record
**Date**: 2026-05-20
**Path**: #368 — Spike Path: CI Hardening — Remediate and Prevent Live GitHub API Calls in Test Suite
**Probe Node**: #369 Align

---

## Root Cause (Confirmed from CI Log)

**Failing test**: `test_backlog_list_subcommand` in `tests/test_bash_wrappers.py:109`

**Failure chain**:
```
bin/backlog list
  → mgr_backlog.py list
    → github_client.get_open_issues()
      → subprocess.run(['gh', 'issue', 'list', '--state', 'open', ...])
        → per-issue: gh issue view 298 --json state  ← EXIT CODE 1
```

**Why it fails in CI**:
- Issue #298 may have been closed or no longer exists in the repo
- The GitHub Actions runner authenticates via `GITHUB_TOKEN` with repo-scoped
  permissions, but `gh issue view` on a deleted/missing issue returns exit 1
- Even with valid auth, stale issue numbers make the test non-deterministic

**This is a pre-existing fragility**: our PR #367 adds only a docs file with zero
Python/shell changes. The test was already broken before our work.

---

## Why This Pattern Is Wrong

`test_bash_wrappers.py` tests the CLI shell wrappers (`bin/backlog`, `bin/node`,
etc.) by invoking them as subprocesses. These wrappers call out to the real GitHub
API via `gh`. This means:

1. **Tests are non-deterministic**: depend on live GitHub state (issue numbers,
   auth tokens, rate limits, network availability)
2. **Tests are not isolated**: a closed issue breaks unrelated test runs forever
3. **Tests are slow**: real network round-trips in a unit test suite
4. **Tests violate the Orthogonality principle**: bash wrapper behavior should be
   testable without GitHub API availability

---

## Alignment Decision

**The bash wrapper tests MUST be made hermetic.** Two acceptable approaches:

### Option A: Environment-level mock (Recommended)
Set `GH_TOKEN` to a dummy value and stub the `gh` binary with a shell script
fixture that returns canned JSON responses. Placed in `tests/fixtures/gh`.
The test suite prepends `tests/fixtures/` to `PATH`.

**Pros**: Zero changes to production code; tests the real bin/ scripts end-to-end
**Cons**: Fixture `gh` stub must cover all `gh` subcommand patterns used

### Option B: Subprocess mock via `unittest.mock`
Patch `subprocess.run` at the Python layer in tests that indirectly trigger `gh`.

**Pros**: Fine-grained control per test
**Cons**: Doesn't test the bash wrapper itself — only the Python layer below it

### Decision: Option A

A `tests/fixtures/gh` stub shell script is the correct solution. It tests the
actual bash wrapper end-to-end while keeping the test suite hermetic and fast.
The stub must handle:
- `gh issue list --state open --limit N --json number,title,body`
- `gh issue view N --json state`
- `gh issue view N --json number,title,body`
- `gh pr create ...`
- `gh pr list ...`

---

## Feedforward Invariants

- `[ ]` `tests/fixtures/gh` stub script created and covers all gh subcommand patterns
- `[ ]` `tests/test_bash_wrappers.py` injects `tests/fixtures/` into PATH before subprocess calls
- `[ ]` No live `gh` calls in any test marked as a unit test
- `[ ]` CI passes on PR #367 after fix is merged
- `[ ]` All 112+ tests still pass locally via `spao test`
- `[ ]` Changes delivered via PR from node/371 branch — no hotfixes
