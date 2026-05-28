# WHY-1085: Technical and Philosophical Mechanics of KB Deprecation

## Classification
- **Type**: WHY (Architectural Decision Record)
- **ID**: WHY-1085
- **Author**: agent-sg5 (SG-0005: Autonomous Knowledge Accrual)
- **Created**: 2026-05-28 (Node 1085, Path 1094)
- **Context**: Investigating and formalizing the repository's Knowledge Base (KB) deprecation check mechanics.

---

## 1. The Philosophical Context

The DZ-CIL operates under a strict ontology to preserve inner-loop velocity and prevent cognitive drift. As our understanding of system dynamics evolves, terminology and operational procedures must adapt. However, raw deletions or renaming can cause a "Split-Brain Crash" where active scripts or processes expect legacy terminology.

To prevent this, the metasystem establishes a structured, asynchronous decay lifecycle:
1. **Declare Intent**: Mark legacy terms as `deprecated` in the semantic ledger.
2. **Accept Reality**: Allow existing execution patterns to run on deprecated terms.
3. **Accrue Gravitational Pull**: Log passive friction when deprecated terms are used.
4. **Cleanse (Purge)**: Refine and refactor the codebase to new terminology when the environment naturally elevates the task.

---

## 2. Technical Implementation details

Knowledge base integrity is enforced through static conflict checks performed during planning and commit hooks.

### 2.1 The Semantic Ledger (`kb/semantic_ledger.yml`)
The ledger is the authoritative source for term lifecycle management:
- **`immune_zones`**: Directories or specific files exempt from the deprecated terms check.
- **`terms`**: Maps deprecated words to their modern counterpart (e.g. `epic` -> `path`).
- **`proposed`**: Declared semantic intents which represent known debt.

### 2.2 Static Conflict Checking (`drivers/knowledge_accrual_skill.py`)
Static checking is executed via `check_kb_conflicts(diff_text)` which operates on modified lines:
1. **File Target**: The check only triggers on files within the `kb/` directory (or containing `/kb/` in their path).
2. **Line Filter**: Only newly added lines (beginning with `+`) in the git diff are checked.
3. **Immune Zone Exemption**: Files declared in `immune_zones` (such as `GLOSSARY.md` and any file with a `WHY-` prefix) bypass the deprecated term search.
4. **Command Invariance**:
   - Direct shell invocation signatures of `git` or `gh` commands (e.g. `git-checkout` or `gh-issue`) are strictly forbidden in *all* KB files, including immune zones.
   - Documentation must refer to these actions descriptively or using hyphenated forms (e.g. `git-checkout`, `remote fetch`).

---

## 3. Enforcement Gradient

Currently, the conflict check runs in two modes:
- **Lax / Dry-Run**: Warnings are outputted to stdout, but the execution continues (e.g. CLI operations).
- **Strict / Block**: Raises a fatal exception blocking lifecycle transition commands (e.g. `node plan-finish`).

This dual-tier approach guarantees that no new semantic entropy is introduced into the immutable repository memory (ROM) during planning or reflection.
