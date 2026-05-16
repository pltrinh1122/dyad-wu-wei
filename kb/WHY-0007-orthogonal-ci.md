# WHY-0007: Orthogonal CI vs Local Harness

**Date:** 2026-05-16
**Status:** Accepted

## Context
During the materialization of the testing infrastructure, we built `skills/testing_harness.py`. This skill encapsulates the local `.venv` and allows the Agent to natively execute and parse `pytest` output during the SPAO loop. However, as the repository scales, we require an enterprise-grade cloud gatekeeper (GitHub Actions). 

## Options Considered
1. **CI Uses Local Harness:** GitHub Actions is configured to execute `python skills/testing_harness.py`. This breaks because GitHub runners manage their own global python state via `actions/setup-python` and do not utilize a local `.venv` directory.
2. **Harness is CI-Aware:** The testing harness checks for `GITHUB_ACTIONS=true` and alters its execution path. This violates orthogonality, adding unnecessary complexity to an Agent skill.
3. **Strict Orthogonality:** The testing harness remains exclusively an *Agentic Local Tool*. GitHub CI runs a completely decoupled, raw `pytest` pipeline in the cloud.

## Decision
We decided to adopt **Option 3: Strict Orthogonality**.

## Rationale
Agentic tools (Skills) are built to bridge the gap between complex shell constraints and LLM execution. Cloud CI pipelines (GitHub Actions) are declarative, pristine environments that do not suffer from the same cognitive constraints as an Agent. By strictly decoupling them, the Agent can use its bespoke harness for rapid local iteration, while the repository relies on the un-abstracted, industry-standard `pytest` command as its ultimate cloud verification gatekeeper.
