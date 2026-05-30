# Retrospective 977: Maintenance: Refine Knowledge Accrual Mechanisms

## Incident Summary
The Knowledge Accrual mechanisms, specifically the synthesized lexical guard and the test harness around `daemon_knowledge_accrual`, experienced false-positives and isolation leaks. Lexical guards using naive substring matching flagged permitted words like `depict` because they contained `epic`. Additionally, node lifecycle tests that triggered the Plan phase did not mock `daemon_knowledge_accrual`, causing unauthorized modifications in the `kb/` directory during test runs.

## Root Cause
1. `check_content` in `tests/test_lexical_guard.py` used `if word in content_lower:`, failing to respect word boundaries.
2. `kernel/node_lifecycle.py` invokes `run_kb_check` in the Plan phase, which tests in `tests/test_node_lifecycle.py` invoked without a `@mock.patch` for `run_kb_check`.

## Remediation
- **Node 978/979**: Initialized Dual-Discovery and formulated the Implementation Blueprint for Path 977.
- **Node 981**: Refactored `check_content` to use regular expressions with word boundaries (`\b`), eliminating substring-based false positives. 
- **Node 1294**: Added `@mock.patch("kernel.daemon_knowledge_accrual.run_kb_check")` to relevant node lifecycle tests to seal the mocking breach and ensure hermetic test execution.
- **Node 1441**: Audited and confirmed sufficient test coverage for the knowledge accrual module.

## Structural Invariants Reinforced
- **Lexical Guard Specificity**: Lexical restrictions must use word boundaries or precise token extraction, avoiding raw substring logic.
- **Mocking Hermeticity**: Test suites invoking any phase of the Node Lifecycle (like Plan) MUST mock daemon operations (like `run_kb_check`) that alter physical artifacts in the `kb/` directory, preventing unintended side effects during CI.
