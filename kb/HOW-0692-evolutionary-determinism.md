# HOW-0692: Technical Plan for Evolutionary Determinism

## 1. Objective
This document outlines the technical mechanism for enforcing "Evolutionary Determinism" as codified in `WHAT-0692`. The system must guarantee that any modifications to the core SPAO execution engine (`bin/node`, `bin/reflect`, `drivers/`, `kb/`) must be deployed through the exact same `Plan -> Checkout -> Act -> Reflect` loop they govern.

## 2. Technical Directives

### 2.1. Dogfooding Execution Pipeline
- **Agentic Engine Updates**: When the Agent is tasked with fixing a bug in the `SPAOR` loop, it MUST generate a Path/Node for it, check it out, execute the change, and run the `bin/run-tests` harness before reflecting.
- **Implementation**: The system's ruleset (`AGENT.md`) MUST explicitly mandate that structural framework edits follow the standard path execution protocol. Ad-hoc terminal edits via standard unix utilities outside a Node execution are forbidden.

### 2.2. Ledger Consistency
- **Audit Trace**: The audit daemon (`drivers/audit_daemon.py`) passively scans the git history for commits on `main` that did not originate from a properly merged `node/*` branch PR. 
- **Implementation**: The audit logic must ensure `git log --merges` matches the issue closure events. If a direct commit to `main` is detected, the `passive_ziran_auditor.py` or similar telemetry hook flags it as a physics violation.

### 2.3. Test Isolation
- **Safety Boundaries**: Because upgrading the engine while running it can cause execution collapse, all `bin/` changes MUST execute strictly inside the `.worktrees/node/` boundary. The root `bin/node` execution context remains shielded until the PR merges.

## 3. Implementation Plan
1. **Inject Directive into AGENT.md**: Add explicit language requiring that any modification to the execution engine (`bin/`, `drivers/`) requires node checkout and PR merge.
2. **Review Ziran Auditor**: Ensure the existing test suites (e.g. `test_ziran_auditor.py`) and PR validation checks account for strict PR-only commits to `main`.
