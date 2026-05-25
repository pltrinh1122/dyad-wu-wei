# WHY-1058: Workspace Isolation Audit & Next Steps

## Context
During Path 1054, the Metasystem conducted an empirical assessment of the Model 1 (Dual-Context Workspace) installation flow. The Operator's objective was to initialize a new Workspace at an arbitrary local path (`/mnt/shared_data/dzw`) and seamlessly launch the SPAO loop using the `agy` bootloader.

## Epistemic Audit (User Research Findings)
Through manual execution observation, the system identified two fundamental architectural violations of Wu-wei (effortless flow) and Ziran (natural inference):

1. **The Arbitrary Path Violation**: The initialization mechanism (`kernel/daemon_workspace.py:init_workspace`) hardcodes the child workspace target path to `<parent_engine_root>/.workspace`. It completely ignores Operator-defined target directories, enforcing a rigid nested structure that prevents independent workspace deployment.
2. **The Auto-Inference Failure**: The system's agent bootloader (`agy`) lacks the situational awareness to passively detect if it is running inside a Model 1 Workspace. It requires the Operator to explicitly declare `SPAO_WORKSPACE_DIR` as an environment variable before boot. Without this explicit manual declaration, the Agent spawns in Global Engine Mode, even when spawned directly inside a workspace directory containing a valid `GEMINI.md`.

## Architectural Mandate (Next Steps)
To correct these violations, a subsequent implementation Path MUST be initialized with the following objectives:
- **Refactor `init_workspace`**: Evolve the daemon to accept arbitrary absolute/relative target directory paths (e.g., `init_workspace(repo_url, target_dir)`).
- **Implement Bootloader Inference**: Refactor the initial invocation stack to automatically evaluate the Current Working Directory (CWD). If the CWD (or any of its parents) contains a valid Workspace `GEMINI.md`, the system must autonomously export `SPAO_WORKSPACE_DIR` dynamically to engage Model 1 Redirection seamlessly.
