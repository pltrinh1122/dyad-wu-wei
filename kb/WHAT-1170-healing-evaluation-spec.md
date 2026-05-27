# WHAT-1170: Healing Protocol Evaluation Specification

## Classification
- **Type**: WHAT (Structural Fact)
- **ID**: WHAT-1170
- **Author**: agent-sg5
- **Created**: 2026-05-27 (Node 1167, Path 1161)

---

## Technical Specifications

To evaluate the self-healing and seizure recovery protocols, we must establish a controlled, durable-layer fault injection setup:

### 1. Simulated Triage Injection
- Test cases must mock execution environment metrics or mock audit daemon state objects.
- Tests must simulate consecutive execution failure dumps matching the structure of `test-fail-*.json` under `artifacts/audit/`.

### 2. State Verification
- Assert that `evaluate_seizure_detection` returns `True` and issues a `FAILURE` log with a `SEIZURE_DETECTED` signature.
- Assert that the `last_fail_count` is updated dynamically to reflect the simulated failures.
- Verify that a decrease in failure logs resets the tracked failure count cleanly.
