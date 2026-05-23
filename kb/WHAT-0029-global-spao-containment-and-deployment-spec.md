# WHAT-0029: Global SPAO System Containment, Deployment, and CLI Integration Specification

## 1. Directory & Path Resolution Architecture

To run the SPAO system globally, we must separate the **SPAO Core (source code and modules)** from the **Active Workspace (target project repository)**. 

### 1.1 Core Environments
- **`SPAO_CORE_DIR`**: The absolute path to the directory containing the SPAO orchestrator clone. This is where Python modules (`kernel/`, `drivers/`) are located.
- **`SPAO_WORKSPACE_DIR`**: The active target repository root where files, ledgers, and backlog items are managed. Defaults to the closest parent directory containing a `.git` folder relative to the current working directory of invocation.

### 1.2 Path Resolution Mapping

All ledgers and configurations will be resolved dynamically relative to `SPAO_WORKSPACE_DIR`:

| File | Resolution Path | Description |
| :--- | :--- | :--- |
| `frontier_state.yml` | `os.path.join(SPAO_WORKSPACE_DIR, "artifacts", "frontier_state.yml")` | The project's active state ledger |
| `frontier_state.md` | `os.path.join(SPAO_WORKSPACE_DIR, "artifacts", "frontier_state.md")` | Human-readable log of node state |
| `prompt_backlog.yml` | `os.path.join(SPAO_WORKSPACE_DIR, "artifacts", "prompt_backlog.yml")` | The project prompt queue |
| `audit_state.json` | `os.path.join(SPAO_WORKSPACE_DIR, "artifacts", "audit_state.json")` | Metasystem audit record |
| `node.yml` | `os.path.join(SPAO_WORKSPACE_DIR, "node.yml")` | Project-specific status and classification mappings |

If a project does not contain a custom `node.yml`, the orchestrator will fall back to using the default `node.yml` template located in `SPAO_CORE_DIR`.

---

## 2. Unified CLI Interface: The `spao` Command

We will implement a unified `spao` script that acts as the single entry point for all SPAO actions.

### 2.1 Command Mapping

The unified CLI maps subcommands directly to their respective orchestrator entry points:

- `spao node [args]` ➔ `kernel.daemon_node`
- `spao backlog [args]` ➔ `kernel.daemon_backlog`
- `spao prompt [args]` ➔ `kernel.daemon_prompt`
- `spao rt [args]` ➔ `kernel.daemon_rt`
- `spao test [args]` ➔ `kernel.daemon_testing`

### 2.2 Wrapper Script Design

The global `spao` wrapper script will be placed in `~/.local/bin/spao` (or another directory in the user's `PATH`). It will contain:

```bash
#!/usr/bin/env bash
# Global SPAO CLI Entrypoint Wrapper

# 1. Locate Core SPAO Installation
SPAO_CORE_DIR="/mnt/shared_data/git_repos/agent-antigravity"

# 2. Resolve Active Project Workspace Root
if [ -n "$SPAO_WORKSPACE_DIR" ]; then
    WORKSPACE_ROOT="$SPAO_WORKSPACE_DIR"
else
    # Fallback to nearest git root
    WORKSPACE_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
    if [ -z "$WORKSPACE_ROOT" ]; then
        WORKSPACE_ROOT="$(pwd)"
    fi
fi

# 3. Export Environment Variables for Python modules
export SPAO_CORE_DIR="$SPAO_CORE_DIR"
export SPAO_WORKSPACE_DIR="$WORKSPACE_ROOT"

# 4. Route Subcommands
SUB=$1
shift

case "$SUB" in
    node)
        PYTHONPATH="$SPAO_CORE_DIR" python3 "$SPAO_CORE_DIR/kernel/daemon_node.py" "$@"
        ;;
    backlog)
        PYTHONPATH="$SPAO_CORE_DIR" python3 "$SPAO_CORE_DIR/kernel/daemon_backlog.py" "$@"
        ;;
    prompt)
        PYTHONPATH="$SPAO_CORE_DIR" python3 "$SPAO_CORE_DIR/kernel/daemon_prompt.py" "$@"
        ;;
    rt)
        PYTHONPATH="$SPAO_CORE_DIR" python3 "$SPAO_CORE_DIR/kernel/daemon_rt.py" "$@"
        ;;
    test)
        PYTHONPATH="$SPAO_CORE_DIR" python3 "$SPAO_CORE_DIR/kernel/daemon_testing.py" "$@"
        ;;
    *)
        echo "Usage: spao {node|backlog|prompt|rt|test} [options]"
        exit 1
        ;;
esac
```

---

## 3. Global Installation Tooling

We will create a simple, idempotent install utility `bin/spao-install` within the repository root.

### 3.1 Behaviors
1. Resolves the absolute path of the clone as `SPAO_CORE_DIR`.
2. Locates a suitable user bin folder in the path (e.g. `~/.local/bin/` or `~/bin/`).
3. Writes the `spao` wrapper script with the concrete `SPAO_CORE_DIR` path hardcoded.
4. Makes the script executable (`chmod +x`).

---

## 4. Verification & Testing Plan

### 4.1 Unit Tests
- Create a test `tests/test_path_resolver.py` that verifies:
  - Resolution of paths inside active workspace directories.
  - Correct fallback to default `node.yml` in `SPAO_CORE_DIR` if the target workspace lacks one.
  - Proper integration of `SPAO_WORKSPACE_DIR` environment variables.

### 4.2 Manual Verification
- Run `bin/spao-install` to globally register the CLI.
- Navigate to a completely separate git repository (e.g., `/tmp/test-project/`).
- Initialize a mock workspace (`git init`, create `artifacts/` folder, bootstrap a mock `frontier_state.yml`).
- Execute `spao node sync` and verify it runs successfully, modifying the local mock project and ignoring the core orchestrator's ledgers.
