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


def test_resolve_agent_id_env():
    # Test resolving agent_id from SPAO_AGENT_ID environment variable
    with patch.dict(os.environ, {"SPAO_AGENT_ID": "agent-sg3"}):
        assert path_resolver.resolve_agent_id() == "agent-sg3"

def test_resolve_agent_id_basename_auto():
    # Test resolving agent_id from workspace dir with -auto suffix
    with patch.dict(os.environ, {}, clear=True):
        with patch("skills.path_resolver.get_workspace_dir", return_value="/mnt/shared_data/git_repos/agent-SG2-auto"):
            assert path_resolver.resolve_agent_id() == "agent-sg2"

def test_resolve_agent_id_basename_normal():
    # Test resolving agent_id from workspace dir without -auto suffix
    with patch.dict(os.environ, {}, clear=True):
        with patch("skills.path_resolver.get_workspace_dir", return_value="/mnt/shared_data/git_repos/agent-sg2"):
            assert path_resolver.resolve_agent_id() == "agent-sg2"

def test_resolve_agent_id_basename_other():
    # Test resolving agent_id from workspace dir for a different agent
    with patch.dict(os.environ, {}, clear=True):
        with patch("skills.path_resolver.get_workspace_dir", return_value="/mnt/shared_data/git_repos/agent-sg5"):
            assert path_resolver.resolve_agent_id() == "agent-sg5"

def test_resolve_agent_id_non_agent_basename():
    # Test resolving agent_id from a non-agent workspace directory
    with patch.dict(os.environ, {}, clear=True):
        with patch("skills.path_resolver.get_workspace_dir", return_value="/tmp/some-random-dir"):
            assert path_resolver.resolve_agent_id() is None

def test_load_antigravity_yml_override(tmp_path):
    ws_dir_non_agent = str(tmp_path / "some-random-dir")
    os.makedirs(ws_dir_non_agent)
    
    ws_dir_agent = str(tmp_path / "agent-SG2-auto")
    os.makedirs(ws_dir_agent)
    
    anti_yml_content = {
        "node_taxonomy": {
            "terminal": ["activity"]
        },
        "agent_id": "agent-sg5"  # Should be overridden dynamically if dynamic matches, else fallback
    }
    
    with open(os.path.join(ws_dir_non_agent, "antigravity.yml"), "w") as f:
        yaml.safe_dump(anti_yml_content, f)
    with open(os.path.join(ws_dir_agent, "antigravity.yml"), "w") as f:
        yaml.safe_dump(anti_yml_content, f)
        
    # 1. When SPAO_AGENT_ID is set (override should happen)
    with patch("skills.path_resolver.get_workspace_dir", return_value=ws_dir_non_agent):
        with patch.dict(os.environ, {"SPAO_AGENT_ID": "agent-sg2"}):
            config = path_resolver.load_antigravity_yml()
            assert config["agent_id"] == "agent-sg2"
            assert config["node_taxonomy"]["terminal"] == ["activity"]

    # 2. When resolving from workspace dir name starting with agent-
    with patch("skills.path_resolver.get_workspace_dir", return_value=ws_dir_agent):
        with patch.dict(os.environ, {}, clear=True):
            config = path_resolver.load_antigravity_yml()
            assert config["agent_id"] == "agent-sg2"

    # 3. Fallback to static if none resolved
    with patch("skills.path_resolver.get_workspace_dir", return_value=ws_dir_non_agent):
        with patch.dict(os.environ, {}, clear=True):
            config = path_resolver.load_antigravity_yml()
            assert config["agent_id"] == "agent-sg5"


