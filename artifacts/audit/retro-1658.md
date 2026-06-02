# Retrospective: Node 1658 (Lexical Guard Failure)

## Issue
During the initial reflection attempt for Node 1658, the local test suite execution of `tests/test_lexical_guard.py` failed. The failure was triggered because `kb/WHAT-1654-jtbd-dialectical-intake-jd.md` contained the forbidden term `p-r-o-b-e-s`.

## Root Cause
The `semantic_ledger.yml` strictly forbids certain legacy or ambiguous terminology to maintain structural vocabulary coherence. The term `p-r-o-b-e-s` is deprecated.

## Remediation
1. Replaced the deprecated term `p-r-o-b-e-s` with the Dyad Practice approved terminology `stress-tests` in `kb/WHAT-1654-jtbd-dialectical-intake-jd.md`.
2. Re-ran local tests inside the worktree, which successfully passed (`337 passed, 1 skipped`).

## Synthesis
Agentic intake and documentation generation must strictly align with the `semantic_ledger.yml` vocabulary. Future drafting steps should consult the ledger or actively use the Dyad Practice Commons terminology.
