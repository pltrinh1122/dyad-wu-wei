# WHAT-0023: Triple-Node Auto-Initialization Specification

## Overview
This document specifies the technical design and API constraints for programmatically enforcing the Triple-Node Doctrine. 

## Component Specification

### Backlog Manager (`BacklogManager.create`)
The `BacklogManager.create` function in `kernel/daemon_backlog.py` is the entry point for declaring nodes.

#### Parameters:
- `node_type`: `str` (e.g. `'path'`, `'discovery'`, `'activity'`)
- `title`: `str`
- `goal`: `str`
- `path_id`: `str` (optional)
- `depends_on`: `str` (optional)

#### Behavior for Non-Terminal Nodes (Paths):
When `node_type` is matching the non-terminal category (`'path'`):
1. **Parent Creation**:
   - The Path issue is created on GitHub.
   - The Path issue receives a label `'backlog'`.
   - The Path issue is renamed to format: `Path {issue_id}: {title}`.
2. **Sequential Child Creation**:
   - Immediately following parent registration, the manager invokes recursive calls to `create(...)` to establish the three mandatory child nodes.
   - **Harmonize Discovery**:
     - `node_type`: `'discovery'`
     - `title`: `f"Harmonize - {title}"`
     - `goal`: `f"Harmonize on the philosophical and technical intent for {title}."`
     - `path_id`: `{parent_issue_id}`
   - **Plan Discovery**:
     - `node_type`: `'discovery'`
     - `title`: `f"Plan - {title}"`
     - `goal`: `f"Technical design and proposed changes for {title}."`
     - `path_id`: `{parent_issue_id}`
     - `depends_on`: `{align_probe_issue_id}`
   - **Reflect Activity**:
     - `node_type`: `'activity'`
     - `title`: `f"Reflect - {title}"`
     - `goal`: `f"Final reflection and path closure for {title}."`
     - `path_id`: `{parent_issue_id}`
     - `depends_on`: `{plan_probe_issue_id}`
