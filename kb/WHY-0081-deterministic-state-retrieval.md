# WHY-0081: Deterministic State Retrieval

## Context
During the execution of Node 770, the Operator requested a "current status" update. The Agent attempted to construct the status by using its standard probabilistic tools: `view_file` on `artifacts/frontier_state.md`, parsing `bin/prompt list`, and viewing Node configurations. This process took an unacceptable amount of time, triggering an immediate operator correction.

## The Axiomatic Conflict
**SG-0003 (Inner-Loop Velocity)** demands that the inner-loop remain fast and completely offline. 
**Axiom 3 (Materializability)** requires that strategic goals be executable using physically available tools today.

Using a Large Language Model (LLM)—a stochastic, probabilistic inference engine—to read a static text file and retrieve the 4 variables of system state (Active Node, Queue Length, Loop Status, Infrastructure) is an architectural failure. State retrieval is a pure function. Probabilistic inference is computationally expensive, latent, and prone to context-window truncation. 

## The Decision
We conclude that the Operator's claim is mathematically robust and non-falsifiable: **No inferencing is necessary to retrieve static state.**

Therefore, we mandate the creation of a deterministic CLI adapter: `bin/status`.

## Architectural Invariant
1. **The State Dashboard Rule**: The Agent must never manually evaluate flat-files to construct a status dashboard. Any request for "status" must be met by invoking the deterministic `bin/status` wrapper, completely bypassing probabilistic LLM construction of the state. 
2. **Implementation Requirement**: `bin/status` must aggregate the topological Frontier tracker, the Prompt Backlog queue, the Active Git-Worktree status, and the `systemd` daemon infrastructure status into a single stdout payload executing in `<100ms`.
