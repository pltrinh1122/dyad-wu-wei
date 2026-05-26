import os
import sys
import yaml
import json
import subprocess
import re
from pathlib import Path
from drivers.git_client import get_current_branch
from drivers import path_resolver

# Paths
REPO_ROOT = Path(path_resolver.resolve_core_path())
WORKSPACE_DIR = Path(path_resolver.get_workspace_dir())

_workspace_config = Path(path_resolver.resolve_workspace_path("infra", "audit-daemon", "audit_config.yml"))
CONFIG_FILE = _workspace_config if _workspace_config.exists() else Path(path_resolver.resolve_core_path("infra", "audit-daemon", "audit_config.yml"))
STATE_FILE = Path(path_resolver.resolve_workspace_path("artifacts", "audit_state.json"))
FRONTIER_FILE = Path(path_resolver.resolve_workspace_path("artifacts", "frontier_state.md"))
PROMPT_CLI = Path(path_resolver.resolve_core_path("bin", "prompt"))

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
    subprocess.run([str(PROMPT_CLI), "add", message], check=True, cwd=WORKSPACE_DIR)

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
        
    res = subprocess.run(["git", "log", "-1", "--format=%H", "--", file_path], capture_output=True, text=True, cwd=WORKSPACE_DIR)
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
    """Evaluates the Sluice Gate Sensor: detects when the active node PR is merged.

    Delegates all logic to the pure ``drivers.sluice_gate_sensor`` skill and
    surfaces errors explicitly rather than swallowing them.
    """
    from drivers import sluice_gate_sensor

    if not FRONTIER_FILE.exists():
        return False, state

    with open(FRONTIER_FILE, "r") as f:
        frontier_content = f.read()

    sys.path.append(str(REPO_ROOT))
    from drivers.github_client import get_merged_prs

    try:
        merged_prs = get_merged_prs()
    except Exception as e:
        print(f"[Sluice Gate Sensor] Error fetching merged PRs: {e}")
        return False, state

    last_alerted = state.get("last_alerted_node")
    result = sluice_gate_sensor.evaluate(frontier_content, merged_prs, last_alerted_node=last_alerted)

    if result["error"]:
        print(f"[Sluice Gate Sensor] Evaluation error: {result['error']}")
        return False, state

    if not result["triggered"]:
        return False, state

    alert_level = rule.get("alert_level", "NOTIFICATION").upper()
    msg = f"[{alert_level}] {result['message']}"
    inject_prompt(msg)

    state["last_alerted_node"] = result["node_id"]
    return True, state




def evaluate_semantic_immune_system(rule, state):
    sys.path.append(str(REPO_ROOT))
    import yaml
    import re
    from pathlib import Path
    
    ledger_path = REPO_ROOT / "kb" / "semantic_ledger.yml"
    if not ledger_path.exists():
        return False, state
        
    try:
        with open(ledger_path, "r") as f:
            ledger = yaml.safe_load(f)
            
        deprecated_terms = []
        if ledger and "terms" in ledger:
            for term, meta in ledger["terms"].items():
                if meta.get("state") == "deprecated":
                    deprecated_terms.append(term)
                    
        if not deprecated_terms:
            return False, state
            
        kb_dir = REPO_ROOT / "kb"
        pollution_found = []
        
        term_patterns = {term: re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE) for term in deprecated_terms}
        
        immune_zones = ledger.get("immune_zones", [])
        
        for md_file in kb_dir.rglob("*.md"):
            is_immune = False
            for zone in immune_zones:
                zone_type = zone.get("type")
                zone_val = zone.get("value")
                if zone_type == "exact" and md_file.name == zone_val:
                    is_immune = True
                    break
                elif zone_type == "prefix" and md_file.name.startswith(zone_val):
                    is_immune = True
                    break
                    
            if is_immune:
                continue
                
            try:
                with open(md_file, "r") as f:
                    content = f.read()
                    
                for term, pattern in term_patterns.items():
                    if pattern.search(content):
                        pollution_found.append((term, md_file.name))
            except Exception:
                continue
                
        if pollution_found:
            created_activities = state.get("created_activities", [])
            state_changed = False
            
            for term, filename in pollution_found:
                activity_key = f"{term}_{filename}"
                if activity_key not in created_activities:
                    msg = f"[NOTIFICATION] Semantic immune system detected pollution: deprecated term '{term}' found in {filename}. Please remediate."
                    inject_prompt(msg)
                    created_activities.append(activity_key)
                    state_changed = True
                    
            if state_changed:
                state["created_activities"] = created_activities
                return True, state
                
    except Exception as e:
        print(f"Error in evaluate_semantic_immune_system: {e}")
        
    return False, state

def evaluate_backlog_hygiene(rule, state):
    from kernel.daemon_backlog import BacklogDaemon
    try:
        grouped = BacklogDaemon().list()
        unmapped_count = len(grouped.get("📋 [Backlog / Unmapped]", []))
        mapped_count = sum(len(issues) for key, issues in grouped.items() if "Unmapped" not in key)
        
        if unmapped_count > mapped_count:
            msg = f"[NOTIFICATION] Backlog Hygiene Warning: Unmapped Paths ({unmapped_count}) exceed Mapped Paths ({mapped_count}). Repository state is unhealthy."
            last_ratio = state.get("last_ratio")
            current_ratio = f"{unmapped_count}:{mapped_count}"
            if current_ratio != last_ratio:
                inject_prompt(msg)
                state["last_ratio"] = current_ratio
                return True, state
        else:
            if "last_ratio" in state:
                del state["last_ratio"]
                return True, state
    except Exception as e:
        print(f"Error evaluating backlog hygiene: {e}")
        
    return False, state

# Registry mapping rule types to evaluator functions
RULE_REGISTRY = {
    "node_completion_threshold": evaluate_node_completion_threshold,
    "file_modified": evaluate_file_modified,
    "stale_active_node": evaluate_stale_active_node,
    "frontier_integrity": evaluate_frontier_integrity,
    "lexical_guard": evaluate_lexical_guard,
    "pr_merged_monitor": evaluate_pr_merged_monitor,
    "semantic_immune_system": evaluate_semantic_immune_system,
    "backlog_hygiene": evaluate_backlog_hygiene
}

def main(args=None):
    import argparse
    parser = argparse.ArgumentParser(description="Metasystem Integrity Audit Daemon")
    parser.add_argument("--local", action="store_true", help="Bypass remote network-bound checks")
    parsed_args, _ = parser.parse_known_args(args)

    config = load_config()
    
    audit_branches = config.get("audit_branches", ["main"])
    current_branch = get_current_branch()
    
    rules = config.get("rules", [])
    
    if current_branch not in audit_branches:
        print(f"Audit daemon ignoring branch: {current_branch}. Target branches: {audit_branches}. Evaluating global rules only.")
        rules_to_evaluate = [r for r in rules if r.get("type") in ("pr_merged_monitor", "semantic_immune_system", "backlog_hygiene")]
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
            
        if parsed_args.local and rule_type == "pr_merged_monitor":
            print(f"Skipping remote-bound rule {rule_id} in local mode.")
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
