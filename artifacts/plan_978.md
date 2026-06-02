# Node 978: Discovery 978: Harmonize - Maintenance: Refine Knowledge Accrual Mechanisms (Node Contract)

## Context & Rationale
Path 977 addresses two distinct but related issues: false-positives in the lexical guard and test harness isolation problems (specifically related to `daemon_knowledge_accrual` in node lifecycle tests). This Harmonize node is the first step in the Dual-Discovery Initialization pattern, aimed at identifying the exact failures, tracing them to their structural roots, and producing a Discovery artifact.

## Proposed Changes
- Investigate `tests/test_lexical_guard.py`, `kernel/lexical_guard.py`, and `kb/semantic_ledger.yml` to identify the cause of the false-positives.
- Investigate `tests/test_node_lifecycle.py` and `kernel/daemon_knowledge_accrual.py` to identify the test isolation/mocking issue.
- Document findings in `artifacts/discovery_978.md`.

## Pre-Requisite Invariants
- Node locked under persona `agent-sg5`.

## Post-Requisite Invariants
- `artifacts/discovery_978.md` is created and clearly maps the problem state.

## Verification Plan
- Run local tests to establish a baseline of the current failure states.

## User Review Required
> [!IMPORTANT]
> Please review this Node Contract. Once approved, the Universal Merge Gate allows the Agent to autonomously transition to the Act phase.
