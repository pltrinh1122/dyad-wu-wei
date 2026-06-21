# WHAT-0704: The Decoupled Geometry of the State Machine (Meta vs Platform)

## 1. Context and Origin
Derived from Path 704 during the systematization of the Rigidity Guard invariants. This document establishes the strict orthogonal boundary between the Metasystem (the engine, the logic gates, the SPAO execution loop) and the Platform (the context, the domain tasks, the features being built).

## 2. Core Directive
The state machine (SPAO loop: Sense -> Plan -> Act -> Observe -> Reflect) MUST remain completely agnostic to the payload it executes. The structural geometry of the engine must be decoupled from the content of the tasks.

## 3. Strict Invariants

### 3.1. Engine Agnosticism
The `./bin/node` execution framework (and its underlying daemons) must operate on abstract Nodes, Paths, and Strategic Goals. It must not contain hardcoded logic specific to the current domain or the target application being built by the Dyad.

### 3.2. Payload Isolation
The "Why" and "What" of a task reside exclusively in the Backlog (`issues`), Knowledge Base (`kb/`), and Universal Context (`DYAD.md`, `GEMINI.md`). The "How" resides in the execution. The engine only orchestrates the lock, context ingestion, execution space, and reflection commit.

### 3.3. Prevent Structural Entanglement
Any attempt to modify the `bin/` scripts, `drivers/`, or `tests/` must be treated as a Metasystem change and isolated from Platform feature work. A Node cannot simultaneously implement a Platform feature and alter the core logic gates of the engine.

## 4. Remediation of Violations
If a Node conflates Meta and Platform context (e.g., modifying the SPAO runner to accommodate a specific bug fix in the target app), the execution MUST be aborted, and the tasks must be split into orthogonal Nodes.
