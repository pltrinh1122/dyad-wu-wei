import os
import yaml
from unittest.mock import patch, MagicMock
import pytest
from skills import path_resolver

def test_get_core_dir():
    core_dir = path_resolver.get_core_dir()
    assert os.path.isabs(core_dir)
    assert os.path.exists(os.path.join(core_dir, "skills"))

def test_get_workspace_dir_env():
    mock_env = {"SPAO_WORKSPACE_DIR": "/tmp/mock-workspace"}
    with patch.dict(os.environ, mock_env):
        ws_dir = path_resolver.get_workspace_dir()
        assert ws_dir == "/tmp/mock-workspace"

def test_get_workspace_dir_git_fallback():
    # Explicitly remove SPAO_WORKSPACE_DIR so the git-toplevel fallback fires.
    env = {k: v for k, v in os.environ.items() if k != "SPAO_WORKSPACE_DIR"}
    with patch.dict(os.environ, env, clear=True):
        with patch("skills.git_client.get_show_toplevel", return_value="/tmp/git-workspace"):
            ws_dir = path_resolver.get_workspace_dir()
            assert ws_dir == "/tmp/git-workspace"

def test_get_workspace_dir_cwd_fallback():
    # Explicitly remove SPAO_WORKSPACE_DIR so the cwd fallback fires.
    env = {k: v for k, v in os.environ.items() if k != "SPAO_WORKSPACE_DIR"}
    with patch.dict(os.environ, env, clear=True):
        with patch("skills.git_client.get_show_toplevel", side_effect=Exception("not a git repo")):
            ws_dir = path_resolver.get_workspace_dir()
            assert ws_dir == os.path.abspath(os.getcwd())

def test_resolve_workspace_path():
    with patch("skills.path_resolver.get_workspace_dir", return_value="/tmp/ws"):
        path = path_resolver.resolve_workspace_path("sub", "file.txt")
        assert path == "/tmp/ws/sub/file.txt"

def test_resolve_core_path():
    with patch("skills.path_resolver.get_core_dir", return_value="/tmp/core"):
        path = path_resolver.resolve_core_path("sub", "file.txt")
        assert path == "/tmp/core/sub/file.txt"

def test_load_node_yml_workspace(tmp_path):
    ws_dir = str(tmp_path / "ws")
    os.makedirs(ws_dir)
    node_yml_content = {
        "node_attributes": {
            "status": {
                "active": "status/active"
            }
        }
    }
    
    with open(os.path.join(ws_dir, "node.yml"), "w") as f:
        yaml.safe_dump(node_yml_content, f)
        
    with patch("skills.path_resolver.get_workspace_dir", return_value=ws_dir):
        # Even if core has node.yml, we should load workspace one
        config = path_resolver.load_node_yml()
        assert config["node_attributes"]["status"]["active"] == "status/active"

def test_load_node_yml_fallback(tmp_path):
    # Workspace does not have node.yml, fallback to core
    core_dir = str(tmp_path / "core")
    os.makedirs(core_dir)
    node_yml_content = {
        "node_attributes": {
            "status": {
                "fallback": "status/fallback"
            }
        }
    }
    
    with open(os.path.join(core_dir, "node.yml"), "w") as f:
        yaml.safe_dump(node_yml_content, f)
        
    with patch("skills.path_resolver.get_workspace_dir", return_value="/tmp/empty_ws"):
        with patch("skills.path_resolver.get_core_dir", return_value=core_dir):
            config = path_resolver.load_node_yml()
            assert config["node_attributes"]["status"]["fallback"] == "status/fallback"
