# Retrospective 988: Investigation of PR 982 Workspace Boundary Failure

## Context
During Node 981 (PR 982), the Operator noted that the Agent explicitly mutated `knowledge_accrual_skill.py`, but the file was not included in the final PR #982. The prompt `p-1779727242-c961` formally queued this investigation.

## Root Cause Analysis
The Agent violated the Workspace Isolation Boundary. During execution, the Agent targeted the file editing tool (`multi_replace_file_content`) to the absolute path `/mnt/shared_data/git_repos/agent-antigravity/drivers/knowledge_accrual_skill.py`, which is the global root repository.

Because the SPAO Execution Loop utilizes Git Worktrees (`.worktrees/node/<id>/`) to isolate feature development, the local git client active within the worktree (`.worktrees/node/981-fix-lexical-guards/`) was completely unaware of modifications made to the detached root repository. Consequently, when `node reflect` pushed the worktree branch to GitHub, the changes to `knowledge_accrual_skill.py` were orphaned in the root workspace and omitted from the PR.

## Corrective Actions (Codified)
1. **Invariant 18 Added**: Appended `The Workspace Edit Boundary Invariant` to `GEMINI.md` instructing the Agent that it MUST NEVER modify files in the repository root while operating within a SPAO node. All file editing tools MUST explicitly target `.worktrees/node/<id>/`.
2. **Root Workspace Cleanup**: The root repository was safely restored via `git restore` on the orphaned file to prevent subsequent `node sync` detachment errors.
