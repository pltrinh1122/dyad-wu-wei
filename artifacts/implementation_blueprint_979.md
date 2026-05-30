# Implementation Blueprint 979: Maintenance: Refine Knowledge Accrual Mechanisms

## Executive Summary
This blueprint details the execution steps for Path 977, focusing on correcting false positives in the lexical guard and fixing test isolation breaches related to `daemon_knowledge_accrual`.

## 1. Node 981: Remove false-positive lexical guards
**Target:** `tests/test_lexical_guard.py`
**Actions:**
- Refactor the `check_content` function to use a regular expression check rather than a naive substring `in` check.
- Use word boundary patterns (`\b`) or discrete word extraction to match deprecated terms. This will resolve the issue where terms like `epic` trigger on `depict`.
- Ensure tests still correctly catch intended violations while ignoring substrings in unrelated words.

## 2. Node 1294: Fix mock daemon_knowledge_accrual in node lifecycle tests
**Target:** `tests/test_node_lifecycle.py`
**Actions:**
- Identify all tests that trigger the Plan phase in `kernel/node_lifecycle.py` (which internally invokes `daemon_knowledge_accrual.run_kb_check`).
- Add `@mock.patch("kernel.daemon_knowledge_accrual.run_kb_check")` to these test functions.
- Verify test hermeticity by running the suite and ensuring that live filesystem operations within the `kb/` directory are fully bypassed during mock testing.

## Next Steps
Upon completion of this plan node, execution will proceed to Node 980 (Reflect) and subsequently the implementation activity nodes (981 and 1294).
