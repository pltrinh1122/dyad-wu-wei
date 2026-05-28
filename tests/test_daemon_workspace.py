import os
import json
import yaml
import shutil
from unittest.mock import patch, MagicMock
import pytest
from kernel import daemon_workspace
from drivers import git_client
from drivers import github_client
from kernel import daemon_backlog

def test_load_and_save_config(tmp_path):
    mock_config_path = str(tmp_path / "active_workspace.json")
    with patch("kernel.daemon_workspace.get_workspace_config_path", return_value=mock_config_path):
        config = daemon_workspace.load_config()
        assert config == {}
        
        test_config = {"repo_url": "https://github.com/foo/bar.git", "path": "/foo/bar"}
        daemon_workspace.save_config(test_config)
        
        loaded = daemon_workspace.load_config()
        assert loaded == test_config

def test_init_workspace(tmp_path):
    core_dir = str(tmp_path / "parent_project")
    workspace_dir = os.path.join(core_dir, ".workspace")
    os.makedirs(core_dir, exist_ok=True)
    
    parent_gitignore = os.path.join(core_dir, ".gitignore")
    with open(parent_gitignore, "w") as f:
        f.write("node_modules/\n")
        
    mock_config_path = os.path.join(core_dir, "active_workspace.json")
    
    with patch("drivers.path_resolver.get_core_dir", return_value=core_dir), \
         patch("kernel.daemon_workspace.get_workspace_config_path", return_value=mock_config_path), \
         patch("drivers.git_client.clone") as mock_clone, \
         patch("venv.create") as mock_venv_create, \
         patch("subprocess.check_call") as mock_check_call:
         
        daemon_workspace.init_workspace("https://github.com/foo/bar.git")
        
        mock_clone.assert_called_once_with("https://github.com/foo/bar.git", workspace_dir)
        mock_venv_create.assert_called_once_with(os.path.join(workspace_dir, ".venv"), with_pip=True)
        assert mock_check_call.call_count == 2
        
        with open(parent_gitignore, "r") as f:
            content = f.read()
        assert ".workspace/" in content
        
        config = daemon_workspace.load_config()
        assert config["repo_url"] == "https://github.com/foo/bar.git"
        assert config["path"] == workspace_dir

def test_git_client_workspace_redirection():
    mock_env = {"SPAO_WORKSPACE_DIR": "/tmp/workspace_dir"}
    with patch.dict(os.environ, mock_env), \
         patch("subprocess.run") as mock_run:
        
        git_client.add(["file.txt"])
        
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        assert kwargs.get("cwd") == "/tmp/workspace_dir"

def test_github_client_repo_redirection():
    mock_env = {"SPAO_WORKSPACE_DIR": "/tmp/workspace_dir"}
    
    mock_git_remote_res = MagicMock()
    mock_git_remote_res.stdout = "git@github.com:test-owner/test-repo.git\n"
    mock_git_remote_res.returncode = 0
    
    mock_gh_res = MagicMock()
    mock_gh_res.stdout = "[]\n"
    mock_gh_res.returncode = 0
    
    def side_effect(cmd, **kwargs):
        if "remote" in cmd and "get-url" in cmd:
            return mock_git_remote_res
        return mock_gh_res
        
    with patch.dict(os.environ, mock_env), \
         patch("subprocess.run", side_effect=side_effect) as mock_run:
         
        github_client.get_open_prs()
        
        found_gh_repo = False
        for call in mock_run.call_args_list:
            cmd = call[0][0]
            if cmd[0] == "gh":
                env = call[1].get("env", {})
                if env.get("GH_REPO") == "test-owner/test-repo":
                    found_gh_repo = True
                    break
        assert found_gh_repo

def test_backlog_daemon_repository_override():
    mock_env = {"SPAO_WORKSPACE_DIR": "/tmp/workspace_dir"}
    
    mock_git_remote_res = MagicMock()
    mock_git_remote_res.stdout = "git@github.com:test-owner/test-repo.git\n"
    mock_git_remote_res.returncode = 0
    
    with patch.dict(os.environ, mock_env), \
         patch("subprocess.run", return_value=mock_git_remote_res):
         
        backlog = daemon_backlog.BacklogDaemon()
        assert backlog.repository == "test-owner/test-repo"

def test_workspace_bootstrap_invariant_enforcement(tmp_path):
    import importlib.util
    import sys
    
    workspace_dir = tmp_path / "child_workspace"
    workspace_dir.mkdir()
    
    core_dir = tmp_path / "core"
    core_dir.mkdir()
    
    active_workspace_json = core_dir / "artifacts" / "active_workspace.json"
    active_workspace_json.parent.mkdir(parents=True, exist_ok=True)
    import json
    with open(active_workspace_json, "w") as f:
        json.dump({"repo_url": "https://github.com/foo/bar.git", "path": str(workspace_dir)}, f)
        
    bin_workspace_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../bin/workspace'))
    import types
    bin_workspace = types.ModuleType("bin_workspace")
    bin_workspace.__file__ = bin_workspace_path
    
    with open(bin_workspace_path, "r", encoding="utf-8") as f:
        code_content = f.read()
    exec(code_content, bin_workspace.__dict__)
    sys.modules["bin_workspace"] = bin_workspace
    
    mock_config_path = str(active_workspace_json)
    
    with patch("kernel.daemon_workspace.get_workspace_config_path", return_value=mock_config_path), \
         patch("sys.argv", ["bin/workspace", "node", "list"]), \
         patch("subprocess.run") as mock_run, \
         pytest.raises(SystemExit) as excinfo:
         
        bin_workspace.main()
        
    assert excinfo.value.code == 1
    
    strategic_intent_path = workspace_dir / "artifacts" / "strategic_intent.yml"
    strategic_intent_path.parent.mkdir(parents=True, exist_ok=True)
    strategic_intent_path.touch()
    
    with patch("kernel.daemon_workspace.get_workspace_config_path", return_value=mock_config_path), \
         patch("sys.argv", ["bin/workspace", "node", "list"]), \
         patch("subprocess.run") as mock_run, \
         pytest.raises(SystemExit) as excinfo:
         
        bin_workspace.main()
        
    mock_run.assert_called_once()
