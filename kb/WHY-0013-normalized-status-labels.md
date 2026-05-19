# WHY-0013: Normalized Status Labels and Abstraction

## Date
2026-05-18

## Context
As the SPAO lifecycle evolved, physical GitHub label strings (like `status: in-progress` and `backlog`) were hardcoded directly into execution layers (e.g., `TerminalNode.plan_start()`, `TerminalNode.checkout()`). This created tight coupling between the Antigravity orchestration logic and the GitHub issue taxonomy, breaking the domain-agnostic abstraction principles. 

Probe 193 evaluated how to decouple these state transitions into a logical schema configuration, aligning with the `WHY-0012` pattern of domain-specific modular configuration files.

## Decision
1. **Dedicated Configuration (`node.yml`)**: We will introduce a domain-specific `node.yml` configuration to hold `node_attributes.status`. This decouples GitHub label strings entirely from Python source code.
2. **Unified `node set-status` Abstraction**: `BaseNode` will implement a `set_status(status_key: str)` abstraction. Both `TerminalNode` and `NonTerminalNode` will utilize this abstraction to interact with GitHub issues. The system will no longer add/remove labels directly using hardcoded strings.

## Schema Architecture (`node.yml`)
The configuration will map logical state keys (the standard vocabulary used by the SPAO loop) to physical GitHub tags.

```yaml
node_attributes:
  status:
    in_progress: "status: in-progress"
    backlog: "backlog"
```

### Orthogonality Across Node Types
- **Terminal Nodes**: Will natively rely on both the `backlog` key (for Sense phase queuing) and the `in_progress` key (for WIP-N=1 locking).
- **Non-Terminal Nodes (Paths)**: Since Paths serve as meta-containers for tracking Epics/Probes/Activities, they do not enter the Act worktree loop and do not strictly require the `backlog` label. However, invoking `set_status('in_progress')` on a Path can cleanly indicate active traversal without affecting the Sense prompt queue.

### Abstraction Behavior (`BaseNode.set_status`)
- **Lookup**: The method will query `node.yml` for the corresponding label string mapping.
- **Fail-Safe**: If a `status_key` does not exist in `node.yml`, the abstraction will raise a strict `ValueError` preventing silent state desynchronization.
- **CLI Translation**: A `bin/node set-status <issue_id> <status_key>` adapter will be exposed to permit identical decoupling for Operator scripting and tests.

## Consequences
- A `node.yml` file must be materialized at the repository root.
- The `orchestrator/node_lifecycle.py` logic must be refactored to parse this file.
- All hardcoded `add_gh_label("status: in-progress")` calls must be replaced with `self.set_status("in_progress")`.
- Path execution nodes (Activities 194, 195, 196) will proceed linearly to implement these components.
