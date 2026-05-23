# WHY-0019: Ontological Refinement & Command Telemetry

## 1. Problem Statement
The current repository structure has evolved with several violations of the strict **Agentic Architecture** ontology defined in `WHAT-0001`. Specifically, the boundary between **CLI Adapters** (`bin/`), **Orchestrators** (`kernel/`), and **Skills** (`drivers/`) has blurred. This creates stateful logic in supposedly stateless skills and bypasses the orchestrator layer in CLI tools.

Additionally, our **Operational Health Telemetry** currently only tracks Node-level phases (SENSE/PLAN/ACT/REFLECT), leaving a blind spot for individual command executions and internal skill interactions.

## 2. Ontological Realignment
Per `WHAT-0001`, the execution flow must strictly follow:
`Operator/Agent` -> `bin/ (CLI)` -> `kernel/ (Manager/Workflow)` -> `drivers/ (Hands)`.

### 2.1 Backlog Consolidation
`bin/backlog` currently contains embedded Python logic that calls `drivers/github_client.py`. This logic (taxonomy resolution, templating) is stateful and stage-aware. It must be moved to a new `kernel/mgr_backlog.py`.

### 2.2 Skill Purity
`drivers/github_client.py` will be stripped of orchestration logic (`add_to_backlog`, `check_off_meta_index`) and reduced to pure, stateless wrappers around the `gh` CLI. `drivers/nba_evaluator.py`, which acts as a proxy for an orchestrator, will be removed.

## 3. Command-Level Telemetry
To achieve granular observability, we will implement **Command Telemetry**.

### 3.1 Metadata Schema
Every command execution will record:
- `cmd_name`: The name of the script or function.
- `level`: The ontological tier (`bin`, `kernel`, `skill`).
- `args`: Redacted command-line arguments.
- `duration`: Wall-clock execution time.
- `status`: Success/Failure.

### 3.2 Implementation Strategy: The @record_execution Decorator
We will implement a decorator in `TelemetryManager` to wrap entry points.
```python
@record_execution(level="kernel")
def main():
    ...
```
For shell-based CLI adapters in `bin/`, a lightweight Python call will be added to record the start/finish of the script.

## 4. Hierarchical Reporting
The `bin/telemetry report` tool will be updated to support filtering. This allows the operator to drill down into specific tiers (e.g., "Show me all skill-level bottlenecks") to identify which specific "Hands" are slowing down the system.
