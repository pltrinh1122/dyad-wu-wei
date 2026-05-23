import os
import sys
import re
import json
import pytest
from unittest.mock import patch, MagicMock

# Helper to extract the python code dynamically from bin/meta
def extract_audit_python_code():
    bin_path = os.path.join(os.path.dirname(__file__), "../bin/meta")
    with open(bin_path, "r") as f:
        content = f.read()
    # Find the audit) subcommand block to avoid matching earlier python blocks
    audit_part = content.split("audit)")[1]
    match = re.search(
        r'PYTHONPATH="\$\{REPO_DIR\}:\$\{PYTHONPATH:-\}" "\$PYTHON_EXE" -c \'(.*?)\'\s+"\$FRONTIER_FILE"',
        audit_part,
        re.DOTALL
    )
    if not match:
        raise ValueError("Could not find the audit python block in bin/meta")
    return match.group(1)

def test_extract_code_sanity():
    code = extract_audit_python_code()
    assert "taxonomy = BacklogDaemon().load_node_taxonomy()" in code
    assert "completed_nodes" in code

def test_lightweight_audit_workflow(tmp_path):
    # Set up paths
    frontier_dir = tmp_path / "artifacts"
    frontier_dir.mkdir(parents=True, exist_ok=True)
    frontier_file = frontier_dir / "frontier_state.md"
    
    mock_nodes = [
        # Path 503 is active and not completed
        {"name": "Path 503: Optimization of Node Sync Audit Performance (Lightweight Audit)", "status": "In Progress", "kind": "path"},
        # Node 506 is child of Path 503 and is completed
        {"name": "Node 506: Activity 506: Reflect - Optimization of Node Sync Audit Performance (Lightweight Audit)", "status": "Completed", "kind": "activity"},
        # Node 505 is child of Path 503 and is completed
        {"name": "Node 505: Probe 505: Plan - Optimization of Node Sync Audit Performance (Lightweight Audit)", "status": "Completed", "kind": "probe"},
        # Completed path (should be filtered out unless active)
        {"name": "Path 100: Previous Task Completed", "status": "Completed", "kind": "path"},
        # Child node of Path 100
        {"name": "Node 101: Activity 101: Clean up old code", "status": "Completed", "kind": "activity"}
    ]
    
    state_data = {
        "nodes": mock_nodes,
        "current_active_path": 503,
        "current_active_node": "Node 506: Activity 506: Reflect - Optimization of Node Sync Audit Performance (Lightweight Audit)"
    }
    
    code = extract_audit_python_code()
    
    mock_load_state = MagicMock(return_value=state_data)
    mock_taxonomy = MagicMock(return_value={"terminal": ["activity", "probe"], "non_terminal": ["path"]})
    mock_update_body = MagicMock()
    
    issue_body_content = """
## Checklist
- [ ] Node 506: Optimize audit (#506)
- [x] Node 505: Plan audit (#505)
"""
    
    def dummy_run(args, **kwargs):
        cmd_str = " ".join(args)
        if "issue view 503 --json body" in cmd_str:
            mock_res = MagicMock()
            mock_res.stdout = json.dumps({"body": issue_body_content})
            return mock_res
        elif "issue view 503 --json title" in cmd_str:
            mock_res = MagicMock()
            mock_res.stdout = json.dumps({"title": "Path 503: Optimization of Node Sync Audit Performance (Lightweight Audit)"})
            return mock_res
        raise ValueError(f"Unexpected subprocess call: {args}")
        
    mock_sub_run = MagicMock(side_effect=dummy_run)
    
    with patch("kernel.agent_frontier.load_state", mock_load_state), \
         patch("kernel.daemon_backlog.BacklogDaemon.load_node_taxonomy", mock_taxonomy), \
         patch("drivers.github_client.update_issue_body", mock_update_body), \
         patch("subprocess.run", mock_sub_run), \
         patch("sys.argv", ["bin/meta", str(frontier_file)]):
        
        exec(code, {"__builtins__": __builtins__})
        
    mock_load_state.assert_called_once_with(str(frontier_file))
    assert mock_sub_run.call_count > 0
    mock_update_body.assert_called_once()
    called_path, called_body = mock_update_body.call_args[0]
    assert called_path == "503"
    assert "- [x] Node 506: Optimize audit" in called_body
    
    cache_file = tmp_path / "artifacts" / "audit_state.json"
    assert cache_file.exists()
    with open(cache_file, "r") as f:
        cache_content = json.load(f)
        
    assert "meta-index-audit" in cache_content
    assert "503" in cache_content["meta-index-audit"]
    assert sorted(cache_content["meta-index-audit"]["503"]) == ["505", "506"]

