# Retro Node 607: Probe 607: Plan - Exclude Locked Nodes from NBA Path Continuation

## Failure Mode
The test suite failed locally with exit code 1 during the Plan (TDD) execution phase.

## Root Cause
This failure was intentional and expected. Following strict Test-Driven Development (TDD) practices under the SPAO loop, the unit tests were formulated to assert correct filtering behavior for actively locked nodes. They successfully failed because the underlying logic in `gh_graph_skill.py` has not yet been implemented (which is the goal of the Act phase).

## Remediation / Lesson Learned
The offline test harness is successfully capturing the bug, fulfilling the goal of the Plan Probe. We will proceed to the Act Activity to implement the fix.

## Policy Update
No policy update is required. Intentional TDD failure successfully validated the test harness.
