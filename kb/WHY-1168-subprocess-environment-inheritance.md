# WHY-1168: Subprocess Environment Inheritance Doctrine

## 1. Context and Incident
During the execution of Node 1165, a python orchestration script triggered a `gh` subprocess command using `subprocess.run(..., env={'SPAO_PERSONA_ID': 'frontier'})`. By passing a raw dictionary directly into the `env` parameter, the parent system environment was entirely overwritten, eradicating critical configuration paths such as `PATH`, `HOME`, and `XDG_CONFIG_HOME`. Consequently, the `gh` subprocess failed with exit status 4 because it could not locate its authentication tokens or executable dependencies.

## 2. Core Assertion
When an agent or script delegates logic to a subprocess, the subprocess is functionally an extension of the parent context. Erasing the parent context induces isolation failure where tools operating in the subprocess are blinded to the container's systemic configuration.

## 3. The Required Pattern
To durably prevent downstream configuration failures, all Python orchestrator scripts (`drivers/`, `kernel/`, `bin/`) that inject localized environment variables MUST inherit and merge from the parent environment, rather than replacing it.

**Forbidden Pattern (Overwrites Environment):**
```python
subprocess.run(["gh", "issue", "view", issue_id], env={'SPAO_PERSONA_ID': persona})
```

**Required Pattern (Inherits and Merges):**
```python
import os
import subprocess

env = os.environ.copy()
env['SPAO_PERSONA_ID'] = persona
subprocess.run(["gh", "issue", "view", issue_id], env=env)
```

## 4. Enforcement
By codifying this rule, we align with the principle of Temporal Immutability (WHAT-0001 §2.3) by ensuring the runtime state is deterministically inherited. The semantic immune system should flag instances of `env={...}` in `subprocess` calls as architectural violations.
