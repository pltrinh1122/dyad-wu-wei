import os
import sys
import shutil
import subprocess
from unittest import mock
import pytest
from kernel.node_lifecycle import BaseNode, TerminalNode
from drivers import git_client

def test_installer_script_execution(tmp_path):
    # Setup parent repo structure
    parent_dir = tmp_path / "parent"
    bin_dir = parent_dir / "bin"
    bin_dir.mkdir(parents=True)
    
    # Copy dz-cil-install script to target bin_dir
    src_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin/dz-cil-install")
    dest_script = bin_dir / "dz-cil-install"
    shutil.copy2(src_script, dest_script)
    os.chmod(dest_script, 0o755)
    
    # Create empty parent gitignore
    gitignore = parent_dir / ".gitignore"
    gitignore.touch()
    
    # Create a mock bin directory for the test PATH
    mock_bin_dir = tmp_path / "mock_bin"
    mock_bin_dir.mkdir()
    
    # Create mock python3 script
    mock_python = mock_bin_dir / "python3"
    mock_python.write_text(f"""#!{sys.executable}
import sys
import os
import subprocess

args = sys.argv[1:]
# Log the arguments
with open("{tmp_path}/python_calls.log", "a") as f:
    f.write(" ".join(args) + chr(10))

if len(args) >= 3 and args[0] == "-m" and args[1] == "venv":
    venv_dir = args[2]
    if venv_dir == "--help":
        sys.exit(0)
    # Create mock pip in venv
    pip_dir = os.path.join(venv_dir, "bin")
    os.makedirs(pip_dir, exist_ok=True)
    mock_pip = os.path.join(pip_dir, "pip")
    with open(mock_pip, "w") as pf:
        pf.write(f'''#!{sys.executable}
import sys
with open("{tmp_path}/pip_calls.log", "a") as f:
    f.write(" ".join(sys.argv[1:]) + chr(10))
''')
    os.chmod(mock_pip, 0o755)
else:
    # Forward to real python
    res = subprocess.run(["{sys.executable}"] + args)
    sys.exit(res.returncode)
""")
    os.chmod(mock_python, 0o755)
    
    # Create mock git script
    mock_git = mock_bin_dir / "git"
    mock_git.write_text("""#!/usr/bin/env bash
echo "mock-git"
""")
    os.chmod(mock_git, 0o755)
    
    # Prepare environment with modified PATH
    env = os.environ.copy()
    env["PATH"] = str(mock_bin_dir) + os.path.pathsep + env.get("PATH", "")
    
    # Target workspace dir
    target_workspace = parent_dir / "custom-workspace"
    
    # Execute the installer
    res = subprocess.run(
        [str(dest_script), "custom-workspace"],
        cwd=str(parent_dir),
        env=env,
        capture_output=True,
        text=True
    )
    
    assert res.returncode == 0
    
    # Verify directories
    assert (target_workspace / "kb").is_dir()
    assert (target_workspace / "artifacts").is_dir()
    assert (target_workspace / "GEMINI.md").is_file()
    
    # Verify parent gitignore has entry
    gitignore_content = gitignore.read_text()
    assert "/custom-workspace/" in gitignore_content
    
    # Verify python/pip calls
    python_calls = (tmp_path / "python_calls.log").read_text()
    assert "-m venv" in python_calls
    
    pip_calls = (tmp_path / "pip_calls.log").read_text()
    assert "install pytest pytest-mock pyyaml" in pip_calls


@mock.patch("kernel.node_lifecycle.github_client.get_issue_labels")
def test_node_lifecycle_workspace_redirection(mock_get_labels):
    mock_env = {"SPAO_WORKSPACE_DIR": "/tmp/workspace_dir"}
    mock_get_labels.return_value = ["loop:spao"]
    node = BaseNode("390")
    
    with mock.patch.dict(os.environ, mock_env):
        worktree_path = node.get_worktree_path("node/390-test")
        assert worktree_path == os.path.join("/tmp/workspace_dir", ".worktrees", "node/390-test")


@mock.patch("kernel.node_lifecycle.git_client.worktree_remove")
@mock.patch("kernel.node_lifecycle.git_client.branch_delete")
@mock.patch("os.path.exists")
def test_node_lifecycle_clean_if_merged_workspace(mock_exists, mock_branch_delete, mock_worktree_remove):
    mock_env = {"SPAO_WORKSPACE_DIR": "/tmp/workspace_dir"}
    mock_exists.return_value = True
    
    with mock.patch.dict(os.environ, mock_env):
        TerminalNode.clean_if_merged("node/390-test")
        
        expected_path = os.path.join("/tmp/workspace_dir", ".worktrees", "node/390-test")
        mock_worktree_remove.assert_called_once_with(expected_path, force=True)
        mock_branch_delete.assert_called_once_with("node/390-test")
