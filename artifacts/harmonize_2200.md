# Harmonize - Node 2200

## Intent
Rename the root `DYAD.md` file to `DYAD.md` to prevent naming conflation with external project instructions (e.g., `commons/DYAD.md`) when executing within nested workspaces or interacting with autonomous agent sub-routines.

## Changes
1. Rename the root repository file `DYAD.md` to `DYAD.md`.
2. Update all explicit textual references to `DYAD.md` across the codebase, specifically targeting:
   - `GEMINI.md` (Dao references).
   - `kernel/` and `drivers/` daemon scripts that may reference `DYAD.md` or search for it.
   - Test files (`tests/`) that assert against the existence or contents of `DYAD.md`.
   - `kb/` knowledge base articles and template files that refer to `DYAD.md`.

## Pre-Requisites
- Complete test suite passes before making mutations.
- Proper execution workspace checkouts.

## Post-Requisites
- All tests must pass after the rename.
- The system must successfully read universal instructions from `DYAD.md` (the dyad architecture correctly falls back to `DYAD.md` if `DYAD.md` is absent, or code must be updated to explicitly look for `DYAD.md`).

## Subagent Delegation
- The execution node will perform the widespread codebase refactor and replace operations.
