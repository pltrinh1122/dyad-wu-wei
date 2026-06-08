# WHY-0497: Optimization of Node Sync Audit Performance (Lightweight Audit)

## 1. The Context
The Wu-wei engine continuously enforces metasystem integrity through the `audit_daemon.py`. Historically, this daemon ran a comprehensive, exhaustive check against all known invariants, policies, and remote states. During the crucial `sync` phase of the SPAO loop (where the engine determines the Next-Best-Action), this heavy audit process injected significant latency. 

## 2. The Catalyst
As we pursue **Gateless Autonomous Execution within a Risk-Managed Sandbox (SG-0002)** and the **Preservation of Autonomous Velocity (SG-0003)**, any friction in the core SPAO state transition degrades the Dyad's flow state. The Operator identified that the exhaustive audit during node sync is unnecessary and overly penalizing. We need a way to quickly verify the immediate structural requirements for the SPAO loop to continue without blocking on a full system-wide compliance check.

## 3. The Alignment
We are formally bifurcating the metasystem audit process into two distinct modes:

1.  **Lightweight Audit (The Hot Path):** A fast, structural verification focused solely on the immediate pre-requisites for SPAO execution (e.g., verifying `frontier_state.md` parses correctly, ensuring the workspace isn't hopelessly corrupted, or verifying critical ledger formats). This mode is invoked during `sync` and other high-frequency loop transitions.
2.  **Exhaustive Audit (The Cold Path):** The traditional, comprehensive audit evaluating all system rules, remote API consistency, and deep invariant compliance. This mode runs asynchronously via the background cron scheduler or during explicit `reflect` / manual `audit` invocations.

### The "Fail-Safe" Invariant
If a Lightweight Audit fails, it must immediately trigger an Exhaustive Audit to diagnose the root cause and generate an actionable triage report. Lightweight does not mean "unsafe"; it means "optimistically verifying local structure."

## 4. The Path Forward
This alignment will be materialized in the subsequent Plan and Act nodes. The technical implementation will require:
*   Refactoring `audit_daemon.py` or creating `lightweight_audit.py` to support a `--lightweight` flag.
*   Defining the specific subset of rules that belong in the Lightweight tier.
*   Integrating the Lightweight Audit into the `bin/node sync` or `daemon_nba.py` execution flows.
