## Goal
Implement Spec-First HTIL Inversion (Anti-CI/CD Doctrine) bypassing Hard-HITL gates for Act nodes.

## Execution
- Modified `kernel/node_lifecycle.py` to auto-merge downstream nodes (e.g. Phase == `Act`) if they pass local CI verification, leveraging topological alignment achieved during the upstream `Plan` phase.
- Verified test suite passes (`tests/test_node_lifecycle.py`).
