# WHY-0004: The Audit Remediation Threshold

**Date:** 2026-05-16
**Status:** Accepted

## Context
During the Formal Bootstrap Self-Audit of the meta-repository, a failure was detected: historical GH-Issues were not properly mapped to the Path Meta-Index. The Agent remediated the missing links *during* the audit and logged the fix. This sparked an evaluation: Should an Audit be strictly "Report Only" (halting on failure and spawning a new GH-Issue for the fix), or "Audit + Remediate" (fixing the problem as a single atomic step within the audit ledger)?

## Options Considered
1. **"Audit" (Report Only):** Perfect scope protection and traceability, but introduces extremely high friction for trivial fixes (e.g., spawning an entire SPAO cycle to fix a missing hyperlink).
2. **"Audit + Remediate" (Atomic Step):** High velocity, but risks "Masked Mutations" where massive architectural rewrites are hidden inside a benignly named "Audit" GH-Issue.
3. **The Complexity Threshold:** A hybrid approach where trivial fixes are permitted inline, but complex fixes mandate a spin-out node.

## Decision
We decided to adopt **Option 3: The Complexity Threshold**.

## Rationale
Agentic Architecture requires a balance of velocity and strict traceability. If a compliance failure is trivial, deterministic, and requires no architectural reasoning (e.g., creating a missing folder, updating a markdown list), the Agent may perform an "Audit + Remediate" within the same node, logging the fix in the comments. This achieves the goal of compliance instantly. However, if the compliance failure requires creating new logic, altering core primitives, or crossing the Materialization Boundary, the Agent must treat the audit as "Report Only." It must halt, flag the failure, and spawn a dedicated Remediation Node (GH-Issue). This prevents masked mutations and ensures all major logic changes have their own discrete contract of execution.
