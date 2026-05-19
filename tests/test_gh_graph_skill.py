import pytest
from skills import gh_graph_skill

def test_parse_meta_index_simple():
    body = """
## Meta-Index
- [x] Node 1: Completed Node
- [ ] Node 2: Pending Node
- [ ] Activity 3: Unblocked Activity [Depends: 1]
- [ ] Probe 4: Blocked Probe [Depends: 2]
"""
    nodes = gh_graph_skill.parse_meta_index(body)
    assert nodes["1"]["completed"] is True
    assert nodes["2"]["completed"] is False
    assert nodes["3"]["depends"] == ["1"]
    assert nodes["4"]["depends"] == ["2"]
    assert nodes["3"]["title"] == "Unblocked Activity"

def test_get_ready_nodes():
    nodes = {
        "1": {"completed": True, "depends": []},
        "2": {"completed": False, "depends": []},
        "3": {"completed": False, "depends": ["1"]},
        "4": {"completed": False, "depends": ["2"]}
    }
    ready = gh_graph_skill.get_ready_nodes(nodes)
    # Node 2 is ready (incomplete, no deps)
    # Node 3 is ready (incomplete, dep 1 is completed)
    # Node 4 is NOT ready (incomplete, dep 2 is incomplete)
    assert "2" in ready
    assert "3" in ready
    assert "4" not in ready
    assert ready == ["2", "3"]

def test_parse_meta_index_mixed_formats():
    body = """
- [x] Activity 100: Done
- [ ] Probe 101: Wait
- [ ] 102: Raw ID
"""
    nodes = gh_graph_skill.parse_meta_index(body)
    assert "100" in nodes
    assert "101" in nodes
    assert "102" in nodes
    assert nodes["100"]["completed"] is True
    assert nodes["101"]["title"] == "Wait"
    assert nodes["102"]["title"] == "Raw ID"
