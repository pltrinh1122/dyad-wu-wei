# WHY-0012: Configurable Operator Gates

## Date
2026-05-18

## Context
As the Antigravity architecture scales to encompass multiple orchestrator domains (`mgr_prompt`, `mgr_node`, `mgr_rt`), the system requires human-in-the-loop (HITL) safeguards to prevent autonomous mutations during critical operations. Previously, these gates (e.g., `tty_gate.require_operator_approval`) were hardcoded directly within the execution logic of each orchestrator. This monolithic approach lacked flexibility, tightly coupled the gating mechanism to specific workflows, and prevented clean domain exportation (e.g., sharing a domain with `agent-travel`).

Probe 179 evaluated the best architectural pattern to standardize and enforce these gates across the `mgr_*` ecosystem.

## Decision
1. **Configuration Schema:** Instead of centralizing all configurations in a monolithic `antigravity.yml`, we will implement domain-specific gate configurations (e.g., `{domain}-gates.yml` such as `prompt-gates.yml`, `node-gates.yml`). This ensures modularity and preserves domain portability.
2. **Implementation Pattern:** We have selected **Option C (Manager Base Class / OOP Approach)** as the systemic invariant over Option A (CLI bash wrappers) and Option B (Python Decorators). The system will introduce a `BaseManager` that formally encapsulates the execution flow, automatically enforcing the gates defined in the `{domain}-gates.yml` configuration prior to dispatching commands.

## Rationale
- **Portability:** Domain-specific YAML files allow each manager to be independently extracted and redeployed into other architectures without dragging along unrelated configuration definitions.
- **Systemic Invariant (Option C vs A/B):** The Operator explicitly requested a systemic invariant. Option A (CLI wrappers) is fragile because programmatic invocation of the Python modules bypasses the gate. Option B (Decorators) requires boilerplate on every function, leaving room for human error if a developer forgets the `@operator_gated` tag. Option C ensures that the gating mechanism is a fundamental property of the framework itself; the `BaseManager` owns the routing and inherently guards the underlying logic without requiring manual wiring on each leaf function.

## Consequences
- A `BaseManager` (or equivalent routing primitive) must be developed in the Orchestrator layer to standardize command execution.
- Existing orchestrators (`mgr_prompt`, `mgr_node`, `mgr_rt`) must be refactored to inherit from or interface with this new `BaseManager`.
- Hardcoded `require_operator_approval` calls will be eliminated from the orchestrators.
- A Path Node ("Path: Implement Configurable Operator Gates") will be instantiated to govern the execution of these refactoring Activities.
