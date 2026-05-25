# User Research: Workspace Installation and Setup (Model 1 Redirection)

## 1. Observation Context
- **Operator Persona**: Executing manual setup steps for a new workspace.
- **Goal**: Initialize a new project named "familyloom.app" in a custom directory (`/mnt/shared_data/dzw`).
- **Proposed Flow**: 
  1. Operator manually creates directory `/mnt/shared_data/dzw`.
  2. Operator prompts Agent to install and configure the Workspace project.
  3. Operator changes directory to `/mnt/shared_data/dzw` and launches `agy` to finish setup.

## 2. Friction Points & Bottlenecks Analysis

### Bottleneck 1: Hardcoded Path in `init_workspace`
The current implementation of `kernel/daemon_workspace.py:init_workspace` does not accept a custom target directory. It hardcodes the destination to `parent_root/.workspace` (i.e., nested inside the `agent-antigravity` repository).
- **Impact**: The Agent is physically incapable of satisfying the Operator's request to install the workspace at `/mnt/shared_data/dzw`. Execution will fail or silently initialize in the wrong location, breaking Wu-wei.

### Bottleneck 2: Missing Auto-Detection for `SPAO_WORKSPACE_DIR`
The Operator expects to simply launch `agy` inside the target directory. However, the system relies on the explicit declaration of `SPAO_WORKSPACE_DIR` to trigger Model 1 redirection.
- **Impact**: If the Operator forgets to export `SPAO_WORKSPACE_DIR=/mnt/shared_data/dzw`, the Agent will boot up in Global/Parent mode, completely oblivious to the child workspace's `GEMINI.md` or backlog. This violates Ziran, as the environment should passively infer its state from its surroundings.

## 3. Structural Recommendations
1. **Refactor `init_workspace`**: Modify the daemon to accept a `target_path` argument, defaulting to the current directory if unprovided, rather than forcing `.workspace/`.
2. **Auto-Inference Bootloader**: Update the agent bootloader or `bin/agy` wrappers to auto-detect a workspace if a `GEMINI.md` file declaring `Workspace Mode` is present in the Current Working Directory (CWD), seamlessly setting `SPAO_WORKSPACE_DIR=$PWD`.
