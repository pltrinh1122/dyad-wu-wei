#!/usr/bin/env bash
# bin/standup.sh — dyad-bond stand-up / resume automation (K6, mechanical spine)
#
# WHY (ours — Item-K6, 2026-06-13): the resume routine (carry-forward.md §How to resume) opens with
#   DETERMINISTIC checks a fresh Covalent otherwise hand-runs every session — the ROM-UI diff (anchor
#   hash vs the recorded baseline), the memory-durability check (uncommitted/unpushed = ungrounded
#   memory), and the substrate probe (is the IM daemon even armable here?). Mechanizing them removes a
#   per-session trigger AND removes hand-error. Wired as a Claude Code **SessionStart** hook, `--hook`
#   mode emits the result as `additionalContext` so it loads at boot WITHOUT a `read: carry-forward`.
#
# WHAT IT IS NOT: it does not JUDGE. It SURFACES — the mismatch, the dirty tree, the dark inbox — and
#   hands the disposition to the agent (refresh the baseline? set RESTART-PENDING?). auto-trigger ≠
#   auto-judgment (K6 constraint b). The agent still reads the ledger; this primes the seams.
#
# COVALENT GATE (K6 constraint a / S2): wiring it as a hook was the Operator's act, never an Agent
#   self-grant — DONE 2026-07-04 (.claude/settings.json, main@5e51677); the one-shot installer that did
#   it was retired after, to avoid a permanently-committed generator drifting from the live file it wrote
#   (→ dialectic/standdown-automation.md). This script itself is unaffected — still runnable by hand.
#
# Usage:  bin/standup.sh           # human-readable resume report (stdout)
#         bin/standup.sh --hook    # emit SessionStart additionalContext JSON (hook body)

set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

LEDGER="artifacts/frontier_state.md"
ANCHOR_FILES=(DYAD.md CLAUDE.md GEMINI.md)

lines=()
add() { lines+=("$1"); }

# ── ROM-UI check (per-file boot-set if present, else legacy single-sha baseline) ──────────────
# CRISP form (inv:rom-currency, Operator-corrected 2026-06-25): each anchor file vs its OWN recorded
# sha — the boot SET is {CLAUDE.md, GEMINI.md, DYAD.md}, each pinned independently. The single-sha
# `ROM-baseline (anchor commit…)` line is the legacy/human-gloss fallback; comparing all three files
# against DYAD.md's one sha false-positives whenever the shims sit at a different commit (the norm).
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
if ((${#want[@]} == 0)) && [[ -z "$legacy" ]]; then
  add "ROM-UI: ⚠ could not parse ROM-baseline from $LEDGER — check the ledger by hand."
else
  mism=()
  for f in "${ANCHOR_FILES[@]}"; do
    exp="${want[$f]:-$legacy}"
    cur="$(git log -1 --format=%H -- "$f" 2>/dev/null || true)"
    [[ -n "$cur" && "$cur" == "$exp"* ]] || mism+=("$f@${cur:0:7}≠${exp:0:7}")
  done
  if ((${#mism[@]})); then
    add "ROM-UI: ⚠ MISMATCH — moved: ${mism[*]}."
    add "        → verify the shim boot-chain fired (you read DYAD.md because the shim said to),"
    add "          then notify the Operator + refresh the per-file boot-set line in $LEDGER."
  else
    base="${want[DYAD.md]:-$legacy}"
    add "ROM-UI: ✓ MATCH (boot-set {DYAD.md, CLAUDE.md, GEMINI.md} each at its recorded per-file sha; DYAD.md@${base:0:7})."
  fi
fi

# ── Memory-durability (uncommitted/unpushed = ungrounded memory; the standing substrate threat) ─
dirty="$(git status --porcelain 2>/dev/null || true)"
branch="$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo '?')"
unpushed="$(git log --oneline '@{u}..' 2>/dev/null | wc -l | tr -d ' ' || echo 0)"
if [[ -n "$dirty" ]]; then
  add "Durability: ⚠ working tree DIRTY on \`$branch\` ($(printf '%s\n' "$dirty" | wc -l | tr -d ' ') paths) — commit before relying on the ledger as memory."
elif [[ "$unpushed" != "0" ]]; then
  add "Durability: ⚠ $unpushed unpushed commit(s) on \`$branch\` — push (bin/git.sh) so the remote backs up the memory."
else
  add "Durability: ✓ clean + in sync on \`$branch\`."
fi

# ── Substrate probe (is this the durable home, or an ephemeral clone? is the IM daemon armable?) ─
home_ok=0; gh_ok=0; falsify_ok=0
[[ -d /mnt/shared_data/dzw ]] && home_ok=1
command -v gh >/dev/null 2>&1 && gh_ok=1
{ [[ -e commons/scripts/falsify.py ]] || find commons -name falsify.py 2>/dev/null | grep -q .; } && falsify_ok=1
if ((home_ok && gh_ok && falsify_ok)); then
  add "Substrate: ✓ durable home + gh + falsify.py present → IM daemon armable (step 6, im-daemon.md verbatim)."
else
  miss=()
  ((home_ok))   || miss+=("no /mnt/shared_data/dzw mount")
  ((gh_ok))     || miss+=("no gh")
  ((falsify_ok))|| miss+=("no commons/falsify.py")
  missjoin="$(printf '%s, ' "${miss[@]}")"; missjoin="${missjoin%, }"
  add "Substrate: ⚠ ephemeral/partial ($missjoin) → IM daemon NOT armable here; DM-watch is dark this session."
fi

# ── Scratch tier RETIRED 2026-06-27 (Operator fold+land) — durability-of-record is now the Agent-owned
#    WIP auto-save (commit+push at natural pauses), Stop-hook-enforced. → dialectic/substrate-access.md §Scratch RETIRED.

# ── Output ───────────────────────────────────────────────────────────────────────────────────
header="dyad-bond stand-up (bin/standup.sh) — mechanical resume checks. Operate as Covalent; read $LEDGER; then take the NBA / Item-K queue."
body="$(printf '%s\n' "$header" '' "${lines[@]}")"

if [[ "${1:-}" == "--hook" ]]; then
  CTX="$body" python3 - <<'PY'
import json, os
print(json.dumps({"hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": os.environ["CTX"],
}}))
PY
else
  printf '%s\n' "$body"
fi
