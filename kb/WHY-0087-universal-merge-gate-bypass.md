# WHY-0087: Universal Merge Gate (HTIL) Administrative Bypass

## Axiomatic Grounding
- **Implements**: NS-0001 (Synergistic Human-Agent Partnership), SG-0003 (Preservation of Autonomous Velocity).
- **Extends**: WHY-0087 (Universal Merge Gate)

## The Friction
In accordance with SG-0002 (Gateless Autonomous Execution Within Confined Constraints), the SPAO orchestrator traditionally halted all executions at the `node reflect` boundary, entering a Human-in-the-Loop (HTIL) block to ensure no codebase mutations entered the `main` branch without explicit Operator approval.

However, subjecting all code mutations to a hard HTIL gate introduces unnecessary Operator cognitive load and bottlenecking, fundamentally breaking the Operator's Flow State (Wu-wei). Given that the offline test harness (`./bin/run-tests`) can structurally validate operational and functional execution integrity, a universal gate is redundant for the majority of execution paths.

## The Resolution
To optimize for Wu-wei while preserving structural safety, the SPAO execution loop will autonomously bypass the HTIL PR merge gate for ALL pull requests, **EXCEPT** those that modify the `sacred_files` as explicitly configured in `dyad-wu-wei.yml`.

**The Sacred Boundary:**
A node reflection is defined as "Operational" (and auto-merged) if the physical `git diff` against `origin/main` reveals that **0% of the modified files** are `sacred_files`.

- **`sacred_files` (e.g., `DYAD.md`, `GEMINI.md`)**: Represents the system's fundamental psychic architecture and "ROM". Mutating these primitives alters core agentic decision-making and identity. These MUST be subjected to HTIL review to prevent hallucinatory policy drift.
- **`artifacts/`, `kb/`, `kernel/`, `drivers/`, `tests/`**: Represents state, general knowledge, and executable code. These are structurally trusted to be validated by the automated offline test harness and will be auto-merged.

If a PR is determined to NOT touch any `sacred_files`, the orchestrator will autonomously merge it, clearing the WIP lock and allowing execution to proceed continuously.
