# WHAT-1086: Verification Standards for KB Deprecation Checkers

## Classification
- **Type**: WHAT (Specification)
- **ID**: WHAT-1086
- **Author**: agent-sg5 (SG-0005: Autonomous Knowledge Accrual)
- **Created**: 2026-05-28 (Node 1086, Path 1094)
- **Depends on**: WHAT-0001, WHAT-0059

---

## 1. Specification Overview

This document specifies the verification and test suite invariants for the Knowledge Base (KB) static conflict checkers. These checkers guarantee that no stale vocabulary or raw git/gh command strings pollute the universal repository memory.

---

## 2. Invariants & Rules

### 2.1 The Specification Requirement Rule
- Any issue whose title matches the `Plan` phase (e.g. `Discovery 1086: Plan - ...` or `Plan - ...`) **must** modify or create a corresponding specification file located at `kb/WHAT-*.md`.
- Transitioning via `plan-finish` will fail if a `kb/WHAT-*.md` file is not staged in the active git index.

### 2.2 Checked File Paths & Lines
- The conflict checks are restricted to changes targeting files located in the `kb/` directory (or containing `/kb/` in their paths).
- Only additions (lines beginning with `+`) in the git diff are evaluated.

### 2.3 Forbidden Items
- **Deprecated Terms**: Any term matching keys under `terms` (whose state is `deprecated`) in `kb/semantic_ledger.yml`.
- **Forbidden Commands**: Command strings matching direct CLI invocations of version control tools (e.g., `git checkout`, `gh issue`).

### 2.4 Immune Zones
- Immune zones (e.g. `GLOSSARY.md` and any file with a `WHY-` prefix) are exempt from **Deprecated Terms** checking.
- Immune zones are **NOT** exempt from the **Forbidden Commands** check.

---

## 3. Verification & Test Suite Invariants

The `tests/test_knowledge_accrual.py` test suite must:
1. Verify that `check_kb_conflicts` correctly flags deprecated terms on newly added lines.
2. Verify that immune zones successfully bypass deprecated term checking.
3. Verify that raw command patterns are blocked even inside immune zones.
4. Complete test execution in under 200ms to preserve inner-loop velocity.
