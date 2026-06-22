import os
import pytest
import textwrap
import hashlib
from drivers.frontier_editor import (
    read_active_path,
    set_active_path
)
from kernel import agent_frontier

@pytest.fixture
def dummy_frontier(tmp_path):
    filepath = tmp_path / "frontier_state.yml"
    initial_content = textwrap.dedent("""\
        current_active_path: "Path 181: Configurable Sense Hooks"
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
    agent_frontier.write_markdown_derived(str(filepath), str(tmp_path / "frontier_state.md"))
    
    return str(tmp_path / "frontier_state.md")



def test_read_active_path(dummy_frontier):
    path = read_active_path(dummy_frontier)
    assert path == "Path 181: Configurable Sense Hooks"

def test_set_active_path(dummy_frontier):
    set_active_path(dummy_frontier, "Path 192: Another Path")
    assert read_active_path(dummy_frontier) == "Path 192: Another Path"
    
    set_active_path(dummy_frontier, "None")
    assert read_active_path(dummy_frontier) is None



def test_checksum_mismatch(dummy_frontier):
    yml_path = dummy_frontier[:-3] + ".yml"
    
    # Mutate the YAML file out-of-band without rehashing
    with open(yml_path, "a") as f:
        f.write("\n# manual edit\n")
        
    with pytest.raises(agent_frontier.StateCorruptionError) as exc_info:
        read_active_path(dummy_frontier)
        
    assert "checksum mismatch" in str(exc_info.value)
    
    # Rehash and check if it resolves
    agent_frontier.rehash(dummy_frontier)
    path = read_active_path(dummy_frontier)
    assert path == "Path 181: Configurable Sense Hooks"

def test_register_backlog_node(dummy_frontier):
    agent_frontier.register_backlog_node(
        dummy_frontier,
        node_id=45,
        node_title="Backlog Task",
        description="A task in backlog."
    )
    
    content = open(dummy_frontier).read()
    assert "## #45: Backlog Task" in content
    assert "- **Status**: Backlog" in content
    assert "- **Learnings & Context**: A task in backlog." in content

