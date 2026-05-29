# WHAT-1398: Mechanism Catalog - Generate Family

## Concept
The Dyad Practice dictates that the `Generate` family of mechanisms is used to break out of local maxima and create novel candidate hypotheses. The Agent and Operator must deliberately employ these techniques to expand the frontier before narrowing it via `Validate` mechanisms.

## Mechanisms
1. **Composition**: The act of combining two previously orthogonal or unrelated concepts within the system to produce a novel solution. It leverages the existing ontology to synthesize new capabilities.
2. **Elicitation**: Proactively querying the environment, the Operator, or external APIs to surface latent context that is not immediately visible in the active worktree. It is the active pursuit of the unknown unknowns.
3. **Reframing**: Temporarily abandoning the current abstraction layer (e.g., "how do we fix this bug?") to view the problem from a structurally different level (e.g., "does this component even need to exist?"). 

## Structural Requirements
- During the `Plan` phase, the Dyad MUST leverage at least one `Generate` mechanism to ensure the proposed Node Contract is not trivially derivative.
- Generative mechanisms must always be paired with a Validation mechanism before merging.
