# WHY-1069: Child Workspace Inheritance and Decoupling Policy

## Context
When instantiating a child workspace (Setup phase), we must define a clear policy for what configuration and validation rules are inherited from the parent engine, and when they must be decoupled to preserve local autonomy (Wu-wei).

## Decisions

### 1. What is Inherited (Baseline Physics)
Child workspaces inherit the parent engine's core mechanics and structural rules to maintain overall architectural coherence (Telos Coherence):
- **SPAOR Loop Stages & Autonomous Learning**: The transitions (plan-start, plan-finish, checkout, reflect) remain identical. **Falsification Insight**: To ensure the child accumulates its own domain learning, the Autonomous Learning Loop (epistemic knowledge accrual into the local `kb/` directory) is explicitly inherited as an inescapable baseline physical invariant of the Reflect phase.
- **Test Integrity**: Executing local test suites must verify code correctness before reflection.

### 2. What is Decoupled (Local Sovereignty)
To prevent parent-level administrative locks from stalling child workspace development (SG-0003):
- **Gate Decoupling**: The child workspace is exempt from parent-level remote PR gates (`WIP-N=1`). Multiple local child checkout branches or offline steps are permitted without waiting for remote PR merges.
- **Branch Topology Sovereignty**: Child workspaces are explicitly exempt from the parent engine's strict `node/<id>-<kebab-case>` branch naming constraint. They possess full autonomy to define their own integration branching structures. **Falsification Insight**: Rigid branch naming prevents a child from implementing distinct output versioning strategies (e.g., maintaining multiple long-lived `release/v1.x` branches to support decoupled mobile app versions in the market where the end-customer controls updates).
- **Tool Exemption**: Child scripts and tools may directly execute `git` or `gh` CLI commands to interact with their own domain repository, bypassing the parent's strict Abstraction Doctrine limits.
- **Bilateral Chat Protocol Bypass**: Conversational policing and templated chat formats are disabled inside child workspace terminals, allowing natural alignment on domain tasks.
- **Persona Gate Graceful Fallback**: If the child workspace does not possess its own custom `WHAT-0062` or `WHAT-0065` indices, strategic gates must gracefully bypass the persona check instead of failing-closed.
