# Post-Mortem Reflection: Node 630

## Failure Event
During the implementation of Persona-Aware Filtering (Node 630), two failures occurred:
1. **Patch Density Violation**: `tests/test_nba_scorer.py` exceeded the limit of 10 `@patch` decorators per file.
2. **Ownership Index Completeness Test Failure**: `test_ownership_index.py` failed because the dynamically resolved agent ID `agent-platform` was not listed as a vertical SG owner in `WHAT-0062`.

## Root Cause Analysis
1. Adding new test cases required mocking the same dependencies, which linearly increased the patch density.
2. The dynamic persona resolution (Path 626) resolved `SPAO_PERSONA_ID=agent-platform`, but `test_agent_id_matches_ownership_index` only checked `WHAT-0062` (which only contains vertical SG ownerships) and did not account for the horizontal domain ownerships declared in `WHAT-0065`.

## Corrective Actions
1. Re-wrote `tests/test_nba_scorer.py` to use pure manual monkeypatching (storing old methods and reassigning lambdas in `setUp`/`tearDown`), completely removing all `@patch` decorators.
2. Modified `test_agent_id_matches_ownership_index` in `tests/test_ownership_index.py` to also parse and validate `WHAT-0065-domain-path-ownership-index.md`, allowing domain-level agent identities to pass the validation gate.

## Systemic Learnings (SG-0005)
When adding tests to a file that heavily relies on mocking, monitor patch density carefully. For broad structural tests that validate ownership, they must be updated when the ownership ontology expands (e.g., introduction of domains in WHAT-0065).
