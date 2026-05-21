# WHY-0063: Persona-Aware Soft-Routing in NBA Evaluator

## Context
Path 578 decomposes the domain collision problem into static ownership (SG-0005), soft-routing (SG-0001), and hard-gating (SG-0002).
The Next-Best-Action (NBA) evaluator must pre-filter and score mismatched paths as 0 based on the active persona, ensuring soft-routing away from unauthorized paths before hitting the hard-gate.

## Decision
We introduce a `c_persona` modifier in the NBA Scorer that cross-references the running `SPAO_PERSONA_ID` with the `WHAT-0062` index. 
To resolve DAG execution deadlocks during parallel agent bootstrapping, if `WHAT-0062` does not exist, `c_persona` defaults to `1.0` (fail-open). This ensures offline velocity and decoupled orthogonal execution between Agent-SG1 and Agent-SG5.

## Consequences
- **Positive:** Agents are naturally routed toward their assigned Strategic Goals.
- **Positive:** Reduces wasted cycles and PR collisions by preventing agents from attempting to lock paths they are not authorized for.
- **Positive:** Fails open gracefully during system bootstrapping to maintain velocity.
