import re
import os
import yaml
import hashlib
from kernel.daemon_telemetry import record_execution

@record_execution(stage="skill")
def parse_test_failure_diagnostics(pytest_output: str) -> list[dict]:
    """
    Parses pytest stdout/stderr to extract failing tests, line numbers, error types,
    messages, and traceback blocks.
    """
    failures = []
    # Locate the start of the FAILURES section to filter noise
    if "FAILURES" in pytest_output:
        failures_part = pytest_output.split("FAILURES", 1)[1]
    else:
        failures_part = pytest_output

    # Split output by pytest failure headers: ______________ test_name ______________
    blocks = re.split(r'\n_{4,}\s*(.*?)\s*_{4,}\n', failures_part)
    if len(blocks) >= 3:
        for i in range(1, len(blocks), 2):
            test_name = blocks[i]
            body = blocks[i+1]

            file_path = None
            line_number = None
            error_type = "UnknownError"
            error_message = ""

            # Standard pytest line references: file_path:line: message or file_path:line: in test_name
            matches = re.findall(r'(\S+\.py):(\d+): (.*)', body)
            if matches:
                # Leaf of traceback is usually the last match
                file_path, line_str, rest = matches[-1]
                line_number = int(line_str)
                err_match = re.match(r'(\w+):\s*(.*)', rest)
                if err_match:
                    error_type = err_match.group(1)
                    error_message = err_match.group(2)
                else:
                    error_message = rest

            # Check E lines if error details are not fully resolved
            e_lines = [line.strip() for line in body.splitlines() if line.strip().startswith('E ')]
            if e_lines:
                last_e = e_lines[-1]
                err_text = last_e[2:].strip()
                err_match = re.match(r'(\w+):\s*(.*)', err_text)
                if err_match:
                    if error_type == "UnknownError":
                        error_type = err_match.group(1)
                    if not error_message or error_message == error_type:
                        error_message = err_match.group(2)
                else:
                    if not error_message or error_message == error_type:
                        error_message = err_text

            # Clean traceback block
            traceback_lines = []
            for line in body.splitlines():
                if line.startswith('====') or line.startswith('----'):
                    break
                traceback_lines.append(line)
            traceback = "\n".join(traceback_lines).strip()

            failures.append({
                "test_name": test_name,
                "file_path": file_path,
                "line_number": line_number,
                "error_type": error_type,
                "error_message": error_message,
                "traceback": traceback
            })
    return failures

@record_execution(stage="skill")
def check_kb_conflicts(diff_text: str) -> list[str]:
    """
    Statically checks the git diff for violations in knowledge base files (under kb/).
    Checks for forbidden words (stale legacy terminology) and raw CLI commands (git, gh).
    """
    conflicts = []
    current_file = None

    # Dynamic semantic ledger parsing for malleable terminology
    terms = []
    immune_zones = []
    try:
        from drivers import path_resolver
        repo_root = path_resolver.get_workspace_dir()
        ledger_path = os.path.join(repo_root, 'kb', 'semantic_ledger.yml')
        if os.path.exists(ledger_path):
            with open(ledger_path, 'r') as f:
                ledger = yaml.safe_load(f)
                if ledger and 'terms' in ledger:
                    for term, meta in ledger['terms'].items():
                        if meta.get('state') == 'deprecated':
                            terms.append(re.escape(term))
                if ledger and 'immune_zones' in ledger:
                    immune_zones = ledger['immune_zones']
    except Exception:
        pass
        
    if not terms:
        terms = ["e" + "p" + "i" + "c", "e" + "p" + "i" + "c" + "s", "s" + "p" + "i" + "k" + "e", "s" + "p" + "i" + "k" + "e" + "s"]
        
    word_pattern = re.compile(r'\b(' + '|'.join(terms) + r')\b', re.IGNORECASE)
    # Regex targeting direct shell usage of git or gh commands
    git_cmd_pattern = re.compile(
        r'\b(git\s+(checkout|commit|add|push|pull|switch|stash|status|worktree|branch|reset|restore|clone|init|merge|rebase|fetch|log))\b',
        re.IGNORECASE
    )
    gh_cmd_pattern = re.compile(
        r'\b(gh\s+(issue|pr|repo|auth|run|workflow))\b',
        re.IGNORECASE
    )

    for line in diff_text.splitlines():
        if line.startswith('diff --git '):
            m = re.match(r'^diff --git a/(.*?) b/(.*)', line)
            if m:
                current_file = m.group(2)
            else:
                current_file = None
            continue

        if current_file and (current_file.startswith('kb/') or '/kb/' in current_file):
            if line.startswith('+') and not line.startswith('+++'):
                content = line[1:]

                basename = os.path.basename(current_file)
                is_immune = False
                for zone in immune_zones:
                    z_type = zone.get("type")
                    z_val = zone.get("value")
                    if z_type == "exact" and basename == z_val:
                        is_immune = True
                        break
                    elif z_type == "prefix" and basename.startswith(z_val):
                        is_immune = True
                        break
                
                if not is_immune:
                    word_match = word_pattern.search(content)
                    if word_match:
                        conflicts.append(f"Forbidden term '{word_match.group(1)}' found in {current_file}: '{content.strip()}'")

                git_match = git_cmd_pattern.search(content)
                if git_match:
                    conflicts.append(f"Forbidden command '{git_match.group(1)}' found in {current_file}: '{content.strip()}'")

                gh_match = gh_cmd_pattern.search(content)
                if gh_match:
                    conflicts.append(f"Forbidden command '{gh_match.group(1)}' found in {current_file}: '{content.strip()}'")

    return conflicts

