# WHAT-2423: Audit Daemon Serializes Anomalies

## Objective
Modify the `drivers/audit_daemon.py` to programmatically open a new issue labeled `type: intent, status: todo` containing the Node ID and crash context whenever it performs an autonomous abort. 

## Requirements
- Use `subprocess.run` to trigger the `gh issue create` CLI command during a node abort.
- The spawned issue MUST have `type: intent` and `status: todo` labels.
- The spawned issue MUST optionally have a `[BUG]` title prefix.
- Provide the Node ID and the crash context (e.g., time elapsed of inactivity) in the issue body.

## Rationale
To bridge the Dark Substrate with the Operator UI, ensuring that when the daemon deterministically aborts a stalled node, the LLM is notified via a standardized `[BUG]` intent in the backlog for cognitive investigation.

