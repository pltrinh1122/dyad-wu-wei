# Infrastructure State Ledger

This document mathematically tracks the physical state of the Host OS infrastructure and daemons provisioned by the `agent-antigravity` system.

## Active Daemons

| Daemon Name | Type | Status | Provisioning Script | Description |
| :--- | :--- | :--- | :--- | :--- |
| `github-runner` | `systemd_user` | Pending | `infra/github-runner/provision.sh` | Local Pre-Merge CI verification. |

## Daemon Governance
The Agent must use `skills/infra_manager.py` to programmatically interact with these daemons.
