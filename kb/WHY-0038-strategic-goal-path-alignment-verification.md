# WHY-0038: Strategic Goal Path Alignment Verification

## Context

As the backlog evolves, paths prioritized within our strategic goals can be closed or completed. If the strategic intent ledger (`artifacts/strategic_intent.yml`) is not updated concurrently, it will contain stale references to closed or non-existent paths. This degrades the fidelity of the Next-Best-Action (NBA) prioritizer. We need an automated verification mechanism to ensure that all path references in active strategic goals map directly to existing, open backlog issues.

This document details the alignment decisions on how to enforce this mapping without compromising developer velocity.

---

## Alignment Decisions

### 1. Strict Compliance Enforcement (Fail-Fast)
To prevent decay of our strategic intent tracking:
- **Decision**: The strategic ledger verification process (`./bin/strategic verify`) must execute a strict mapping check.
- **Severity**: Any stale (closed) or non-existent path ID listed in `prioritized_paths` under `Active` strategic goals will cause `strategic verify` to exit with a non-zero status.
- **Guardrail**: This check will block pre-commit/pre-push stages when running locally (if hooks are enabled) and will fail CI builds in GitHub Actions.

### 2. Offline Test Isolation
To adhere to **SG-0003** (Preservation of Autonomous Velocity), which restricts test executions from utilizing live network calls:
- **Decision**: Unit tests under `tests/` checking the ledger structure must mock all GitHub API queries.
- **Runtime Separation**: Live API verification of backlog paths on GitHub is restricted to:
  1. The GitHub Actions runner (which runs with proper credentials and network access).
  2. Direct user/agent terminal invocations of the CLI command (`./bin/strategic verify`).
- **TDD Behavior**: Running `./bin/run-tests` locally in offline environments will skip the live GitHub API validation and rely on mock data to keep test execution under the 60-second limit.

---

## Invariant Formalization

A future `WHAT-*` spec document will define the structural rules:
1. `INVARIANT_STRATEGIC_PATH_EXISTS`: Every path ID referenced in the active prioritized lists must exist in the backlog repository.
2. `INVARIANT_STRATEGIC_PATH_OPEN`: Every path ID referenced in the active prioritized lists must have an `OPEN` state.
