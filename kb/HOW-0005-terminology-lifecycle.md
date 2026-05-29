# HOW-0005: Terminology Promotion & Demotion Lifecycle

## Purpose
The DZ-CIL relies on absolute architectural coherence. When terminology (ontology) must change to better map to the Operator's intent, the system must navigate this philosophical shift without inducing a mechanical Split-Brain Crash. This document dictates the Wu-wei (effortless) protocol for promoting and demoting terminology.

## 1. The Terminology State Machine
Any formal term in the DZ-CIL follows a strict state progression inside `kb/semantic_ledger.yml`:

* **`proposed` (The Sprout)**: The Operator or Agent suggests a new term. It is not codified and does not trigger enforcement.
* **`active` (The Root)**: The term is formally ratified via a Harmonization node. It is codified into `kb/GLOSSARY.md` and added to `semantic_ledger.yml` as `active`. Usage is enforced.
* **`deprecated` (The Decay)**: The term has been superseded by a new `active` term. The old term is flagged as `state: deprecated` with a `superseded_by` pointer. The `audit_daemon.py` actively accrues passive telemetry whenever it encounters this term.
* **`purged` (The Cleansing)**: The term has been structurally purged from the entire repository (engines, scripts, logs). It remains in the ledger purely as an historical tombstone to block regressions.

## 2. The Ziran Execution Loop (Wu-wei)
We reject the cybernetic "Shim" (artificial force) and we reject the "Split-Brain Crash" (ignoring reality). We accept the system's current reality while holding the intent for its future.

The formal lifecycle execution is:

1. **The Declaration (Harmonization)**: 
   - We update `kb/semantic_ledger.yml` (shifting `X` to active, and `Y` to `deprecated`).
   - *Crucially, we do not force the interface to accept the new term yet, and we do not build an alias/Shim.* We accept that the structural reality (e.g. Python CLI parsers) is still running on term `Y`. 
   
2. **The Passive Acceptance (Wu-wei)**: 
   - The Operator and Agent must continue to use the `deprecated` term `Y` when executing system commands to ensure the system flows without crashing. We ride the transition effortlessly, without fighting the engine.
   - Meanwhile, the `audit_daemon.py` passively flags the deprecated term, quietly accruing gravitational mass in the `prompt_backlog.yml`.

2.5. **The Generative Invariant**:
   - During *any* content generation or restructuring (e.g., updating a `WHAT-` or `HOW-` spec), the Agent must proactively cross-check `kb/semantic_ledger.yml` to ensure that previously deprecated terms are not inadvertently reintroduced. Lexical Guard failures during testing indicate a failure to map generated text to the superseded ontology.


3. **The Gravitational Pull (Refinement)**: 
   - When the telemetry mass naturally elevates a Refinement Node to the top of the NBA queue, the Agent pulls it.
   - The Agent performs the deep structural purge, officially bridging the engine to the new terminology.
   - Only from this point forward do we shift to using the new term `X` in our interactions.

## Summary
Declare intent. Accept current reality. Accrue passive friction. Refine when the environment demands it.
