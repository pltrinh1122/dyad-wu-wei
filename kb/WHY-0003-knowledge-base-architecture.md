# WHY-0003: The Knowledge Base (kb) Pillar

**Date:** 2026-05-16
**Status:** Accepted

## Context
After migrating to the Linguistic Primitives (`WHAT`, `WHY`, `HOW`), the files were initially placed at the root of the repository. This created clutter and blurred the lines between immutable system governance and standard repository entry points (like `README.md` or `AGENT.md`). The Operator requested an evaluation of "house-cleaning" to determine if these files belonged in `artifacts/` or elsewhere.

## Options Considered
1. **The Root Directory:** Leave primitives at the root. Cluttered and unscalable.
2. **The `artifacts/kb/` Directory:** Store them inside `artifacts/`. This violates the definition of `artifacts/`, which is designated for *mutable state, memory, and output* (RAM), whereas primitives are *immutable governance* (ROM).
3. **The `kb/` Directory:** Create a brand new, top-level pillar in the Agentic Architecture.

## Decision
We decided to adopt **Option 3** and establish the `kb/` (Knowledge Base) directory as the fourth pillar of the Agentic Architecture.

## Rationale
This decision creates perfect architectural symmetry. It physically separates the "Laws of the System" from the "State of the System." The Agentic Architecture is now composed of four clean pillars:
1. `artifacts/`: The **RAM** (Mutable state, `frontier_state.md`).
2. `skills/`: The **Hands** (Tools).
3. `orchestrator/`: The **Engine** (Execution loop).
4. `kb/`: The **ROM** (Immutable `WHAT`, `WHY`, and `HOW` primitives).
