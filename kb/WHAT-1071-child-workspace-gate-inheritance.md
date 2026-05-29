# WHAT-1071: Child Workspace Gate Inheritance Definitions

## 1. Intent
This document defines the formal ontology and rules governing how child workspaces (running under SPAO_WORKSPACE_DIR redirection) inherit, bypass, or override the parent repository's strategic security gates.

## 2. Terminology & Definitions

*   **Sovereign Workspace (Child)**: A sandboxed, detached worktree environment spawned programmatically (e.g. for subagent execution or parallel tasks).
*   **Sovereign Bypass**: The policy allowing a Sovereign Workspace to gracefully transition through SASE phases (Sense, Plan, Act) and execution steps without raising blocking persona-matching warnings.
*   **Parent Gates**: The authoritative security and policy gates (such as `_verify_persona` in `kernel/daemon_strategic.py` or remote PR checks) configured on the parent repository main-branch context.

## 3. Inheritance Rules

1.  **Local Bypass Principle**: If a Sovereign Workspace does not possess local ownership index files (`WHAT-0062` and `WHAT-0065` under the workspace's `kb/` directory), the strategic gates MUST emit a non-blocking warning rather than a blocking error.
2.  **Ultimate Gatekeeping Principle**: Safety is preserved because sovereign local worktree changes are isolated. Verification occurs offline, and the changes are only integrated via the parent-level Pull Request review. The ultimate integration gate remains the parent PR merge.
3.  **Dynamic Persona Resolution**: When `SPAO_PERSONA_ID` is absent inside a child workspace, the system dynamically resolves the persona by parsing the local `dz-cil.yml` configuration (which may be customized per-workspace) or by scanning parent path ownership.

## 4. Manifest Registration
This specification is immune to project-specific constraints and remains a core primitive of the Antigravity engine.
