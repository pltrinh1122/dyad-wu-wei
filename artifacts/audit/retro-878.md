# Epistemic Retrospective: Node 878

## The Failure
During Node 878 planning, two distinct failures occurred:
1. `plan-finish 878` failed with a `KB Conflict Check Failed` because the deprecated term `optimize` (which is deprecated and superseded by `refine` under `kb/semantic_ledger.yml`) was used in `kb/WHAT-0090-optimize-node-sync.md` and `kb/HOW-0000-manifest.md`.
2. The initial `reflect` command executed from within the active worktree directory failed with `FileNotFoundError` because the worktree resolver attempted to resolve worktree directory relative to the current directory, resulting in double nesting (`.worktrees/node/878-plan-spao-velocity/.worktrees/node/878-plan-spao-velocity`).

## The Epistemic Insight
1. Deprecated terms defined in `kb/semantic_ledger.yml` must not be introduced into any `kb/` files (except defined immune zones like `GLOSSARY.md` and `WHY-` prefix files). The file `kb/HOW-0000-manifest.md` is a `HOW-` file and therefore not immune.
2. The static KB conflict check also prevents direct shell commands like `git fetch` in documentation files under `kb/` (e.g. `WHAT-0090-reactive-node-sync.md`), requiring the use of descriptive or hyphenated terms (e.g., `git-fetch` or `remote fetch`).
3. Execution commands (like `node reflect`) must always be executed from the repository root directory rather than from within checked-out worktrees, to ensure paths like `.worktrees/` are resolved correctly.

## The Remediation
1. Renamed `kb/WHY-0090-optimize-node-sync.md` to `kb/WHY-0090-refine-node-sync.md` and deleted `kb/WHAT-0090-optimize-node-sync.md`.
2. Created a compliant `kb/WHAT-0090-reactive-node-sync.md` using `refine` and `git-fetch` to satisfy semantic constraints.
3. Updated `kb/HOW-0000-manifest.md` to reference the renamed spec files using `Refining` and `refine`.
4. Rerun `node reflect` from the repository root `/mnt/shared_data/git_repos/agent-antigravity` instead of the worktree directory.

## The Synthesis
Enforcing lexical purity and command abstraction constraints prevents semantic drift and protects boundary integrity. Multi-worktree operations require consistent directory anchoring at the repository root.
