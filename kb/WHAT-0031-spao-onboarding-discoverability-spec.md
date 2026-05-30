# WHAT-0031: SPAO One-Step Onboarding & CLI Discoverability — Technical Specification

## Overview
**Path**: #362 — Discovery Path: SPAO Release Packaging, One-Step Onboarding & CLI Discoverability
**Plan Node**: #364
**Implements decisions from**: WHY-0030

---

## Scope

Three concrete changes to be implemented in Activity node #365:

1. **`bin/spao-install`** — usage banner on no-args `run-spao.sh`, one-liner output
2. **`run-spao.sh` template** — prints usage/welcome on no-args before handing to `agy`
3. **`README.spao.md` template** — generated in workspace root by `--local` install

---

## 1. `bin/spao-install` Changes

### 1a. Bootstrap one-liner surfaced in `--local` success output

After a successful `--local` install, the final output block MUST print:

```
✅ SPAO workspace ready: /path/to/project
   Pinned to:  v0.1.0
   Launch:     ./run-spao.sh

   One-step bootstrap (share with teammates):
   curl -sSL https://raw.githubusercontent.com/pltrinh1122/dyad-wu-wei/main/bin/spao-install | bash -s -- --local
```

### 1b. Global install output also prints the one-liner

After global install success, append:

```
   Bootstrap any project in one command:
   curl -sSL https://raw.githubusercontent.com/pltrinh1122/dyad-wu-wei/main/bin/spao-install | bash -s -- --local
```

### 1c. `_write_readme` helper — generates `README.spao.md`

New internal function `_write_readme TARGET_DIR` called at end of `--local` install.
Template content specified in §3 below.

---

## 2. `run-spao.sh` Template Changes

When invoked with **no arguments**, `run-spao.sh` MUST print a welcome/usage banner
**before** launching `agy` interactively:

```
╔══════════════════════════════════════════════════════════╗
║  SPAO Workspace Runner  (v<pinned-version>)              ║
║  Core: ~/.spao/versions/<version>                        ║
║  Workspace: /path/to/this/project                        ║
╠══════════════════════════════════════════════════════════╣
║  Usage:                                                  ║
║    ./run-spao.sh                    Interactive session  ║
║    ./run-spao.sh -p "spao node sync"  Single prompt      ║
║    ./run-spao.sh --continue / -c    Resume conversation  ║
║    ./run-spao.sh -i "resume"        Interactive + prompt ║
║  See README.spao.md for full documentation.              ║
╚══════════════════════════════════════════════════════════╝
```

Implementation: add banner echo block in the `if [ $# -eq 0 ]` branch,
before the `exec agy` call. Version resolved from `.spao/version`.

---

## 3. `README.spao.md` Template

Generated at `<workspace>/README.spao.md` by `_write_readme`.
Content:

```markdown
# SPAO — Sense-Plan-Act-Observe System

This project is managed by the **SPAO Frontier Agent** via
[Antigravity CLI (`agy`)](https://github.com/pltrinh1122/dyad-wu-wei).

## Quick Start

Launch an agy session with full SPAO context:

    ./run-spao.sh

Run a single SPAO command non-interactively:

    ./run-spao.sh -p "spao node sync"

Resume your last conversation:

    ./run-spao.sh --continue

## Bootstrap (share with teammates)

    curl -sSL https://raw.githubusercontent.com/pltrinh1122/dyad-wu-wei/main/bin/spao-install | bash -s -- --local

## Version Management

| File | Purpose |
|---|---|
| `.spao/version` | Pinned SPAO core version for this workspace |
| `GEMINI.md` | SPAO invariants injected into agy context |
| `run-spao.sh` | agy launcher with SPAO env wired in |

Upgrade to latest SPAO:

    spao-install --upgrade
    spao-install --local --version <new-version>

## How it works

`run-spao.sh` sets two environment variables before invoking `agy`:
- `SPAO_CORE_DIR` — path to the installed SPAO orchestration codebase
- `SPAO_WORKSPACE_DIR` — this project's root

`agy` reads `GEMINI.md` from the workspace root for its Frontier Agent
instructions. The `--add-dir` flag makes the SPAO core scripts available
as an additional workspace for the agent.
```

### Idempotency

If `README.spao.md` already exists in the workspace, `_write_readme` MUST NOT
overwrite it — print a warning instead:
```
  ⚠️  README.spao.md already exists — skipping (edit manually to update)
```

---

## 4. Files Changed

| File | Change |
|---|---|
| `bin/spao-install` | Add `_write_readme` helper; call it in `--local` mode; add one-liner to success output |
| `run-spao.sh` (template inside installer) | Add banner block in no-args branch |

No other files require modification.

---

## 5. Verification Plan

### Automated
- `spao test` — all 112 tests must continue to pass (no Python changes)
- `bash -n bin/spao-install` — shell syntax check

### Manual
1. Run `spao-install --local /tmp/test-ws` on clean dir — verify `README.spao.md` created
2. Run `/tmp/test-ws/run-spao.sh` with no args — verify banner printed before agy launches
3. Run `spao-install --local /tmp/test-ws` again — verify README not overwritten
4. Verify one-liner appears in success output
5. Run `bash -c "$(curl -sSL .../bin/spao-install)" -- --local /tmp/test-ws2` — verify full one-step flow

---

## Feedforward Invariants

- `[ ]` `README.spao.md` created by `--local`, not overwritten on re-run
- `[ ]` `run-spao.sh` prints banner before handing off to `agy` (no-args only)
- `[ ]` Bootstrap one-liner appears in both `--local` and global install success output
- `[ ]` All 112 tests still pass
- `[ ]` Changes delivered via PR from node/365 branch — no hotfixes
