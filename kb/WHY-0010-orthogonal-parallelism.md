# WHY-0010: Orthogonal Parallelism

> [!NOTE]
> This decision record codifies the architecture required to safely lift the flat `WIP-N=1` invariant into a concurrent model that allows multiple agents to operate simultaneously on orthogonal directories within the repository.

---

## 1. Context & Problem
Currently, the Antigravity architecture enforces a strict Single-Piece Flow (`WIP-N=1`), meaning only one node (Activity or Probe) may occupy the Act phase across the entire repository. As the workload scales, this serialization creates artificial bottlenecks for agents working on completely unrelated (orthogonal) areas of the codebase.

Lifting this restriction requires strict worktree management and state synchronization to prevent Git collisions and corruption of shared meta-artifacts.

---

## 2. Decision: Full Multi-Activity/Probe Parallelism
We will transition to a model supporting full multi-Activity and multi-Probe parallelism, provided the execution happens in orthogonal directories.

### 2.1 Git Worktree Isolation
To prevent branch collisions and active workspace corruption, parallel executions must NOT operate in the same physical directory. We will manage this through **`git worktree`** directories.
- Each parallel execution (Node-Loop) will operate in its own isolated `git worktree` tied to its respective Git branch.
- Simplifying Assumption: `git_repos` workspaces reside as sibling directories at the root of the environment, meaning new worktrees should be checked out within this shared environment safely.

### 2.2 Shared Artifact State Synchronization
Concurrent execution introduces race conditions on centralized Metasystem-tier state files, notably:
- `artifacts/frontier_state.md`
- `artifacts/prompt_backlog.yml`

To resolve this, we will implement an explicit **File-Locking Mechanism** (e.g., optimistic or pessimistic lock files). An agent must acquire the lock before transitioning states, closing ledgers, or consuming prompts.

### 2.3 Probe vs Activity Invariant Re-Assertion
This architectural shift does NOT change the definition of a Probe.
- **Probe**: Investigatory. Produces architectural decisions (`WHY-*`) and Backlog nodes. NO logic mutations.
- **Activity**: Functional implementation. Modifies `drivers/`, `kernel/`, `bin/`, etc.

---

## 3. Implementation Pathway
The actual implementation of these decisions will be executed through standard **Activity** nodes pulled from the backlog:
1. Implement `git worktree` orchestration.
2. Implement file-level locking for shared artifacts.
3. Explicitly codify invariants (Probe boundaries, Prompt processing) in `GEMINI.md` to ensure all sessions are bound by the same meta-rules.
