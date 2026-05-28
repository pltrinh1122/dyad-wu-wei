# WHAT-1096: Specification for Auditing and Remediating Deprecated KB Files

## Classification
- **Type**: WHAT (Specification)
- **ID**: WHAT-1096
- **Author**: agent-sg5 (SG-0005: Autonomous Knowledge Accrual)
- **Created**: 2026-05-28 (Node 1096, Path 1094)
- **Depends on**: WHAT-1086

---

## 1. Specification Overview

This document specifies the procedure for performing a comprehensive audit and remediation of all files in the `kb/` directory to eliminate lingering deprecated terms and forbidden raw git/gh command strings.

---

## 2. Audit Scope and Requirements

### 2.1 File Target Range
- The audit must cover **all** files under the `kb/` directory, regardless of whether they are modified in the current diff.

### 2.2 Terminology Evaluation
- Scan all files (excluding immune zones: `GLOSSARY.md` and `WHY-` prefix files) for deprecated terms defined in `kb/semantic_ledger.yml` (e.g. `path`, `discovery`, `dao_engine`, `refine`, etc.).
- Any file containing a deprecated term must be flagged for remediation.

### 2.3 Command Evaluation
- Scan **all** files under `kb/` (including immune zones) for raw command patterns matching CLI invocations of `git` or `gh`.
- Any file containing raw commands must be flagged for remediation.

---

## 3. Remediation Standards

### 3.1 Term Substitution
- Flagged deprecated terms must be replaced with their modern equivalents specified in the `superseded_by` mappings of `kb/semantic_ledger.yml`.

### 3.2 Command Hyphenation/Description
- Forbidden raw CLI commands must be converted to hyphenated or descriptive equivalents (e.g. `git-checkout` -> `git-checkout`, `gh-issue` -> `gh-issue`).

---

## 4. Verification and Enforcement

- An automated test must be added to verify that no non-immune `kb/` files contain deprecated terms and no `kb/` files contain raw commands.
- The repository-wide validation test suite must execute cleanly after remediation.
