# HOW-0681: Implementing The Guardian of Rigidity

## 1. Objective
This document translates the philosophical invariants defined in `WHAT-0681` (The Guardian of Rigidity) into actionable architectural rules for the `agent-meta` execution substrate (`kernel/` and `bin/`).

## 2. Technical Directives

### 2.1. Eradicate Soft-Fails in SPAO State Transitions
The `SPAOR` state machine must never "soft-fail" or attempt to auto-recover when an invariant is broken.
- **Example**: In `bin/node checkout`, if there are uncommitted changes, the script must throw an `exit 1` error rather than attempting to stash or commit them automatically. This preserves the absolute deterministic state of the repository.
- **Action**: Audit `bin/*` and `kernel/*` to ensure all invariant checks (e.g., WIP=1 validation, PR status checks) terminate the process explicitly on failure.

### 2.2. Eliminate Contextual Branching
The core loop scripts (`kernel/node_lifecycle.py`, `kernel/daemon_strategic.py`) must not contain any `if` statements that evaluate the *content* of the Node or Path. 
- **Example**: A rule like `if "docs:" in title: skip_tests()` is strictly prohibited. The pipeline is an agnostic conveyor belt.
- **Action**: All validation decorators and assertion functions must apply uniformly to all execution paths.

### 2.3. The Sluice Gate Strictness
The boundary between Domain A (Dyadic Design) and Domain B (Autonomous Execution) is mediated by the NBA evaluation. 
- **Action**: The NBA evaluation must rigidly depend on the explicit structural mapping in GitHub (Paths/Nodes) and never on free-text interpretation of the operator's intent during Domain B execution. If the backlog is unmapped, the system halts with a Hygiene Warning.

## 3. Implementation Plan
1. **Audit Phase**: Review `kernel/daemon_strategic.py` and `kernel/node_lifecycle.py` for any existing "smart recovery" logic or context-aware branching.
2. **Hardening**: Replace any graceful degradation logic with explicit `sys.exit(1)` and clear terminal error messages.
3. **Validation**: Rely on the continuous CI loops and local `run-tests` to ensure that standard execution paths remain functional while edge cases crash aggressively.
