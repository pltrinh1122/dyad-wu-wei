# WHAT-0010: PR Discipline and Universal Test Gates

## 1. The Core Principle
The Dyad framework mandates that no codebase mutation shall be deployed to the `main` trunk without rigorous local testing. This is the **PR Discipline Invariant**. 

## 2. Structural Ingraining
To prevent human or agentic errors (e.g. bypassing test scripts before cutting a PR), this invariant is ingrained into the deployment engines themselves:
- `kernel/node_lifecycle.py` (`reflect`): Synchronously executes `spao test` before opening a Node PR.
- `kernel/daemon_rt.py` (`hotfix`): Synchronously executes `spao test` before opening a Tier-2 Hotfix PR.
- `kernel/daemon_rt.py` (`insight`): Synchronously executes `spao test` before opening an Insight PR.

## 3. The Failing Fast Axiom
If the test suite emits a non-zero exit code during any of the above operations, the materialization pipeline MUST immediately halt and trigger a `[🚫 BLOCKED]` failure. The PR must NOT be created, and the branch must NOT be pushed if it violates the local test assertions.
