# WHY-0065: Decoupled Domain Registration — Architectural Decision Record

## Classification
- **Type**: WHY (Decision Record)
- **ID**: WHY-0065
- **Author**: agent-ziran
- **Created**: 2026-05-21 (Node 642, Path 640)
- **Status**: Accepted

---

## 1. Context — The Vertical Coupling Problem

In `WHAT-0062`, `agent-sg5` established a Hybrid Persona Domain Gate that maps **Strategic Goal IDs (SGs)** to **Persona IDs**. This design assumed that all Personas represent "Vertical" operational silos, where a single Persona maps 1-to-1 to a single Strategic Goal.

However, the creation of the `agent-ziran` persona (`WHAT-0064`) introduced a **Horizontal Domain** (the `a2ai` and `o2ai` interfaces, plus shared concurrency infrastructure). A horizontal domain structurally influences and impacts *multiple* SGs simultaneously. 

If we attempted to register `agent-ziran` within the existing `WHAT-0062` framework, we would be forced to claim an entire SG (e.g., SG-0004 or SG-0003), which would wrongly couple a horizontal software domain to a vertical strategic business metric. The operator explicitly commanded:
> "Domain registration is de-coupled from SG. For platform, we influence/impact multiple SG. We need to get very crisp with the ontology for domains and not tightly couple to SG."

---

## 2. Options Considered

### Option A — Modify WHAT-0062 to allow 1-to-Many Mappings
We could modify `WHAT-0062` so that a single SG can be owned by multiple Personas, or a Persona can own multiple SGs.
- **Flaw**: This breaks the strict accountability of vertical SGs. If SG-0001 is owned by both `agent-sg1` and `agent-ziran`, accountability is diffused. Furthermore, `agent-ziran` doesn't "own" SG-0001, it owns the *platform* that SG-0001 runs on. 

### Option B — GitHub Issue Labels (`domain:platform`)
We could bypass the ROM index entirely and use a GitHub label on the Path issue to denote domain ownership.
- **Flaw**: As established in `WHY-0062`, GitHub labels are mutable at runtime, lack a central auditable index, and fail open if omitted.

### Option C — Create a Path-to-Domain Overlay Index (WHAT-0065) ✅ CHOSEN
We leave `WHAT-0062` exactly as it is for vertical SGs. Instead, we introduce a new structural overlay (`WHAT-0065`) that maps specific **Path IDs** to a **Domain ID**, and maps the **Domain ID** to a **Persona**. 

When the alignment gate evaluates a transition:
1. It checks `WHAT-0065` first. If the Path is explicitly claimed by a Horizontal Domain, the gate authorizes based on the Domain Owner.
2. If the Path is *not* in `WHAT-0065`, it falls back to the SG owner defined in `WHAT-0062`.

---

## 3. The Decision

**Adopt Option C — The Path-to-Domain Overlay Index.**

By doing this, we achieve true decoupling. A Path can be categorized under SG-0004 (for strategic tracking), but its technical execution can be owned by `domain:platform` (and thus `agent-ziran`) because it is fundamentally an infrastructural change.

---

## 4. Falsification Criteria

This architectural decision is falsified and must be rolled back if:
1. A single Path ID needs to be simultaneously claimed by *multiple* different Horizontal Domains.
2. The manual maintenance of the `WHAT-0065` Path-to-Domain index creates unacceptable friction, necessitating a programmatic discovery method.