def test_lightweight_audit_bypasses_network_when_cached(tmp_path):
    frontier_dir = tmp_path / "artifacts"
    frontier_dir.mkdir(parents=True, exist_ok=True)
    frontier_file = frontier_dir / "frontier_state.md"
    
    cache_file = tmp_path / "artifacts" / "audit_state.json"
    cache_data = {
        "meta-index-audit": {
            "503": ["505", "506"]
        },
        "some-other-namespace": {
            "99": ["1"]
        }
    }
    with open(cache_file, "w") as f:
        json.dump(cache_data, f)
        
    mock_nodes = [
        {"name": "Path 503: Optimization of Node Sync Audit Performance (Lightweight Audit)", "status": "In Progress", "kind": "path"},
        {"name": "Node 506: Activity 506: Reflect - Optimization of Node Sync Audit Performance (Lightweight Audit)", "status": "Completed", "kind": "activity"},
        {"name": "Node 505: Probe 505: Plan - Optimization of Node Sync Audit Performance (Lightweight Audit)", "status": "Completed", "kind": "probe"}
    ]
    
    state_data = {
        "nodes": mock_nodes,
        "current_active_path": 503,
        "current_active_node": "Node 506: Activity 506: Reflect - Optimization of Node Sync Audit Performance (Lightweight Audit)"
    }
    
    code = extract_audit_python_code()
    
    mock_load_state = MagicMock(return_value=state_data)
    mock_taxonomy = MagicMock(return_value={"terminal": ["activity", "probe"], "non_terminal": ["path"]})
    mock_update_body = MagicMock()
    mock_sub_run = MagicMock()
    
    with patch("kernel.agent_frontier.load_state", mock_load_state), \
         patch("kernel.daemon_backlog.BacklogDaemon.load_node_taxonomy", mock_taxonomy), \
         patch("drivers.github_client.update_issue_body", mock_update_body), \
         patch("subprocess.run", mock_sub_run), \
         patch("sys.argv", ["bin/meta", str(frontier_file)]):
        
        exec(code, {"__builtins__": __builtins__})
        
    mock_sub_run.assert_not_called()
    mock_update_body.assert_not_called()
    
    with open(cache_file, "r") as f:
        updated_cache = json.load(f)
    assert updated_cache["some-other-namespace"] == {"99": ["1"]}
    assert updated_cache["meta-index-audit"] == {"503": ["505", "506"]}

