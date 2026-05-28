# WHAT-0018: The Telemetry Primitive

The **Telemetry** primitive is a first-class **Meta-Primitive** in the Antigravity ontology. While a **Node** represents a unit of work, a **Telemetry** event represents a unit of *observation* of that work.

## 1. Role and Purpose
Telemetry provides the "Nervous System" for the agentic environment. It enables high-fidelity observability into the **SPAO Loop** (Temporal Dimension) to identify operational bottlenecks, measure agentic efficiency, and provide the data required for autonomous self-optimization.

## 2. Anatomical Structure
As a first-class primitive, Telemetry is composed of three layers:

### 2.1 The Ledger (`artifacts/telemetry.jsonl`)
An append-only, structured ledger that persists every significant state transition and event. Each entry is a discrete **Observation Point**.

### 2.2 The Kernel_Daemon (`kernel/daemon_telemetry.py`)
The stateful manager that owns the Telemetry logic. It is responsible for:
- **Ingestion**: Recording events from other kernel_daemons (e.g., `daemon_node`).
- **Synthesis**: Aggregating raw observations into high-level **Health Metrics**.
- **Alerting**: Identifying "Loop Stalls" or "Ambiguity Bottlenecks".

### 2.3 The Adapter (`bin/telemetry`)
The CLI interface for the operator and agent to interact with the telemetry state.

## 3. The Observation Schema
Every Telemetry event must adhere to the following minimal schema:
- `timestamp`: ISO-8601 (microsecond precision).
- `node_id`: The ID of the Node being observed (if applicable).
- `path_id`: The ID of the Path being observed (if applicable).
- `stage`: The SPAO stage (`SENSE`, `PLAN`, `ACT`, `OBSERVE`, `REFLECT`).
- `event`: The specific transition (e.g., `START`, `FINISH`, `FAIL`).
- `metadata`: A dictionary of context-specific data (e.g., commit hash, tool call count).

## 4. Operational Invariants
1. **The Transparency Invariant**: Telemetry recording must be non-blocking and silent during standard operations.
2. **The Integrity Invariant**: The telemetry ledger must never be manually edited; it is an immutable record of system performance.
3. **The Lifecycle Invariant**: Every `TerminalNode` transition must be accompanied by a corresponding Telemetry event.
