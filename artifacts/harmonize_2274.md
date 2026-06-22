# Harmonize - Path: Formulate Elevation Invariants

## 1. Intent (WHY)
The repository uses a Two-Tier Backlog Abstraction where raw ideas sit in the `staging` queue (status: todo) and must be elevated into formal directed acyclic graphs (Paths) before execution. The process of structuring these raw ideas into formal DAGs is known as "Rigging" (via the `rub:` protocol). To prevent the systemic deadlock of raw, unrefined ideas bleeding into the execution floor and breaking the WIP-N=1 constraints, we need a formalized set of invariants that govern this elevation.

## 2. Technical Strategy (WHAT)
We will formulate the **Agentic Elevation Invariant** (or Rigging Invariant) that explicitly mandates:
1. **Raw Issue Quarantine**: Any issue tagged with `status: todo` is strictly prohibited from entering the `plan-start` phase or being assigned to the Wu-wei engine for autonomous execution until it is fully rigged.
2. **The Rigging Gate (The `rub:` Protocol)**: To elevate an issue into a Path, the Operator (Strategist/Architect) or the Agent (in a collaborative "rub" session) MUST formally convert it. This requires:
   - Expanding the raw intent into a structured `Goal`.
   - Creating the `## Meta-Index` DAG (Harmonize -> Plan -> Act -> Reflect nodes).
   - Removing the `status: todo` label and applying the `path` label.
3. **Execution Domain Separation**: The `staging` queue is the domain of the Operator's unformed Telos. The `path` queue is the domain of the Factory Floor (Actors/Agents). The `rub:` protocol is the sluice gate between them.

## 3. Scope
- Draft the specific invariant text for Agentic Elevation to be appended to the Meta-Rules (The Invariants) section of `DYAD.md` during the Act phase.
- Update `kb/` knowledge primitives to reflect the "Rigging" taxonomy and `rub:` protocol.
