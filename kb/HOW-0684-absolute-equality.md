# HOW-0684: Implementing Absolute Equality of Execution

## 1. Objective
This document outlines the technical implementation plan for enforcing "The Absolute Equality of Execution (No God-Mode)" as specified in `WHAT-0684`. The goal is to structurally guarantee that no node execution bypasses standard SPAO state validations, regardless of its domain or administrative intent.

## 2. Technical Directives

### 2.1. Eradication of Meta-Bypass Logic
The execution kernel and CLI tools must be swept for any logic that short-circuits validation based on node metadata. 
- **Prohibited Patterns**: `if 'docs' in issue.title: skip_tests()`, `if 'administrative' in labels: bypass_hitl()`.
- **Action**: All validations in `kernel/node_lifecycle.py` and `bin/node` must run unconditionally. If an administrative task has no tests, the test runner itself must gracefully return success (e.g., `pytest` passing with 0 tests or 0 failures), rather than the pipeline explicitly skipping the test step.

### 2.2. HTIL Spec-First Inversion Clarification
The autonomous bypass of the HTIL block (as established in `HOW-0993`) is not a "God Mode." It is a structurally sound rule where the Sluice Gate formally pre-approves the merge logic if the PR is purely administrative/documentation and strictly complies with the original intent. 
- **Action**: Ensure that the `is_administrative()` classifier in `kernel/node_lifecycle.py` only changes the *merge authority* (from Operator to Agent) but does NOT skip any execution steps (Plan, Checkout, Act, Reflect, Tests).

### 2.3. Sluice Gate Equality
Every execution request must originate from a GitHub issue. No local "shadow nodes" or in-memory execution states are permitted.
- **Action**: The `node checkout` script must assert the physical existence of the remote GitHub issue and refuse to operate on ad-hoc branch names or manual IDs that do not exist in the ledger.

## 3. Implementation Plan
1. **Code Audit**: Review `kernel/node_lifecycle.py` and `bin/run-tests` to ensure no "God-Mode" branches exist that skip the test runner or Sluice Gate validation.
2. **Test Runner Resilience**: Ensure `./bin/run-tests` executes cleanly even on branches that only modify `.md` files, so that it does not falsely fail the pipeline and tempt future bypasses.
3. **Validation**: Execute administrative and payload nodes back-to-back to verify identical execution logging and gate enforcement.
