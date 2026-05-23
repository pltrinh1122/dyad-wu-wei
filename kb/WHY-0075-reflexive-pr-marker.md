# WHY-0075: The Reflexive PR Marker

**Date:** 2026-05-22
**Status:** Accepted

## Context
As we move toward a Ziran auditing approach relying on Natural Exhaust (`WHY-0072`), we must perfectly map physical Node execution to the specific epistemic insights (`kb/WHY-*`) that governed them. We evaluated purely ambient exhaust signals (Context Window Tracing, Diff Resonance, NBA Score Predictions) but mathematically falsified them all due to massive noise, Is-Ought separation, and execution divergence. We require a minimal structural marker.

## Decision
We formally adopt the **Reflexive PR Marker**. 
When the Agent closes a Node (the `REFLECT` phase) or initiates an Insight Materialization pipeline, it is structurally required to append a strict metadata footer to the Pull Request body declaring its intent:
`Active-Insights: WHY-XXXX, WHY-YYYY`

## Rationale
1. **Solves Context Noise:** Instead of an automated Auditor attempting to guess which of the dozens of KB documents in the LLM's context window actually mattered, the Agent explicitly filters the noise by declaring the exact insights that governed its physical keystrokes while its memory is fresh.
2. **Solves Prediction Divergence:** Because the marker is written *after* the stochastic `ACT` phase, it perfectly captures the physical reality of the execution, completely bypassing the predictive hallucinations of the NBA Scorer.
3. **Solves the Is-Ought Problem:** By embedding the tag directly into the Pull Request body, explicit epistemic *Intent* is permanently bonded to the physical *Diff* at the exact moment of state mutation.
4. **Pure Ziran for the Operator:** The Human Operator is subjected to zero friction. You never manually tag an issue. The Agent autonomously generates the marker during the `REFLECT` phase as natural exhaust, allowing the subsequent passive Audit script to map telemetry to the KB with zero manual bureaucracy.
