# 1613 Harmonization: Implement PR Discipline Formalization

## Philosophical Intent
In the pursuit of Wu-wei autonomy, the Agent must act as a reliable cognitive offloader for the Operator. Previously, the Agent could finalize a node and throw a Pull Request over the wall without verifying its stability. This violates the trust invariant, as it shifts the burden of base-level CI validation back onto the Operator. 

To formalize the PR discipline, the Agent must proactively execute the local test suite and ensure no merge conflicts exist *before* informing the Operator or entering the HARD HITL (Human-in-the-loop) wait state. The Agent should not require the Operator to tell it to run tests; it must be an intrinsic, automated part of the `reflect` lifecycle.

## Technical Harmonization
1. **Automated Pre-flight Checks**:
   - The `spao node reflect` command MUST automatically trigger `spao test` (or `./bin/run-tests`) prior to committing and pushing the branch.
   - If tests fail, the reflection sequence MUST abort, forcing the Agent to remediate the errors in the `Act` phase rather than proceeding to `Reflect`.
2. **Current State**:
   - We observed that `daemon_node.py` successfully intercepts the `reflect` command, runs `pytest`, and conditionally blocks reflection on failure.
   - The formal codification of this discipline into the agent's core rule-set ensures future Dyad instantiations inherit this robust behavior.
3. **Next Steps (Node 1614 Plan)**:
   - Identify if any remaining guardrails are missing (e.g. merge conflict validation before pushing).
   - Update `kb/` documentation or `DYAD.md` guidelines if they do not yet fully articulate this strict invariant.
