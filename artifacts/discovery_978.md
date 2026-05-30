# Discovery 978: Harmonize - Maintenance: Refine Knowledge Accrual Mechanisms

## Executive Summary
This discovery node addresses two distinct maintenance issues on Path 977: identifying false positives in the lexical guard and addressing a mock leak in the test harness related to knowledge accrual.

## 1. Lexical Guard False Positives
**Location:** `tests/test_lexical_guard.py` (`check_content` function)
**Diagnosis:** 
The lexical guard currently relies on a naive Python `in` substring search (`if word in content_lower:`). This approach mistakenly flags perfectly valid words that happen to contain a deprecated term as a substring. For example, the deprecated term `epic` triggers a false positive on `depict`.
**Proposed Fix:** 
Refactor `check_content` in `tests/test_lexical_guard.py` to use a regular expression with word boundaries (e.g., `\b`) ensuring that we only match exact, discrete instances of deprecated terms while accounting for hyphenated variants.

## 2. Test Harness Isolation (Mock Leak)
**Location:** `tests/test_node_lifecycle.py`
**Diagnosis:** 
`tests/test_node_lifecycle.py` applies `@mock.patch("kernel.daemon_knowledge_accrual.enforce_reflection_hook")` across several tests to prevent side effects during node reflection. However, `kernel/node_lifecycle.py` also invokes `daemon_knowledge_accrual.run_kb_check(...)` during the Plan phase. Because `run_kb_check` is not mocked, test executions implicitly run the actual `run_kb_check` routine, which parses the live `kb/` directory and creates test isolation breaches.
**Proposed Fix:**
Extend the patching in `tests/test_node_lifecycle.py` to also mock `"kernel.daemon_knowledge_accrual.run_kb_check"` wherever the Node Lifecycle tests trigger the Plan phase, ensuring complete test hermeticity.

## Next Steps
Proceed to Node 979 to plan these implementations and schedule the respective Activity nodes (981 and 1294).
