# WHY-0004: Multi-Phase Node Planning

## 1. The Phenomenon
The SPAO loop fundamentally relies on `bin/node plan <id>` to construct the implementation contract before execution (`checkout`). However, the current architecture treats planning as an instantaneous, atomic event. 

In a true agentic workflow, planning is a multi-turn, multi-state phase. The agent must research the codebase, draft artifacts (`implementation_plan.md`), and potentially await Human-In-The-Loop (HITL) approval. During this protracted planning window, the GitHub Issue remains functionally unlocked. This creates a critical race condition where parallel agent threads might query the backlog and simultaneously initiate redundant planning cycles for the exact same Node.

## 2. Architectural Evolution
To preserve the WIP-N=1 invariant at the system level, the "Plan" phase must be decomposed into a stateful, two-step lock-and-commit protocol.

### 2.1. `bin/node plan-start <id>` (The Lock)
- **Mechanics**: Immediately applies the `status: in-progress` label to the GitHub Issue via the API.
- **Outcome**: The Node is instantly removed from the view of `bin/node sync` for all other parallel agents. The active agent safely assumes exclusive ownership of the Node during the multi-turn research and drafting process.

### 2.2. `bin/node plan-finish <id> <contract>` (The Commit)
- **Mechanics**: Finalizes the planning phase by uploading the compiled markdown contract to the GitHub Issue body.
- **Outcome**: The Node is now formally contracted and ready for `bin/node checkout`.

## 3. Impact on Checkout Mechanics
Currently, `bin/node checkout` enforces locking by verifying the *absence* of the `status: in-progress` label before applying it. With multi-phase planning, the Node is already locked during `plan-start`. 

Therefore, `checkout` must be refactored to verify that the active agent legitimately owns the locked Node (e.g., by checking the local agent context or safely assuming ownership if the current thread possesses the plan context).

## 4. Conclusion
Decomposing the `plan` command into `plan-start` and `plan-finish` fundamentally hardens the Antigravity infrastructure against parallel-planning race conditions. This strategy has been formally queued as an Activity for implementation in the core orchestrator.
