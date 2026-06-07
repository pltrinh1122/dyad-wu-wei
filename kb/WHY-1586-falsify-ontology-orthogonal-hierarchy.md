# WHY-1586: Falsification of Ontology Orthogonal Hierarchy

## 1. The Falsified Thesis
The thesis proposed that child projects and the SPAO Engine (`dyad-wu-wei`) could exist as orthogonal peers or independent repositories mounted as submodules in a flat directory hierarchy.

## 2. Evidence of Failure
When the Engine and the Child project are decoupled orthogonally, the Agent's context scope is immediately lobotomized. The LLM Agent can only reliably parse directives, invariants, and systemic goals if they are physically present in the active working directory root.

Orthogonal workspaces meant the Agent lost access to `GEMINI.md`, `AGENT.md`, and the `kb/` primitives. This led to systemic regressions, invariant breaches, and loss of the Dao inheritance during agent instantiations.

## 3. The Re-Grounding
As established in `WHY-0921` and reaffirmed here, the Dyad must strictly adhere to the **Model 1 Dual-Context Workspace Architecture**:
- The Engine (`dyad-wu-wei`) MUST be the Root Parent repository and the primary IDE working directory.
- The target child project MUST be nested inside the parent at `./.workspace/`.
- The Engine MUST NEVER be mounted as an orthogonal peer.

## 4. Final Disposition
The orthogonal hierarchy for ontology workspaces is formally falsified. The nested Model 1 architecture is the sole valid topology for the Frontier Dyad.
