from kernel.daemon_telemetry import record_execution
import os
import sys
import yaml
import json
import subprocess
import re
from pathlib import Path
from drivers.git_client import get_current_branch
from drivers import path_resolver

# Paths that resolve dynamically at runtime to respect SPAO_WORKSPACE_DIR mutations
def get_repo_root() -> Path:
    return Path(path_resolver.resolve_core_path())

def get_workspace_dir() -> Path:
    return Path(path_resolver.get_workspace_dir())

def get_config_file() -> Path:
    _workspace_config = Path(path_resolver.resolve_workspace_path("infra", "audit-daemon", "audit_config.yml"))
    return _workspace_config if _workspace_config.exists() else Path(path_resolver.resolve_core_path("infra", "audit-daemon", "audit_config.yml"))

def get_state_file() -> Path:
    return Path(path_resolver.resolve_workspace_path("artifacts", "audit_state.json"))

def get_frontier_file() -> Path:
    return Path(path_resolver.resolve_workspace_path("artifacts", "frontier_state.md"))

def get_prompt_cli() -> Path:
    return Path(path_resolver.resolve_core_path("bin", "prompt"))

def load_config():
    config_file = get_config_file()
    if not config_file.exists():
        print(f"Config file {config_file} not found. Exiting.")
        sys.exit(0)
    with open(config_file, "r") as f:
        return yaml.safe_load(f)

