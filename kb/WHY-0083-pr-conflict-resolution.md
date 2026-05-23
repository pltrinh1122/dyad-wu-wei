# WHY-0083: PR Conflict Resolution

## 1. Problem Statement
The standard execution loop (`bin/node reflect`) generates a Pull Request automatically upon completion of the Act phase. However, if the `main` branch has progressed (e.g., other agents merging paths), the local branch may contain severe unresolved merge conflicts against `origin/main`. Submitting a PR with a broken branch shifts the burden of conflict resolution from the Agent to the Operator, which is a direct violation of **SG-0002 (Containment & Delegation)** and **SG-0003 (Inner-Loop Velocity)**. 

## 2. The Decision
We mandate that the Agent is structurally responsible for resolving its own merge conflicts *before* invoking the `reflect` command. 
If the Agent pushes a branch with unresolved conflicts, it constitutes an execution failure. The Agent must pull the latest `origin/main`, merge it, resolve any file conflicts via internal scripting or tools, ensure the test harness still passes, and only then submit the PR.

## 3. Architectural Implications
1. **The Conflict Guardrail**: A new pre-reflection hook will be implemented in `kernel/daemon_node.py` or the `HookManager`. It will perform a dry-run merge or verify branch compatibility against `origin/main`. If conflicts exist, the `reflect` operation will fail-closed and force the Agent to manually resolve them in the Act phase.
2. **Procedural Invariant**: All `kb/HOW-*` documentation will be updated to require agents to proactively sync their worktrees with `origin/main` prior to the `reflect` phase.
