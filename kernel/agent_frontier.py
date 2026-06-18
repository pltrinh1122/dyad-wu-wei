import hashlib
import os
import yaml
from drivers.file_locker import lock_file
from kernel.daemon_telemetry import record_execution

class StateCorruptionError(Exception):
    """Raised when frontier_state.yml checksum fails or syntax is invalid."""
    pass

def resolve_yml_path(filepath: str) -> str:
    """Resolves a Markdown frontier path to its YAML counterpart."""
    if filepath.endswith(".md"):
        return filepath[:-3] + ".yml"
    return filepath

def get_checksum_path(filepath: str) -> str:
    """Returns the checksum file path for a given state file."""
    return filepath + ".sha256"

def verify_checksum(filepath: str) -> None:
    """Verifies that the filepath checksum matches its .sha256 file."""
    yml_path = resolve_yml_path(filepath)
    checksum_path = get_checksum_path(yml_path)
    
    if not os.path.exists(yml_path):
        return
    if not os.path.exists(checksum_path):
        # Bootstrap: create it if it is missing
        rehash(yml_path)
        return
        
    with open(yml_path, 'rb') as f:
        current_hash = hashlib.sha256(f.read()).hexdigest()
        
    with open(checksum_path, 'r') as f:
        expected_hash = f.read().strip()
        
    if current_hash != expected_hash:
        raise StateCorruptionError(
            f"Frontier state checksum mismatch!\n"
            f"Expected: {expected_hash}\n"
            f"Actual:   {current_hash}\n"
            f"This indicates out-of-band corruption or manual edits.\n"
            f"To resolve, verify the changes and run: `./bin/meta rehash`"
        )

def rehash(filepath: str) -> None:
    """Updates the checksum file for the given filepath."""
    yml_path = resolve_yml_path(filepath)
    checksum_path = get_checksum_path(yml_path)
    if not os.path.exists(yml_path):
        return
    with open(yml_path, 'rb') as f:
        current_hash = hashlib.sha256(f.read()).hexdigest()
    with open(checksum_path, 'w') as f:
        f.write(current_hash + "\n")

def load_state(filepath: str) -> dict:
    """Loads and verifies the frontier state from YAML."""
    yml_path = resolve_yml_path(filepath)
    verify_checksum(yml_path)
    with open(yml_path, 'r') as f:
        try:
            return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise StateCorruptionError(f"Failed to parse frontier YAML: {e}")

def save_state(filepath: str, data: dict) -> None:
    """Saves the frontier state to YAML, updates checksum, and regenerates markdown."""
    yml_path = resolve_yml_path(filepath)
    with lock_file(yml_path):
        with open(yml_path, 'w') as f:
            yaml.safe_dump(data, f, sort_keys=False, default_flow_style=False)
        rehash(yml_path)
        
    # Regenerate markdown derived log
    md_path = yml_path[:-4] + ".md"
    write_markdown_derived(yml_path, md_path)

