# WHY-0040: CI Hardening — Architectural Rationale for Hermetic Offline Test Suite Enforcement

## Context & Problem Statement
In previous iterations, tests in `tests/test_bash_wrappers.py` executed shell scripts that made real `gh` CLI invocations against the live GitHub API. This behavior led to the following issues:
1. **CI Fragility**: GitHub Actions runners often execute in restricted, unauthenticated environments lacking valid `GITHUB_TOKEN` credentials, causing tests to fail.
2. **State Dependency**: Stale issue numbers (e.g. #298) or deleted issues cause tests to break non-deterministically even if the code remains correct.
3. **Performance Degradation**: Real network round-trips slow down local TDD loops and waste CI resources.
4. **Lack of Containment**: There was no global safety net to intercept unmocked shell commands running `gh` in new or modified test modules.

## Decision
We enforce a **zero-network/zero-live-CLI-dependency** policy across the entire pytest suite.

### 1. Global Autouse PATH-Injection Fixture
Instead of restricting the stubbing mechanism to a module-level fixture inside `tests/test_bash_wrappers.py`, we elevate the `stub_gh_cli` fixture to `tests/conftest.py` with `autouse=True` and `scope="session"`. This ensures:
- Every test module in the repository automatically runs with the stubbed `gh` fixture injected at the front of `PATH`.
- Any unexpected subprocess call to `gh` is caught and returned gracefully by the stub rather than calling the real GitHub CLI.

### 2. Comprehensive Stub Coverage
The `tests/fixtures/gh` executable stub is maintained as a clean pattern matcher that mirrors all valid subprocess actions. If a developer introduces a new `gh` pattern, it must be added to the stub rather than hitting the live network.

## Invariants & Guardrails
- **The Zero Network Invariant**: No test execution during local `spao test` or CI runner stages may make real network connections or execute live `gh` commands.
- **Fail-Safe Fallback**: Any unhandled `gh` command pattern must print a warning to `stderr` and exit with code `0` (or raise a controlled error if expected), preventing test suite crashes while logging the violation.
