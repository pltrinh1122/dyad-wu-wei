# WHY-1153: Falsification of kernel/ and bin/ Coexistence Thesis

## Context
When first inspecting the codebase layout, one might observe a potential overlap of responsibilities between the `bin/` directory and the `kernel/` (formerly `orchestrator/`) directory, as both contain executable entry points and lifecycle management scripts.

## The Coexistence Thesis (Falsified)
*Thesis:* The `bin/` and `kernel/` directories represent a confusing overlap of orchestrator tools that duplicate execution patterns and responsibilities.

## The Falsification
The thesis is false. `bin/` and `kernel/` represent a clean decoupling of execution boundaries and concerns:

1. **`bin/` (CLI Adapter Boundary)**
   - Contains pure, lightweight, non-interactive CLI entry point scripts.
   - Responsible for setting up the environment, parsing arguments, and routing commands.
   - Translates raw user/developer/process inputs into kernel operations.
   - Exclusively acts as the external interface wrapper layer.

2. **`kernel/` (Domain Orchestrator)**
   - Houses the core stateful, stage-aware domain orchestrators (e.g. `daemon_node.py`, `daemon_prompt.py`, `daemon_status.py`).
   - Implements the business logic, state machines, transaction controls, and invariant gates.
   - Completely independent of the specific CLI adapter interface wrapper details.

## Bedrock Principle
This decoupling ensures that the system logic remains robust and testable in isolation, while the entry points can be whitelisted or adapted safely under user permissions without exposing the core engine's modules directly.