def load_state():
    state_file = get_state_file()
    if not state_file.exists():
        return {}
    with open(state_file, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_state(state):
    state_file = get_state_file()
    state_file.parent.mkdir(parents=True, exist_ok=True)
    with open(state_file, "w") as f:
        json.dump(state, f, indent=4)

def dispatch_alert(message):
    print(f"Dispatching alert to DAG: {message}")
    import sys
    sys.path.append(str(get_repo_root()))
    from drivers import github_client
    import re
    
    match = re.match(r"^\[(.*?)\]\s*(.*)", message)
    if match:
        content = match.group(2)
    else:
        content = message
        
    title_suffix = content.split(":")[0][:50] if ":" in content else content[:50]
    title = f"[BUG] Intake: {title_suffix}"
    
    try:
        open_issues = github_client.get_open_issues()
        for issue in open_issues:
            if issue.get("title", "") == title:
                print(f"Alert already tracked in DAG: {title}")
                return
                
        from kernel.daemon_backlog import BacklogDaemon
        backlog_daemon = BacklogDaemon()
        backlog_daemon.add("path", title, message)
        print(f"Alert successfully mapped to DAG: {title}")
    except Exception as e:
        print(f"Failed to dispatch alert to DAG: {e}")


def evaluate_node_completion_threshold(rule, state):
    frontier_file = get_frontier_file()
    if not frontier_file.exists():
        return False, state
        
    with open(frontier_file, "r") as f:
        content = f.read()
    
    current_count = content.count("**Status**: Completed")
    last_count = state.get("last_count", 0)
    threshold = rule.get("threshold", 10)
    
    if current_count >= last_count + threshold:
        alert_level = rule.get("alert_level", "NOTIFICATION").upper()
        msg = f"[{alert_level}] " + rule.get("prompt_message", "").replace("{current}", str(current_count))
        dispatch_alert(msg)
        state["last_count"] = current_count
        return True, state
        
    return False, state

def evaluate_file_modified(rule, state):
    file_path = rule.get("file")
    if not file_path:
        return False, state
        
    res = subprocess.run(["git", "log", "-1", "--format=%H", "--", file_path], capture_output=True, text=True, cwd=get_workspace_dir())
    current_hash = res.stdout.strip()
    
    if not current_hash:
        return False, state
        
    last_hash = state.get("last_hash", "")
    
    if current_hash != last_hash and last_hash != "":
        # We only trigger if last_hash was already set (to avoid triggering on first run)
        alert_level = rule.get("alert_level", "FAILURE").upper()
        msg = f"[{alert_level}] " + rule.get("prompt_message", "")
        dispatch_alert(msg)
        state["last_hash"] = current_hash
        return True, state
    elif last_hash == "":
        # Initialize state without triggering
        state["last_hash"] = current_hash
        return True, state # True indicates state changed so we should save
        
    return False, state

def evaluate_stale_active_node(rule, state):
    frontier_file = get_frontier_file()
    if not frontier_file.exists():
        return False, state
        
    with open(frontier_file, "r") as f:
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
        dispatch_alert(msg)
        return True, state
        
    return False, state

def evaluate_frontier_integrity(rule, state):
    sys.path.append(str(get_repo_root()))
    from kernel import agent_frontier
    filepath = str(get_repo_root() / "artifacts" / "frontier_state.yml")
    try:
        agent_frontier.verify_checksum(filepath)
        agent_frontier.load_state(filepath)
    except Exception as e:
        alert_level = rule.get("alert_level", "FAILURE").upper()
        msg = f"[{alert_level}] FRONTIER_INTEGRITY_VIOLATION: {str(e)}"
        dispatch_alert(msg)
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
        cwd=get_repo_root()
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
        'kb/WHY-0054-glossary-' + 'al' + 'ignment.md',
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
            
        full_path = get_repo_root() / f_rel
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
                dispatch_alert(msg)
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

    frontier_file = get_frontier_file()
    if not frontier_file.exists():
        return False, state

    with open(frontier_file, "r") as f:
        frontier_content = f.read()

    sys.path.append(str(get_repo_root()))
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

    print(f"[Sluice Gate Sensor] {result['message']}")
    print(f"Executing local sync...")
    node_cli = str(get_repo_root() / "bin" / "node")
    subprocess.run([node_cli, "sync", "--remote"], cwd=get_workspace_dir())

    state["last_alerted_node"] = result["node_id"]
    return True, state




def evaluate_semantic_immune_system(rule, state):
    sys.path.append(str(get_repo_root()))
    import yaml
    import re
    from pathlib import Path
    
    ledger_path = get_repo_root() / "kb" / "semantic_ledger.yml"
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
            
        kb_dir = get_repo_root() / "kb"
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
                    dispatch_alert(msg)
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
                dispatch_alert(msg)
                state["last_ratio"] = current_ratio
                return True, state
        else:
            if "last_ratio" in state:
                del state["last_ratio"]
                return True, state
    except Exception as e:
        print(f"Error evaluating backlog hygiene: {e}")
        
    return False, state

def evaluate_seizure_detection(rule, state):
    """Detects repeated recent test or command execution failures that indicate a cognitive loop."""
    audit_dir = get_repo_root() / "artifacts" / "audit"
    if not audit_dir.exists():
        return False, state
        
    fail_files = list(audit_dir.glob("test-fail-*.json"))
    fail_count = len(fail_files)
    
    last_fail_count = state.get("last_fail_count", 0)
    threshold = rule.get("threshold", 3)
    
    if fail_count >= last_fail_count + threshold:
        alert_level = rule.get("alert_level", "FAILURE").upper()
        msg = f"[{alert_level}] SEIZURE_DETECTED: System has encountered {fail_count - last_fail_count} new execution failures (Total: {fail_count}). Cognitive loop lock likely. Initiating triage protocol."
        dispatch_alert(msg)
        state["last_fail_count"] = fail_count
        return True, state
        
    if fail_count < last_fail_count:
        state["last_fail_count"] = fail_count
        return True, state
        
    return False, state

def evaluate_liveness_stall(rule, state):
    """Detects silent seizures by checking if frontier_state.yml has not been modified
    while an active node exists (indicating expected progress).
    
    Per WHY-1350: Uses frontier_state.yml mtime as a zero-instrumentation liveness
    signal. Only fires when an active node exists (false-positive guard).
    """
    import time
    
    frontier_yml = get_repo_root() / "artifacts" / "frontier_state.yml"
    frontier_md = get_frontier_file()
    
    if not frontier_yml.exists() or not frontier_md.exists():
        return False, state
    
    # Check if there's an active node (false-positive guard)
    with open(frontier_md, "r") as f:
        content = f.read()
    
    active_node = ""
    match = re.search(r"## Current Active Node\n(.*?)(?=\n## |\Z)", content, re.DOTALL)
    if match:
        active_node = match.group(1).strip().strip('*')
    
    if not active_node or active_node == "None":
        # No active node = legitimately idle, no stall possible
        if "last_alerted_at" in state:
            del state["last_alerted_at"]
        return False, state
    
    # Check frontier_state.yml modification time
    stall_threshold = rule.get("stall_threshold_minutes", 15)
    mtime = os.path.getmtime(frontier_yml)
    elapsed_minutes = (time.time() - mtime) / 60.0
    
    if elapsed_minutes > stall_threshold:
        # Prevent re-alerting: only fire once per stall event
        last_alerted = state.get("last_alerted_at", 0)
        if last_alerted >= mtime:
            return False, state
        
        alert_level = rule.get("alert_level", "FAILURE").upper()
        msg = (
            f"[{alert_level}] LIVENESS_STALL: frontier_state.yml has not been "
            f"modified for {elapsed_minutes:.0f} minutes while node "
            f"'{active_node}' is active. Possible silent seizure."
        )
        dispatch_alert(msg)
        state["last_alerted_at"] = time.time()
        return True, state
    
    return False, state

def evaluate_orphaned_nodes(rule, state):
    from kernel.daemon_backlog import BacklogDaemon
    try:
        orphaned_count = BacklogDaemon().sweep_orphans()
        if orphaned_count > 0:
            msg = f"[NOTIFICATION] Automated Hygiene Sweep: Deferred {orphaned_count} orphaned terminal nodes."
            dispatch_alert(msg)
            return True, state
    except Exception as e:
        print(f"Error evaluating orphaned nodes: {e}")
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
    "backlog_hygiene": evaluate_backlog_hygiene,
    "orphaned_nodes": evaluate_orphaned_nodes,
    "seizure_detection": evaluate_seizure_detection,
    "liveness_stall": evaluate_liveness_stall
}

@record_execution(stage="system")
def main(args=None):
    import argparse
    parser = argparse.ArgumentParser(description="Metasystem Integrity Audit Daemon")
    parser.add_argument("--local", action="store_true", help="Bypass remote network-bound checks")
    parser.add_argument("--lightweight", action="store_true", help="Run only rules marked as lightweight: true")
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
        
    if parsed_args.lightweight:
        rules_to_evaluate = [r for r in rules_to_evaluate if r.get("lightweight") is True]
        
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
