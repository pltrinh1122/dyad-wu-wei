# WHAT-0696: Temporal Immutability (The Lock-State Axiom)

## 1. Axiom Definition
The "Temporal Immutability" axiom dictates that the execution pipeline acts as an absolute lock on the progression of system state. When a Node is actively checked out (`WIP-N=1`), the files, rules, and domains it touches enter a locked temporal state. 

## 2. Invariants
1. **Out-of-Band Prohibition**: No entity (Operator, Agent, or Daemon) may execute out-of-band structural alterations on the `main` branch while a Node lock is active if those alterations overlap with the Node's domain.
2. **Rebase Protocol**: If an external force strictly necessitates a `main` update (e.g. an urgent patch from a separate subsystem), the active Node must either be aborted, or strictly rebased against the new temporal sequence. It cannot bypass sequence validation.
3. **Temporal Linearity**: The SPAOR loop assumes that the universe it spawned from (the commit hash at `checkout`) is the only valid predecessor to its reflection. If `main` diverges, the timeline must be reconciled before `reflect` completes.

## 3. The Why
Without Temporal Immutability, the rigid SPAOR pipelines can create divergent realities (merge conflicts) that require manual HTIL intervention, breaking the Wu-wei autonomic flow. By treating the active execution phase as an inviolable lock, we ensure that state transitions are always linear, deterministic, and free of collision-induced seizures.
