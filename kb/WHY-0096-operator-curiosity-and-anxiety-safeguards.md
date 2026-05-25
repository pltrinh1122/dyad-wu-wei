# WHY-0096: Managing Operator Curiosity and Emotional Turbulence

## Context
During operations, the human-agent dyad is highly sensitive to information signals. When a test run returns skipped tests, it can trigger cognitive or emotional friction in the Operator—who may interpret any non-passing test metric as an active failure, structural regression, or alignment gap (Turbulence). 

This document codifies the operational distinction between **Operator Curiosity** and **System Turbulence** (as defined in [WHAT-0079](file:///mnt/shared_data/git_repos/agent-antigravity/kb/WHAT-0079-ziran-flow-riverbed-framework.md)), and defines the guidelines and safeguards for managing Operator anxiety without degrading system efficiency or introducing communication bloat.

## 1. Defining the Boundary: Curiosity vs. Turbulence

To maintain stable, low-energy communication (SG-0004), the Agent and Operator must clearly distinguish between system errors and environment-specific constraints:

*   **System Turbulence (Friction)**: Genuine operational or logic failures (e.g., failed test assertions, runtime crashes, command execution failures). These indicate that the system's invariants are broken, requiring immediate remediation.
*   **Operator Curiosity (Scope Boundaries)**: Expected, environment-specific variations (e.g., skipped tests, bypassed optional configurations, soft-locking warnings). These do not represent a failure of the codebase, but rather the system's adaptation to its current environment (such as running tests in a generic CI environment without persona keys).

Trying to treat expected scope boundaries as failures and attempting to force their elimination (e.g., removing skips) is a form of artificial forcing (*wei*), which increases total system friction.

## 2. Rules for Managing Curiosity and Bypasses

To prevent unnecessary communication loops and reassure the Operator, the following rules apply:

### Rule 2.1: The Diagnostic Separation Principle
The system's default state monitoring must remain highly concise, focusing on a clean signal-to-noise ratio. Verbose explanations of routine skips or environmental bypasses must be separated from default outputs:
1.  **Default Output (Clean Monitor)**: Keep metrics clean and consolidated (e.g., `246 passed, 1 skipped`). 
2.  **Diagnostic Channel (On-Demand Audits)**: Detailed rationale for skipped steps or optional bypasses must be accessible on-demand via standard diagnostic flags (such as passing the `-rs` flag to the test-runner).

### Rule 2.2: Operator Safeguard Protocols
When the Operator expresses concern over bypassed checks or skipped tests:
1.  **Check Context First**: The Operator should utilize standard diagnostic flags (e.g., the `-rs` flag on the test-runner) or inquire about the specific skip reasons before concluding that the system is broken.
2.  **Clear Agent Reporting**: If asked about a skipped test in chat, the Agent must explain the exact environmental pre-conditions required for the test to run, showing that the bypass is expected and safe. And the Agent should proxy the command should it infer the Operator's actual intent is curiosity (e.g. running the test suite with `-rs` to fetch and present the exact skip reason inline).
3.  **Preventive Documentation**: Any conditional bypass or test skip in the codebase must be documented inline with a clear, operator-readable explanation in the test's `pytest.skip()` or skip decorator string (see the example in [TestOwnershipIndex](file:///mnt/shared_data/git_repos/agent-antigravity/tests/test_ownership_index.py#L114-L123)).

## Rationale

*   **Wu-wei (Lowest Energy)**: Flooding the Operator's screen or chat logs with explanations for every expected bypass on every run increases cognitive load and noise. Separating clean monitoring from verbose diagnostics allows the dyad to focus attention only on genuine failures (aligned with [HOW-0006](file:///mnt/shared_data/git_repos/agent-antigravity/kb/HOW-0006-decision-making-invariant.md)).
*   **Ziran (Coherence with Environment)**: Standard diagnostic tools (like `-rs` for reporting test skip reasons) are native to the testing substrate. Utilizing these native capabilities on-demand is more coherent and robust than inventing custom reporting templates or forcing tests to pass artificially via complex mocks.
