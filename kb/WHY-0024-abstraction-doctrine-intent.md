# WHY-0024: Abstraction Doctrine Intent

## Context & Rationale
Currently, the codebase executes raw `git` and `gh` shell commands across several modules (e.g. `flow_state_manager.py`, `daemon_backlog.py`, etc.). Invoking system commands directly in bash wrapper subprocesses has several downsides:
- **Portability**: Dependent on local binaries of `git` and `gh` CLI being correctly installed and authenticated.
- **Safety**: Risk of shell argument injections or unhandled process errors.
- **Aesthetics**: Raw subprocess calls lack structured data types, forcing string splitting and scraping.

## Architectural Decision
We establish the **Abstraction Doctrine**:
- No raw shell command executions of `git` or `gh` shall be invoked by any scripts or agents.
- Instead, Git/GitHub integrations must use native Python API abstractions.
- These abstractions are structured per-concept:
  - **Backlog & Path**: Consolidate backlog and path management under a single public class interface to simplify work registration, state transitions, and child tracking.
  - **Node**: Treat node operations (planning, checking out, and reflecting) as internal primitives that must only be called by the consolidated backlog/path layer and admin CLI scripts.
