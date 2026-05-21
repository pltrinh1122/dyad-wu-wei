import pytest
from skills import gh_graph_skill
from skills.gh_graph_skill import DAGValidationError

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

def test_parse_multi_dependencies():
    body = """
- [x] Node 1: First
- [x] Node 2: Second
- [ ] Node 3: Multi-dependent [Depends: 1, 2]
- [ ] Node 4: Spaces dependency [Depends: 1 , 2]
- [ ] Node 5: Empty dependency [Depends: ]
"""
    nodes = gh_graph_skill.parse_meta_index(body)
    assert nodes["3"]["depends"] == ["1", "2"]
    assert nodes["4"]["depends"] == ["1", "2"]
    assert nodes["5"]["depends"] == []

def test_referential_integrity_violation():
    body = """
- [ ] Node 1: A node depending on non-existent [Depends: 99]
"""
    with pytest.raises(DAGValidationError) as excinfo:
        gh_graph_skill.parse_meta_index(body)
    assert "Referential Integrity Violation: Node 1 depends on non-existent Node 99" in str(excinfo.value)

def test_self_dependency_violation():
    body = """
- [ ] Node 1: A node depending on itself [Depends: 1]
"""
    with pytest.raises(DAGValidationError) as excinfo:
        gh_graph_skill.parse_meta_index(body)
    assert "Self-Dependency Violation: Node 1 cannot depend on itself" in str(excinfo.value)

def test_cycle_detection_direct():
    body = """
- [ ] Node 1: Cycle A [Depends: 2]
- [ ] Node 2: Cycle B [Depends: 1]
"""
    with pytest.raises(DAGValidationError) as excinfo:
        gh_graph_skill.parse_meta_index(body)
    err_msg = str(excinfo.value)
    assert "Cycle Detected:" in err_msg
    assert ("1 -> 2 -> 1" in err_msg) or ("2 -> 1 -> 2" in err_msg)

def test_cycle_detection_three_nodes():
    body = """
- [ ] Node 1: First [Depends: 2]
- [ ] Node 2: Second [Depends: 3]
- [ ] Node 3: Third [Depends: 1]
"""
    with pytest.raises(DAGValidationError) as excinfo:
        gh_graph_skill.parse_meta_index(body)
    err_msg = str(excinfo.value)
    assert "Cycle Detected:" in err_msg
    assert ("1 -> 2 -> 3 -> 1" in err_msg) or ("2 -> 3 -> 1 -> 2" in err_msg) or ("3 -> 1 -> 2 -> 3" in err_msg)

def test_deterministic_nba_sorting():
    nodes = {
        "10": {"completed": False, "depends": []},
        "2": {"completed": False, "depends": []},
        "100": {"completed": False, "depends": []},
        "1": {"completed": True, "depends": []},
        "5": {"completed": False, "depends": ["1"]}
    }
    ready = gh_graph_skill.get_ready_nodes(nodes)
    assert ready == ["2", "5", "10", "100"]
