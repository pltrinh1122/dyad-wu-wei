import os
import subprocess
import pytest

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

FORBIDDEN_WORDS = {'epic', 'spike'}

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

def check_content(content):
    """Checks string content for any occurrences of forbidden words, returning matching words."""
    content_lower = content.lower()
    found = []
    for word in FORBIDDEN_WORDS:
        # Check for raw substring match to prevent evasion
        if word in content_lower:
            found.append(word)
    return found

def test_lexical_guard_logic():
    """Unit test for the lexical check function itself."""
    assert check_content("This is a clean path.") == []
    assert check_content("We run a diagnostic probe.") == []
    assert check_content("This is an epic task.") == ['epic']
    assert check_content("We have a spike node here.") == ['spike']
    assert check_content("Case insensitivity: EpIcS.") == ['epic']

def test_modified_files_lexical_compliance():
    """Enforces vocabulary invariants on all newly introduced/modified workspace files."""
    modified_files = get_modified_files()
    violations = []
    
    for filepath in modified_files:
        # Ignore files not ending with standard documentation or source formats
        if not (filepath.endswith('.py') or filepath.endswith('.md') or filepath.endswith('.txt')):
            continue
            
        # Ignore files in the strict exemptions list
        if filepath in EXEMPTIONS:
            continue

        # Ignore files inside git worktrees to maintain test harness isolation
        if filepath.startswith('.worktrees/') or '/.worktrees/' in filepath:
            continue
            
        # Read the file's current workspace content
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            found = check_content(content)
            if found:
                violations.append(f"{filepath} contains forbidden terms: {found}")
                
    if violations:
        pytest.fail(
            "LEXICAL GUARD FAILURE: Stale terms detected in modified files!\n"
            "Please replace 'epic' with 'path', and 'spike' with 'probe'.\n"
            "Violations:\n" + "\n".join(violations)
        )
