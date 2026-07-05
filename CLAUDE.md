# Claude Code Hardware Abstraction Layer & Dyad Anchor

**Read `DYAD.md` immediately.** It contains all universal instructions: the SPAOR execution loop, invariants, registries, and chat protocol.

This file serves as the **Personalized Anchor** and the **Claude-specific Hardware Abstraction Layer (HAL)** for the Dyad Instantiation.

---

## RESTART-PENDING (Owed from `agy` 2026-07-04 session)
> **ACTION REQUIRED ON NEXT LAUNCH**: 
> During the recent Antigravity (`agy`) session, several critical structural updates were landed to enforce cross-substrate symmetry. You MUST sync and mirror these updates into this `CLAUDE.md` shim:
> 1. **The Scripting Discipline (The Bash-Complexity Ceiling)**: Mirror the exact "Rule of Two" and `.scratch/<task>.py` scripting mandates added to `GEMINI.md` to prevent compound bash execution.
> 2. **Cross-Substrate Symmetry**: Acknowledge that the native `SessionStart`/`SessionEnd` automated hooks (previously via `.claude/settings.json`) have been entirely retired in favor of the manual, declarative `d-start` and `d-reflect` disciplines.
> 3. Clear this RESTART-PENDING block once mirrored.
