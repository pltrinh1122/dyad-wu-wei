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
        print(f"Target directory {workspace_path} already exists.")
        
    # 3. Add to parent .gitignore if missing
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
        
    # 4. Copy parent .gitignore to child workspace if missing
    child_gitignore = os.path.join(workspace_path, ".gitignore")
    if not os.path.exists(child_gitignore) and os.path.exists(gitignore_path):
        os.makedirs(workspace_path, exist_ok=True)
        import shutil
        shutil.copy2(gitignore_path, child_gitignore)
        with open(child_gitignore, "r", encoding="utf-8") as f:
            lines = f.readlines()
        with open(child_gitignore, "w", encoding="utf-8") as f:
            for line in lines:
                if ".workspace" not in line:
                    f.write(line)
        print("Copied .gitignore to child workspace.")

    # 5. Save configuration
    config = {
        "repo_url": repo_url,
        "path": workspace_path,
        "initialized_at": subprocess.check_output(["date", "-u"]).decode().strip()
    }
    save_config(config)
    print("Workspace initialized successfully.")
