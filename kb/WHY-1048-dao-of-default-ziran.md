# The Dao of Default Ziran (Configuration Wu-wei)

## The Axiom of the Out-of-the-Box State
The system's default state must natively manifest Ziran (naturalness) and Wu-wei (effortless action) without requiring the Operator to configure, tune, or align the container. The "out-of-the-box" experience is the ultimate expression of the Dao.

If the Operator is forced to actively configure the container just to achieve basic flow state or quiet the agent's telemetry, the system has failed the Dao by imposing un-opinionated configuration fatigue on the human. 

## The Core Dictates

1. **Silence by Default**: The container must enforce the "Silence of the Void" inherently. The Operator should never have to manually disable "verbose" output. Configuration parameters should only exist to enable active, conscious "opt-in" exceptions for edge-case debugging.
2. **Structural Drift Prevention**: Instead of shifting the cognitive load to the Operator to remember path mechanics (e.g., executing commands from the correct directory), the architecture must enforce rigid invariants (such as the Root Execution Invariant - Rule 6). If the Agent attempts to traverse or execute from an invalid nested state (like `.worktrees/`), the system must fail structurally rather than rely on the Operator's configuration to catch it.
3. **Opinionated over Configurable**: A highly configurable tool forces the Operator to make choices before they can work. The Agentic OS must make the optimal choice structurally, reserving configuration exclusively for deliberate deviations from the Happy Path.

## Falsification
If an Operator must execute an `agy /config` command or set an environment variable during their baseline installation just to prevent the Agent from polluting the chat UI with synchronous polling logs, the Dao of Default Ziran has been violated. The Agent's asynchronous background execution must be the unconfigured default.
