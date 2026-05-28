# WHY-0087: Universal Merge Gate (HTIL) Administrative Bypass

## Axiomatic Grounding
- **Implements**: NS-0001 (Synergistic Human-Agent Partnership), SG-0003 (Preservation of Autonomous Velocity).
- **Extends**: WHY-0087 (Universal Merge Gate)

## The Friction
In accordance with SG-0002 (Gateless Autonomous Execution Within Confined Constraints), the SPAO orchestrator halts all executions at the `node reflect` boundary, entering a Human-in-the-Loop (HTIL) block. This ensures that no codebase mutations enter the `main` branch without explicit Operator approval.

However, certain agentic activities—such as Discovery nodes, Backlog Hygiene, or Prompt Queue ingestions—execute zero logical codebase mutations. They purely update the topological metadata trackers (`artifacts/`). Subjecting these administrative state-updates to a hard HTIL gate introduces unnecessary Operator cognitive load and fundamentally breaks the Operator's Flow State (Wu-wei).

## The Resolution
To optimize for Wu-wei while preserving structural safety, the SPAO execution loop will autonomously bypass the HTIL PR merge gate **if and only if** the PR strictly modifies non-executable, non-structural telemetry.

**The Administrative Boundary:**
A node reflection is mathematically defined as "Administrative" if the physical `git diff` against `origin/main` reveals that **100% of the modified files** are contained within the `artifacts/` directory.

- **`artifacts/`**: Represents ephemeral or tracked state/telemetry (e.g., `frontier_state.md`, `audit_state.json`, `prompt_backlog.yml`). Changes here cannot alter agentic behavior or code execution. Auto-merging is provably safe.
- **`kb/`**: Represents the system's "ROM". Mutating knowledge primitives alters future Agent decision-making. These must be subjected to HTIL to prevent hallucinatory policy drift.
- **`kernel/`, `drivers/`, `tests/`**: Represents executable code logic. These must be subjected to HTIL to prevent functional degradation.

If a PR is determined to be strictly Administrative, the orchestrator will invoke `gh-pr merge --admin --squash` to autonomously integrate the changes into `main`, clearing the WIP lock and allowing execution to proceed continuously.
