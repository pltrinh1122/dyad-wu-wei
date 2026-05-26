# WHY-0929: Architectural Decision Record for the DZ-CIL Bootstrap Installer

## Classification
- **Type**: WHY (Architectural Decision Record)
- **ID**: WHY-0929
- **Author**: agent-frontier
- **Created**: 2026-05-24 (Node 929, Path 928)
- **Related Path**: Path 928 (Implement DZ-CIL Deployment and Bootstrap Installer)

---

### 1. Context & Design Tension

The Operator requested a deployment playbook/script to install a new DZ-CIL deployment to start working on a project under the Model 1 Workspace architecture (see [WHY-0921](file:///mnt/shared_data/git_repos/dz-cil/kb/WHY-0921-dz-cil-workspace-architecture.md)).

We must establish:
1. A clear separation from the legacy `spao-install` script, which is left alone as it belongs to the old-Dao Model 2 full-runtime deployment framework.
2. A lightweight, robust mechanism to bootstrap a new child project workspace under Model 1.
3. Automatically configure the required target directories: `./.workspace/kb/`, `./.workspace/artifacts/`, and `./.workspace/GEMINI.md`.
4. Ensure the parent core engine operates in a secure **read-only** mode while the nested workspace has full read/write/push authority.

---

### 2. Evaluated Options

#### Option A: Self-Contained Bash Installer Script (`bin/dz-cil-install` / `bin/dz-cil_install.sh`)
* **Mechanism**: A dedicated shell script that runs from the parent root. It initializes `./.workspace/`, creates the required directories (`kb/`, `artifacts/`), writes a template-based `GEMINI.md` to the workspace root, and configures a workspace-specific virtual environment (`.venv/`) with the required python dependencies (`pytest`, `pytest-mock`, `pyyaml`).
* **Pros**: Idempotent, executable outside the python context, easily whitelisable in operator environment guards.
* **Cons**: Introduces bash-specific script overhead.

#### Option B: Python-Integrated Workspace Bootstrapper (`bin/workspace bootstrap`)
* **Mechanism**: Write the initialization logic inside the existing `kernel/daemon_workspace.py` workflow, triggered by a new CLI subcommand (e.g. `./bin/workspace bootstrap`).
* **Pros**: Type-safe, cross-platform file manipulation using Python's standard library.
* **Cons**: Requires Python virtual environments and packages to be fully functional *prior* to running the bootstrapper.

---

### 3. Selection & Architectural Rationale

We select **Option B** (`bin/workspace init`).

* **Reasoning**: The original selection of Option A (`bin/dz-cil-install`) was a systemic failure. The bash script provisioned the target directory with folders and virtual environments *before* the python script attempted to run `git clone`. This created a fatal sequence bug where Git would abort because the directory was not empty. Furthermore, forcing the Operator to run two fragmented scripts (`bin/dz-cil-install` followed by `./bin/workspace init`) introduced unnecessary manual friction that violates the Wu-wei Gate.
* **Dialectical Falsification**: The assumption that a bash `curl` script was the optimal entry point was falsified. For the current Operator who already possesses the local core engine, invoking the Python wrapper (`./bin/workspace init`) directly is completely frictionless and allows us to guarantee the exact sequence of initialization (Clone -> Provision -> Inject GEMINI.md) in a type-safe manner. The legacy Bash script has been fully deprecated and removed.
* **Model 1 Workspace Redirection**: The created `./.workspace/GEMINI.md` will explicitly declare the workspace-specific invariants, directing the Agent to run exclusively within the local `./.workspace/` directory and treating the parent engine as read-only.
* **Directory Layout Invariance**: The python bootstrapper enforces the creation of `./.workspace/kb/` and `./.workspace/artifacts/` folders to isolate state-machine logs and prevent parent-level contamination.
