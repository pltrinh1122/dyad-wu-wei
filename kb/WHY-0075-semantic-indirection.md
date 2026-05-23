# WHY-0075: The Semantic Indirection Invariant

## The Problem
Node 840 (Refine: Remediate Legacy Terminology) demonstrated that terminology changes in DZ-CIL require surgical code-level refactoring when terminology strings are hardcoded directly in executable code. Specifically:
- `antigravity.yml` contained `terminal: [probe]` as a literal YAML value
- `kernel/daemon_backlog.py` contained `node_type="probe"` as a Python string literal
- Test fixtures contained `"Probe 101: Align - New Path Title"` as assertion strings

When the Operator ratified `probe` → `discovery`, the Agent was forced to touch 10+ source files, navigate synthesized lexical guard false positives, and manage detached HEAD failures across multiple retry cycles. This is the antithesis of Wu-wei.

## The Root Cause: Semantic Coupling
Terminology is physically embedded in the computational substrate. The `kb/semantic_ledger.yml` — the single source of truth for canonical DZ-CIL terminology — is **completely disconnected** from the Python engines. The engines maintain their own independent vocabulary, hardcoded at authorship time.

This creates a **Dual-Brain State**: the ledger declares philosophical intent, but the engines run on a separate, frozen vocabulary. Every terminology transition requires closing this gap manually — a forced, turbulent act (*you-wei*).

## The Architectural Invariant: Semantic Indirection

> **All taxonomy-bearing string values in executable code MUST be resolved at runtime from `kb/semantic_ledger.yml`. Hardcoded terminology strings in source code are a structural violation of the Ziran principle.**

### Correct Pattern (Semantic Indirection)
```python
# Engine reads canonical term from ledger at runtime
from drivers.semantic_client import load_taxonomy
TAXONOMY = load_taxonomy()  # reads kb/semantic_ledger.yml

# Term is never hardcoded — it is a ledger lookup
node_type = TAXONOMY.get("investigatory_terminal")  # → "discovery"
```

### Violated Pattern (Semantic Coupling — FORBIDDEN)
```python
# Term is physically embedded in the substrate
node_type = "probe"  # ← VIOLATION: hardcoded terminology string
```

## The Ziran Consequence
Under Semantic Indirection, a terminology change is **purely a ledger edit**:
1. Operator declares: `probe` → `deprecated`, `discovery` → `active` in `semantic_ledger.yml`
2. Engines automatically resolve the new canonical term at runtime
3. Zero code refactoring. Zero test fixture changes. Zero turbulence.

The Declaration (Harmonization step) *is* the purge. The Refinement node disappears entirely.

## Scope of Application
This invariant applies to:
- Node taxonomy values (`terminal`, `non_terminal` types)
- Auto-generated issue title prefixes (`"Probe XX: ..."`, `"Discovery XX: ..."`)
- CLI argument validation strings
- Test fixture assertion strings that encode terminology

It does NOT apply to:
- Internal variable names in Python logic (e.g., `is_terminal`, `align_url`)
- Comments and docstrings
- Historical data in `artifacts/frontier_state.yml` (immutable record)
