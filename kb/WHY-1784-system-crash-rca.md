# WHY-1784: Root Cause Analysis of Path 1567 System Crashes

## 1. Intent
This document provides a formal Root Cause Analysis (RCA) for the series of systemic crashes addressed during Path 1567. The goal is to isolate the underlying architectural failures rather than treating the symptoms, allowing us to derive robust structural invariants that prevent these classes of errors from seizing the engine in the future.

## 2. Methodology: From Symptom to Root Cause

The SPAO loop was repeatedly interrupted by a series of exceptions. The immediate fixes (bandages) restored execution, but the system remained structurally vulnerable. We analyze each failure below:

### A. Git Switch Conflicts (Node 1531)
*   **The Symptom:** The kernel_daemon crashed during `git switch` because it encountered a detached HEAD or a conflicting local branch.
*   **The Bandage:** Catching the git exception inside `sync_and_clean_node`.
*   **The Root Cause:** The engine implicitly trusted the sandbox environment. It executed a critical state transition (`git switch`) on the assumption that the local Git repository was pristine, using Git as a perfectly reliable, synchronous datastore without validating pre-conditions.
*   **The Systemic Gap:** The orchestration loop lacks a topological pre-condition validation phase before enacting state changes.

### B. Prompt Daemon Initialization (Node 1572)
*   **The Symptom:** `daemon_prompt.py` crashed when attempting to append a list item to an object that was incorrectly initialized as a dictionary.
*   **The Bandage:** Changing the initialization type from `{}` to `[]`.
*   **The Root Cause:** The daemon blindly trusted the implicit structure of the data loaded from disk (`artifacts/prompt_backlog.yml`). It lacked a schema enforcement boundary.
*   **The Systemic Gap:** There is no strict data contract or type validation layer separating persistent disk storage from the daemon's active execution memory.

### C. Validation Gate Escapes (Node 1579)
*   **The Symptom:** A localized error inside a specific validation gate threw an unhandled Python exception, which seized the entire `kernel_daemon` process.
*   **The Bandage:** Refactoring the specific validation gates to catch their own errors and use `sys.exit(2)` for clean operational exits.
*   **The Root Cause:** The core SPAO execution loop lacks a universal fault-isolation boundary. It delegates execution authority to child components (like validation gates) without wrapping them in a protective containment layer.
*   **The Systemic Gap:** The macro-kernel_daemon is not operating as a fault-tolerant supervisor. A failure in a leaf node (a gate) can crash the root process.

### D. GitHub GraphQL Deprecation Noise (Node 1641)
*   **The Symptom:** The `gh issue view` command emitted a GraphQL deprecation warning to `stderr`. The Python `subprocess` wrapper intercepted this as a fatal error (exit code 1), causing `daemon_nba.py` to crash.
*   **The Bandage:** Adding specific logic to safely parse and ignore `stderr` noise in the GitHub client wrapper.
*   **The Root Cause:** The engine relies on brittle, raw `subprocess` executions of external CLI tools. It tightly couples the stability of the autonomous loop to the unpredictable execution noise (like deprecation warnings) of third-party binaries.
*   **The Systemic Gap:** There is no robust SDK or abstraction layer that strictly isolates structured payload data (e.g., `--json`) from CLI execution noise (`stderr`) and explicit exit code management.

## 3. Epistemic Conclusion
The common denominator across all these failures is **Implicit Trust**. The engine trusted the Git sandbox, the disk files, the child validation gates, and the third-party CLI tools. 

To achieve "Gateless Autonomous Execution within a Risk-Managed Sandbox" (SG-0002) and "Preservation of Autonomous Velocity" (SG-0003), the engine must shift from an architecture of *implicit trust* to an architecture of *explicit verification*.

The invariants derived from this RCA are formalized in `WHAT-1784-system-crash-invariants.md`.
