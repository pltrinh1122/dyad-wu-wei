# Epistemic Retrospective: Node 861

## The Failure
During the initiation of Node 861 (`plan-start 861`), the execution block occurred because the `SPAO_PERSONA_ID` environment variable was absent, triggering a Persona Gate failure.

## The Epistemic Insight
When executing node transitions under the persona governance rules (`WHY-0062`), the environment variable `SPAO_PERSONA_ID` must always be explicitly defined (e.g., `SPAO_PERSONA_ID="frontier"`) to authorize transition permissions. Running a bare lifecycle command will result in a gate rejection.

## The Remediation
We reran the `plan-start`, `plan-finish`, and `checkout` commands prepended with `SPAO_PERSONA_ID="frontier"`, which successfully authorized the transitions and established the active worktree.

## The Synthesis
The Persona Gate behaved exactly as specified in `WHY-0062` to prevent anonymous or incorrect agent identities from performing state mutations. Ensuring the environment carries the appropriate identity remains a critical loop invariant.
