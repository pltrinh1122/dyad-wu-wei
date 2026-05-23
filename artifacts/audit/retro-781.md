# Retro 781: CLI Execution Failures (Persona Gate and Arguments)

## 1. Incident Overview
During the execution of Node 781, two `bin/node` execution failures occurred due to strict invocation requirements being omitted by the agent.

## 2. Telemetry Traces
1. **Persona Gate Blocked**:
   ```
   Exception: Persona Gate Blocked: SPAO_PERSONA_ID environment variable is absent. Cannot verify identity.
   ```
   *Cause*: Executed `./bin/node plan-start 781` without the mandatory `SPAO_PERSONA_ID="frontier"` environment variable.
2. **Missing Checkout Argument**:
   ```
   daemon_node.py checkout: error: the following arguments are required: branch_name
   ```
   *Cause*: Executed `./bin/node checkout 781` without specifying the target `branch_name`, which is a required argument for this CLI tool.

## 3. Structural Root Cause
The agent attempted to invoke `bin/node` CLI adapters from memory without first explicitly running the `--help` flag or cross-referencing the required environment variables mandated by the new Persona Gate rules.

## 4. Codified Insight
When invoking SPAO orchestration commands (`bin/node`), the `SPAO_PERSONA_ID="frontier"` environment variable MUST be exported. Additionally, the agent must verify CLI arguments using `--help` if the signature is not explicitly known.
