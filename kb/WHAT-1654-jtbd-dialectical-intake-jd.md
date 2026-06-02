# Requirements-Discovery Discipline (JTBD & Dialectical Falsification)

**Status:** Proposed (Node 1658)  
**Parent:** Path 1654  
**Strategic Goal:** SG-0005 (Autonomous Knowledge Accrual)  
**Lineage:** Borrowing epistemic framing from `dyad-bond` (The Dyad Practice Commons).

## 1. The Core Precept: The Pre-SPAOR Boundary
The most critical mechanism of this discipline is recognizing the difference between **Requirements-Discovery** and **Execution-Discovery**. 
*   **Requirements-Discovery** is the pure epistemic shaping of intent. It exists in the void *before* materialization. It is a strictly dyadic cycle between Operator and Agent.
*   **Execution-Discovery** is materialized exploration (e.g., prototyping, reading a codebase) that requires the strict `SPAOR` execution loop, Git worktrees, and Node locks.

**The Rule:** When engaged in Requirements-Discovery, the Agent MUST NOT invoke the SPAOR loop (no `bin/backlog`, no `plan-start`, no branch checkouts). The Agent operates purely as a conversational architect in the signaling layer.

## 2. The JTBD Formulation Phase
The foundation of Requirements-Discovery is identifying the fundamental "Job To Be Done" independent of any proposed technical solution.
*   **Intake:** The Operator provides a raw intent, pain point, or goal.
*   **Expansion:** The Agent explicitly helps the Operator strip away implementation assumptions to isolate the core problem. 

## 3. The Dialectical Falsification Phase
Drawing directly from `dyad-bond`'s tenet of *genuine falsification*, every proposal must survive structural dissent before it is accepted as a valid requirement.
*   **Thesis:** The initial assumption, requirement, or proposed constraint provided during intake.
*   **Antithesis:** The Agent aggressively stress-tests the thesis using the Dyad-UI as a load-bearing, falsifiable medium. *Is this a true structural constraint (physics of the system) or merely an iatrogenic/artificial constraint? Does it violate the North Star of autonomous inferencing?*
*   **Synthesis:** The hardened requirement that strips away false constraints. The result is a rigorous "Problem vs. Constraint" framing.

## 4. The Discernment Gate & Materialization (Handoff)
The Discernment Gate is the final evaluation step of Intake:
*   **Ambiguous or Conceptual:** If the JTBD introduces new philosophical primitives or the thesis has not yet survived an antithesis, the Agent must halt autonomous execution and initiate a co-development cycle.
*   **Fully Synthesized (The Handoff):** Once the problem statement is undeniable and its true constraints are established, the dyadic cycle terminates. The Agent injects the hardened JTBD into the execution pipeline (e.g., `prompt_backlog.yml` or `bin/backlog`), formally crossing the boundary into the autonomous SPAOR loop.
