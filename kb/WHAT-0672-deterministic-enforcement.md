# WHAT-0672: Deterministic Enforcement of System Rules

## Abstract
System rules must be enforced deterministically through hard-coded logic gates, not through LLM interpretation or prompt reminders. `agent-meta` defines the rules, and `agent-platform` builds the gates, but the environment itself enforces them via stateless, exception-throwing mechanics.

## The Physics of Enforcement
If a rule exists, it must be shifted entirely out of the LLM domain. An LLM agent should never have to manually step in to enforce hygiene, bounds, or workflow rules.

### Axioms of Deterministic Enforcement
1. **Hard Failure over Soft Warning**: If a process violates a rule, the engine MUST immediately crash or halt execution with a hard Python exception rather than warn the agent.
2. **Stateless Locks**: Concurrency rules (like WIP-N=1) must be enforced by atomic file locks, preventing simultaneous execution at the filesystem level.
3. **Mechanized Verification**: Invariants (e.g., Reflection) must be enforced by verifying the physical presence of artifacts (`artifacts/audit/retro-[ID].md`) rather than trusting conversational state.

## Example Gates
- **Concurrency Gate**: `mgr_node.py` throws `FlowTransaction failed: Active lock exists` if an agent attempts a second checkout.
- **Sluice Gate**: `node_lifecycle.py` blocks reflection completion if tests fail or if an execution crash occurred without a corresponding post-mortem file.

## Falsifiability
If an agent is found manually correcting another agent or itself to follow a system invariant (e.g., "Please remember to wait for the PR to merge"), this concept is falsified. The engine must be patched to enforce the invariant automatically via physics.
