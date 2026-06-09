# WHAT-1960: Daemon DAG Mutation & Sluice Gate Refinement Spec

## Intent
Enforce the Intake Context Boundary Invariant by permanently removing the `prompt:` queue as a communication channel for background daemons. Daemons must exclusively mutate the physical DAG or trigger silent, safe internal executions.

## Mechanism

### 1. Deprecate `inject_prompt` in `audit_daemon.py`
- Remove all references to `bin/prompt add` or `inject_prompt`.
- The daemon must never append to `artifacts/prompt_backlog.yml`.

### 2. Sluice Gate Refinement (Direct Execution)
- Modify `audit_daemon.py` to handle Sluice Gate Opened events by directly calling `subprocess.run(["./bin/node", "sync", "--remote-bypass"])` or equivalent local silent execution.
- Modify `kernel/daemon_node.py` (`sync_and_clean_node`) to remove the block that reads pending `[NOTIFICATION] Sluice Gate Opened` prompts from `prompt_backlog.yml` and clears them.
- *Constraint:* The sync operation triggered by the daemon must be mathematically safe and orthogonal to the Agent's active `WIP` branch.

### 3. Structural Incident Generation (Direct DAG Mutation)
- Modify `audit_daemon.py` to route all hygiene violations (e.g., Backlog Size > 30, Falsification rules triggered, Lexical Guard breaks) directly to the global DAG.
- Use `from drivers.issue_factory import IssueFactory` (or `kernel.daemon_backlog`) to silently create a `[BUG] Intake: <Alert>` issue in the backlog.
- Attach the traceback or violation context in the issue body.
- *Constraint:* Prevent infinite loop generation by checking if an identical open hygiene issue already exists in the backlog before creating a new one.

## Architectural Verification
This specification structurally decouples the Conversational Domain (`prompt:`) from the Structural Domain (DAG). The Agent will interact with the generated hygiene issues only when it hits `WIP=0` and automatically acquires the next top-scored NBA.
