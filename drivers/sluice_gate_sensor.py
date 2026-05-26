"""Sluice Gate Sensor — a pure, stateless skill driver.

Responsibilities
----------------
- Detect whether the active node's PR branch has been merged into main.
- Return a structured, serializable result dict for the caller to act on.
- Surface errors explicitly rather than swallowing them.

This module MUST remain a pure, stateless, deterministic callable mapping to a
single system interaction (Architectural Boundary Invariant). It must not manage
state files, prompt queues, or orchestration logic.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover — type-checking only
    pass


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def detect_active_node_id(frontier_content: str) -> str | None:
    """Parses the active node ID from frontier_state.md content.

    Args:
        frontier_content: Raw text of ``artifacts/frontier_state.md``.

    Returns:
        The numeric node ID string (e.g. ``"806"``), or ``None`` if no active
        node is present or the content is empty.
    """
    match = re.search(
        r"## Current Active Node\n(.*?)(?=\n## |\Z)",
        frontier_content,
        re.DOTALL,
    )
    if not match:
        return None

    active_node = match.group(1).strip().strip("*")
    if not active_node or active_node.lower() == "none":
        return None

    id_match = re.search(r"(\d+)", active_node)
    return id_match.group(1) if id_match else None


def check_node_pr_merged(node_id: str, merged_prs: list[dict]) -> dict | None:
    """Scans a list of merged PRs for one that belongs to ``node_id``.

    Args:
        node_id:    The numeric node ID string to look for (e.g. ``"806"``).
        merged_prs: A list of PR dicts, each expected to have at minimum a
                    ``headRefName`` field (e.g. ``"node/806-implement-..."``)
                    and a ``number`` field.

    Returns:
        The matching PR dict if found, otherwise ``None``.
    """
    prefix = f"node/{node_id}-"
    for pr in merged_prs:
        head_ref = pr.get("headRefName", "")
        if head_ref.startswith(prefix):
            return pr
    return None


def evaluate(
    frontier_content: str,
    merged_prs: list[dict],
    last_alerted_node: str | None = None,
) -> dict:
    """Evaluates the sluice gate condition and returns a structured result.

    This is the primary entry point for the audit daemon rule evaluator.

    Args:
        frontier_content:   Raw text of ``artifacts/frontier_state.md``.
        merged_prs:         List of merged PR dicts from ``github_client.get_merged_prs()``.
        last_alerted_node:  The node ID from the persisted audit state, used to
                            prevent duplicate alerts.

    Returns:
        A dict with the following keys:

        - ``triggered`` (bool): Whether the sluice gate condition fired.
        - ``node_id`` (str | None): The active node ID that was checked.
        - ``pr`` (dict | None): The matching merged PR, if found.
        - ``message`` (str | None): A human-readable alert message.
        - ``error`` (str | None): Error description if something went wrong;
          ``None`` on success.
    """
    result: dict = {
        "triggered": False,
        "node_id": None,
        "pr": None,
        "message": None,
        "error": None,
    }

    node_id = detect_active_node_id(frontier_content)
    result["node_id"] = node_id

    if node_id is None:
        return result

    if last_alerted_node == node_id:
        # Already fired for this node — suppress duplicate.
        return result

    matched_pr = check_node_pr_merged(node_id, merged_prs)
    if matched_pr is None:
        return result

    result["triggered"] = True
    result["pr"] = matched_pr
    result["message"] = (
        f"Sluice Gate Opened: PR for Node {node_id} merged "
        f"(PR #{matched_pr.get('number', '?')}). "
        f"Run `./bin/node sync` to continue."
    )
    return result
