# GEMINI (Antigravity) Agent Configuration

**Read `AGENT.md` immediately.** It contains all universal instructions: the SPAOR execution loop, invariants, registries, chat protocol, and support line.

This file contains only Gemini/Antigravity-specific overrides.

## Antigravity-Specific: Background Daemon Setup
During the Bring-Up Process (AGENT.md §2, Step 5), use your `schedule` tool to establish background cron jobs:
- Set `CronExpression` according to `infra/audit-daemon/audit_config.yml` (e.g., `*/5 * * * *`)
- Set `Prompt="Run ./skills/audit_daemon.py"`

## Antigravity-Specific: Asynchronous Execution
For AGENT.md §5 Rule 19 (Asynchronous Execution Invariant), use the `run_command` tool for background bash tasks and the `schedule` tool for timers. The Agent's conversational turn must function exclusively as an "I am ready for the next prompt" signal while work completes silently in the background, waking the Agent via system callbacks. The Agent must never halt execution by yielding without a pending background task or timer, as this causes the Agent to become stuck.

<!-- Testing True Hotfix -->

<!-- CONTEXTUAL_ROM_INJECTION_START -->
<!-- CONTEXTUAL_ROM_INJECTION_END -->
