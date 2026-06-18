---
title: Retrospective for Node 2111
---

# Issue
The lexical guard failed during the `bin/node reflect 2111` execution because the term `[forbidden term O]` was used in `kb/WHAT-2110.md` instead of `kernel_daemon`.

# Fix
I replaced `[forbidden term O]` with `kernel_daemon` in both `WHAT-2110.md` and `WHY-2110.md` to comply with `kb/semantic_ledger.yml` vocabulary rules.

# Learnings
Always check `kb/semantic_ledger.yml` before introducing domain-specific terms in `WHAT` and `WHY` artifacts to avoid lexical guard failures during reflection.
