import re

def read_active_node(filepath: str) -> str:
    """Reads the current active node from frontier_state.md."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if line.strip() == "## Current Active Node":
            for j in range(i + 1, len(lines)):
                next_line = lines[j].strip()
                if next_line:
                    # Strip bold asterisks
                    return next_line.strip('*')
    return ""

def complete_active_node(filepath: str, node_name: str, learnings: str, invariants: list[str]) -> None:
    """Appends the completed node block above the Current Active Node header."""
    with open(filepath, 'r') as f:
        content = f.read()
        
    invariant_str = "\n".join([f"  - `{inv}`" for inv in invariants])
    if not invariant_str:
        invariant_str = "  - `[ ]` None"
        
    completed_block = f"""## {node_name}
- **Status**: Completed
- **Learnings & Context**: {learnings}
- **Feedforward Invariants**:
{invariant_str}

"""
    # Find the existing node block and replace it
    pattern = r"## " + re.escape(node_name) + r"\n.*?(?=\n## |\Z)"
    
    # We need to strip the trailing newline from completed_block so we don't add extra newlines, 
    # but wait, completed_block already ends with \n\n. Let's just use it and rely on the regex matching up to \n##
    content, count = re.subn(pattern, completed_block.strip() + "\n", content, count=1, flags=re.DOTALL)
    
    if count == 0 and "## Current Active Node" in content:
        # Fallback if the node wasn't found for some reason
        content = content.replace("## Current Active Node", completed_block + "\n## Current Active Node")
    
    with open(filepath, 'w') as f:
        f.write(content)

def set_active_node(filepath: str, node_name: str) -> None:
    """Updates the text below Current Active Node."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if line.strip() == "## Current Active Node":
            # Find the next non-empty line and replace it
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    lines[j] = f"**{node_name}**\n"
                    break
            break
            
    with open(filepath, 'w') as f:
        f.writelines(lines)

def append_active_node(filepath: str, node_id: int, node_title: str, description: str, invariants: list[str]) -> None:
    """Appends a new active node block above the Current Active Node header,
    and sets it active.
    """
    with open(filepath, 'r') as f:
        content = f.read()

    invariant_str = "\n".join([f"  - `{inv}`" for inv in invariants])
    if not invariant_str:
        invariant_str = "  - `[ ]` None"

    node_name = f"Node {node_id}: {node_title}"

    completed_block = f"""## {node_name}
- **Status**: [///] Act Phase
- **Learnings & Context**: {description}
- **Feedforward Invariants**:
{invariant_str}

"""
    # Find the Current Active Node block and insert before it
    if "## Current Active Node" in content:
        content = content.replace("## Current Active Node", completed_block + "## Current Active Node")

    with open(filepath, 'w') as f:
        f.write(content)

    # Now set it active
    set_active_node(filepath, node_name)
