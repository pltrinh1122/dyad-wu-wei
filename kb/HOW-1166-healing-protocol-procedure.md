# HOW: Healing Protocol Procedure and Discipline

## 1. Triage Gate & Operator's Procedural Role
- **Triage Gate:** A Healer is warranted *only* when the SPAO loop itself is seized. Routine faults must be handled by the running Agent.
- **Procedural Role:** The Operator detects, halts, instantiates the Healer, steers, ratifies, authorizes, and co-observes. Perceptual detection remains human.

## 2. Healer Discipline
- Falsify each hypothesis.
- Walk back to PR-zero (differentiate trigger vs. origin).
- Minimum wu-wei cut.
- Instrument before reviving.
- Point, don't fix (preserve the patient's agency).
- **Intervention Threshold (Default to Bare `continue`):** Let the patient self-heal. Observe and flag-on-evidence, do not pre-empt. Provide more than a bare `continue` ONLY when: (a) the next step is irreversible/high-blast; (b) patient cannot access the source; (c) the ward gave insufficient context. If (c), enrich the ward source first.

## 3. Communication and Handoff Framing
- **Framing, Not Channel:** An imperative loops in any channel re-read before its consumption point. Handoffs must be **passive + idempotent + observed**.
- **No Self-Emitted Boot Beacon:** Confirm boot via the Operator's one-shot prompt or natural progress events.
- **Measured Comms:** Tag recommendations by reversibility. Emergency-stop (halt/exit) = pre-authorized reflex. Constructive/irreversible = require Operator deliberation.

## 4. Observation and Recovery Cadence
- **Observe Durable Artifacts:** Health is measured by commits, node-state changes, and PRs over a longer window—not phase churn.
- **Loop vs. Grind Signatures:** Genuine loop = identical repetition or zero durable-artifact change. Grind = varied errors producing new durable artifacts.
- **Dual Observation (Flag and Vouch):** Either party may halt. The Operator may *vouch* to let a grind continue based on their terminal view.
- **Graduated Recovery Cadence:** Crawl (HITL after every step) → Walk (HITL at node boundaries) → Run (autonomy + merge gate). Deliver via Operator, not a re-read imperative.
- **Resume Mode:** Do not use `-c` on a seized/poisoned context. Use `-c` only on a healthy mid-task session.

## 5. Pre-Sew-Up and Recovery-State Hazards
- **Sponge Count:** Reconcile the patient's `git-status` against the intended delta. Remove Healer residue. Never touch the patient's pre-existing state.
- **Known Hazards:**
  - **Stale active-node lock:** Resolve via `complete_active_node` before planning new nodes.
  - **Stale root after sync:** Anticipate a correct ROM-drift restart on the next sync if the root is behind `origin/main`.
  - **PR/Node Conflation:** Always merge by the real PR number, not the Node ID.