def write_markdown_derived(yml_path: str, md_path: str) -> None:
    """Generates a clean read-only Markdown log from the YAML source of truth."""
    with open(yml_path, 'r') as f:
        try:
            data = yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            raise StateCorruptionError(f"Failed to parse frontier YAML for markdown output: {e}")
        
    lines = []
    lines.append("# Agentic Frontier State\n")
    
    nodes = data.get("nodes", [])
    for node in nodes:
        name = node.get("name", "Unknown Node")
        status = node.get("status", "")
        learnings = node.get("learnings", "")
        invariants = node.get("invariants", [])
        
        lines.append(f"## {name}")
        lines.append(f"- **Status**: {status}")
        if node.get("loop"):
            lines.append(f"- **Loop**: {node['loop']}")
        if node.get("area"):
            lines.append(f"- **Area**: {node['area']}")
        if node.get("kind"):
            lines.append(f"- **Kind**: {node['kind']}")
        lines.append(f"- **Learnings & Context**: {learnings}")
        lines.append("- **Feedforward Invariants**:")
        if invariants:
            for inv in invariants:
                # Wrap in backticks if no backticks are present
                formatted_inv = f"`{inv}`" if "`" not in inv else inv
                lines.append(f"  - {formatted_inv}")
        else:
            lines.append("  - `[ ]` None")
        lines.append("")  # Empty line after node
        
    # Add pointers at the bottom
    lines.append("## Active Agents Matrix")
    active_agents = data.get("active_agents")
    if active_agents:
        for persona, state in active_agents.items():
            lines.append(f"* **{persona}**:")
            path = state.get("current_active_path") or "None"
            node = state.get("current_active_node") or "None"
            lines.append(f"  - Current Active Path: `{path}`")
            lines.append(f"  - Current Active Node: `{node}`")
    else:
        # Legacy fallback
        lines.append("* **agent-default**:")
        path = data.get("current_active_path") or "None"
        node = data.get("current_active_node") or "None"
        lines.append(f"  - Current Active Path: `{path}`")
        lines.append(f"  - Current Active Node: `{node}`")
    lines.append("")  # Empty line
    
    # Write derived markdown file under lock
    with lock_file(md_path):
        with open(md_path, 'w') as f:
            f.write("\n".join(lines))

def extract_active_node_from_state(state: dict) -> str:
    persona = os.environ.get("SPAO_PERSONA_ID") or "agent-default"
    active_agents = state.get("active_agents")
    if active_agents is not None and persona in active_agents:
        if "current_active_node" in active_agents[persona]:
            val = active_agents[persona].get("current_active_node")
            return val if val is not None else ""
    return state.get("current_active_node") or ""

def read_active_node(filepath: str) -> str:
    """Reads the current active node from frontier_state."""
    yml_path = resolve_yml_path(filepath)
    state = load_state(yml_path)
    return extract_active_node_from_state(state)

def read_last_completed_node(filepath: str) -> str:
    """Reads the most recently completed node."""
    yml_path = resolve_yml_path(filepath)
    state = load_state(yml_path)
    nodes = state.get("nodes", [])
    for node in reversed(nodes):
        if node.get("status") == "Completed":
            return node.get("name") or ""
    return ""

def extract_active_path_from_state(state: dict) -> str | None:
    persona = os.environ.get("SPAO_PERSONA_ID") or "agent-default"
    active_agents = state.get("active_agents")
    if active_agents is not None and persona in active_agents:
        if "current_active_path" in active_agents[persona]:
            return active_agents[persona].get("current_active_path")
    return state.get("current_active_path")

def read_active_path(filepath: str) -> str | None:
    """Reads the current active path."""
    yml_path = resolve_yml_path(filepath)
    state = load_state(yml_path)
    return extract_active_path_from_state(state)

def extract_path_id(path_str: str) -> str | None:
    """Extracts the numeric ID from a Path string."""
    from drivers.frontier_editor import extract_path_id as raw_extract
    return raw_extract(path_str)

def get_all_active_locked_issue_ids(filepath: str) -> set[str]:
    """Returns a set of all currently locked issue IDs (Nodes and Paths) across all active agents."""
    import re
    yml_path = resolve_yml_path(filepath)
    state = load_state(yml_path)
    active_agents = state.get("active_agents") or {}
    
    locked_ids = set()
    for persona, data in active_agents.items():
        node_str = data.get("current_active_node")
        path_str = data.get("current_active_path")
        
        if node_str:
            match = re.search(r"#(\d+)", node_str)
            if match:
                locked_ids.add(match.group(1))
                
        if path_str:
            match = re.search(r"#(\d+)", path_str)
            if match:
                locked_ids.add(match.group(1))
            else:
                # Fallback to extract_path_id logic
                pid = extract_path_id(path_str)
                if pid:
                    locked_ids.add(pid)
                    
    # Also parse legacy current_active_node/path just in case
    legacy_node = state.get("current_active_node")
    legacy_path = state.get("current_active_path")
    if legacy_node:
        match = re.search(r"#(\d+)", legacy_node)
        if match:
            locked_ids.add(match.group(1))
    if legacy_path:
        match = re.search(r"#(\d+)", legacy_path)
        if match:
            locked_ids.add(match.group(1))
            
    return locked_ids

