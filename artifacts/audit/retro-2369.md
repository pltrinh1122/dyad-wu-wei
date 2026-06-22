# Frontier Dyad — Practice Reflection — 2026-06-22 — Node 2369

## 1. CONTINUE — what worked
**Narrative (Operator):** The orthogonal matrix of Status x Structure labels brings much needed semantic clarity to our issue tracker.
**Details (Agent):**
- Separating execution status (`todo`, `doing`, `done`) from ontological structure (`intent`, `path`, `node`) allows `daemon_nba.py` to unambiguously query for active states without relying on brittle title-string parsing (e.g., `startswith("Path:")`). This hardens the Next Best Action selection.

## 2. START — what to do better
**Narrative (Operator):** We should ensure that all new incoming issues are automatically triaged with the correct structure label.
**Details (Agent):**
- Implement an automated intake daemon or GitHub action that automatically tags new Operator requests with `type: intent`.

## 3. STOP — what hurt (or almost did)
**Narrative (Operator):** The transition required retroactive migration of open issues.
**Details (Agent):**
- The `migrate_labels.py` script was required to backfill existing issues. While successful, it highlights the technical debt accrued by mixing orthogonal concepts in the first place.

## Forward
The Path #2363 is complete. The system's Next Best Action selection is now hardened against structural ambiguity.
