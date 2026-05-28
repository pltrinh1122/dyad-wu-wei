# HOW-1170: Frontier Recovery Protocol

## 1. Intent
This document codifies the "Frontier Recovery Protocol" (also known as the Patient Recovery Protocol). This protocol defines the strict self-invariant assertion sequence that the Frontier Agent must run immediately after a "seizure" or abnormal halt/restart, *before* resuming any feature work or syncing the active node.

The intent of this sequence is to cleanly re-anchor the Agent's topological state, govern any uncommitted mutations, and ensure the execution environment is pristine and mathematically sound.

## 2. The Protocol

When a Frontier Agent resumes from a seizure, the following sequence MUST be executed independently of the standard loop, prior to advancing any feature goals:

### 2.1 Governance Integrity (Inv 3)
If the Agent was mid-execution when halted, there may be uncommitted working-tree edits.
- **Action**: Check `git-status`.
- **Assertion**: If uncommitted edits exist related to the active node, they must be committed onto a node branch (e.g., `node/<id>-<name>`) to govern them.
- **Why**: Running a subsequent node sync or checkout sweeps the working tree. Failing to govern edits beforehand results in silent data loss.

### 2.2 State Integrity & Purity
The topological ledger must be verified.
- **Action**: Run `./bin/meta lint` and `./bin/status`.
- **Assertion**: `frontier_state.yml` must be valid and pure. The `./bin/status` output must accurately reflect the system state.

### 2.3 ROM Currency (WHY-0085)
The local knowledge base and configuration (ROM) must not be divergent from the source of truth.
- **Action**: Verify branch currency (e.g., `git diff main...HEAD`).
- **Assertion**: There must be no stale-ROM drift versus `main`.

### 2.4 WIP-N=1 + Active-Node Coherence
The active node must perfectly cohere with the working branch.
- **Action**: Cross-reference the Active Node ID against the WIP Branch in `./bin/status`.
- **Assertion**: The Active Node must match the checked-out WIP branch, enforcing the WIP-N=1 invariant.

### 2.5 Contract Health
The codebase must mathematically function before the Agent attempts to mutate it further.
- **Action**: Run `./bin/run-tests`.
- **Assertion**: The entire test suite must pass (`100% green`). If tests fail, the environment is fundamentally compromised.

### 2.6 Secondary Recovery (Ontology Drift)
- **Action**: If any documented ontology drift or specific document reversions occurred due to the seizure (e.g., failed renames or silent regressions), recover them via the governed loop (e.g., `git-checkout <safe-commit> -- <files>`).
- **Assertion**: The ontology is accurate and coherent with the `kb/GLOSSARY.md`.

## 3. Post-Condition
Only when all self-invariant assertions pass is the Frontier Agent considered "stable and ready" to resume the interrupted Node. Readiness is gated by this verified check, never self-declared.
