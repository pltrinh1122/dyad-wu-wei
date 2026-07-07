#!/usr/bin/env bash
# bin/standdown.sh — dyad-bond stand-down ritual (K6: mechanical spine + judgment template)
#
# WHY (Item-K6, 2026-06-13): close the session so the next one recovers-forward without re-deriving.
#   The stand-down has a MECHANICAL half (deterministic — automate it) and a JUDGMENT half (what is
#   queue-worthy; single-home; bloat-guard — NOT automatable: that is the agent's covalent act).
#
# HOOK BOUNDARY (verified against the Claude Code hook contract, 2026-06-13): a **SessionEnd** hook is
#   TEARDOWN-ONLY — it fires after the agent is gone and CANNOT inject context back, and **Stop** fires
#   every turn-end (cannot mean "stand-down"). So the judgment write CANNOT be hook-fired into the agent.
#   Therefore: the AGENT runs this at stand-down and reads the template below; a SessionEnd hook may run
#   it `--log` only for the mechanical durability line (debug log). This is K6 constraint (b) made hard.
#
# COVALENT GATE (K6 constraint a / S2): wiring the SessionEnd hook was the Operator's act, never an
#   Agent self-grant — DONE 2026-07-04 (.claude/settings.json, main@5e51677); the one-shot installer
#   that did it was retired after (→ dialectic/standdown-automation.md).
#
# Usage:  bin/standdown.sh          # mechanical checks + the stand-down template (agent runs at close)
#         bin/standdown.sh --log    # mechanical line only (SessionEnd hook body; output is debug-log)

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

LEDGER="artifacts/frontier_state.md"
ANCHOR_FILES=(DYAD.md CLAUDE.md GEMINI.md)

# ── Mechanical: did the anchor move past the recorded baseline this session? (ROM-UI stand-down rule) ─
# Per-file boot-set (inv:rom-currency CRISP form) if present, else legacy single-sha baseline. Each
# anchor file is compared to its OWN recorded sha — the boot SET {CLAUDE.md, GEMINI.md, DYAD.md} is
# pinned independently, so one sha for all three false-positives when the shims differ from DYAD.md.
perfile="$(grep -m1 'inv:rom-currency.*per-file boot-set' "$LEDGER" 2>/dev/null || true)"
legacy="$(grep -m1 'ROM-baseline (anchor commit' "$LEDGER" 2>/dev/null \
            | grep -oE 'DYAD\.md@[0-9a-f]{7,40}|`[0-9a-f]{7,40}`' | head -1 \
            | grep -oE '[0-9a-f]{7,40}' || true)"   # handles `DYAD.md@<sha>` + bare `<sha>` (legacy)
declare -A want=()
if [[ -n "$perfile" ]]; then
  for f in "${ANCHOR_FILES[@]}"; do
    s="$(printf '%s' "$perfile" | grep -oE "${f//./\\.}@[0-9a-f]{7,40}" | head -1 | grep -oE '[0-9a-f]{7,40}' || true)"
    [[ -n "$s" ]] && want["$f"]="$s"
  done
fi
rom_line="anchor: unknown (could not parse baseline)"
if ((${#want[@]})) || [[ -n "$legacy" ]]; then
  moved=()
  for f in "${ANCHOR_FILES[@]}"; do
    exp="${want[$f]:-$legacy}"
    cur="$(git log -1 --format=%H -- "$f" 2>/dev/null || true)"
    [[ -n "$cur" && "$cur" == "$exp"* ]] || moved+=("$f@${cur:0:7}")
  done
  base="${want[DYAD.md]:-$legacy}"
  if ((${#moved[@]})); then
    rom_line="anchor MOVED past per-file boot-set (${moved[*]}) → SET RESTART-PENDING + refresh the boot-set line AFTER commit."
  else
    rom_line="anchor + shims each at recorded per-file sha (DYAD.md@${base:0:7}) → RESTART-PENDING stays none."
  fi
fi

dirty="$(git status --porcelain 2>/dev/null || true)"
branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')"
unpushed="$(git log --oneline '@{u}..' 2>/dev/null | wc -l | tr -d ' ' || echo 0)"
dur_line="clean + in sync on \`$branch\`."
[[ -n "$dirty" ]] && dur_line="⚠ DIRTY on \`$branch\` — commit + push so the memory is grounded."
[[ -z "$dirty" && "$unpushed" != "0" ]] && dur_line="⚠ $unpushed unpushed commit(s) on \`$branch\` — push (bin/git.sh)."

# Scratch tier RETIRED 2026-06-27 (Operator fold+land) — durability-of-record is the Agent-owned WIP
# auto-save (commit+push at natural pauses), Stop-hook-enforced. → dialectic/substrate-access.md §Scratch RETIRED.

mech="$(printf '%s\n' \
  "dyad-bond stand-down — mechanical:" \
  "  ROM: $rom_line" \
  "  Durability: $dur_line")"

if [[ "${1:-}" == "--log" ]]; then
  printf '%s\n' "$mech"
  exit 0
fi

cat <<TEMPLATE
$mech

dyad-bond stand-down — JUDGMENT (the agent fills; auto-trigger ≠ auto-judgment, K6-b):
  Queue-worthy filter — record an item ONLY if it is (a) in-flight (a live front, not closed),
    (b) not already single-homed elsewhere (no restating dialectic/ or kb/ — point to it), and
    (c) load-bearing for resume (the next session needs it to recover-forward). Else DROP it.
  Bloat-guard — the ledger is the memory, not the journal. Prefer one line + a pointer to prose.
    If the resume-visible queue outgrows a screen it has failed its own bound (rub-forward, 2026-06-11).

  Stand-down checklist:
   1. ROM (above): if the anchor moved, set RESTART-PENDING in $LEDGER + refresh the ROM-baseline
      line; else leave 'none'. Record a one-line Stand-Down note (date · what changed · baseline).
   2. Open-items / Item-K queue: update statuses; drop what closed; add only queue-worthy in-flight.
   3. Intermission reflection (D3 — substance + durability, no four-step ceremony): what was authored/
      learned, what is now the live front, what carries. Single-home the prose in relationship-craft.md /
      cross-dyad-craft.md; the ledger holds the pointer + the resume-visible delta.
   4. Theory-pipeline: advance exec_phase / next_probe for any candidate touched this session.
   5. Scratch (above): triage the tank while context is live — land the settled into dialectic/, then
      bin/scratch.sh --done <id>; --done or discard the rest. An un-triaged tank rots (Item-I) and the
      reload-cost lands on next-session-you. (save ≠ land; the tank is a transient buffer, not a home.)
   6. Durability (above): commit + push before stepping away — unpushed history is ungrounded memory.
TEMPLATE
