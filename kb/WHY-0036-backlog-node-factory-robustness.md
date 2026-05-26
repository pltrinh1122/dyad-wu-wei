# WHY-0036: Backlog Node Factory Robustness & Path Template Retrospectives

## Context

The Backlog Node Factory (primarily managed via `BacklogManager` in `kernel/daemon_backlog.py`) orchestrates the creation of Path issues and terminal child nodes on GitHub. During an audit of this system, several robustness gaps were identified that can compromise state synchronization:
1. **Partial Failures**: If creation fails mid-way, duplicate issues or orphaned child nodes are created.
2. **Orphan Control**: API-level guards are needed to completely enforce that terminal nodes cannot exist without parent paths.
3. **Dependency Mapping**: Inconsistencies or TBD strings in dependencies.
4. **Frontier Synchronization**: Newly created issues on GitHub are not immediately registered locally in `artifacts/frontier_state.yml` until explicit checkout.
5. **Path Retrospectives**: No standardized template mechanism exists to enforce post-mortem capture (Continue, Stop, Start) when paths are closed.

This document details the alignment decisions on these issues.

---

## Alignment Decisions

### 1. Idempotency & Clean Recovery
- **Decision**: Introduce pre-creation validation. Before calling the GitHub API to create an issue, the `BacklogManager` must search the current open issues for a matching title prefix. If a duplicate is found, the manager will reuse the existing issue ID instead of creating a new one, permitting safe re-run recovery.
- **Rollback / Cleanup**: In the event of a critical failure during a composite command (like `new-path`), the command must execute rollback operations (closing newly created issues with a failure explanation comment) to prevent polluting the backlog.

### 2. Strict Labeling & Orphan Prevention
- **Decision**: Programmatic label validation. Every backlog item created by the system must be tagged with the `backlog` label, and terminal nodes must be tagged with `status: open` automatically. 
- **Enforcement**: Validate that the `--path` argument is a valid, open Path issue ID. Reject any creation request for a terminal node if the parent path does not exist or is already closed.

### 3. Dependency Verification
- **Decision**: Implement dependency constraint checks. If a node depends on a set of IDs, the `BacklogManager` must verify that those dependent issues exist in the backlog. During execution, the `FlowStateManager` must prevent a user/agent from starting planning on a node if its dependencies are not closed.

### 4. Direct Frontier Auto-Registration
- **Decision**: Auto-register new issues in the local state. Upon successful creation of a new backlog node, the `BacklogManager` will append it directly to `artifacts/frontier_state.yml` under a new status of `Backlog` (or `status: Backlog` in the YAML structure). This ensures the local state matches GitHub without needing a manual checkout or sync step to discover them.

### 5. Path Retrospective Integration
- **Decision**: Update [kb/templates/path_tracker.md](file:///mnt/shared_data/git_repos/dz-cil/kb/templates/path_tracker.md) to automatically include a `## Agent Retrospective` section containing placeholders for:
  - **Continue**: Success patterns to persist.
  - **Stop**: Dysfunctions or anti-patterns to halt.
  - **Start**: Optimizations to introduce moving forward.

---

## Invariant Formalization

A future `HOW-*` document (to be designed in the Plan phase) will formalize the following constraints:
1. `INVARIANT_ID_BACKLOG_IDEMPOTENCY`: Backlog issue creation must be idempotent and reuse matching titles.
2. `INVARIANT_ID_FRONTIER_AUTO_REGISTRATION`: All backlog creation actions must write directly to the local frontier ledger.
3. `INVARIANT_ID_PATH_RETROSPECTIVE`: Every Path issue template must define and enforce an Agent Retrospective section.
