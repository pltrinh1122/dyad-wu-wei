# WHY-1810: CSI Governance Model for HTIL Block

> [!NOTE]
> **Status**: Finalized  
> **Node**: 1811 (Harmonize — Path 1810)  
> **Persona**: frontier (Agentic Mechanics Engine)  
> **Date**: 2026-06-06

## 1. Intent
To replace the passive "soft dormancy" expectation during the Hard Human-in-the-Loop (HTIL) block with a mechanically enforced Asymmetric CSI (Cybernetic Steering Invariant) Guard.

## 2. The Abstraction Leak (Current State)
Currently, the PR Review wait state (the HTIL block) relies on the Agent "remembering" to go to sleep and the `audit_daemon.py` checking GitHub to wake it up. If the system is perturbed or the Agent acts on an injected message during this period, the state machine can drop into an execution loop while the PR is unmerged, violating the `WIP-N=1` invariant.

## 3. The Cybernetic Steering Invariant
We inherit the CSI from `dyad-cairn`: deterministic guardrails are active steering vectors, not passive obstacles. 

Instead of asking the LLM to follow a soft rule, we build a **CSI Guard** — a computational wrapper that structurally blocks invalid execution and mechanically funnels the system toward resolution.

## 4. The HTIL Asymmetric Guard Architecture
The HTIL block is formalized as an Asymmetric (Process-Bound) CSI Guard:

1. **The Arm (State Lock)**: When `./bin/node reflect` successfully opens a pull request, it physically materializes the locked state by writing `HTIL_ACTIVE.lock`.
2. **The Gate (Validation Linter)**: All orchestration wrappers (`./bin/node`, `./bin/backlog`, etc.) are wrapped with a hard guard. If `HTIL_ACTIVE.lock` exists, execution crashes violently with a vector message (e.g., "Run ./bin/observe").
3. **The Disarm (Closure Script)**: The lock cannot be trivially bypassed by deleting the file or bypassing checks. It requires a dedicated closure script (`./bin/observe` or similar) that securely validates the PR merge status on GitHub and synchronizes the ledger before physically destroying the lock.

## 5. Invariants to be Tested
- **Lock Generation**: `node reflect` must generate `HTIL_ACTIVE.lock` upon PR creation.
- **Execution Rejection**: System orchestrators must crash structurally if invoked while the lock exists.
- **Bypass Falsification**: The system must verify the PR state independently against the ledger to prevent trivial lock-file deletion bypasses.
- **Closure Resolution**: The closure script must safely unlock the system only upon genuine PR merge.
