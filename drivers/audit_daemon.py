import os
import sys
import yaml
import json
import subprocess
import re
from pathlib import Path
from drivers.git_client import get_current_branch

# Paths
REPO_ROOT = Path(__file__).parent.parent.resolve()
CONFIG_FILE = REPO_ROOT / "infra" / "audit-daemon" / "audit_config.yml"
STATE_FILE = REPO_ROOT / "artifacts" / "audit_state.json"
FRONTIER_FILE = REPO_ROOT / "artifacts" / "frontier_state.md"
PROMPT_CLI = REPO_ROOT / "bin" / "prompt"

def load_config():
    if not CONFIG_FILE.exists():
        print(f"Config file {CONFIG_FILE} not found. Exiting.")
        sys.exit(0)
    with open(CONFIG_FILE, "r") as f:
        return yaml.safe_load(f)

def load_state():
    if not STATE_FILE.exists():
        return {}
    with open(STATE_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def inject_prompt(message):
    print(f"Injecting prompt: {message}")
    subprocess.run([str(PROMPT_CLI), "add", message], check=True, cwd=REPO_ROOT)

def evaluate_node_completion_threshold(rule, state):
    if not FRONTIER_FILE.exists():
        return False, state
        
    with open(FRONTIER_FILE, "r") as f:
        content = f.read()
    
    current_count = content.count("**Status**: Completed")
    last_count = state.get("last_count", 0)
    threshold = rule.get("threshold", 10)
    
    if current_count >= last_count + threshold:
        alert_level = rule.get("alert_level", "NOTIFICATION").upper()
        msg = f"[{alert_level}] " + rule.get("prompt_message", "").replace("{current}", str(current_count))
        inject_prompt(msg)
        state["last_count"] = current_count
        return True, state
        
    return False, state

def evaluate_file_modified(rule, state):
    file_path = rule.get("file")
    if not file_path:
        return False, state
        
    res = subprocess.run(["git", "log", "-1", "--format=%H", "--", file_path], capture_output=True, text=True, cwd=REPO_ROOT)
    current_hash = res.stdout.strip()
    
    if not current_hash:
        return False, state
        
    last_hash = state.get("last_hash", "")
    
    if current_hash != last_hash and last_hash != "":
        # We only trigger if last_hash was already set (to avoid triggering on first run)
        alert_level = rule.get("alert_level", "FAILURE").upper()
        msg = f"[{alert_level}] " + rule.get("prompt_message", "")
        inject_prompt(msg)
        state["last_hash"] = current_hash
        return True, state
    elif last_hash == "":
        # Initialize state without triggering
        state["last_hash"] = current_hash
        return True, state # True indicates state changed so we should save
        
    return False, state

def evaluate_stale_active_node(rule, state):
    if not FRONTIER_FILE.exists():
        return False, state
        
    with open(FRONTIER_FILE, "r") as f:
        content = f.read()
        
    # Extract Active Node using simple regex to avoid complex imports
    active_node = ""
    match = re.search(r"## Current Active Node\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    if match:
        active_node = match.group(1).strip().strip('*')
        
    if not active_node or active_node == "None":
        return False, state
        
    # Look for ## <active_node> followed by "- **Status**: Completed"
    pattern = r"## " + re.escape(active_node) + r"\n- \*\*Status\*\*: Completed"
    if re.search(pattern, content):
        alert_level = rule.get("alert_level", "FAILURE").upper()
        msg = f"[{alert_level}] STALE_POINTER: Node '{active_node}' is marked as Active but is already Completed in the ledger."
        inject_prompt(msg)
        return True, state
        
    return False, state

def evaluate_frontier_integrity(rule, state):
    sys.path.append(str(REPO_ROOT))
    from kernel import agent_frontier
    filepath = str(REPO_ROOT / "artifacts" / "frontier_state.yml")
    try:
        agent_frontier.verify_checksum(filepath)
        agent_frontier.load_state(filepath)
    except Exception as e:
        alert_level = rule.get("alert_level", "FAILURE").upper()
        msg = f"[{alert_level}] FRONTIER_INTEGRITY_VIOLATION: {str(e)}"
        inject_prompt(msg)
        return True, state
    return False, state

def evaluate_lexical_guard(rule, state):
    pattern = rule.get("pattern")
    if not pattern:
        return False, state
        
    res = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT
    )
    if res.returncode != 0:
        return False, state
        
    modified_files = []
    for line in res.stdout.splitlines():
        if not line:
            continue
        status = line[:2].strip()
        filepath = line[3:].strip()
        if '->' in filepath:
            filepath = filepath.split('->')[-1].strip()
        if status != 'D':
            modified_files.append(filepath)
            
    import hashlib
    exemptions = {
        'kb/GLOSSARY.md',
        'artifacts/frontier_state.md',
        'artifacts/coherence_validation.md',
        'tests/test_lexical_guard.py',
        'kb/WHY-0054-glossary-alignment.md',
        'kb/WHAT-0054-glossary-spec.md'
    }
    
    regex = re.compile(pattern)
    triggered = False
    new_state = dict(state)
    triggered_files_state = new_state.get("triggered_files", {})
    
    for f_rel in modified_files:
        if f_rel in exemptions:
            continue
        if not (f_rel.endswith('.py') or f_rel.endswith('.md') or f_rel.endswith('.txt')):
            continue
            
        full_path = REPO_ROOT / f_rel
        if not full_path.exists():
            continue
            
        try:
            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            continue
            
        if regex.search(content):
            content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
            if triggered_files_state.get(f_rel) != content_hash:
                alert_level = rule.get("alert_level", "FAILURE").upper()
                msg = f"[{alert_level}] " + rule.get("prompt_message", f"Lexical Guard Violation in {f_rel}")
                inject_prompt(msg)
                triggered_files_state[f_rel] = content_hash
                triggered = True
                
    new_state["triggered_files"] = triggered_files_state
    return triggered, new_state

def evaluate_pr_merged_monitor(rule, state):
    if not FRONTIER_FILE.exists():
        return False, state
        
    with open(FRONTIER_FILE, "r") as f:
        content = f.read()
        
    active_node = ""
    match = re.search(r"## Current Active Node\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    if match:
        active_node = match.group(1).strip().strip('*')
        
    if not active_node or active_node == "None":
        return False, state
        
    id_match = re.search(r"(\d+)", active_node)
    if not id_match:
        return False, state
        
    node_id = id_match.group(1)
    
    if state.get("last_alerted_node") == node_id:
        return False, state
        
    sys.path.append(str(REPO_ROOT))
    from drivers.github_client import get_merged_prs
    
    try:
        merged_prs = get_merged_prs()
        for pr in merged_prs:
            head_ref = pr.get("headRefName", "")
            if head_ref.startswith(f"node/{node_id}-"):
                alert_level = rule.get("alert_level", "NOTIFICATION").upper()
                msg = f"[{alert_level}] Sluice Gate Opened: PR for Node {node_id} merged. Run `./bin/node sync` to continue."
                inject_prompt(msg)
                
                state["last_alerted_node"] = node_id
                return True, state
    except Exception:
        pass
        
    return False, state


# Registry mapping rule types to evaluator functions
RULE_REGISTRY = {
    "node_completion_threshold": evaluate_node_completion_threshold,
    "file_modified": evaluate_file_modified,
    "stale_active_node": evaluate_stale_active_node,
    "frontier_integrity": evaluate_frontier_integrity,
    "lexical_guard": evaluate_lexical_guard,
    "pr_merged_monitor": evaluate_pr_merged_monitor
}

def main():
    config = load_config()
    
    audit_branches = config.get("audit_branches", ["main"])
    current_branch = get_current_branch()
    
    rules = config.get("rules", [])
    
    if current_branch not in audit_branches:
        print(f"Audit daemon ignoring branch: {current_branch}. Target branches: {audit_branches}. Evaluating global rules only.")
        rules_to_evaluate = [r for r in rules if r.get("type") == "pr_merged_monitor"]
        if not rules_to_evaluate:
            return
    else:
        rules_to_evaluate = rules
        
    state = load_state()
    state_changed = False
        
    for rule in rules_to_evaluate:
        rule_id = rule.get("id")
        rule_type = rule.get("type")
        
        if not rule_id or not rule_type:
            continue
            
        evaluator = RULE_REGISTRY.get(rule_type)
        if not evaluator:
            print(f"Unknown rule type: {rule_type} for rule {rule_id}")
            continue
            
        rule_state = state.get(rule_id, {})
        triggered, new_rule_state = evaluator(rule, dict(rule_state))
        
        if triggered:
            state[rule_id] = new_rule_state
            state_changed = True
            
    if state_changed:
        save_state(state)

if __name__ == "__main__":
    main()
