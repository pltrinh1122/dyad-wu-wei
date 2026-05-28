# WHY-1031: Telemetry Logging Visibility Remediation Plan

## Classification
- **Type**: WHY (Architectural Decision Record)
- **ID**: WHY-1031
- **Author**: agent-sg5 (SG-0005: Autonomous Knowledge Accrual)
- **Created**: 2026-05-28 (Node 1031, Path 1029)
- **Depends on**: WHY-1030
- **Context**: Detailing the design plan to fix telemetry logging visibility by modifying output buffering behavior.

---

## 1. Remediation Objective

The scoping audit in `WHY-1030` identified that telemetry events are buffered during background execution.
The objective of this plan is to define the exact code change and test cases required to resolve this buffering behavior. This change will be implemented in the subsequent node (`Node 1032: Activity 1032: Reflect - Fix Telemetry Logging Visibility`).

---

## 2. Technical Remediation Plan

### 2.1 Code Modifications (`kernel/node_lifecycle.py`)
Modify `log_stage_advancement` to guarantee that all console/file output is immediately flushed:
- Replace standard `print(message)` calls with `sys.stdout.write(message + '\n')` followed by a direct invocation of `sys.stdout.flush()`.

### 2.2 Test Additions (`tests/test_node_lifecycle.py`)
Create unit tests to verify flushing behavior:
- Verify that `log_stage_advancement` executes `sys.stdout.write` and `sys.stdout.flush`.
- Stub `sys.stdout` to capture writes and verify that a flush action occurs synchronously with the write call.

---

## 3. Verification Post-Requisites
Remediation actions in Node 1032 must pass:
1. The TDD pytest suite containing the new stdout logging test cases.
2. Zero functional logic regressions across all other domain managers.
