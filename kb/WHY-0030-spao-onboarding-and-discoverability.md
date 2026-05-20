# WHY-0030: SPAO One-Step Onboarding & run-spao.sh Discoverability

## Decision Record
**Date**: 2026-05-20
**Path**: #362 — Spike Path: SPAO Release Packaging, One-Step Onboarding & CLI Discoverability
**Probe Node**: #363 Align

---

## Context

The SPAO system now has a working nvm-style installer (`spao-install`) and a
`v0.1.0` tagged release. However, two UX problems remain:

1. **Onboarding friction**: Users must first discover `spao-install`, understand
   its modes, and run multiple commands to get started in a new project.
2. **run-spao.sh invisibility**: The runner is generated inside the project root
   but users may not know what it does, how to invoke it, or that it is the
   primary agy entry point for SPAO-managed projects.

---

## Alignment Decisions

### 1. One-Step Onboarding

The canonical onboarding for a new project MUST be a single command:

```bash
curl -sSL https://raw.githubusercontent.com/pltrinh1122/agent-antigravity/main/bin/spao-install | bash -s -- --local
```

This single invocation must:
- Auto-fetch the latest release into `~/.spao/` if not already installed
- Create `.spao/version`, `.gitignore` entry, `GEMINI.md`, and `run-spao.sh`
  in the current working directory
- Print a clear "next step" summary pointing users to `./run-spao.sh`

The `--local` flag already auto-bootstraps the global install. The only missing
piece is surfacing this as the canonical one-liner in documentation.

### 2. run-spao.sh Discoverability

`run-spao.sh` must be self-announcing. Decisions:
- It MUST print a short usage banner when invoked with no arguments BEFORE
  handing off to `agy` (so the user sees it on first run)
- A `README.spao.md` file MUST be generated alongside `run-spao.sh` in the
  workspace root, explaining its purpose, usage, and the SPAO system
- The install success message MUST explicitly call out `./run-spao.sh` as the
  next step

### 3. What is NOT changing

- The `~/.spao/` version management layout — already correct
- The `.spao/` hidden directory in workspaces — already correct
- The `spao` global shim at `~/.local/bin/spao` — already correct
- The `GEMINI.md` inheritance model — already correct

---

## Feedforward Invariants

- `[ ]` One-liner curl bootstrap documented in README and installer output
- `[ ]` `run-spao.sh` prints usage banner on first run (no args)
- `[ ]` `README.spao.md` generated in workspace by `--local` install
- `[ ]` All changes delivered via PR from node/365 branch, not hotfix
