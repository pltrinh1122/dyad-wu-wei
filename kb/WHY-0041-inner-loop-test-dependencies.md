# WHY-0041: Architectural Rationale for Auditing and Hardening Inner-Loop Test Dependencies

## Context & Problem Statement
As the SPAO system grows and runs in diverse environments (such as isolated developer machines, sandboxed CI runners, or restricted offline testing environments), ensuring the hermeticity of the test suite is critical. If tests make undeclared external network or GitHub API requests, it leads to:
1. **Silent Failures**: Tests that pass in developer environments (which are authenticated and online) fail silently or crash non-deterministically in sandboxed or offline environments.
2. **Security & Data Leakage Risks**: External network requests in test suites can leak internal tokens, local repository paths, or metadata to public endpoints.
3. **Auditability Deficit**: Without a formal ledger mapping test dependencies, we cannot mathematically assert that a code change is safe to test offline.

## Decision
We establish a formal, audited baseline mapping the isolation status of every test file in the repository.

1. **Test Classification Ledger**: All tests must be categorized into either:
   - **Type A (Hermetic / Network-Isolated)**: Tests that run completely offline using mocks, fixtures, and local test-doubles.
   - **Type B (Network-Dependent)**: Tests that make real external network connections or live API calls (which should be minimized or deprecated).
2. **Automated Audits**: The test runner or compliance manager must enforce boundary limits to ensure new tests do not introduce unmocked network dependencies.

## Invariants & Guardrails
- **The Dependency Traceability Invariant**: Every test file must be documented in the technical specification (`kb/WHAT-0041-inner-loop-test-dependencies.md`) detailing its network dependency status.
- **Hermetic Baseline Enforcement**: All core unit and integration tests must remain 100% network-isolated (Type A). Any transition of a test file to Type B is prohibited unless explicitly approved in a strategic decision document.
