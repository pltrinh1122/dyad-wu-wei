# WHY-0054: Glossary & Terminology Alignment Decisions

> [!NOTE]
> This decision record codifies the philosophical and technical alignment for Path 515 ("QA the GLOSSARY against repository artifacts") based on operator guidance and agentic consistency invariants.

---

## 1. Rationale & Collaborative Grounding

Terminology drift across multi-session agentic operations introduces cognitive friction for both the operator and the models. A single, authoritative glossary is critical to maintain North Star alignment. This path audits the internal coherence of `kb/GLOSSARY.md` and enforces consistent terminology usage across the repository.

---

## 2. Target Scope of Artifacts

To prevent over-auditing of non-governance files, the audit is strictly bound to the following core system artifacts:
* **Knowledge Base Laws**: All files under `kb/` (including `WHAT-*`, `WHY-*`, `HOW-*` primitives).
* **System Guidelines**: `GEMINI.md` and `README.md`.
* **State Tracking Logs**: `artifacts/frontier_state.md` and `artifacts/strategic_intent.yml`.
* **System Templates**: All files under `kb/templates/`.

---

## 3. Prioritization & Strategic Alignment

Path 515 is prioritized under **SG-0005 (Autonomous Knowledge Accrual)** because `kb/GLOSSARY.md` serves as a core Read-Only Memory (ROM) knowledge primitive. Ensuring its coherence directly impacts the agent's ability to codify and recall operational lessons without repeating semantic errors.

---

## 4. Treatment of Deprecated Terms

Legacy terms such as **Epic** and **Spike** must be marked as deprecated in `kb/GLOSSARY.md` rather than completely deleted, ensuring historical traceability for old issues, PRs, and retrospective reports.
* Historical logs (e.g. `artifacts/retrospective_path_404_461.md`) will preserve these terms for audit logging but will be exempt from modern lexical checks via `tests/test_lexical_guard.py`.

---

## 5. Alternatives to "Spike" (Exploratory Tasks)

To support "quick and dirty" exploratory codebase mutations without violating Invariant 5 (Probes are non-mutating), we define a tiered alternative to "Spike" that aligns with our existing taxonomy:

| Deprecated Term | Proposed Alternative | Type | Definition / Scope |
| :--- | :--- | :--- | :--- |
| **Spike Path** | **Seed Path** | Non-Terminal | A minimally scoped, non-production Path designed for rapid prototyping. Its goal is to resolve technical feasibility or design uncertainty before production code is written. |
| **Spike Node** | **Exploratory Activity** | Terminal | An Activity node within a **Seed Path** that executes temporary, "quick-and-dirty" codebase modifications. It is explicitly expected to be superseded or refactored holistically by a follow-on production Path. |

### Minimum Scope Assumption
All Paths in the repository should be assumed to be minimally scoped. A complex feature should not be solved in one massive path. Instead, it must be split into:
1. A **Seed Path** (to build the exploratory prototype and gather learnings).
2. A **Production/Hardening Path** (to implement the complete, clean, tested feature).

---

## 6. Surfaced Glossary Gaps

The consistency audit identified several key metasystem terms used across the codebase that are missing from `kb/GLOSSARY.md`. We will plug these gaps by adding them to the glossary:
* **Three-Loop Governance**: The framework separating `loop:spao` (non-mutating) and `loop:sdlc` (mutating) lifecycles.
* **Workspace Routing**: The process of checking out branches to specific directories based on loop class (e.g. `.worktrees/spao/` or `.worktrees/sdlc/`).
* **Seed Path**: As defined above.
* **Exploratory Activity**: As defined above.
* **NBA Scorer (Next-Best-Action Scorer)**: The algorithmic scoring engine evaluating prioritized backlog paths.
* **Dual-Probe Initialization**: The mandatory pattern requiring an Align Probe and a Plan Probe before starting functional Activities on a Path.