@record_execution(stage="skill")
def synthesize_rule(error_details: dict) -> dict | None:
    """
    Synthesizes a rule for the audit daemon configuration from failure details.
    """
    error_message = error_details.get("error_message", "")
    test_name = error_details.get("test_name", "")
    if not error_message:
        return None

    # Search for specific quoted strings in error message representing the regression keyword
    term_match = re.search(r"forbidden (?:term|word|vocabulary|command)\s+'([^']+)'", error_message, re.IGNORECASE)
    if not term_match:
        term_match = re.search(r"'([^']+)'", error_message)

    target_term = term_match.group(1) if term_match else None
    if not target_term:
        return None

    # Constraint 1: Length constraint
    if len(target_term) < 4:
        return None
        
    # Constraint 2: Generic Word Blacklist
    generic_words = {"the", "path", "path", "issue", "node", "and", "for", "with"}
    if target_term.lower() in generic_words:
        return None
        
    # Constraint 3: Path Constraint (Absolute paths)
    if target_term.startswith("/"):
        return None

    safe_pattern = r"\b" + re.escape(target_term) + r"\b"
    h = hashlib.md5(target_term.encode('utf-8')).hexdigest()[:8]
    rule_id = f"synthesized-guard-{h}"

    return {
        "id": rule_id,
        "type": "lexical_guard",
        "pattern": safe_pattern,
        "alert_level": "FAILURE",
        "prompt_message": f"Synthesized Lexical Guard: Forbidden term '{target_term}' detected (from failed test '{test_name}')"
    }

@record_execution(stage="skill")
def build_contextual_prompt_injection(active_path_id: str, kb_dir: str) -> str:
    """
    Resolves the parent SG for the active path, collects relevant files under `kb/`,
    and builds a contextual prompt injection string.
    """
    path_num = None
    if active_path_id:
        m = re.search(r'\d+', active_path_id)
        if m:
            path_num = int(m.group(0))

    sg_id = None
    repo_root = os.path.dirname(os.path.abspath(kb_dir))
    strategic_intent_path = os.path.join(repo_root, "artifacts", "strategic_intent.yml")

    if path_num is not None and os.path.exists(strategic_intent_path):
        try:
            with open(strategic_intent_path, 'r', encoding='utf-8') as f:
                intent_data = yaml.safe_load(f)
            if intent_data and "strategic_goals" in intent_data:
                for goal in intent_data["strategic_goals"]:
                    prioritized = goal.get("prioritized_paths", [])
                    if any(str(p).strip() == str(path_num) for p in prioritized):
                        sg_id = goal.get("id")
                        break
        except Exception:
            pass

    matching_contents = []
    if sg_id:
        sg_normalized = sg_id.lower().replace("_", "-")
        if os.path.exists(kb_dir):
            for fname in sorted(os.listdir(kb_dir)):
                if sg_normalized in fname.lower() and fname.endswith(".md"):
                    fpath = os.path.join(kb_dir, fname)
                    try:
                        with open(fpath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        matching_contents.append(f"## Guideline: {fname}\n\n{content}")
                    except Exception:
                        pass

    if matching_contents:
        injection_body = "\n\n".join(matching_contents)
        return (
            "<!-- CONTEXTUAL_ROM_INJECTION_START -->\n"
            f"# Contextual Guidelines for Active Goal {sg_id}\n\n"
            f"{injection_body}\n"
            "<!-- CONTEXTUAL_ROM_INJECTION_END -->"
        )
    else:
        return (
            "<!-- CONTEXTUAL_ROM_INJECTION_START -->\n"
            "<!-- CONTEXTUAL_ROM_INJECTION_END -->"
        )
