# WHY-0039: NBA Strict Transition Enforcement Gate

## Context
The Antigravity system manages task execution using a topological Meta-Graph of non-terminal `Paths` and terminal `Nodes` (Activities and Probes). Strategic prioritization is managed via the strategic intent ledger ([strategic_intent.yml](file:///mnt/shared_data/git_repos/agent-antigravity/artifacts/strategic_intent.yml)). 

Currently, the flow state manager allows executing state transitions (`plan-start`, `checkout`, and `meta path`) on any node or path in the backlog, even if the target is not aligned with any active prioritized goals.

## Problem
Without automated transition-level enforcement, the system is vulnerable to token drift and attention fragmentation. An operator or an autonomous agent could begin work on an unprioritized path or node, violating **SG-0001 (Backlog Dynamics and Resource Budget Alignment)**. 

To maintain strict alignment between execution and strategic intent, the flow state manager must programmatically enforce transition guardrails before any work begins on a path.

## Decision: Strict Transition Enforcement

We will implement an automated transition enforcement gate in the orchestrator that intercepts state mutations and enforces strict alignment with the active strategic intent ledger.

### 1. Invariants

*   **`INVARIANT_NBA_TRANSITION_PRIORITIZED`**: A terminal node (Activity/Probe) or a Path can only be set active or transitioned to `in_progress` if its parent Path ID (or its own ID, if it is a Path) is explicitly registered and prioritized in the active strategic intent ledger ([strategic_intent.yml](file:///mnt/shared_data/git_repos/agent-antigravity/artifacts/strategic_intent.yml)).
*   **`INVARIANT_OFFLINE_BYPASS`**: During offline execution (detected via `ANTIGRAVITY_RUNNING_TESTS` or `SPAO_OFFLINE`), live GitHub parent-path resolution is bypassed or mocked to respect the offline velocity constraint (**SG-0003**).

### 2. Implementation Mechanics

#### A. Parent Path Resolution
Because terminal nodes do not natively store a hard back-link to their parent Path on their GitHub issue labels, the orchestrator will resolve the parent-child relationship by:
1.  Querying GitHub to fetch all open issues labeled `path` (using `github_client.list_issues_by_label`).
2.  Inspecting the bodies of these Path issues under the `## Meta-Index` checklist to locate the checkbox matching the target terminal node ID.
3.  Mapping the terminal node to its parent Path ID.

#### B. Enforcement Points
The guardrail will be integrated into:
1.  **Node Planning & Checkout**: `plan_start` and `checkout` methods in `kernel/node_lifecycle.py` will verify that the parent Path ID of the target terminal node is listed in the `prioritized_paths` of an `Active` goal.
2.  **Path Activation**: The `set_active_path` command in `kernel/mgr_frontier.py` will verify that any new active path is prioritized.

#### C. Error Handling
If verification fails, the orchestrator will print a descriptive alignment failure message and exit with code `1`, preventing branch checkout, planning locks, or active path updates.
