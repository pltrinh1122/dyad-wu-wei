# HOW-0696: Technical Plan for Temporal Immutability

## 1. Objective
This document outlines the technical mechanisms for enforcing "Temporal Immutability" as codified in `WHAT-0696`. The system must guarantee that active nodes represent an unbroken, collision-free timeline from `checkout` to `reflect`.

## 2. Technical Directives

### 2.1. Strict Rebase Enforcements
- **Pre-Reflection Check**: Before a Node can successfully close and merge during the `reflect` phase, it MUST verify that its upstream parent (`main`) has not diverged from its starting context. 
- **Implementation**: `bin/reflect` (or the underlying git layer it uses) must automatically fetch the latest `main`. If `main` is ahead of the `checkout` commit, the merge should either automatically rebase the `node/*` branch or securely pause and mandate the Agent handles the integration via `git rebase` prior to `reflect`.

### 2.2. OOB Commit Deflection
- **Continuous Polling**: The audit daemons MUST ensure that while `WIP-N=1` is true, no rogue commits hit `main`. If they do, the daemon signals a "seizure" event to alert the Agent.
- **Implementation**: The `active_node` state parser in `bin/status` should emit a warning if `main` has progressed past the `checkout` hash of the active node.

### 2.3. Agent Level Directives
- **Instruction Injection**: Add an invariant to `DYAD.md` strictly prohibiting the Agent from opening concurrent shells or sub-agents that attempt to alter `main` behind the back of the actively running node lock.

## 3. Implementation Steps
1. **Inject Directive into DYAD.md**: Add explicit language stating the Agent must not bypass the Node Lock timeline via direct CLI git pushes or out-of-band pull requests.
2. **Review bin/reflect mechanisms**: Ensure `bin/reflect` requires a clean merge path. If it relies on GitHub's API (`gh pr merge`), GitHub inherently enforces this if branch protection rules are set correctly. Document that the repository's branch protection MUST require branches to be up-to-date before merging.
