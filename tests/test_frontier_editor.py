import os
import pytest
import textwrap
from skills.frontier_editor import read_active_node, complete_active_node, set_active_node, append_active_node

@pytest.fixture
def dummy_frontier(tmp_path):
    filepath = tmp_path / "frontier_state.md"
    initial_content = textwrap.dedent("""\
        # Frontier State
        
        ## Node 1: Initialization
        - **Status**: Completed
        - **Learnings**: Did things.
        
        ## Current Active Node
        **Node 2: Do the next thing**
    """)
    filepath.write_text(initial_content)
    return str(filepath)

def test_read_active_node(dummy_frontier):
    node = read_active_node(dummy_frontier)
    assert node == "Node 2: Do the next thing"

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
    # The active node marker should still be there, but empty or pushed down
    assert "## Current Active Node" in content

def test_set_active_node(dummy_frontier):
    set_active_node(dummy_frontier, "Node 3: Profit")
    content = open(dummy_frontier).read()
    
    assert "## Current Active Node" in content
    assert "**Node 3: Profit**" in content
    assert "**Node 2: Do the next thing**" not in content # The old one should be replaced

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
