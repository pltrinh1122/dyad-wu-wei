# WHAT-0045: Global Metadata Audit & Divergence Mapping — Specification

## 1. Issue Label Rules
- **Nodes**: Any issue starting with `Node `, `Discovery `, or `Activity ` must carry the `backlog` label.
- **Paths**: Any issue starting with `Path `, `Discovery Path `, or `Discovery Path:` must carry the `path` label.

## 2. Transition Rules
- **Plan Start**: Transitioning a node to `Plan Start` sets `status: in-progress`.
- **Close / Reflect**: When any node or path issue is closed:
  - Remove all labels matching `status:*` (such as `status: in-progress` or `status: todo`).

## Verification & Status
- **Status**: Draft
- **Verified by**: Node 302 Discovery
