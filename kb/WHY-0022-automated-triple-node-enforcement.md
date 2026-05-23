# WHY-0022: Automated Triple-Node Enforcement

## Context
While WHY-0020 established the Triple-Node Path Initialization Doctrine, enforcement was initially left to manual execution. This resulted in paths being created without the mandatory Align Probe, Plan Probe, and Reflect Activity, violating topological invariants. To eliminate manual omissions and guarantee compliance, we must programmatically enforce this trinity of children during path creation in the backlog manager.

## Decision
We will automate the creation of the mandatory Align Probe, Plan Probe, and Reflect Activity directly within the backlog manager during the execution of `backlog new path`.

### Implementation Rules
1. **Atomic Creation**: Creating a `path` node type via `daemon_backlog.py` will trigger the sequential creation of the Align Probe, Plan Probe, and Reflect Activity issues on GitHub.
2. **Dependency Chaining**:
   - The **Align Probe** is created first (no dependencies).
   - The **Plan Probe** is created second, with a dependency on the **Align Probe**'s issue ID.
   - The **Reflect Activity** is created third, with a dependency on the **Plan Probe**'s issue ID.
3. **Checklist Integration**: All three generated child nodes will be automatically added to the parent Path's `## Meta-Index` body section.
4. **Error Handling**: If any child issue creation fails during the sequence, the process must abort to prevent a partially initialized Path.

## Rationale
- **Zero Manual Overhead**: Prevents developers/agents from forgetting to initialize the Trinity of child nodes.
- **Topological Correctness**: Ensures the parent-child relationship and dependencies are established at creation time.
