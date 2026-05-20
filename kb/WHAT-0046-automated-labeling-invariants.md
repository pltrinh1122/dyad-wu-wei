# WHAT-0046: Automated Labeling Invariants — Specification

## 1. Backlog Creation Hooks (`orchestrator/mgr_backlog.py`)
When a new issue is created via `BacklogManager.add`:
- If the node type is a Path, the `path` and `backlog` labels must be automatically added to the GitHub issue.
- If the node type is an Activity or Probe, the `backlog` and `status: todo` labels must be automatically added.

## 2. Node Plan-Start Hooks (`orchestrator/mgr_node.py`)
When a node transitions to `Plan Start`:
- Remove `status: todo` if present.
- Apply `status: in-progress` label.

## 3. Reflection and Close Hooks (`orchestrator/mgr_node.py` and `skills/github_client.py`)
When a Node or Path issue is closed:
- Fetch the issue's existing labels.
- Remove all labels starting with the `status:` prefix.

## Verification & Status
- **Status**: Approved
- **Verified by**: Node 303 Probe
