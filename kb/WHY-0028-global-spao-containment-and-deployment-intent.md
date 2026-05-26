# WHY-0028: Global SPAO System Containment, Deployment, and CLI Integration

## Context & Rationale
Our SPAO (Sense-Plan-Act-Observe) loop orchestrator is currently confined to the `dz-cil` repository itself. However, to operate as a general-purpose agent across other projects that use the `antigravity` (`agy`) CLI, we need a mechanism to contain, deploy, and execute the SPAO orchestrator globally. 

We need a design that allows:
1. **Global availability**: Invoking SPAO tools (like `node`, `backlog`, `prompt`) from any arbitrary project repository.
2. **Contextual awareness**: Dynamically targeting the current working directory (CWD) of the active project repository (resolving local `node.yml`, `artifacts/`, etc.).
3. **Simplicity of updates**: Ensuring bug fixes and enhancements made to the main SPAO codebase automatically propagate without requiring manual rebuilds or updates in every project.

---

## Architectural Options

### Option 1: Symbolic Linkage (`~/spao/` linking to main codebase)
- **Concept**: Maintain the core SPAO codebase in a central repository (e.g. `~/src/spao`). Provide a global wrapper script or symlink the binaries (e.g. `bin/node` -> `~/spao/bin/node`) into the user's path, configured to dynamically evaluate dependencies and resolve target paths relative to the current project's root.
- **Pros**:
  - Extremely easy to update (single `git pull` in the central repository).
  - Minimal footprint and zero overhead.
- **Cons**:
  - Requires dynamic resolution of paths (e.g. the CLI scripts must locate python modules and configuration relative to the central repo, but target artifacts relative to the active target project).

### Option 2: Python Package / Distribution (`pipx` or `pip install -e`)
- **Concept**: Package the SPAO orchestrator as a standard Python package. Installation via `pipx` or `pip install -e .` exposes `node`, `backlog`, and `prompt` as global commands.
- **Pros**:
  - Standardized installation and version pinning.
  - Clean separation of execution logic.
- **Cons**:
  - Slightly higher setup complexity.
  - Editable mode (`-e`) is required to preserve live code updates without reinstalling.

### Option 3: Containerized Wrapper (Docker/Podman)
- **Concept**: Build a container image containing the SPAO runtime. Provide a shell script wrapper that mounts the host target project into the container.
- **Pros**:
  - Complete dependency isolation.
- **Cons**:
  - Substantial execution overhead.
  - Complicates credentials/SSH key forwarding and git worktree access on the host system.

---

## Evaluation Matrix

| Vector | Option 1 (Symlink) | Option 2 (Python Package) | Option 3 (Container) |
| :--- | :--- | :--- | :--- |
| **Ease of Propagation** | ⭐️⭐️⭐️ (Instant via git pull) | ⭐️⭐️ (Requires rebuild/reinstall) | ⭐️ (Requires image rebuild) |
| **Path Isolation** | ⭐️⭐️ (Requires careful path management) | ⭐️⭐️⭐️ (Standard packaging) | ⭐️⭐️⭐️ (Complete isolation) |
| **Invocation CWD Awareness**| ⭐️⭐️ (Shell script resolves target CWD) | ⭐️⭐️⭐️ (System resolves automatically) | ⭐️ (Requires volume mounts) |
| **Implementation Complexity**| ⭐️⭐️⭐️ (Very simple shell wrappers) | ⭐️⭐️ (Requires setup.py/pyproject.toml) | ⭐️ (Complex mounting/credentials) |

---

## Proposed Direction

We will pursue a **Hybrid Linkage & Python Package** architecture (combining elements of Option 1 and Option 2):
1. **Central Codebase**: Maintain a single source of truth repository.
2. **Path Resolution Refactoring**: Update CLI entry points to separate the *Execution Path* (where Python scripts and dependencies reside) from the *Target Workspace Path* (where `artifacts/`, `node.yml`, and `git` commands should be executed).
3. **Global Linker Script**: Provide a bootstrap installer that establishes a `~/spao` bin directory or symlinks globally, forwarding calls to the active project context.

## Next Steps

1. **Probe 356 (Align)**: Align on the deployment options (this document).
2. **Probe 357 (Plan)**: Specify the path-resolution changes and wrapper scripts (`WHAT-xxxx`).
3. **Activity 358 (Reflect)**: Conclude research outcomes and implement/prune.
