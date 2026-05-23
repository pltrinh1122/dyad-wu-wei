# WHY-0013: Sense-Phase Operator Gating (DEPRECATED)

> **DEPRECATION NOTICE**: This document has been officially superseded by `WHY-0076-telemetry-over-dialogue.md`. The "Sense-Gate Invariant" was proven to be mathematically incompatible with the Ziran (Wu-Wei) Continuous Inference Loop and was abolished.

## 1. Context
Antigravity agents are designed to execute the SPAO (Sense-Plan-Act-Observe) loop autonomously. As the Frontier Agent, the agent reads the topological state, consults the `nba_evaluator`, and sequentially processes Nodes from the backlog.

However, a fundamental architectural flaw was observed: agents consistently execute `bin/node sync` (Sense phase), observe the `Next-Best-Action` output, and autonomously jump straight into `bin/node plan-start` (Plan phase). This creates a runaway train effect, stripping the human operator of the ability to re-prioritize, pause execution, or seamlessly switch Paths without forcibly interrupting the agent mid-plan.

## 2. Legacy Decision (Now Abolished)
To restore strict operational control, we originally implemented a **Two-Pronged Sense-Gate**:
1. **The Behavioral Gate (Meta-Instruction Invariant)**: We mathematically forbid SENSE -> PLAN transitions without explicit operator alignment.
2. **The Environmental Gate (Visual Cue)**: We inject an inescapable ANSI-colored blocker string directly into the output of the Next-Best-Action evaluator to physically halt the agent's contextual momentum.

## 3. The Reversal (Ziran Falsification)
The Sense-Gate was falsified under the Daoist mechanics of "Wu-Wei" (effortless flow) for the following reasons:
1. **Redundancy**: The true physical boundary is the **Observe-Gate (HITL)** (PR merge). Creating a bureaucratic checkpoint before planning is artificially redundant.
2. **Forced Coordination**: The Sense-Gate forces the Operator to use conversational alignment for execution, violating the Anti-Forced Coordination Principle (`WHY-0076`).

Consequently, the Sense-Gate has been destroyed. The Frontier Agent is now authorized to autonomously cascade from Sense into Plan when executing a prioritized backlog path.
