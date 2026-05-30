# WHAT-0064: Dynamic Agent Identity Resolution Specification

## 1. Definition & Intent
To prevent conflicts on the `main` branch due to hardcoded, git-tracked `agent_id` values in configuration files (e.g. `dyad-wu-wei.yml`), the system must dynamically resolve the identity of the executing agent at runtime.

## 2. Resolution Mechanism
The agent identity must be resolved using the following order of precedence:
1. **Environment Variable**: Check for the presence of the `SPAO_AGENT_ID` environment variable. If set, use its value.
2. **Directory Basename Fallback**: Extract the basename of the active workspace directory (e.g., `/mnt/shared_data/git_repos/agent-SG2-auto` -> `agent-SG2-auto`), sanitize it to lowercase kebab-case (e.g., `agent-sg2-auto`), strip any `-auto` suffix to yield `agent-sg2`, and use it if it matches the agent ID pattern (`agent-[a-z0-9]+`).
3. **Default / None Fallback**: If neither source resolves to a valid agent ID, fall back to `None`.

## 3. Configuration Invalidation
The configuration field `agent_id` inside `dyad-wu-wei.yml` must not be hardcoded or tracked in Git. Instead, the `load_engine_config()` loader function in `drivers/path_resolver.py` must invoke the dynamic identity resolution helper and inject the resolved `agent_id` dynamically into the loaded configuration.
