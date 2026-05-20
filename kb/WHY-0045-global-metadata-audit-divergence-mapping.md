# WHY-0045: Global Metadata Audit & Divergence Mapping — Alignment

## Rationale
To ensure absolute topological traceability, the repository metadata (e.g. GitHub issue labels) must correspond precisely with the local frontier state. The current setup allows for label drift:
1. **Stale Status Labels**: Closed issues frequently retain active status labels (like `status: in-progress` or `status: todo`), causing confusion during external tooling scans and board visualizations.
2. **Missing Path Labels**: Closed path issues frequently lack the `path` label, which can break path verification logic.

A global scan of 272 issues revealed 92 instances of labeling drift.

## Solution Direction
To prevent future drift, we must:
1. Define a strict metadata labeling contract for Node/Path transitions.
2. Automate the cleanup of active status labels when an issue is closed.
3. Automatically label Path issues with the `path` label during initialization and transitions.
