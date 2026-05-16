# KDR-0002: Key Decision Records (KDR) as Philosophical Memory

**Date:** 2026-05-16
**Status:** Accepted

## Context
Following the codification of the "Materialization Boundary" (the rules defining when an Agent may converse in a Side-Bar versus when it must demand a GH-Issue Plan), a critical gap was identified. While GH-Issues excellently capture *execution* (Scope, Acceptance Criteria, HITL Constraints), they do not capture the *philosophical rationale* generated during Side-Bar brainstorming. If a Side-Bar conversation resulted in a major decision, the context behind the decision was lost when the ephemeral chat session ended.

## Options Considered
1. **Status Quo (Lossy Side-Bars):** Accept that rationale is lost and only execution is preserved in GH-Issues.
2. **Verbose GH-Issues:** Force the Agent to dump the entire Side-Bar conversation transcript into the GH-Issue body. This leads to massive, unreadable execution ledgers.
3. **Key Decision Records (KDR):** Introduce an `artifacts/kdr/` directory to hold distinct Markdown files capturing context, options, and decisions.

## Decision
We decided to implement the **Key Decision Records (KDR)** Knowledge Base.

## Rationale
Creating a distinct `artifacts/kdr/` directory separates "Philosophical Memory" from "Execution Ledgers." 
* It ensures GH-Issues remain crisp, actionable contracts.
* It preserves the *"why"* permanently in the repository.
* The structure is highly indexable for Retrieval-Augmented Generation (RAG). Future Agents can instantly query `artifacts/kdr/` to understand why past architectural choices were made without parsing noisy GH-Issue comment threads. 

The Materialization Boundary is updated to mandate a "KDR Handoff": if a Side-Bar reaches an architectural conclusion, the Agent must draft a KDR before drafting the GH-Issue execution plan.
