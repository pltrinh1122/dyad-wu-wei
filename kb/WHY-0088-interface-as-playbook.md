# WHY-0088: The Interface as the Playbook

## Context
As the governance of the repository has transitioned to the Universal Merge Gate (HTIL) model, the question of how to guide the Operator (human) and the Agent (machine) through the lifecycle of Nodes, Paths, and Retrospectives has emerged. In traditional systems, this is managed via text-based procedural playbooks. 

However, written playbooks introduce critical failure modes:
1. **Operator Cognitive Load**: Humans must read and cross-reference files during active context-switching, acting as manual execution parsers.
2. **Dogmatic Rigidity**: Playbooks resist organic adaptation to novel environments or failures, violating Ziran (natural flow).
3. **Semantic Drift**: Written documentation inevitably drifts from the executable codebase (drivers, kernel, daemons).

## Decision
We establish the principle of **Substrate-Embedded Playbooks**. We formally reject the creation of external, human-facing text playbooks for routine operations. Instead, the system interface itself (the UX substrate: GitHub templates, CLI readouts, interactive checklists, and error messages) must act as the dynamic playbook, guiding the Operator and programmatically enforcing constraints on the Agent.

## Rationale

### 1. Ziran Alignment (Dynamic Guidance)
Rather than forcing the human Operator to memorize static documentation, the system’s interface adapts to the immediate context of the problem. Telemetry alerts, terminal error messages containing recovery tips, and automatically generated PR descriptions ensure that the instruction is delivered *in-place* at the exact moment of execution.

### 2. Wu-wei (Minimized Friction)
By embedding constraints and instructions directly into the interface:
*   The Agent is programmatically constrained (e.g. `WIP-N=1` blocks checkout if open PRs exist).
*   The Operator interacts with the state via visual checkpoints (GitHub issues and checkboxes) rather than manual procedural steps.
This reduces dyad coordination energy to its absolute minimum.

### 3. Absolute Coherence (No Semantic Drift)
When the "playbook" is code (e.g., error validation strings, issue templates, and CLI status output), it cannot drift. The behavior of the Agent and the instructions to the Operator are derived from the same source of truth, ensuring the Meta-Loop remains physically coherent.

## Substrate Readiness Assessment
As of Path 853, the codebase exhibits high readiness:
1.  **State Constraints (High)**: Handled programmatically via `node_lifecycle.py` and `daemon_strategic.py`. Invariants (e.g. dependency locks, SPEC requirements, PR blocks) are enforced in code, raising clear, self-documenting exceptions.
2.  **Operator Dashboards (Medium-High)**: `bin/status` provides zero-latency state readout, and `bin/retro` compiles blameless metrics.
3.  **Lacking Elements**: CLI error outputs should continue to evolve to print the *exact recovery command* (e.g., instead of just "Open PR exists," print "Run `./bin/node sync` after merging PR #XX").
