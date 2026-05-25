# WHY-1055: Empirical Assessment Plan for Workspace Installation and Setup (Model 1 Redirection)

## Context
The Metasystem has transitioned towards supporting sovereign workspace isolation (Model 1 Redirection) via the `SPAO_WORKSPACE_DIR` environment variable. This allows agents to operate in child workspaces where they inherit core mechanics from the parent engine while maintaining sovereignty over domain-specific logic, backlogs, and execution rules. To validate the stability and safety of this architecture, an empirical assessment is required.

## Empirical Test Plan Objectives

The assessment will validate the system against the following core criteria defined in the Workspace rules:

1. **Rule Inheritance & Merge Mechanics**:
   - Verify that the child workspace dynamically merges the parent `GEMINI.md` core loop invariants with the child's `GEMINI.md` local domain overrides upon initialization.

2. **Domain Sovereignty (Gate Decoupling)**:
   - Verify that the child workspace's inner execution loop is fully decoupled from the parent's `WIP-N=1` HTIL PR merge gates.
   - Confirm that local offline checkout, testing, and reflection can cycle continuously without blocking on upstream PR approvals.

3. **Tool Execution Sovereignty**:
   - Verify that within the boundaries of `SPAO_WORKSPACE_DIR`, the agent is permitted to execute standard version control tools (e.g., `git` or `gh` CLI) directly, bypassing the strict parent Abstraction Doctrine wrappers.

4. **Bootstrapping Invariant**:
   - Verify that upon initial workspace instantiation, the agent successfully captures the unformed Operator intent and codifies it within the child's `artifacts/strategic_intent.yml`.

5. **Dynamic Persona Decoupling Invariant**:
   - Verify that when `SPAO_WORKSPACE_DIR` is active, the system's strategic transition gates (`_verify_persona`) correctly load the child workspace's indices, bypassing parent gate failures gracefully if the child indices are uninitialized.

## Execution Strategy

The empirical assessment will be executed sequentially through the following discrete Activity Nodes under Path 1054:

- **Node 1**: Initialize an isolated mock `SPAO_WORKSPACE_DIR` environment and verify the Bootstrapping Invariant (generation of `artifacts/strategic_intent.yml`).
- **Node 2**: Execute a localized SPAO loop (Plan -> Act -> Observe -> Reflect) within the child workspace to verify Gate Decoupling and Tool Execution Sovereignty.
- **Node 3**: Tear down the isolated workspace, audit the telemetry for parent-level bleed, and synthesize findings into an Epistemic Retrospective (`retro-<id>.md` or `WHY-` document).

## Next Steps
Upon reflection of this Discovery Node, the DAG will advance to the first Activity Node to physically initialize the test environment.
