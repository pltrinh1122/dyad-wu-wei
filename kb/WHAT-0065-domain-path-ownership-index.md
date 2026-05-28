# WHAT-0065: Domain Path Ownership Index

<!-- MACHINE-PARSE CONTRACT
  Format:    GitHub Flavored Markdown pipe-delimited tables
  Consumers: kernel/daemon_strategic.py (578-B enforcement gate)
  Parse hint: The indices begin after the respective headings.
              Each data row (non-header, non-separator) is one authoritative record.
-->

## Classification
- **Type**: WHAT (Structural Fact)
- **ID**: WHAT-0065
- **Author**: agent-ziran
- **Created**: 2026-05-21 (Node 642, Path 640)
- **Depends on**: WHAT-0062
- **Decision record**: WHY-0065

---

## Purpose

This index establishes the **decoupled registration method for horizontal software domains**. While `WHAT-0062` maps vertical Strategic Goals (SGs) to Personas, `WHAT-0065` allows a Persona to own a generic "Domain" and then explicitly claim specific Path IDs under that Domain, regardless of which vertical SG the Path happens to be categorized under in `strategic_intent.yml`.

When the CLI harmonization gate evaluates a node transition, it MUST:
1. Check if the target node's parent Path ID is present in the **Path-to-Domain Index** below.
2. If present, resolve the Domain ID to the Owner Persona via the **Domain-to-Persona Index**.
3. If the executing `SPAO_PERSONA_ID` matches the Owner Persona, **ALLOW** the transition.
4. Only if the Path ID is *not* present in this index should the gate fall back to the vertical `WHAT-0062` SG mapping logic.

---

## Domain-to-Persona Index

| domain_id         | owner_persona   | description                                      |
|-------------------|-----------------|--------------------------------------------------|
| domain:platform   | agent-ziran  | Horizontal kernel, a2ai, o2ai, shared observability |

---

## Path-to-Domain Index

| path_id | domain_id         | status  | description                                              |
|---------|-------------------|---------|----------------------------------------------------------|
| 634     | domain:platform   | claimed | Refactor frontier_state for concurrent agent awareness   |
| 626     | domain:platform   | claimed | Implement Dynamic Agent Identity Resolution              |
| 622     | domain:platform   | claimed | Dynamic agent identity resolution and policy ledger harmonization |
| 605     | domain:platform   | claimed | Exclude Locked Nodes from NBA Path Continuation          |
| 588     | domain:platform   | claimed | 578-C: Integrate Persona-Aware Filtering into NBA Scorer |
| 587     | domain:platform   | claimed | Path 578-B: Implement Persona and Path Harmonization Gates in CLI Runtime |
| 640     | domain:platform   | claimed | Codify Platform Domain Path Ownership Index |
| 716     | domain:platform   | claimed | Remediate Synthesized Lexical Guards in Audit Config |
| 727     | domain:platform   | claimed | Prevent Overly Broad Synthesized Lexical Guards |
