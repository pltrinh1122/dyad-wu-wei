# Implementation Blueprint 1244: Triage Holding

## Overview
This blueprint outlines the technical integration of a Standalone Triage queue into the dyad-wu-wei repository.

## Components
1. **Triage Backlog Queue:**
   - A dedicated YAML file (`artifacts/triage_backlog.yml`) to store raw, unmapped signals.
2. **Daemon Triage Manager:**
   - A new script `kernel/daemon_triage.py` that maps these raw signals into structured Path requests using the `issue_factory` templates.
3. **CLI Adapter:**
   - A new bash wrapper `bin/triage` exposing operations: `list`, `accept`, `reject`.

## Execution Steps
1. Create `artifacts/triage_backlog.yml`.
2. Implement `kernel/daemon_triage.py` with parsing and GH issue generation.
3. Implement `bin/triage` adapter.
4. Hook the triage count into `sync_and_clean_node` Sense phase so the Operator is notified if the holding zone is full.

## Constraints
- The SPAO loop MUST NOT execute unverified signals directly.