def test_lightweight_audit_with_new_completed_node(tmp_path):
    frontier_dir = tmp_path / "artifacts"
    frontier_dir.mkdir(parents=True, exist_ok=True)
    frontier_file = frontier_dir / "frontier_state.md"
    
    cache_file = tmp_path / "artifacts" / "audit_state.json"
    cache_data = {
        "meta-index-audit": {
            "503": ["505", "506"]
        }
    }
    with open(cache_file, "w") as f:
        json.dump(cache_data, f)
        
    mock_nodes = [
        {"name": "Path 503: Optimization of Node Sync Audit Performance (Lightweight Audit)", "status": "In Progress", "kind": "path"},
        {"name": "Node 506: Activity 506: Reflect - Optimization of Node Sync Audit Performance (Lightweight Audit)", "status": "Completed", "kind": "activity"},
        {"name": "Node 505: Probe 505: Plan - Optimization of Node Sync Audit Performance (Lightweight Audit)", "status": "Completed", "kind": "probe"},
        {"name": "Node 507: Activity 507: Verify performance fixes - Optimization of Node Sync Audit Performance (Lightweight Audit)", "status": "Completed", "kind": "activity"}
    ]
    
    state_data = {
        "nodes": mock_nodes,
        "current_active_path": 503,
        "current_active_node": "Node 506: Activity 506: Reflect - Optimization of Node Sync Audit Performance (Lightweight Audit)"
    }
    
    code = extract_audit_python_code()
    
    mock_load_state = MagicMock(return_value=state_data)
    mock_taxonomy = MagicMock(return_value={"terminal": ["activity", "probe"], "non_terminal": ["path"]})
    mock_update_body = MagicMock()
    
    issue_body_content = """
## Checklist
- [x] Node 505: Plan audit (#505)
- [x] Node 506: Optimize audit (#506)
- [ ] Node 507: Verify performance fixes (#507)
"""
    
    def dummy_run(args, **kwargs):
        cmd_str = " ".join(args)
        if "issue view 503 --json body" in cmd_str:
            mock_res = MagicMock()
            mock_res.stdout = json.dumps({"body": issue_body_content})
            return mock_res
        elif "issue view 503 --json title" in cmd_str:
            mock_res = MagicMock()
            mock_res.stdout = json.dumps({"title": "Path 503: Optimization of Node Sync Audit Performance (Lightweight Audit)"})
            return mock_res
        raise ValueError(f"Unexpected subprocess call: {args}")
        
    mock_sub_run = MagicMock(side_effect=dummy_run)
    
    with patch("kernel.agent_frontier.load_state", mock_load_state), \
         patch("kernel.daemon_backlog.BacklogDaemon.load_node_taxonomy", mock_taxonomy), \
         patch("drivers.github_client.update_issue_body", mock_update_body), \
         patch("subprocess.run", mock_sub_run), \
         patch("sys.argv", ["bin/meta", str(frontier_file)]):
        
        exec(code, {"__builtins__": __builtins__})
        
    mock_update_body.assert_called_once()
    called_path, called_body = mock_update_body.call_args[0]
    assert called_path == "503"
    assert "- [x] Node 507: Verify performance fixes" in called_body
    
    with open(cache_file, "r") as f:
        updated_cache = json.load(f)
    assert sorted(updated_cache["meta-index-audit"]["503"]) == ["505", "506", "507"]

def test_lightweight_audit_path_detection_formats(tmp_path):
    frontier_dir = tmp_path / "artifacts"
    frontier_dir.mkdir(parents=True, exist_ok=True)
    frontier_file = frontier_dir / "frontier_state.md"
    
    mock_nodes = [
        # Recognized as path via regex
        {"name": "Path 503: Custom Title", "status": "In Progress", "kind": "activity"},
        # Completed node for path 503
        {"name": "Node 506: Activity 506: Reflect - Custom Title", "status": "Completed", "kind": "activity"},
        
        # Recognized as path via taxonomy kind
        {"name": "Node 100: Custom Title 2", "status": "In Progress", "kind": "path"},
        # Completed node for path 100
        {"name": "Node 101: Activity 101: Plan - Custom Title 2", "status": "Completed", "kind": "activity"}
    ]
    
    state_data = {
        "nodes": mock_nodes,
        "current_active_path": 503,
        "current_active_node": "Node 506: Activity 506: Reflect - Custom Title"
    }
    
    code = extract_audit_python_code()
    
    mock_load_state = MagicMock(return_value=state_data)
    mock_taxonomy = MagicMock(return_value={"terminal": ["activity", "probe"], "non_terminal": ["path"]})
    mock_update_body = MagicMock()
    mock_sub_run = MagicMock()
    
    def dummy_run(args, **kwargs):
        cmd_str = " ".join(args)
        if "issue view 503" in cmd_str or "issue view 100" in cmd_str:
            mock_res = MagicMock()
            mock_res.stdout = json.dumps({"body": "No checklist", "title": "Some title"})
            return mock_res
        raise ValueError(f"Unexpected subprocess call: {args}")
        
    mock_sub_run.side_effect = dummy_run
    
    with patch("kernel.agent_frontier.load_state", mock_load_state), \
         patch("kernel.daemon_backlog.BacklogDaemon.load_node_taxonomy", mock_taxonomy), \
         patch("drivers.github_client.update_issue_body", mock_update_body), \
         patch("subprocess.run", mock_sub_run), \
         patch("sys.argv", ["bin/meta", str(frontier_file)]):
        
        exec(code, {"__builtins__": __builtins__})
        
    # Both paths should have been view-checked
    called_cmds = [ " ".join(call[0][0]) for call in mock_sub_run.call_args_list ]
    assert any("view 503" in cmd for cmd in called_cmds)
    assert any("view 100" in cmd for cmd in called_cmds)
