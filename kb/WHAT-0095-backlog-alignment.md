# WHAT-0095: Group and Align Backlog list with Strategic Goals Specification

This document codifies the requirements, schema, and layout mapping rules for grouping backlog items by Strategic Goals and rendering DAG dependencies in the CLI backlog output.

---

## 1. Backlog Query & Extraction Invariants

The backlog daemon must compile the backlog dataset in a single-request remote transaction to satisfy inner-loop velocity (SG-0003):
- **Single Remote Call**: The CLI must fetch all open issues using the `github-cli-list` API wrapper containing `number`, `title`, `body`, and `labels` in a single subprocess run.
- **Path Filtering**: The CLI must isolate issues that contain the `path` label.

---

## 2. DAG Dependency Resolution

- **Dependency Extract Pattern**: For each path issue, the daemon must scan its body for the following case-insensitive pattern:
  `## Depends On\s*\n+([^\n#]+)`
- **Dependency Matching**: It must parse comma-separated issue numbers from the matching text.
- **DAG Status**: Resolved path dependencies are appended to the path entry in the layout as `[Depends: <comma-separated-ids>]`.

---

## 3. Strategic Goal Grouping Layout

The output layout printed by the list command must group paths according to active strategic goal mappings:
1. **Load Ledger**: Load the local `strategic_intent.yml` to retrieve all active strategic goals (`status: Active`) and their `prioritized_paths`.
2. **Prioritized Goal Sections**: Render a header for each active Strategic Goal, e.g.:
   `🎯 [SG-XXXX] <Strategic Goal Title>`
   Beneath the header, list all matching open backlog paths in the prioritized order defined by the ledger.
3. **Unmapped Backlog Section**: Render a header for unmapped paths:
   `📋 [Backlog / Unmapped]`
   Beneath it, list all open backlog paths that are not prioritized in any active Strategic Goal.

---

## 4. Execution Velocity Invariant

The entire listing operation (remote single-request fetch, local ledger parsing, body parsing, and printing) must execute in under 1.5 seconds.
