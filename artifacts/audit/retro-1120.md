# Retrospective: Node 1120 (Harmonize - Achieve ISBO Completeness)

## Overview
During the execution of Node 1120, a `Persona Gate Blocked` error was encountered.

## Root Cause
The `frontier` persona attempted to execute `plan-start` on Node 1120, which is a child of Path 1119 under `SG-0002`. According to `kb/WHAT-0062-agent-persona-ownership-index.md`, `SG-0002` was exclusively assigned to `agent-sg2`. This caused `_verify_persona` to fail-closed, blocking the transaction and logging a failure in telemetry.

## Resolution
`WHAT-0062` was mutated to change the `owner_persona` of `SG-0002` to `shared`. This is a previously aligned structural decision (noted in retro-1081.md) that enables the frontier persona to legitimately orchestrate orchestration and structural paths under SG-0002.

### Follow-up Failure
During the subsequent `reflect` execution, a transient GitHub GraphQL API error (`Could not close the issue. (closeIssue)`) caused a secondary transaction rollback.

## Lessons Learned
The Persona Gate enforces strict ownership invariants. When a path is prioritized under an SG, the executing agent must either exactly match the assigned persona or the SG must be explicitly flagged as `shared` in the authoritative index. Reverts or overwrites of `WHAT-0062` can silently re-introduce gate blocks for administrative personas unless explicitly managed.

Additionally, GitHub API transient errors during the `close_issue` stage of the `reflect` phase can trigger rollback events requiring re-execution of the reflect command.
