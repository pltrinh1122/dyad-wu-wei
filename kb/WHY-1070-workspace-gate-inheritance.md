# WHY-1070: Child Workspace Gate Inheritance and Sovereign Bypass Rationale

## Context
In the Antigravity Metasystem, workspaces can run concurrently and independently under the `SPAO_WORKSPACE_DIR` redirection. This is crucial for enabling autonomous subagent execution. However, to preserve inner-loop velocity (SG-0003) and ensure that sovereign workspaces are not bottlenecked by parent-level remote PR gates or persona-specific gate checking, we must evaluate how child workspaces inherit or bypass parent security gates.

## Evaluation and Findings

### 1. The Gateway Bypass (Decoupling)
Under the dynamic workspace resolution in `kernel/daemon_strategic.py`, if a child workspace does not define its own local ownership index files (`WHAT-0062` and `WHAT-0065` under the `kb/` directory of the workspace), the strategic gates (`_verify_persona`) emit a warning and gracefully allow transition bypass.
- **Why it is secure**: Sovereign workspaces are sandboxed and operate locally. Their changes are committed and pushed locally, and are only integrated into the parent repository via Pull Request review. The ultimate gatekeeping occurs during parent-level PR merge review, meaning offline bypass does not threaten parent repository main-branch integrity.
- **Why it is necessary**: Without this bypass, a child workspace would either fail to transition (failing-closed due to missing files in a fresh clone) or be forced to carry massive boilerplate KB primitives, reducing execution efficiency.

### 2. Persona Auto-Resolution Invariant
When `SPAO_PERSONA_ID` is absent inside a child workspace, the system dynamically resolves the persona by parsing the local `dz-cil.yml` configuration (which may be customized per-workspace) or by scanning parent path ownership. This ensures that even when the operator runs a CLI command inside a worktree without setting environmental flags, the system resolves to the correct persona context.

### 3. Merging Rules & Intent
Sovereign workspaces are allowed to merge child `GEMINI.md` overrides to resolve local strategic goals. This prevents configuration drift and allows subagents to run customized inner-loop policies under the parent ruleset baseline.

## Architectural Decision
We formally validate the current decoupling implementation in `kernel/daemon_strategic.py` and `drivers/path_resolver.py`.
No functional mutations are required. The current implementation correctly balances local autonomy with ultimate parent PR gatekeeping.

## Next Actions
As this Probe is completed, we will close Node 1070 and transition to reflecting the results.
