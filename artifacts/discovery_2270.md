# Discovery 2270: Harmonize - Remediate Zombie Triage Holding Mechanism

## Context
Path 2046 successfully falsified the "Triage Holding" mechanism, concluding that bug intakes should dynamically spawn their own Path containers to bypass the administrative overhead of a holding queue.
However, a zombie invariant was left intact within `kernel/daemon_node.py` which continually scans for, re-creates, and herds nodes into a "Triage Holding" Path if it is missing.

## Analysis
The offending invariant lives in `kernel/daemon_node.py`. It is broken down into two main blocks:
1. **Block A (Lines 250-278)**: `# A. Find or create the Triage Holding Path`. It queries GitHub for an issue with "triage holding" in the title and `path` label. If not found, it autonomously calls `github_client.create_issue()` to resurrect it.
2. **Block D (Lines 305-348)**: `# D. Map unpromoted status:triage terminal nodes to Triage Holding Path`. It iterates through all open `status:triage` nodes and herds them into the Triage Holding Path's Meta-Index.
3. **Fallback logic (Line 410)**: Method C ignores the triage holding path explicitly, which is correct, but relies on the variable `triage_holding_path`.

## Execution Intent
- **Excise Block A**: Completely remove the logic that attempts to find or create the Triage Holding Path.
- **Excise Block D**: Completely remove the logic that maps triage nodes to a holding path.
- **Refactor Method C**: Since `triage_holding_path` will no longer exist as a local variable, remove the explicit exclusion of it from the fallback selection logic.
- Ensure the `tests/test_daemon_node.py` is updated if it contains assertions related to Triage Holding path creation.

This structural remediation will permanently kill the Triage Holding mechanism and restore compliance with Path 2046.
