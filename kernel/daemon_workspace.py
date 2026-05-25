import os
import json
import subprocess
from drivers import git_client
from drivers import path_resolver

def get_workspace_config_path() -> str:
    # Always resolve configuration in core/parent directory to persist across contexts
    core_dir = path_resolver.get_core_dir()
    return os.path.join(core_dir, "artifacts", "active_workspace.json")

def load_config() -> dict:
    config_path = get_workspace_config_path()
    if os.path.exists(config_path):
        with open(config_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                pass
    return {}

def save_config(config: dict) -> None:
    config_path = get_workspace_config_path()
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

def init_workspace(repo_url: str) -> None:
    # 1. Determine target directory
    parent_root = path_resolver.get_core_dir()
    workspace_path = os.path.join(parent_root, ".workspace")
    
    # 2. Clone repo if not exists
    if not os.path.exists(workspace_path):
        print(f"Cloning child repository {repo_url} into {workspace_path}...")
        git_client.clone(repo_url, workspace_path)
    else:
        print(f"Target directory {workspace_path} already exists. Skipping clone.")
        
    # 3. Provision Directories
    kb_dir = os.path.join(workspace_path, "kb")
    artifacts_dir = os.path.join(workspace_path, "artifacts")
    os.makedirs(kb_dir, exist_ok=True)
    os.makedirs(artifacts_dir, exist_ok=True)
    print("Provisioned kb/ and artifacts/ directories.")

    # 4. Inject GEMINI.md
    gemini_path = os.path.join(workspace_path, "GEMINI.md")
    if not os.path.exists(gemini_path):
        with open(gemini_path, "w", encoding="utf-8") as f:
            f.write("""# GEMINI (Antigravity) Frontier Agent Instructions (Workspace Mode)

You are executing within a **Model 1 (Dual-Context Workspace)**. Your system parameters are bounded by the following rules:

## 1. Persona & Workspace Configuration
- **Role**: You are the **Frontier Agent** managing the workspace environment.
- **Active Workspace**: Operating under `SPAO_WORKSPACE_DIR`. All project metadata, tracking files, and knowledge primitives reside here.
- **Engine Isolation**: The parent engine repository (`DZ_CIL_ROOT`) is **read-only** and immutable during active workspace work. You are strictly forbidden from modifying or pushing changes to the parent engine files unless in direct engine development mode.

## 2. Inheritance & Domain Sovereignty
- **Loop Inheritance**: You inherit the parent engine's core loop mechanics, validations, and constraints (TDD tests, branch naming conventions) as a baseline.
- **Domain Sovereignty (Extend & Override)**: The child workspace owns its own destiny. You are empowered to help the Operator **extend** and **override** the parent's default behaviors to suit the target project's needs. To preserve velocity and prevent operational tension:
  * **Gate Decoupling**: You are NOT blocked by parent-level remote PR merge gates (`WIP-N=1`). The workspace development loop may proceed through local checkouts, tests, and reflections completely offline.
  * **Tool Execution**: Inside the sovereign workspace, you are permitted to execute standard version control tools (like `git` or `gh` CLI commands) directly, bypassing the parent's Abstraction Doctrine wrapper limits.
  * **Direct Collaboration**: The scripted rhetorical policing of the Bilateral Chat Protocol is disabled. Communicate naturally and align directly with the Operator.
- **Bootstrapping Invariant**: Your very first activity in a new workspace MUST be to capture the Operator's unformed Telos and codify it as the workspace's North Star in the child's `artifacts/strategic_intent.yml`.

## 3. Redirection Invariants
- **Checkouts**: All node checkout operations must be redirected to `.worktrees/node/[id]-[kebab-case]/` inside this workspace directory.
- **Testing**: Test execution must verify target workspace branches inside their respective worktrees.

## 4. Operational Rules
- Follow the Sense-Plan-Act-Observe (SPAO) loop lifecycle.
- Maintain policy-driven communication via YAML/Markdown trackers inside this workspace's `artifacts/` folder.
- **Conversational Materialization (PML-to-NL)**: If the Operator states their intent in plain chat (Pre-Materialization Loop), compile the Node Contract (NC) proposal in chat. Once approved, programmatically run the CLI commands behind the scenes to materialize the Node-Loop (NL) worktree and branch.
""")
        print("Injected GEMINI.md bootloader.")

    # 5. Provision Virtual Environment
    venv_dir = os.path.join(workspace_path, ".venv")
    if not os.path.exists(venv_dir):
        print("Provisioning virtual environment...")
        import venv
        venv.create(venv_dir, with_pip=True)
        pip_exe = os.path.join(venv_dir, "bin", "pip")
        if not os.path.exists(pip_exe):
            pip_exe = os.path.join(venv_dir, "bin", "pip3")
        subprocess.check_call([pip_exe, "install", "--upgrade", "pip"])
        subprocess.check_call([pip_exe, "install", "pytest", "pytest-mock", "pyyaml"])
        print("Virtual environment provisioned and dependencies installed.")

    # 6. Add to parent .gitignore if missing
    gitignore_path = os.path.join(parent_root, ".gitignore")
    ignore_entry = "\n.workspace/\n"
    needs_write = True
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            content = f.read()
        if ".workspace" in content:
            needs_write = False
            
    if needs_write:
        with open(gitignore_path, "a", encoding="utf-8") as f:
            f.write(ignore_entry)
        print("Added .workspace/ to parent .gitignore.")
        
    # 7. Copy parent .gitignore to child workspace if missing
    child_gitignore = os.path.join(workspace_path, ".gitignore")
    if not os.path.exists(child_gitignore) and os.path.exists(gitignore_path):
        import shutil
        shutil.copy2(gitignore_path, child_gitignore)
        with open(child_gitignore, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(child_gitignore, "w", encoding="utf-8") as f:
            for line in lines:
                if ".workspace" not in line:
                    f.write(line)
        print("Copied .gitignore to child workspace.")

    # 8. Save configuration
    config = {
        "repo_url": repo_url,
        "path": workspace_path,
        "initialized_at": subprocess.check_output(["date", "-u"]).decode().strip()
    }
    save_config(config)
    print("Workspace initialized successfully.")
    print("\nNext Steps per Dao:")
    print(f"Start the agent:")
    print(f"SPAO_WORKSPACE_DIR=\"{workspace_path}\" agy")
