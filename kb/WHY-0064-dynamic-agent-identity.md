# WHY-0064: Dynamic Agent Identity Resolution Rationale

## 1. Context & Problem
Previously, the agent's identity was statically hardcoded inside `antigravity.yml` as `agent_id: agent-sg5` or similar. This resulted in:
1. Git merge conflicts on the `main` branch when different agents merged their PRs, since they would overwrite each other's configured `agent_id`.
2. Brittle execution in multi-agent environments where different directories/workspaces are mapped to different agent identities (e.g. `agent-SG2-auto` running in `.worktrees` vs `agent-sg5`).

## 2. Decision
We decouple `agent_id` from the version-controlled `antigravity.yml` configuration and resolve it dynamically at runtime.

## 3. Rationale for Precedence Rules
1. **`SPAO_AGENT_ID` Environment Variable**: Provides a clean, standardized override hook for orchestrators or containers to specify an agent's identity explicitly.
2. **Directory Basename Fallback**: Uses the physical workspace directory name (e.g., `/mnt/shared_data/git_repos/agent-SG2-auto`), parsing it to strip any environment-specific suffix like `-auto` and lowercasing it. This leverages directory isolation to map executing instances to the correct agent persona (e.g., `agent-sg2`) without needing config mutations.
3. **No tracking of `agent_id` in Git**: Ensures that the root configuration is generic and shared cleanly across all agents on the `main` branch.
