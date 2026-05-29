# WHY-1421: Automated Observe Phase and the Elimination of Local HITL

## Context
During execution, it was observed that the SPAOR loop contained a contradiction. `WHY-0087` (Universal Merge Gate) dictated that all intermediate manual and local gates be deprecated, establishing the GitHub Pull Request (PR) merge as the sole non-negotiable hard block (HTIL). However, the `Observe` phase of the SPAOR loop (`HOW-0001`) still required the Agent to locally halt execution, forcing the Operator to perform an intermediate review before the PR was even generated in the `Reflect` phase.

## Decision
The local HITL pause in the `Observe` phase is formally falsified and abolished. The `Observe` phase is redefined as a fully automated phase where the Agent autonomously verifies test telemetry and flushes asynchronous prompt queues before immediately advancing to `Reflect`.

## Rationale
1. **Dyadic Cycle Frictionless Flow**: The Dyadic Cycle asserts that the Agent manages mechanical hypothesis generation (`Sense`, `Plan`, `Act`, `Reflect`) while the Operator provides strategic validation. A local pause *before* reflection interrupts the Agent's natural velocity and requires synchronous coordination.
2. **Alignment with Universal Merge Gate**: The true Human-In-The-Loop (HTIL) gate is the Universal Merge Gate (the PR merge). Halting before the PR exists forces the Operator to be a tactical gatekeeper rather than a strategic reviewer, directly violating `WHY-0087`.
3. **Survivor Implementation**: The survivor state shifts the block. The Agent will no longer halt in `Observe`. Instead, it will halt *after* reflection, being physically blocked from entering the next Node's `Sense` phase until the active PR is merged. This aligns perfectly with the physics of `WIP-N=1` and Ziran Flow.
