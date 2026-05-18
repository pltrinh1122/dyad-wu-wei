import os
import sys
import yaml
import json
import subprocess
from pathlib import Path

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

def get_current_branch():
    res = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True, cwd=REPO_ROOT)
    return res.stdout.strip()

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

# Registry mapping rule types to evaluator functions
RULE_REGISTRY = {
    "node_completion_threshold": evaluate_node_completion_threshold,
    "file_modified": evaluate_file_modified
}

def main():
    config = load_config()
    
    audit_branches = config.get("audit_branches", ["main"])
    current_branch = get_current_branch()
    
    if current_branch not in audit_branches:
        print(f"Audit daemon ignoring branch: {current_branch}. Target branches: {audit_branches}")
        return
        
    state = load_state()
    state_changed = False
    
    rules = config.get("rules", [])
    for rule in rules:
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
