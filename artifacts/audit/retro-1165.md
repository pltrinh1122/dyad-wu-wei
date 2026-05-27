# Retrospective: Node 1165

## 1. Description of Failure
During the `plan-finish` phase of Node 1165, the helper script ran the `bin/node plan-finish` command with a replaced environment dictionary (`env={'SPAO_PERSONA_ID': 'frontier'}`). This wiped out the parent environment context (like `PATH`, `HOME`, and other system variables), causing `gh` to fail with exit status 4.

## 2. Root Cause Analysis
The Python subprocess call in the helper script passed a custom dictionary directly to `env`, which replaces the entire environment in Python subprocesses instead of merging. Consequently, the GitHub CLI executable was unable to locate configuration or authentication info.

## 3. Corrective Action
The helper script was corrected to inherit the parent environment dictionary using `env = os.environ.copy()` and then merge `SPAO_PERSONA_ID` into it. Subsequent planning ran successfully.