@record_execution(stage="skill")
def set_active_path(filepath: str, path_name: str) -> None:
    """Updates the text below Current Active Path."""
    yml_path = resolve_yml_path(filepath)
    state = load_state(yml_path)
    val = None
    if path_name != "None" and path_name is not None:
        path_id = extract_path_id(path_name)
        if path_id:
            from kernel.daemon_strategic import verify_path_activation_allowed
            verify_path_activation_allowed(path_id)
        val = path_name
        
    persona = os.environ.get("SPAO_PERSONA_ID") or "agent-default"
        
    if "active_agents" not in state:
        state["active_agents"] = {}
    if persona not in state["active_agents"]:
        state["active_agents"][persona] = {
            "current_active_path": state.get("current_active_path"),
            "current_active_node": state.get("current_active_node")
        }
    state["active_agents"][persona]["current_active_path"] = val
    save_state(yml_path, state)

def set_active_node(filepath: str, node_name: str) -> None:
    """Updates the text below Current Active Node."""
    yml_path = resolve_yml_path(filepath)
    state = load_state(yml_path)
    persona = os.environ.get("SPAO_PERSONA_ID") or "agent-default"
    
    val = None
    if node_name != "None" and node_name is not None:
        val = node_name
        
    if "active_agents" not in state:
        state["active_agents"] = {}
    if persona not in state["active_agents"]:
        state["active_agents"][persona] = {
            "current_active_path": state.get("current_active_path"),
            "current_active_node": state.get("current_active_node")
        }
    state["active_agents"][persona]["current_active_node"] = val
    save_state(yml_path, state)

def get_node_metadata(node_id: int | str) -> dict:
    """Queries issue labels to extract loop, area, and kind metadata."""
    from drivers import github_client
    metadata = {}
    try:
        labels = github_client.get_issue_labels(str(node_id))
        for label in labels:
            if label.startswith("loop:"):
                metadata["loop"] = label.split(":", 1)[1].strip()
            elif label.startswith("area:"):
                metadata["area"] = label.split(":", 1)[1].strip()
            elif label.startswith("kind:"):
                metadata["kind"] = label.split(":", 1)[1].strip()
            elif label == "path":
                metadata["kind"] = "path"
    except Exception:
        # Ignore errors (e.g. offline tests or missing API stubs)
        pass
    return metadata

@record_execution(stage="skill")
def complete_active_node(filepath: str, node_name: str, learnings: str, invariants: list[str], clear_pointers: bool = True) -> None:
    """Marks the active node as completed in the YAML ledger."""
    yml_path = resolve_yml_path(filepath)
    state = load_state(yml_path)
    
    node_id = extract_path_id(node_name)
    nodes = state.get("nodes", [])
    found = False
    for node in nodes:
        if node.get("name") == node_name:
            node["status"] = "Completed"
            node["learnings"] = learnings
            node["invariants"] = invariants
            if node_id:
                node.update(get_node_metadata(node_id))
            found = True
            break
            
    if not found:
        new_node = {
            "name": node_name,
            "status": "Completed",
            "learnings": learnings,
            "invariants": invariants
        }
        if node_id:
            new_node.update(get_node_metadata(node_id))
        nodes.append(new_node)
        
    state["nodes"] = nodes
    if clear_pointers:
        persona = os.environ.get("SPAO_PERSONA_ID") or "agent-default"
        if "active_agents" in state and persona in state["active_agents"]:
            state["active_agents"][persona]["current_active_node"] = None
        else:
            state["current_active_node"] = None
        
    save_state(yml_path, state)

