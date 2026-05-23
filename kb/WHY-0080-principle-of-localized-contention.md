# WHY-0080: The Principle of Localized Contention

## Context
During the physical implementation of the Ziran Auditor (Node 764/765), an epistemic contradiction emerged: `HOW-0078` mandated the existence of `Node 763` (telemetry writers), but the active backlog and repository graph showed no physical trace of `Node 763`. 

This raised the fundamental question of **Contention Resolution**: Must we re-falsify every `WHAT` and `WHY` primitive every single time an Agent parses it to ensure structural integrity?

## The Principle
The Principle of Localized Contention dictates that **we only falsify the bedrock when the water physically hits a rock (Turbulence).**

If a knowledge primitive is functioning perfectly and generates no friction (Laminar flow), re-evaluating its philosophical validity upon every read induces an infinite regress of analysis paralysis, destroying inner-loop velocity.

### Core Tenets
1. **Trust by Default**: An Agent must assume historical KBs are mathematically valid representations of the Dao at the time of writing (Temporal Immutability).
2. **Falsify on Friction**: If an Agent encounters a physical impossibility (e.g., a file that is mandated but doesn't exist, a test that contradicts a rule), the Agent must declare *Localized Contention* and proactively falsify/update the offending rule.
3. **Automated Falsification**: The burden of falsification should be offloaded to autonomous physical systems (e.g., the Passive Ziran Auditor) rather than manual chat-based re-litigation.

## Architectural Application
When an Agent reads a `kb/` document that conflicts with the physical filesystem:
1. Do not halt execution.
2. Formulate a localized defensive strategy (e.g., defensive parsing).
3. Codify the falsification of the old rule as a physical mutation to the graph.
