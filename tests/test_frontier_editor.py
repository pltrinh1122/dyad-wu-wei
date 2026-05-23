import os
import pytest
import textwrap
import hashlib
from drivers.frontier_editor import (
    read_active_node,
    complete_active_node,
    set_active_node,
    append_active_node,
    read_active_path,
    set_active_path
)
from kernel import mgr_frontier

@pytest.fixture
def dummy_frontier(tmp_path):
    filepath = tmp_path / "frontier_state.yml"
    initial_content = textwrap.dedent("""\
        current_active_path: "Path 181: Configurable Sense Hooks"
        current_active_node: "Node 2: Do the next thing"
        nodes:
          - name: "Node 1: Initialization"
            status: "Completed"
            learnings: "Did things."
            invariants: []
    """)
    filepath.write_text(initial_content)
    
    # Compute and write initial checksum
    checksum = hashlib.sha256(initial_content.encode("utf-8")).hexdigest()
    (tmp_path / "frontier_state.yml.sha256").write_text(checksum + "\n")
    
    # Also write initial markdown representation so it exists
    mgr_frontier.write_markdown_derived(str(filepath), str(tmp_path / "frontier_state.md"))
    
    return str(tmp_path / "frontier_state.md")

def test_read_active_node(dummy_frontier):
    node = read_active_node(dummy_frontier)
    assert node == "Node 2: Do the next thing"

def test_read_active_path(dummy_frontier):
    path = read_active_path(dummy_frontier)
    assert path == "Path 181: Configurable Sense Hooks"

def test_set_active_path(dummy_frontier):
    set_active_path(dummy_frontier, "Path 192: Another Path")
    assert read_active_path(dummy_frontier) == "Path 192: Another Path"
    
    set_active_path(dummy_frontier, "None")
    assert read_active_path(dummy_frontier) is None

def test_complete_active_node(dummy_frontier):
    complete_active_node(
        dummy_frontier, 
        node_name="Node 2: Do the next thing",
        learnings="I learned a lot.",
        invariants=["[x] Tested well."]
    )
    
    content = open(dummy_frontier).read()
    assert "## Node 2: Do the next thing" in content
    assert "- **Status**: Completed" in content
    assert "- **Learnings & Context**: I learned a lot." in content
    assert "- `[x] Tested well.`" in content
    assert "## Current Active Node" in content

def test_set_active_node(dummy_frontier):
    set_active_node(dummy_frontier, "Node 3: Profit")
    content = open(dummy_frontier).read()
    
    assert "## Current Active Node" in content
    assert "**Node 3: Profit**" in content
    assert "**Node 2: Do the next thing**" not in content

def test_append_active_node(dummy_frontier):
    append_active_node(
        dummy_frontier,
        node_id=40,
        node_title="Great Success",
        description="Completed the mission.",
        invariants=["[ ] Verified system is stable."]
    )
    content = open(dummy_frontier).read()

    assert "## Node 40: Great Success" in content
    assert "- **Status**: [///] Act Phase" in content
    assert "- **Learnings & Context**: Completed the mission." in content
    assert "- `[ ] Verified system is stable.`" in content
    assert "## Current Active Node" in content
    assert "**Node 40: Great Success**" in content

def test_checksum_mismatch(dummy_frontier):
    yml_path = dummy_frontier[:-3] + ".yml"
    
    # Mutate the YAML file out-of-band without rehashing
    with open(yml_path, "a") as f:
        f.write("\n# manual edit\n")
        
    with pytest.raises(mgr_frontier.StateCorruptionError) as exc_info:
        read_active_node(dummy_frontier)
        
    assert "checksum mismatch" in str(exc_info.value)
    
    # Rehash and check if it resolves
    mgr_frontier.rehash(dummy_frontier)
    node = read_active_node(dummy_frontier)
    assert node == "Node 2: Do the next thing"

def test_register_backlog_node(dummy_frontier):
    mgr_frontier.register_backlog_node(
        dummy_frontier,
        node_id=45,
        node_title="Backlog Task",
        description="A task in backlog."
    )
    
    content = open(dummy_frontier).read()
    assert "## Node 45: Backlog Task" in content
    assert "- **Status**: Backlog" in content
    assert "- **Learnings & Context**: A task in backlog." in content

