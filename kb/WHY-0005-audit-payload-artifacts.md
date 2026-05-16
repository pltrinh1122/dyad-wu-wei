# WHY-0005: Audit Ledger vs. Audit Payload

**Date:** 2026-05-16
**Status:** Accepted

## Context
During the V2 Bootstrap Audit, the Operator proposed retaining formal audit reports as physical markdown files inside `artifacts/audit/` with informative, chronological names. Up to this point, the entire audit lived solely as a GitHub Issue checklist. 

## Options Considered
1. **Dynamic Control Ledger Only (Original Standard):** The audit is just a GH-Issue. Once closed, it acts as an immutable transaction in the cloud, but leaves no physical trace in the local file tree.
2. **Static Control Artifact Only:** The audit is just a local file (e.g., `audit_matrix.md`) that the Agent checks off. This clutters the repository and blurs the line between execution (GH-Issues) and memory (artifacts).
3. **Ledger + Payload Paradigm:** The GH-Issue is used to *execute* the audit (The Ledger), but the final result is written to a physical markdown file in `artifacts/audit/` (The Payload).

## Decision
We decided to adopt **Option 3: Ledger + Payload Paradigm**.

## Rationale
This decision respects all existing architectural pillars:
* **The Ledger (GH-Issue):** GH-Issues remain the exclusive domain for micro-state checklists, HITL constraints, and execution boundaries. 
* **The Payload (`artifacts/audit/`):** The `artifacts/` pillar is defined as the Agent's mutable state and *outputs*. An audit report is undeniably an output of diagnostic execution. 
* **Enterprise Traceability:** Storing detailed, chronologically named markdown files (e.g., `0001-bootstrap-v2-compliance.md`) provides immediate, offline-accessible visibility into the repository's health history, perfectly setting up future audits (Security, Performance, Dependency) as the repository scales.
