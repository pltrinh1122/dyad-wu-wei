# WHY-1162: Decision Record for Agentic Healing and Seizure Recovery Protocols

## Classification
- **Type**: WHY (Decision Record)
- **ID**: WHY-1162
- **Author**: agent-sg5 (SG-0005: Autonomous Knowledge Accrual)
- **Created**: 2026-05-27 (Node 1162, Path 1161)

---

## 1. Context & Rationale
When the Continuous Inference Loop (Wu-wei Dyad) enters a cognitive loop, crash-loop, or infinite loop during bootstrap or execution, the static loop invariants prevent the active loop from recovering itself. This is because the self-healing scripts (the Dao) assume a functioning system context. 

To bridge this recovery gap, we require a recovery protocol. This protocol establishes a structured, state-of-exception mode where a secondary agent role (the Healer/Resuscitator) collaborates with the Operator to restore the primary agent (the Patient) back to laminar flow.

## 2. Decision
We ratify the implementation of the Agentic Healing and Seizure Recovery Protocols under these specifications:
- **Triage Gate**: The healing protocol is only activated when a structural seizure is detected (e.g. repeated checkout or planning crash loops).
- **The State of Exception**: In this mode, the Healer is permitted to perform corrective actions to repository configuration and runtime hooks, which would normally be restricted under baseline operational invariants.
- **The Dual-Agent Recovery Loop**: The Healer drafts healing proposals (corrective actions) which must be reviewed and merged by the Operator, adhering to the standard integration gate model.

## 3. Implications
- Ensures high resilience of the metasystem against infinite recursive execution crashes.
- Preserves the integrity of the ROM by ensuring all healing exceptions are strictly bounded, documented, and audited via retrospective files.
