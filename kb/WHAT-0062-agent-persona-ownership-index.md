# WHAT-0062: Agent Persona Ownership Index

<!-- MACHINE-PARSE CONTRACT
  Format:    GitHub Flavored Markdown pipe-delimited table
  Consumers: kernel/daemon_strategic.py (578-B enforcement gate)
             kernel/daemon_nba.py (578-C NBA path filter)
  Key field: sg_id (exact match to strategic_intent.yml id values)
  Parse hint: The ownership table begins after the "## Ownership Index" heading.
              Each data row (non-header, non-separator) is one authoritative record.
-->

## Classification
- **Type**: WHAT (Structural Fact)
- **ID**: WHAT-0062
- **Author**: agent-sg5 (SG-0005: Autonomous Knowledge Accrual)
- **Created**: 2026-05-21 (Node 601, Path 591)
- **Depends on**: WHAT-0059, WHAT-0057, WHAT-0061
- **Decision record**: WHY-0062 (forthcoming — Activity 602)

---

## Purpose

This index is the **static authorization source of truth** for the Hybrid Persona
Domain Gate (see WHY-0062). It maps every Strategic Goal (SG) in
`artifacts/strategic_intent.yml` to its authoritative agent persona, preventing
cross-agent domain collisions at plan-start time.

The enforcement gate (Path 578-B, agent-sg2) reads this table to verify that the
executing agent's `SPAO_PERSONA_ID` environment variable matches the `owner_persona`
for the target node's strategic goal. If the mapping is absent or the identity
cannot be verified, the gate **must fail-closed**.

---

## Ownership Index

| sg_id   | owner_persona | spec_file                                   | why_file                                    | status      |
|---------|---------------|---------------------------------------------|---------------------------------------------|-------------|
| NS-0001 | shared        | —                                           | —                                           | shared      |
| SG-0001 | agent-sg1     | kb/WHAT-0061-agent-persona-sg-0001-ownership.md | kb/WHY-0061-agent-persona-sg-0001-ownership.md | covered |
| SG-0002 | agent-sg2     | kb/WHAT-0057-agent-persona-sg-0002-ownership.md | kb/WHY-0057-agent-persona-sg-0002-ownership.md | covered |
| SG-0003 | unassigned    | (pending)                                   | (pending)                                   | gap         |
| SG-0004 | unassigned    | (pending)                                   | (pending)                                   | gap         |
| SG-0005 | agent-sg5     | kb/WHAT-0059-agent-persona-sg-0005-ownership.md | kb/WHY-0059-agent-persona-sg-0005-ownership.md | covered |

---

## Schema Definition

| Column          | Type     | Description |
|-----------------|----------|-------------|
| `sg_id`         | string   | Strategic Goal identifier — must exactly match `id` values in `artifacts/strategic_intent.yml` |
| `owner_persona` | string   | Canonical agent persona ID (e.g. `agent-sg1`), or `shared` for North Star goals, or `unassigned` for unmapped goals |
| `spec_file`     | path     | Relative path to the `WHAT-*` ownership spec file, or `(pending)` if unassigned |
| `why_file`      | path     | Relative path to the `WHY-*` decision record, or `(pending)` if unassigned |
| `status`        | enum     | One of: `covered` \| `shared` \| `gap` |

---

## Fail-Closed Invariant

> **Any gate that reads this index MUST treat the following as hard-block conditions:**
> - `sg_id` not present in this table → **block** (unknown goal, fail-closed)
> - `owner_persona` is `unassigned` → **block** (no owner registered, fail-closed)
> - `owner_persona` is `shared` → **allow** (NS-0001 is intentionally cross-agent)
> - `SPAO_PERSONA_ID` env var absent → **block** (cannot verify identity, fail-closed)
> - `SPAO_PERSONA_ID` ≠ `owner_persona` → **block** (persona mismatch, fail-closed)

---

## Falsification Criteria

This document is stale and **must be updated** if any of the following are true:
1. A new Strategic Goal is added to `artifacts/strategic_intent.yml` without a corresponding row here
2. An `unassigned` entry is given an owner but this table is not updated
3. A spec file listed here does not exist on disk
4. The `agent_id` field in `antigravity.yml` does not match any `owner_persona` in this table

The structural validation tests in `tests/test_ownership_index.py` (Activity 603)
enforce conditions 1, 3, and 4 automatically on every CI run.

---

## Amendment Process

1. Operator assigns an agent persona to an unassigned SG
2. Agent creates a `WHAT-*` ownership spec and `WHY-*` decision record in `kb/`
3. Agent submits a PR updating this table's row: `unassigned` → `agent-sg{N}`, `(pending)` → actual file paths, `gap` → `covered`
4. PR must pass structural validation tests (Activity 603) before merge
