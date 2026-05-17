# KDR-0001: Hybrid Path-Ledger GH-Issue Governance

**Date:** 2026-05-16
**Status:** Accepted

## Context
During the orchestration of the `agent-travel` repository and the subsequent codification of the `INTAKE_BOOTSTRAP.md` standards, an issue arose regarding GitHub Issue lifecycle management. The strict `1:1 Node-to-Issue` rule (creating an issue and closing it immediately upon node completion) preserved immutability but resulted in a fragmented narrative and high "open/close" noise. The Operator requested an evaluation of approaches that preserve the audit-trail while allowing a cohesive index.

## Options Considered
1. **Discrete Node Transactions (Original):** 1 Node = 1 Issue. High noise, fragmented narrative.
2. **Unified Path Ledger:** 1 Master Goal = 1 Issue. The issue body is constantly overwritten. Creates a single thread but sacrifices micro-state historical immutability.
3. **Session Log:** 1 Session = 1 Issue. Breaks flow-state continuity if a session drops.
4. **Hybrid Path-Ledger:** A long-lived "Path" issue holds the overarching Meta-Index, while ephemeral "Node" issues hold the granular checklist and HITL constraints.

## Decision
We decided to adopt the **Hybrid Path-Ledger** approach. 

## Rationale
This approach perfectly maps our local filesystem architecture into the cloud-hosted GitHub UI:
* The Path Issue mirrors `artifacts/frontier_state.md` (Macro-State).
* The Node Issue mirrors `artifacts/task.md` (Micro-State).

It resolves the narrative fragmentation by providing a single Meta-Index (the Path), while simultaneously preserving strict, zero-scope-creep immutability (the discrete Node Issues). Future agents can use the Path Issue to instantly reconstruct the topological frontier.
