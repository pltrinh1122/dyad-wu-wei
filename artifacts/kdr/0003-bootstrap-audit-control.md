# KDR-0003: Dynamic Control Ledgers for Bootstrap Audits

**Date:** 2026-05-16
**Status:** Accepted

## Context
As the Agent-Antigravity ecosystem matures, a formal audit process is required to ensure new repositories strictly comply with our Agentic Architecture (`artifacts/`, `skills/`, `orchestrator/`, `AGENT.md`, KDR structures) before transitioning into active Operations. We needed to determine what form the "Control Artifact" should take.

## Options Considered
1. **Static Control Artifact (`artifacts/audit_matrix.md`):** A persistent markdown file injected into every repository. The Agent checks boxes within the file. This creates permanent repository bloat with administrative files that are only used once.
2. **Dynamic Control Ledger (GH-Issue Template):** Host a master `BOOTSTRAP_AUDIT_TEMPLATE.md` in the meta-repository (`agent-antigravity`). When an Agent bootstraps a repo, it uses the template to create a GitHub Issue. The issue serves as the one-time, immutable transaction ledger for the audit.

## Decision
We decided to adopt the **Dynamic Control Ledger** approach (Option 2).

## Rationale
This perfectly aligns with our established governance (KDR-0001: Hybrid Epic-Ledger). GH-Issues are the mandated container for micro-state checklists (The Micro-Ledger). An audit is fundamentally an execution checklist. By hosting the master template in `agent-antigravity`, we maintain centralized governance over the audit standards, while keeping individual project repositories clean of single-use administrative files. The GH-Issue Audit becomes an immutable, auditable transaction log of the repository's initial compliance.
