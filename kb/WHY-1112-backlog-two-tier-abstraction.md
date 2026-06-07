# WHY-1112: Two-Tier Backlog Abstraction Contract

> [!NOTE]
> **Status**: Finalized  
> **Node**: 1112 (Probe — Path 769)  
> **Persona**: agent-sg5 (SG-0005: Autonomous Knowledge Accrual)  
> **Date**: 2026-06-06

## 1. Intent
To formalize the encapsulation of terminal Node creation (`activity`, `discovery`) behind a Path-level interface. The goal is to enforce the architectural boundary where the Operator operates at the Strategic/Path tier, and the Substrate/Agent operates at the Tactical/Node tier.

## 2. The Abstraction Leak (Current State)
Currently, `bin/backlog new` exposes `path`, `activity`, and `discovery` symmetrically to the Operator. This allows the Operator to manually map terminal execution units, which causes friction:
1. **Cognitive Load**: The Operator is forced into the weeds of SPAO node linking, dependencies, and IDs.
2. **Structural Drift**: Manually created nodes often bypass the rigorous Harmonize/Plan/Reflect structure enforced at the Path level.

## 3. The Two-Tier Contract
We formally codify a two-tier abstraction:
- **Tier 1 (Strategic/Operator)**: The Operator interacts exclusively via `bin/backlog new path`. Paths represent holistic philosophical goals.
- **Tier 2 (Tactical/Agent)**: Terminal nodes (`activity`, `discovery`) represent atomic SPAO execution units. They are managed entirely by the substrate. 

### Substrate Internalization
Terminal node creation should be internalized via two mechanisms:
1. **Interactive Decomposition (Operator Handoff)**: When the Operator creates a Path (`bin/backlog new path`), the CLI may optionally drop into an interactive prompt allowing the Operator to describe the feature work, which the substrate then translates into auto-generated Activity nodes attached to the Path.
2. **Autonomous Derivation (Agent Planning)**: During the autonomous Plan phase, the Agent generates the explicit feature execution nodes to satisfy the Path. 

To enforce this, `bin/backlog new activity` and `bin/backlog new discovery` must be restricted from direct Operator invocation, gated behind a programmatic context (e.g., `SPAO_WORKSPACE_DIR` or an `--internal` flag).

## 4. Feasibility & Resolution
The encapsulation is structurally feasible and aligns directly with the Wu-wei cognitive offloading philosophy.

### Result
- The Two-Tier Abstraction Contract is codified.
- Activity node #1808 has been spawned to implement the interactive decomposition and restrict Operator CLI usage.
