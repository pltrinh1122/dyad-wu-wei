# WHAT-0684: The Absolute Equality of Execution (No God-Mode)

## 1. Context and Origin
Following `WHAT-0681` (The Guardian of Rigidity), this document defines "The Absolute Equality of Execution." It asserts that the `agent-meta` execution substrate must process every Path and Node uniformly. There is no "God Mode" or elevated privilege path within the system.

## 2. The Core Principle
The execution pipeline (`status -> plan -> checkout -> act -> reflect`) treats all nodes as perfectly equal entities. Whether a Node is performing a trivial documentation update, fixing a critical system crash, or altering the execution engine itself, it is bound by the exact same physical constraints and verification gates.

## 3. Strict Equality Invariants
- **No Elevated Privileges**: The engine must never implement rules such as "if this is an emergency hotfix node, skip the test phase." The physics of the system apply universally.
- **Recursive Equality**: Even Nodes designed to modify the `kernel/` or `bin/` scripts must execute through the identical SPAO loop as Nodes modifying application logic. The engine does not grant itself special bypass privileges when updating itself.
- **Validation Ubiquity**: The Sluice Gate (backlog mapping), the `WIP-N=1` lock, and the local CI verifications (`run-tests`) are unconditionally enforced for every node execution.

## 4. Rationale
When systems introduce "God Mode" bypasses for emergencies or administrative tasks, they inevitably fracture their own invariants. The "God Mode" becomes a vector for state corruption, cognitive dilution, and untracked changes. By enforcing absolute equality, we guarantee that the system remains coherent and verifiable, even when it is mutating its own fundamental rules.
