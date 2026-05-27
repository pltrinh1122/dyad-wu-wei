import os
import subprocess
import pytest
import yaml

# Strict Exemption List of files allowed to reference stale terms for historical/mapping purposes
EXEMPTIONS = {
    'kb/GLOSSARY.md',
    'artifacts/frontier_state.md',
    'artifacts/coherence_validation.md',
    'tests/test_lexical_guard.py',
    'kb/WHY-0054-glossary-alignment.md',
    'kb/WHAT-0054-glossary-spec.md',
    'kb/WHAT-0034-three-loop-governance-spec.md',
    'kb/WHY-0030-spao-onboarding-and-discoverability.md',
}

def load_semantic_ledger():
    """Loads deprecated terms and immune zones from kb/semantic_ledger.yml."""
    # Find ledger path relative to this test file
    ledger_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "kb", "semantic_ledger.yml"))
    if not os.path.exists(ledger_path):
        return set(), []
    
    with open(ledger_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    forbidden = set()
    terms = data.get("terms", {})
    for term, term_data in terms.items():
        if term_data.get("state") == "deprecated":
            forbidden.add(term)
            
    immune_zones = data.get("immune_zones", [])
    return forbidden, immune_zones

def is_immune(filepath, immune_zones):
    """Checks if a file is covered by immune zones or legacy exemptions."""
    if filepath in EXEMPTIONS:
        return True
        
    for zone in immune_zones:
        zone_type = zone.get("type")
        zone_value = zone.get("value")
        if zone_type == "exact":
            if os.path.basename(filepath) == zone_value or filepath == zone_value:
                return True
        elif zone_type == "prefix":
            if os.path.basename(filepath).startswith(zone_value) or filepath.startswith(zone_value):
                return True
    return False

def get_modified_files():
    """Retrieves list of modified, added, renamed, or untracked files in workspace."""
    try:
        res = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
        
    files = []
    for line in res.stdout.splitlines():
        if not line:
            continue
        status = line[:2].strip()
        filepath = line[3:].strip()
        # Handle renamed files: status oldpath -> newpath
        if '->' in filepath:
            filepath = filepath.split('->')[-1].strip()
        # Exclude deleted files
        if status != 'D':
            files.append(filepath)
    return files

def check_content(content, forbidden_words):
    """Checks string content for any occurrences of forbidden words, returning matching words."""
    content_lower = content.lower()
    found = []
    for word in forbidden_words:
        # Check for raw substring match to prevent evasion
        if word in content_lower:
            found.append(word)
    return found

def test_lexical_guard_logic():
    """Unit test for the lexical check function itself."""
    forbidden, immune_zones = load_semantic_ledger()
    
    assert "epic" in forbidden
    assert "spike" in forbidden
    assert "orchestrator" in forbidden
    assert "align" in forbidden
    
    assert is_immune("kb/GLOSSARY.md", immune_zones) is True
    assert is_immune("kb/WHY-1153-kernel-bin-coexistence.md", immune_zones) is True
    assert is_immune("kernel/daemon_node.py", immune_zones) is False
    
    assert check_content("This is a clean path.", forbidden) == []
    assert check_content("This is an epic task.", forbidden) == ['epic']
    assert check_content("We have a spike node here.", forbidden) == ['spike']

def test_modified_files_lexical_compliance():
    """Enforces vocabulary invariants on all newly introduced/modified workspace files."""
    forbidden, immune_zones = load_semantic_ledger()
    if not forbidden:
        return
        
    modified_files = get_modified_files()
    violations = []
    
    for filepath in modified_files:
        # Ignore files not ending with standard documentation or source formats
        if not (filepath.endswith('.py') or filepath.endswith('.md') or filepath.endswith('.txt') or filepath.endswith('.yml')):
            continue
            
        # Ignore immune files
        if is_immune(filepath, immune_zones):
            continue

        # Ignore files inside git worktrees to maintain test harness isolation
        if filepath.startswith('.worktrees/') or '/.worktrees/' in filepath:
            continue
            
        # Read the file's current workspace content
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            found = check_content(content, forbidden)
            if found:
                violations.append(f"{filepath} contains forbidden terms: {found}")
                
    if violations:
        pytest.fail(
            "LEXICAL GUARD FAILURE: Stale terms detected in modified files!\n"
            "Please replace deprecated terms with their active counterparts defined in semantic_ledger.yml.\n"
            "Violations:\n" + "\n".join(violations)
        )
