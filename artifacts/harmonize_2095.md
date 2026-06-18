# Harmonize - Path: The Sub-Agent Gateway Controller (Ignition)

## 1. Intent Alignment
Per the Operator's directives for **Cognitive Offloading**, the Main Agent (Frontier) must be permanently elevated to act solely as the strategic kernel_daemon, decoupling high-level design thinking from low-level execution.
This Path implements the Sub-Agent Gateway Controller, which is the atomic component responsible for transitioning a Node from the kernel_daemon's execution domain into an active Sub-Agent execution domain.

## 2. Technical Design & Orthogonality
To guarantee atomicity and orthogonality, the implementation is decomposed:
1. **Concurrent State Binding (Completed):** Path #2090 established the concurrent lock ledger (`active_agents`), ensuring the system can track locks held by multiple personas.
2. **Gateway Controller CLI (This Path):** We will build `bin/node dispatch <issue_id> <persona>`. This command will:
   - Verify the kernel_daemon's readiness.
   - Update the concurrent ledger, formally binding the Node to the target sub-agent persona.
   - Invoke the background sub-agent process.
   - Ensure the kernel_daemon respects True Dormancy (yielding execution) while the sub-agent executes.

## 3. Structural Pre-Requisites & Post-Requisites
**Pre-Requisite:** Concurrent lock ledger materialization (Path #2090) is verified.
**Post-Requisite:** Execution Exhaust & Telemetry Partitioning (Path #2099) must provide telemetry isolation so sub-agents do not corrupt global logging contexts.

## 4. Plan Phase
The upcoming Plan node will define the precise CLI arguments, telemetry integration, and internal daemon locking sequence required to execute the `dispatch` gateway.
