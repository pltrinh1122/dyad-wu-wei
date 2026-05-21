# WHY-0053: Optimization of Node Sync Audit Performance (Lightweight Audit)

## Context
During the execution of the MetaSystem integrity checks, the `bin/meta audit` script is run to verify that all completed nodes recorded in the local frontier file (`artifacts/frontier_state.md`) are successfully checked off in their corresponding parent path issues on GitHub.

Historically, this script parsed the local frontier to identify all paths, and sequentially invoked `gh issue view` for every single path ever created. As the project scaled and the number of paths increased, this sequential CLI execution pattern introduced significant network latency, resulting in an O(N) scaling bottleneck where N is the total number of historical paths.

## Problem Statement
The O(N) scaling pattern is unsustainable and violates our strategic goal of high inner-loop velocity (SG-0003). There are two primary redundancies in the legacy audit design:
1. **Historical Path Invariance**: Once a path is completed and closed, its child node checklists are topologically closed and immutable. Auditing fully completed paths in every run is redundant.
2. **Redundant Active Path Auditing**: Even for active, non-completed paths, calling `gh issue view` on every sync is redundant if no new nodes have been completed under that path since the last successful audit.

## Proposed Solutions

### Option A: Shared Directory Layout (Status Quo)
This option preserves the single shared directory for node worktrees (`.worktrees/node/<branch-name>`) as chosen by the operator in Concept C1, ensuring zero path resolver conflicts.

### Optimization 1: Topological Filtering of Completed Paths
Rather than auditing all paths found in the frontier state, the script will read the local `frontier_state.yml` file and filter out any paths whose status is marked as `Completed`. Since completed paths are closed, we only need to verify and audit paths that are still active or in-progress. In standard tiered execution, this reduces the audited paths from N to a maximum of 1 or 2, instantly achieving O(1) scaling for the common case.

### Optimization 2: Local Audit Checksum & State Caching
To completely eliminate redundant network requests for active paths when no state transitions have occurred, we will cache the last successfully audited completed node set in `artifacts/audit_state.json`. 

Specifically:
- For each active path, we store the list of its child nodes that have already been verified as checked off.
- During the audit, we compare the current list of globally completed nodes under that path against the cached list.
- If no new completed nodes have been registered since the last successful audit, the network call for that path is bypassed entirely.

## Architectural Decision
We will implement both Optimization 1 (filtering out completed paths) and Optimization 2 (caching last verified nodes) within the status quo Option A directory structure. This delivers maximum latency reduction while strictly maintaining all safety and compliance verification guarantees of the integrity audit.
