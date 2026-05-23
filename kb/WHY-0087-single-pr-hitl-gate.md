# WHY-0087: Transition to Single-PR-Gate Governance

## Context
As the Dao-Ziran Continuous Inference Loop (DZ-CIL) has evolved, the repository has accumulated multiple Human-in-the-Loop (HITL) checkpoints to safeguard execution. These include plan reviews in chat, local interactive TTY prompts, and strategic path-alignment checks. 

While originally designed to protect the system's invariants, these intermediate checkpoints create substantial coordination overhead, block autonomous cascading flow, and force unnecessary dialogue turns in the chat interface.

## Decision
We establish the **Single-PR-Gate Governance Model** as the primary integration and containment primitive for the metasystem. We formally deprecate all intermediate manual and local gates. The Pull Request (PR) merge event on GitHub is now the **only** non-negotiable hard block in the system.

## Rationale

### 1. NS-0001 (Partnership Synergy)
Transitioning to a single-gate model shifts the Operator from a tactical gatekeeper (managing intermediate planning blocks and chat dialogue loops) to a strategic manager (reviewing the final code, documentation, and test results in the PR). This maximizes the Agent's execution autonomy and velocity while preserving Operator containment.

### 2. Wu-wei (Lowest Energy)
Consolidating all validation gates into the cloud PR merge removes conversational context-switching noise and minimizes total dyad energy. The Agent can transition from Sense to Plan and Act autonomously without halting. Safety is maintained locally via the offline test harness (`./bin/run-tests`) which must pass before reflection.

### 3. Ziran (Coherence with Substrate)
As defined in `WHY-0069`, the Pull Request is the native physical law of the GitHub host environment. Aligning our sole integration gate with this native primitive is more natural and robust than maintaining brittle local locks or conversational gates.

## Deprecation Scope
*   **Strategic Prioritized Path Check**: The hard block in `verify_node_transition_allowed` (blocking execution of non-prioritized paths) is deprecated, transitioning to a warning rather than a fatal exception.
*   **Conversational Plan Reviews**: The requirement to halt in chat for intermediate plan approval is abolished. The Agent is authorized to autonomously transition from Plan to Act once a Node Contract is locked.
*   **TTY Prompts**: Interactive TTY gates are deprecated where automated execution pathways exist.
