# WHAT-1836: Alignment on CSI Guards vs Mechanism Guards

## 1. Intent
Address the Operator's concern regarding Local CI latency. The test suite execution and continuous validation checks (mechanism guards) have become heavy. With the recent formalization of Asymmetric CSI (Cybernetic Steering Invariant) Guards (e.g., the HTIL lock), we can rely on structural blockers rather than exhaustive symptomatic testing.

## 2. The Problem: Local CI Latency
Local CI (e.g., `bin/run-tests` invoked during `bin/node reflect`) validates the entire system state, which has historically taken a long time to complete (as referenced in PR #1794). Many of these tests are "symptomatic guards"—unit tests that try to catch downstream symptoms of invariant breaches rather than enforcing the invariant at the structural gate.

## 3. Definitions
- **True Invariant Guards (CSI Guards)**: Structural mechanisms that physically block invalid execution at the entry point (e.g., checking for `HTIL_ACTIVE.lock`). These are computationally cheap $O(1)$ operations.
- **Symptomatic Guards (Mechanism Guards)**: Exhaustive test suites or daemons that scan the codebase or state space $O(N)$ to ensure no symptoms of a breach exist.

## 4. The Strategy: Falsify and Implement Survivor
1. **Falsification**: Identify symptomatic tests (e.g., tests that mock complex flows just to check if an API was called) that are rendered obsolete by a CSI Guard.
2. **Pruning (The Survivor)**: Strip down the mechanism guards. Only the true invariant guards should survive the cull. This reduces the CI load and accelerates the SPAOR execution loop velocity.

## 5. Next Steps for Implementation (Plan Phase)
1. Audit the `tests/` directory to identify high-latency or redundant symptomatic guards.
2. Determine which tests can be safely removed because an upstream CSI Guard mathematically prevents the state they are testing for.
3. Execute the falsification (removal) of these tests.
