# WHY-1157: Lexical Guard and Semantic Ledger Extension

## Context
As the codebase ontology evolves (e.g. from SPAO to SPAOR, from North Star to Telos), manual reviews of files for deprecated terminology are error-prone and time-consuming.

## The Proposal
We design a programmatic extension to the semantic immune system to automate this validation:

1. **`semantic_ledger.yml` Configuration**
   - We maintain a list of deprecated terms mapped to their active superseding terms.
   - We define immune zones (such as `GLOSSARY.md` or `WHY-` prefix files) where historical context must be preserved.

2. **`lexical_guard` Extension**
   - The test suite (`tests/test_lexical_guard.py`) will read the active `semantic_ledger.yml` file.
   - It will dynamically scan all modified, added, renamed, or untracked files in the active git index.
   - Any matches on deprecated keys (e.g. "align" -> "harmonize") outside of the immune zones will fail the test suite immediately.

## Bedrock Principle
Automated, continuous ontology policing prevents semantic drift and ensures that all LLM context windows remain synchronized on the authoritative glossary definitions without human oversight.
