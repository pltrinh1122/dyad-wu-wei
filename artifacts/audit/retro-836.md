# Epistemic Retrospective: Node 836

## The Failure
During the codification of the DZ-CIL Hybrid Triad, we updated `kb/semantic_ledger.yml` to deprecate the term `probe` (replaced by `discovery`). 
When we ran `./bin/run-tests`, `tests/test_knowledge_accrual.py::test_check_kb_conflicts_clean` failed because its test payload contained the newly forbidden string "This is a clean path and probe task."

## The Epistemic Insight
This failure was actually a success of the system architecture! The Semantic Immune System successfully read the dynamic ledger and immediately enforced the new lexical immunity across the repository, catching the term "probe" in the test payload.

## The Remediation
We updated the test payload in `tests/test_knowledge_accrual.py` to use "discovery task" instead of "probe task." This aligns the test harness with the new DZ-CIL Hybrid Triad ontology.

## The Synthesis
The system's data-driven semantic immunity (implemented in Node 834) perfectly prevented semantic pollution from entering the knowledge base. No further structural changes are necessary; the system behaved exactly as designed.
