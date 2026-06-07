# WHAT-0676: The Void of the Metasystem (Agnostic Payload Execution)

## Abstract
The Metasystem (the SPAO execution loop and the CLI) operates in "The Void." It is an agnostic infrastructure layer that executes payloads without understanding their semantics. Whether an agent is planning a roadmap, writing code, or documenting a philosophy, the engine must execute the identical state transitions (`status -> plan-start -> checkout -> act -> reflect`).

## The Physics of The Void
1. **Semantic Ignorance**: The execution engine does not care about the contents of the payload. It only cares about the metadata and the invariants.
2. **Identical State Machine**: The state transitions remain the same regardless of what the user is building. There is no special "documentation mode" or "code refactoring mode" inside the engine.
3. **Decoupled Geometry**: Intelligence and domain-specific knowledge are contained entirely within the `kb/` documents and prompt histories (the payload), not hard-coded into the engine Python scripts (the metasystem).

## Falsifiability
If the engine (`node_lifecycle.py`, `daemon_node.py`) contains logic that inspects the actual content of a user's repository (e.g., branching behavior based on whether a node is a "code task" vs a "docs task"), this principle is falsified. The engine must remain perfectly agnostic to the payload.
