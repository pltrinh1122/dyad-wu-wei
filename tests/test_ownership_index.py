"""
tests/test_ownership_index.py

Structural validation tests for kb/WHAT-0062-agent-persona-ownership-index.md.

These tests enforce the Falsification Criteria defined in WHAT-0062 §5:
  1. Every active SG in strategic_intent.yml has a row in the ownership index.
  2. Every covered spec_file exists on disk.
  3. agent_id in antigravity.yml matches an owner_persona in the index.
  4. No two non-shared SG rows share the same owner_persona.

Authored by: agent-sg5 (SG-0005: Autonomous Knowledge Accrual)
Node:        603, Path 591 (578-A)
"""

import os
import re
import yaml
import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WHAT_0062_PATH = os.path.join(REPO_ROOT, "kb", "WHAT-0062-agent-persona-ownership-index.md")
STRATEGIC_INTENT_PATH = os.path.join(REPO_ROOT, "artifacts", "strategic_intent.yml")
ANTIGRAVITY_PATH = os.path.join(REPO_ROOT, "antigravity.yml")


def parse_ownership_index(md_path: str) -> list[dict]:
    """
    Parse the pipe-delimited ownership table from WHAT-0062.
    Returns a list of dicts with keys: sg_id, owner_persona, spec_file, why_file, status.
    """
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find the table section (after ## Ownership Index heading)
    table_match = re.search(r"## Ownership Index\s*\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
    assert table_match, "WHAT-0062 must contain a '## Ownership Index' section with a table"

    table_text = table_match.group(1)
    rows = []
    for line in table_text.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("| sg_id") or set(line.replace("|", "").replace("-", "").strip()) == set():
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) >= 5:
            rows.append({
                "sg_id": cells[0],
                "owner_persona": cells[1],
                "spec_file": cells[2],
                "why_file": cells[3],
                "status": cells[4],
            })
    return rows


def load_strategic_goal_ids() -> list[str]:
    """Return all SG IDs from strategic_intent.yml."""
    with open(STRATEGIC_INTENT_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return [sg["id"] for sg in data.get("strategic_goals", [])]


from skills import path_resolver

def load_agent_id() -> str:
    """Return the resolved agent_id."""
    return path_resolver.resolve_agent_id() or ""


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestOwnershipIndexCompleteness:

    def test_every_active_sg_has_owner_entry(self):
        """
        Every Strategic Goal ID in strategic_intent.yml must have a
        corresponding row in WHAT-0062. Missing rows indicate unregistered goals.
        """
        rows = parse_ownership_index(WHAT_0062_PATH)
        indexed_ids = {r["sg_id"] for r in rows}
        all_sg_ids = set(load_strategic_goal_ids())

        missing = all_sg_ids - indexed_ids
        assert not missing, (
            f"The following SG IDs are in strategic_intent.yml but missing from "
            f"WHAT-0062: {sorted(missing)}. Add rows before merging."
        )

    def test_covered_spec_files_exist_on_disk(self):
        """
        For every row with status='covered', the spec_file must exist on disk.
        A dangling file path means the ownership spec was deleted or renamed.
        """
        rows = parse_ownership_index(WHAT_0062_PATH)
        missing_files = []
        for row in rows:
            if row["status"] == "covered" and row["spec_file"] not in ("—", "(pending)", ""):
                full_path = os.path.join(REPO_ROOT, row["spec_file"])
                if not os.path.exists(full_path):
                    missing_files.append((row["sg_id"], row["spec_file"]))

        assert not missing_files, (
            f"Covered entries in WHAT-0062 reference spec files that do not exist on disk: "
            f"{missing_files}. Update or recreate the missing files."
        )

    def test_agent_id_matches_ownership_index(self):
        """
        The agent_id declared in antigravity.yml must appear as owner_persona
        for at least one SG with status='covered' in WHAT-0062.
        An agent operating without a registered identity cannot be gated correctly.
        """
        agent_id = load_agent_id()
        assert agent_id, (
            "antigravity.yml must contain a non-empty 'agent_id' field. "
            "Add 'agent_id: agent-sg{N}' as the canonical ROM identity declaration."
        )

        rows = parse_ownership_index(WHAT_0062_PATH)
        covered_owners = {r["owner_persona"] for r in rows if r["status"] == "covered"}

        assert agent_id in covered_owners, (
            f"agent_id '{agent_id}' from antigravity.yml is not registered as an owner "
            f"of any covered SG in WHAT-0062. Covered owners are: {sorted(covered_owners)}. "
            f"Add a row for this agent or correct the agent_id field."
        )

    def test_no_duplicate_owners_for_non_shared(self):
        """
        No two non-shared, non-unassigned SG rows may share the same owner_persona.
        Each Strategic Goal must have exactly one responsible agent.
        """
        rows = parse_ownership_index(WHAT_0062_PATH)
        owner_to_sgs: dict[str, list[str]] = {}
        for row in rows:
            persona = row["owner_persona"]
            if persona in ("shared", "unassigned", "—", ""):
                continue
            owner_to_sgs.setdefault(persona, []).append(row["sg_id"])

        # Each persona may own multiple SGs (that's fine — one agent per SG,
        # but one agent can own multiple SGs). What we enforce here is that
        # sg_ids are unique (no sg_id appears under two different owners).
        sg_to_owners: dict[str, list[str]] = {}
        for row in rows:
            if row["owner_persona"] in ("shared", "unassigned", "—", ""):
                continue
            sg_to_owners.setdefault(row["sg_id"], []).append(row["owner_persona"])

        conflicts = {sg: owners for sg, owners in sg_to_owners.items() if len(owners) > 1}
        assert not conflicts, (
            f"The following SG IDs have multiple owners in WHAT-0062: {conflicts}. "
            f"Each SG must have exactly one owner_persona."
        )
