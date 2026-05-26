"""Tests for drivers.sluice_gate_sensor — the Sluice Gate Sensor skill driver."""

import pytest
from drivers import sluice_gate_sensor


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

FRONTIER_WITH_ACTIVE_NODE = """\
# Frontier State

## Current Active Node
**Node 806: Activity 806: Implement bin/node retro attach**

## Completed Nodes
- Node 805
"""

FRONTIER_NO_ACTIVE_NODE = """\
# Frontier State

## Current Active Node
None

## Completed Nodes
- Node 806
"""

FRONTIER_EMPTY_ACTIVE = """\
# Frontier State

## Current Active Node

## Completed Nodes
"""

MERGED_PRS_MATCH = [
    {"number": 1106, "headRefName": "node/806-implement-bin-node-retro-attach", "title": "Activity 806"},
    {"number": 1099, "headRefName": "node/805-other-node", "title": "Other"},
]

MERGED_PRS_NO_MATCH = [
    {"number": 1099, "headRefName": "node/805-other-node", "title": "Other"},
]


# ---------------------------------------------------------------------------
# detect_active_node_id
# ---------------------------------------------------------------------------

def test_detect_active_node_id_normal():
    node_id = sluice_gate_sensor.detect_active_node_id(FRONTIER_WITH_ACTIVE_NODE)
    assert node_id == "806"


def test_detect_active_node_id_none_literal():
    node_id = sluice_gate_sensor.detect_active_node_id(FRONTIER_NO_ACTIVE_NODE)
    assert node_id is None


def test_detect_active_node_id_empty_section():
    node_id = sluice_gate_sensor.detect_active_node_id(FRONTIER_EMPTY_ACTIVE)
    assert node_id is None


def test_detect_active_node_id_no_section():
    node_id = sluice_gate_sensor.detect_active_node_id("# Some other content\nNo frontier here.")
    assert node_id is None


def test_detect_active_node_id_bare_number():
    content = "## Current Active Node\n1234\n"
    assert sluice_gate_sensor.detect_active_node_id(content) == "1234"


# ---------------------------------------------------------------------------
# check_node_pr_merged
# ---------------------------------------------------------------------------

def test_check_node_pr_merged_match():
    pr = sluice_gate_sensor.check_node_pr_merged("806", MERGED_PRS_MATCH)
    assert pr is not None
    assert pr["number"] == 1106


def test_check_node_pr_merged_no_match():
    pr = sluice_gate_sensor.check_node_pr_merged("807", MERGED_PRS_MATCH)
    assert pr is None


def test_check_node_pr_merged_empty_list():
    pr = sluice_gate_sensor.check_node_pr_merged("806", [])
    assert pr is None


def test_check_node_pr_merged_partial_id_no_false_positive():
    """Node 8 must not match node/806-..."""
    pr = sluice_gate_sensor.check_node_pr_merged("8", MERGED_PRS_MATCH)
    assert pr is None


# ---------------------------------------------------------------------------
# evaluate — full integration of the sensor
# ---------------------------------------------------------------------------

def test_evaluate_triggered():
    result = sluice_gate_sensor.evaluate(
        frontier_content=FRONTIER_WITH_ACTIVE_NODE,
        merged_prs=MERGED_PRS_MATCH,
        last_alerted_node=None,
    )
    assert result["triggered"] is True
    assert result["node_id"] == "806"
    assert result["pr"]["number"] == 1106
    assert "Node 806" in result["message"]
    assert "bin/node sync" in result["message"]
    assert result["error"] is None


def test_evaluate_no_active_node():
    result = sluice_gate_sensor.evaluate(
        frontier_content=FRONTIER_NO_ACTIVE_NODE,
        merged_prs=MERGED_PRS_MATCH,
    )
    assert result["triggered"] is False
    assert result["node_id"] is None


def test_evaluate_no_matching_pr():
    result = sluice_gate_sensor.evaluate(
        frontier_content=FRONTIER_WITH_ACTIVE_NODE,
        merged_prs=MERGED_PRS_NO_MATCH,
    )
    assert result["triggered"] is False
    assert result["node_id"] == "806"
    assert result["pr"] is None


def test_evaluate_suppresses_duplicate_alert():
    """Already-alerted node should NOT retrigger."""
    result = sluice_gate_sensor.evaluate(
        frontier_content=FRONTIER_WITH_ACTIVE_NODE,
        merged_prs=MERGED_PRS_MATCH,
        last_alerted_node="806",  # already alerted
    )
    assert result["triggered"] is False


def test_evaluate_fires_for_different_node():
    """Different node from last_alerted_node SHOULD trigger."""
    result = sluice_gate_sensor.evaluate(
        frontier_content=FRONTIER_WITH_ACTIVE_NODE,
        merged_prs=MERGED_PRS_MATCH,
        last_alerted_node="805",  # different node
    )
    assert result["triggered"] is True


def test_evaluate_empty_merged_prs():
    result = sluice_gate_sensor.evaluate(
        frontier_content=FRONTIER_WITH_ACTIVE_NODE,
        merged_prs=[],
    )
    assert result["triggered"] is False
    assert result["error"] is None


def test_evaluate_pr_number_in_message():
    result = sluice_gate_sensor.evaluate(
        frontier_content=FRONTIER_WITH_ACTIVE_NODE,
        merged_prs=MERGED_PRS_MATCH,
    )
    assert "1106" in result["message"]
