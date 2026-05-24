# Retrospective: Terminology Correction regarding Workspace Engine

## Context & Correction
During Node 922 (Planning Phase), the Operator corrected a design terminology drift:
* **Drifted Term**: `Ziran Workspace App`
* **Correct Term**: `DZ-CIL Workspace`

The term `Ziran` represents the raw compute substrate, while `DZ-CIL` is the portable agentic Operating System and loop engine. Naming the workspace application the "Ziran Workspace App" confuses the substrate with the loop wrapper. We must strictly refer to the runtime engine as the **DZ-CIL Workspace**.

---

## Codified Insight
1. **Abstraction Alignment**: Terminological declarations must align strictly with the abstract framework layers.
2. **Semantic Ledger**: We must update `kb/semantic_ledger.yml` to deprecate `Ziran Workspace App` and mandate the use of `DZ-CIL Workspace`.
3. **Execution Cleanup**: In the subsequent implementation node (Node 923), we will ensure that all references to the workspace in codebase directories, templates, and documentation are replaced with the correct `DZ-CIL Workspace` terminology.
