# WHY-0916: Status Report Progress Bars & Goal Ratios

## Classification
- **Type**: WHY (Decision Record)
- **ID**: WHY-0916
- **Author**: agent-ziran
- **Created**: 2026-05-28 (Node 917, Path 916)
- **Status**: Accepted

---

## 1. Context

To minimize Operator cognitive load (SG-0004), the `bin/status` CLI adapter must provide high-fidelity progress visualization. Previously, `bin/status` only showed a flat list of node counts or open PRs.

To harmonize with Wu-wei, the Operator should be able to instantly scan the status of all active Strategic Goals and see the exact progress/completion ratios of their prioritized paths in a visual format (e.g., ascii progress bars).

---

## 2. Options Considered

### Option A: Raw Node Counts
* **Thesis**: Keep it simple. Show active/completed node counts globally.
* **Antithesis**: Lacks granularity. Does not map progress back to active Strategic Goals.
* **Result**: Rejected.

### Option B: Visual Progress Bars mapped to Strategic Goals ✅ CHOSEN
* **Thesis**: Display each active Strategic Goal, its prioritized paths, and the exact percentage of completed paths using simple ascii progress bars (e.g. `[████░░░░] 50%`).
* **Result**: Accepted. This provides the Operator with immediate, structured, and low-energy system readout.

---

## 3. The Decision

Adopt **Option B: Visual Progress Bars mapped to Strategic Goals**.
We will update the status adapter to dynamically read `strategic_intent.yml`, calculate completed vs prioritized paths, and render visual progress indicators.
