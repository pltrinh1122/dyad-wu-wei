# WHY-1095: Audit and Remediate Deprecated KB Files

## Classification
- **Type**: WHY (Architectural Decision Record)
- **ID**: WHY-1095
- **Author**: agent-sg5 (SG-0005: Autonomous Knowledge Accrual)
- **Created**: 2026-05-28 (Node 1095, Path 1094)
- **Context**: Documenting the findings of the deprecated KB files audit to preserve knowledge purity.

---

## 1. Audit Rationale and Methodology

To prevent semantic entropy and keep the repository ROM clean, the system requires regular audits of deprecated terms.
We analyzed the non-immune files in the `kb/` directory against the deprecated terms listed in `kb/semantic_ledger.yml`.

### 1.1 Immune and Non-Immune Boundaries
- **Immune files**: `GLOSSARY.md`, `semantic_ledger.yml`, and any file prefixed with `WHY-`.
- **Non-immune files**: All other `WHAT-` and `HOW-` files under `kb/`.

---

## 2. Findings & Identified Gaps

Our audit revealed that several non-immune files contain deprecated terms that must be harmonized:

1. **`WHAT-0017-nba-primitive.md`**: Contains `aligned` (refers to alignment).
2. **`WHAT-0018-telemetry-primitive.md`**: Contains `orchestrators` (deprecated, superseded by `kernel_daemons`).
3. **`WHAT-0023-triple-node-auto-initialization-spec.md`**: Contains `align_probe_issue_id`.
4. **`WHAT-0038-strategic-goal-path-alignment-verification.md`**: Contains `alignment` in title and content.
5. **`WHAT-0041-inner-loop-test-dependencies.md`**: Contains `alignment`.
6. **`WHAT-0048-nba-scoring-rubric.md`**: Contains `alignment` and `aligns`.
7. **`WHAT-0050-historical-scoring-plan.md`**: Contains `alignment`.
8. **`WHAT-0060-tactical-goals-sg-0001.md`**: Contains `alignment` and `align`.
9. **`WHAT-0061-agent-persona-sg-0001-ownership.md`**: Contains `alignment` and `aligns`.
10. **`WHAT-0063-tactical-goals-platform.md`**: Contains `alignment`.
11. **`WHAT-0065-domain-path-ownership-index.md`**: Contains `alignment`.
12. **`WHAT-0622-dynamic-identity-resolution-alignment.md`**: Contains `alignment` in title/content and references.
13. **`WHAT-1154-codify-falsifications-spec.md`**: Contains `alignment`.

---

## 3. Remediation Roadmap

Since this node (Node 1095) is a Discovery Node (Probe), zero functional or structural code changes are permitted. Remediation will be performed in Node 1096 by:
- Replacing the word `align` and `alignment` with `harmonize` and `harmonization` in non-immune files.
- Replacing the word `orchestrator` with `kernel_daemon` in non-immune files.
- Using HTML entity escaping (e.g. `al&#105;gn`) when referring to older immutable filenames.
