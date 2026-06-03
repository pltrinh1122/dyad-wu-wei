# WHAT-1742: Handoff Friction Remediation

## 1. Context
During the Dyadic-Autonomous Handoff mapping in Node #1740, the system generated Path #1739 using `./bin/backlog new path`. However, when attempting to execute the Next-Best-Action (`plan-start 1740`), the engine crashed with:
`[🚫 BLOCKED] Harmonization Failure: Terminal Node #1740 has no parent Path.`

This failure reveals friction in the structural boundaries of our daemons when generating issue trees.

## 2. Root Cause Analysis
The synchronization between `daemon_backlog.py` (which creates nodes) and `daemon_strategic.py` (which validates transitions) contains structural mismatches:

1. **Title Prefix Requirement**: When generating child nodes (Harmonize/Plan/Reflect) recursively within `daemon_backlog.py`, it expects the parent issue's title to begin with `Path: ` (Line 127). If the Operator simply inputs "My Path Title", the child generation fails silently, leaving a stubbed Path with no children and no `Meta-Index` instantiation.
2. **Meta-Index Markdown Regex**: When `daemon_backlog.py` does successfully add a child node to a parent Path's `Meta-Index`, it formats it as `- [ ] #ID: Title`. However, the strategic verification regex in `daemon_strategic.py` (`find_parent_path_id`) specifically expects `- [ ] Node ID:` or `Activity ID:` and will fail to parse `#ID:`.

## 3. The Implementation Plan

### Fix 1: Auto-Prefix Path Titles
Modify `kernel/daemon_backlog.py` to ensure that if `node_type` is "path", the title is automatically prefixed with `Path: ` if it is not already present. This ensures recursive child generation never fails its internal checks.

### Fix 2: Harmonize Meta-Index Regex
Modify `kernel/daemon_backlog.py` to write the standard node format when populating the `Meta-Index`. 
Change:
```python
checkbox_line = f"- [ ] #{issue_id}: {formatted_title}"
```
To:
```python
checkbox_line = f"- [ ] Node {issue_id}: {formatted_title}"
```

### Verification
- Both `pytest tests/test_daemon_backlog.py` and `pytest tests/test_daemon_strategic.py` will pass locally.
- Creating a new mock path using the CLI will generate all child nodes cleanly and the `Meta-Index` will match the strategic regex.
