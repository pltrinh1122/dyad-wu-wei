# Emergent Orthogonality of Agent Scopes

## Context
The system previously allowed for 'Global User Prompts' configured at the IDE/Client level (e.g., Antigravity global settings). However, as we scale the Dao-Ziran continuous inference loop across multiple personas (e.g., `agent-sg1`, `agent-sg5`, `dyad-wu-wei`, `dyad-steward`), a single global system prompt introduces a monolithic dependency that dilutes the specialized focus of each agent.

## The Problem
If an Operator injects rules at the global Antigravity level, those rules pollute the context of all agents indiscriminately. This violates the principle of **Emergent Orthogonality**:
Orthogonality is not a top-down dictate from the global meta-system; it is an emergent property of a decentralized contract system. Each agent must define its own scope, invariants, and physics locally through its own `GEMINI.md` and `DYAD.md`.

## The Solution: Deprecation of Global Context
To enforce strict boundary isolation, we formalize the following architectural invariants:
1. **Abolition of Global UI Prompts**: The Operator must clear out all global/IDE-level system prompts. The physical reality of the agent is dictated *entirely* by the repository's local `GEMINI.md`.
2. **Local Governance**: Each dyad/agent repository maintains its own `GEMINI.md` which serves as the ultimate `RULES_FILE`. 
3. **Decentralized Manifests**: The Meta domain provides the schema (the SPAO loop, the `WHAT-xxxx.md` manifest structures), but the individual agents own their coordinates and claims within the system.

By stripping the global settings, we force the system to rely exclusively on the `dyad-wu-wei` local substrate, guaranteeing that our agentic behaviors are fully codified, version-controlled, and orthogonally separated from other dyad instantiations.
