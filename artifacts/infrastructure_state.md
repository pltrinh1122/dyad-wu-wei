# Infrastructure State Ledger

This document mathematically tracks the physical state of the Host OS infrastructure and daemons provisioned by the `dyad-wu-wei` system.

## Active Daemons

| Daemon Name | Type | Status | Provisioning Script | Description |
| :--- | :--- | :--- | :--- | :--- |
| `github-runner` | `systemd_user` | Pending | `infra/github-runner/provision.sh` | Local Pre-Merge CI verification. |
| `audit-daemon` | `agy_schedule` | Active | Agent Managed | Modular rules engine for automated repository health and prompt injection. |

## Daemon Governance
The Agent must use `drivers/infra_manager.py` to programmatically interact with these daemons.

## Managed Artifacts

| Artifact | Path | Provisioned By | Description |
| :--- | :--- | :--- | :--- |
| `ci-venv` | `~/actions-runner/venv/` | `infra/github-runner/provision.sh` | Pre-baked Python venv for zero-network CI execution. Contains pinned packages from `requirements-dev.txt`. |

## Operator Duties
- **On `requirements-dev.txt` change**: Re-run `infra/github-runner/provision.sh` to refresh the `ci-venv`. CI will fail loudly (import error) if this is skipped, ensuring the failure is never silent.