def cancel_active_node(filepath: str, node_name: str, reason: str, clear_pointers: bool = True) -> None:
    """Marks the active node as cancelled in the YAML ledger."""
    yml_path = resolve_yml_path(filepath)
    state = load_state(yml_path)
    
    node_id = extract_path_id(node_name)
    nodes = state.get("nodes", [])
    found = False
    for node in nodes:
        if node.get("name") == node_name:
            node["status"] = "Cancelled"
            node["learnings"] = f"Cancelled: {reason}"
            if node_id:
                node.update(get_node_metadata(node_id))
            found = True
            break
            
    if not found:
        new_node = {
            "name": node_name,
            "status": "Cancelled",
            "learnings": f"Cancelled: {reason}",
            "invariants": []
        }
        if node_id:
            new_node.update(get_node_metadata(node_id))
        nodes.append(new_node)
        
    state["nodes"] = nodes
    if clear_pointers:
        persona = os.environ.get("SPAO_PERSONA_ID") or "agent-default"
        if "active_agents" in state and persona in state["active_agents"]:
            state["active_agents"][persona]["current_active_node"] = None
        else:
            state["current_active_node"] = None
        
    save_state(yml_path, state)

def append_active_node(filepath: str, node_id: int, node_title: str, description: str, invariants: list[str]) -> None:
    """Appends a new active node block to the ledger."""
    yml_path = resolve_yml_path(filepath)
    state = load_state(yml_path)
    
    from kernel.title_utils import clean_node_title
    clean_title = clean_node_title(node_title)
    node_name = f"#{node_id}: {clean_title}"
    nodes = state.get("nodes", [])
    found = False
    for node in nodes:
        if node.get("name") == node_name:
            node["status"] = "[///] Act Phase"
            node["learnings"] = description
            node["invariants"] = invariants
            node.update(get_node_metadata(node_id))
            found = True
            break
            
    if not found:
        new_node = {
            "name": node_name,
            "status": "[///] Act Phase",
            "learnings": description,
            "invariants": invariants
        }
        new_node.update(get_node_metadata(node_id))
        nodes.append(new_node)
        
    state["nodes"] = nodes
    state["current_active_node"] = node_name
    save_state(yml_path, state)

def abort_active_node(filepath: str, node_id: str) -> None:
    """Removes the aborted node from the ledger and clears pointers."""
    yml_path = resolve_yml_path(filepath)
    state = load_state(yml_path)
    
    nodes = state.get("nodes", [])
    # Remove nodes matching this ID
    state["nodes"] = [node for node in nodes if str(extract_path_id(node.get("name", ""))) != str(node_id)]
    
    # Clear pointers
    persona = os.environ.get("SPAO_PERSONA_ID") or "agent-default"
    if "active_agents" in state and persona in state["active_agents"]:
        state["active_agents"][persona]["current_active_node"] = None
    else:
        state["current_active_node"] = None
        
    save_state(yml_path, state)

def register_backlog_node(filepath: str, node_id: int, node_title: str, description: str) -> None:
    """Registers a newly created backlog node in the ledger with Backlog status."""
    yml_path = resolve_yml_path(filepath)
    state = load_state(yml_path)
    
    from kernel.title_utils import clean_node_title
    clean_title = clean_node_title(node_title)
    node_name = f"#{node_id}: {clean_title}"
    nodes = state.get("nodes", [])
    found = False
    for node in nodes:
        if node.get("name") == node_name:
            found = True
            break
            
    if not found:
        new_node = {
            "name": node_name,
            "status": "Backlog",
            "learnings": description,
            "invariants": []
        }
        new_node.update(get_node_metadata(node_id))
        nodes.append(new_node)
        
    state["nodes"] = nodes
    save_state(yml_path, state)

