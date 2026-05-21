# WHAT-0053: Optimization of Node Sync Audit Performance (Lightweight Audit) — Specification

This specification defines the lightweight checksum-based audit mechanism for `bin/meta audit` to resolve performance bottlenecks.

## 1. Local Cache Schema (`artifacts/audit_state.json`)
The `artifacts/audit_state.json` file is expanded to include a new key `meta-index-audit`. This key maps to a dictionary tracking the checked-off nodes for active paths.

```json
{
    "meta-index-audit": {
        "path_states": {
            "<path_id>": [
                "<node_id_1>",
                "<node_id_2>"
            ]
        }
    }
}
```

## 2. Path Filtering Logic (`bin/meta audit`)
To optimize network queries:
1. **Load Frontier State**: Load `artifacts/frontier_state.yml` (after performing the standard signature/checksum validation).
2. **Retrieve Path Nodes**: Identify all path nodes defined in the frontier state. A node is classified as a Path if its title matches a heading containing a Path ID followed by "Path" or if it is classified as a path under the `node_taxonomy` (loaded from `antigravity.yml`).
3. **Filter Active Paths**: Exclude any path node that has `status: Completed` in the local frontier state.
4. **Active Path Fallback**: Include the `current_active_path` ID from the frontier state if defined and not already excluded.

## 3. Network Bypassing Logic (`bin/meta audit`)
For each filtered active path ID:
1. **Retrieve Completed Nodes**: Find the set of all completed node IDs in the local frontier file.
2. **Compute Delta**: Let `cached_verified = path_states.get(path_id, [])`. Compute the difference `unverified = completed_nodes - cached_verified`.
3. **Audit Execution**:
   - If `unverified` is empty: Bypass the network request for this path entirely.
   - If `unverified` is not empty:
     1. Fetch the path issue body via `gh issue view`.
     2. Update the body by marking the completed nodes in the checklist.
     3. If updates were made, write the new body via `skills/github_client.update_issue_body`.
     4. Update `path_states[path_id]` to include all currently completed nodes.
     5. Save the updated states to `artifacts/audit_state.json`.

## Verification & Status
- **Status**: Pending
- **Verified by**: Node 505 Probe
