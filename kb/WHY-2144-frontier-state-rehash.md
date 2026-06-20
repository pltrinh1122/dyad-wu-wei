# Epistemic Insight: Frontier State Manual Intervention

**Issue ID**: 2144
**Source**: `artifacts/audit/retro-2109.md`

## Context
During execution of Node 2109, the agent encountered an issue where the `frontier_state.yml` was out-of-sync with the GitHub locks, causing `plan-start` to fail with an "already in progress" error. When manually attempting to clean up the `frontier_state.yml`, the agent failed to update the checksum, causing subsequent execution failures.

## The Rule
The `artifacts/frontier_state.yml` file is cryptographically locked to prevent unauthorized tampering. 
- **DO NOT** manually edit `frontier_state.yml` using standard text-editing commands without repairing the checksum.
- **DO** run `bin/meta rehash` immediately after any manual, out-of-band edits to the `frontier_state.yml` file.

**Example of Correct Manual Intervention:**
```bash
# 1. Manually edit frontier_state.yml to purge a stuck lock
vim artifacts/frontier_state.yml

# 2. Repair the integrity checksum
bin/meta rehash
```

## Impact
Failure to repair the checksum after manual edits will trigger the system's tamper-protection mechanisms, completely halting all asynchronous and synchronous workflow executions.
