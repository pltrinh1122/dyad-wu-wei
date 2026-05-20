import os
import sys
import yaml
import hashlib
import argparse
import re
from skills import path_resolver
from skills import github_client

def get_ledger_path():
    env_path = os.environ.get("SPAO_STRATEGIC_LEDGER_PATH")
    if env_path:
        return os.path.abspath(env_path)
    return path_resolver.resolve_workspace_path("artifacts", "strategic_intent.yml")

def load_ledger():
    path = get_ledger_path()
    if not os.path.exists(path):
        return {"strategic_goals": []}
    with open(path, "r") as f:
        return yaml.safe_load(f) or {"strategic_goals": []}

def save_ledger(data):
    path = get_ledger_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)
    rehash_ledger()
    generate_markdown(data)

def rehash_ledger():
    path = get_ledger_path()
    checksum_path = path + ".sha256"
    if not os.path.exists(path):
        return
    with open(path, "rb") as f:
        h = hashlib.sha256(f.read()).hexdigest()
    with open(checksum_path, "w") as f:
        f.write(h + "\n")

def generate_markdown(data):
    path = get_ledger_path()
    md_path = path.replace(".yml", ".md")
    
    goals = data.get("strategic_goals", [])
    
    by_status = {"Active": [], "Draft": [], "Achieved": [], "Falsified": []}
    for g in goals:
        status = g.get("status", "Draft")
        if status in by_status:
            by_status[status].append(g)
        else:
            by_status["Draft"].append(g)
            
    content = []
    content.append("# Strategic Intent Ledger\n")
    
    for status in ["Active", "Draft", "Achieved", "Falsified"]:
        content.append(f"## {status} Goals")
        goals_list = by_status[status]
        if not goals_list:
            content.append("*No goals in this state.*\n")
            continue
            
        for g in goals_list:
            paths_str = ", ".join(str(p) for p in g.get("prioritized_paths", [])) or "None"
            content.append(f"### {g.get('id')}: {g.get('title')}")
            content.append(f"- **Collaborative Gap**: {g.get('collaborative_gap')}")
            content.append(f"- **Constraints**: {g.get('constraints')}")
            content.append(f"- **Falsification Signal**: {g.get('falsification_signal')}")
            content.append(f"- **Prioritized Paths**: {paths_str}")
            if g.get("falsification_notes"):
                content.append(f"- **Falsification Notes**: {g.get('falsification_notes')}")
            content.append("")
            
    with open(md_path, "w") as f:
        f.write("\n".join(content))

def validate_goal(goal: dict) -> list[str]:
    errors = []
    
    gap = goal.get("collaborative_gap", "")
    if not gap or not str(gap).strip():
        errors.append("Grounding error: 'collaborative_gap' is empty or missing.")
        
    constraints = goal.get("constraints", "")
    if not constraints or not str(constraints).strip():
        errors.append("Constraint error: 'constraints' is empty or missing.")
    else:
        forbidden_verbs = ["fix", "solve", "remedy", "remove", "eliminate", "correct"]
        constraints_lower = str(constraints).lower()
        for verb in forbidden_verbs:
            if re.search(r'\b' + verb + r'\b', constraints_lower):
                errors.append(f"Constraint error: constraint cannot frame facts as action/problem (contains action verb '{verb}').")
                
        # Axiom (3) (Materializability) Validation
        forbidden_assumptions = ["infinite", "instantaneous", "zero latency", "perfect network", "unlimited token", "unlimited context", "agi"]
        for word in forbidden_assumptions:
            if word in constraints_lower or word in str(gap).lower():
                errors.append(f"Materializability error: goal assumes non-physical or speculative capabilities (contains term '{word}').")
                
    falsification = goal.get("falsification_signal", "")
    if not falsification or not str(falsification).strip():
        errors.append("Falsifiability error: 'falsification_signal' is empty or missing.")
        
    return errors


def cmd_list():
    data = load_ledger()
    goals = data.get("strategic_goals", [])
    if not goals:
        print("No strategic goals found in the ledger.")
        return
        
    print(f"{'ID':<8} | {'Title':<25} | {'Status':<10} | {'Prioritized Paths'}")
    print("-" * 70)
    for g in goals:
        paths = ", ".join(str(p) for p in g.get("prioritized_paths", [])) or "None"
        print(f"{g.get('id'):<8} | {g.get('title', '')[:25]:<25} | {g.get('status', 'Draft'):<10} | {paths}")

def cmd_add(args):
    if args.title is None and args.gap is None and args.constraints is None and args.falsification is None:
        print("=== Add a New Strategic Goal ===")
        title = input("Goal Title: ").strip()
        gap = input("Collaborative Gap (grounding): ").strip()
        constraints = input("Constraints (facts, no action verbs): ").strip()
        falsification = input("Falsification Signal: ").strip()
        paths_str = input("Prioritized Path IDs (comma-separated, optional): ").strip()
        
        paths = []
        if paths_str:
            for p in paths_str.split(","):
                if p.strip():
                    paths.append(int(p.strip()))
    else:
        title = args.title or ""
        gap = args.gap or ""
        constraints = args.constraints or ""
        falsification = args.falsification or ""
        paths = []
        if args.paths:
            paths = [int(p) for p in args.paths]
            
    goal = {
        "title": title,
        "collaborative_gap": gap,
        "constraints": constraints,
        "falsification_signal": falsification,
        "status": "Active",
        "prioritized_paths": paths
    }
    
    errors = validate_goal(goal)
    if errors:
        print("Validation errors occurred. Goal not added:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
        
    data = load_ledger()
    goals = data.get("strategic_goals", [])
    
    max_id = 0
    for g in goals:
        gid = g.get("id", "")
        if gid.startswith("SG-"):
            try:
                num = int(gid[3:])
                if num > max_id:
                    max_id = num
            except ValueError:
                pass
    new_id = f"SG-{max_id + 1:04d}"
    
    goal["id"] = new_id
    goals.append(goal)
    data["strategic_goals"] = goals
    
    save_ledger(data)
    print(f"Successfully added goal {new_id} to ledger.")

def verify_prioritized_paths(goals: list) -> bool:
    """Verifies that all prioritized paths in Active goals exist and are open on GitHub."""
    is_offline = os.environ.get("ANTIGRAVITY_RUNNING_TESTS") == "1" or os.environ.get("SPAO_OFFLINE") == "1"
    if is_offline:
        print("ℹ️  Offline environment detected. Bypassing live GitHub path verification.")
        return True

    print("🔍 Verifying active prioritized path alignments on GitHub...")
    all_paths_ok = True
    for g in goals:
        if g.get("status") == "Active":
            paths = g.get("prioritized_paths", [])
            for path_id in paths:
                try:
                    details = github_client.get_issue_details(str(path_id))
                    if not details or not details.get("number"):
                        print(f"❌ Path {path_id} (under goal {g.get('id')}) does not exist on GitHub.")
                        all_paths_ok = False
                    elif details.get("state", "").upper() != "OPEN":
                        print(f"❌ Path {path_id} (under goal {g.get('id')}) exists but is {details.get('state').upper()} on GitHub (expected OPEN).")
                        all_paths_ok = False
                    else:
                        print(f"✅ Path {path_id} (under goal {g.get('id')}) is open and valid.")
                except Exception as e:
                    print(f"❌ Path {path_id} (under goal {g.get('id')}) could not be verified: {e}")
                    all_paths_ok = False
    return all_paths_ok

def cmd_verify():
    data = load_ledger()
    goals = data.get("strategic_goals", [])
    
    print("🔍 Verifying strategic ledger...")
    all_ok = True
    
    for g in goals:
        errors = validate_goal(g)
        if errors:
            print(f"❌ Goal {g.get('id')} ({g.get('title')}) has validation failures:")
            for err in errors:
                print(f"  - {err}")
            all_ok = False
        else:
            print(f"✅ Goal {g.get('id')} ({g.get('title')}) is valid.")
            
    paths_ok = verify_prioritized_paths(goals)
    if not paths_ok:
        all_ok = False

            
    try:
        backlog_items = github_client.list_issues_by_label("backlog")
        open_paths = []
        for item in backlog_items:
            num = str(item.get("number"))
            labels = github_client.get_issue_labels(num)
            if "path" in labels:
                open_paths.append(item)
                
        if open_paths:
            active_paths = set()
            for g in goals:
                if g.get("status") == "Active":
                    for p in g.get("prioritized_paths", []):
                        active_paths.add(str(p))
                        
            unmapped = []
            for p in open_paths:
                pnum = str(p.get("number"))
                if pnum not in active_paths:
                    unmapped.append(p)
                    
            if unmapped:
                print("⚠️  Warning: The following open backlog Paths are not mapped to any active strategic goal:")
                for p in unmapped:
                    print(f"  - #{p.get('number')}: {p.get('title')}")
            else:
                print("✅ All open backlog Paths are mapped to at least one active strategic goal.")
    except Exception as e:
        print(f"Warning: Failed to fetch backlog issues for mapping check: {e}")
        
    if all_ok:
        print("Ledger verification complete. All invariants satisfied.")
    else:
        print("❌ Ledger verification failed.")
        sys.exit(1)

def cmd_prioritize(args):
    data = load_ledger()
    goals = data.get("strategic_goals", [])
    target = None
    for g in goals:
        if g.get("id") == args.id:
            target = g
            break
            
    if not target:
        print(f"Error: Goal {args.id} not found in the ledger.")
        sys.exit(1)
        
    target["prioritized_paths"] = [int(p) for p in args.paths]
    save_ledger(data)
    print(f"Successfully updated prioritized paths for goal {args.id}.")

def cmd_transition(args):
    data = load_ledger()
    goals = data.get("strategic_goals", [])
    target = None
    for g in goals:
        if g.get("id") == args.id:
            target = g
            break
            
    if not target:
        print(f"Error: Goal {args.id} not found in the ledger.")
        sys.exit(1)
        
    status = args.status
    if status == "Falsified" and not args.notes:
        print("Error: Notes describing the falsification signal are required when transitioning to Falsified.")
        sys.exit(1)
        
    target["status"] = status
    if args.notes:
        target["falsification_notes"] = args.notes
        
    save_ledger(data)
    print(f"Successfully transitioned goal {args.id} to status '{status}'.")

_MOCK_PARENT_PATHS = {}
_FORCE_STRATEGIC_VERIFICATION = False

def find_parent_path_id(node_id: str) -> str | None:
    """Finds the parent path ID for a given terminal node ID by querying open Path issues on GitHub."""
    node_id_str = str(node_id)
    if node_id_str in _MOCK_PARENT_PATHS:
        return _MOCK_PARENT_PATHS[node_id_str]
        
    is_offline = os.environ.get("ANTIGRAVITY_RUNNING_TESTS") == "1" or os.environ.get("SPAO_OFFLINE") == "1"
    if is_offline:
        return None
        
    try:
        backlog_items = github_client.list_issues_by_label("backlog")
        for item in backlog_items:
            num = str(item.get("number"))
            labels = github_client.get_issue_labels(num)
            if "path" in labels:
                details = github_client.get_issue_details(num)
                body = details.get("body", "")
                
                pattern = re.compile(r"-\s+\[\s*x?\s*\]\s+Node\s+" + re.escape(str(node_id)) + r"\b", re.IGNORECASE)
                if pattern.search(body):
                    return num
    except Exception as e:
        print(f"Warning: Failed to find parent path for node {node_id} on GitHub: {e}")
    return None

def verify_node_transition_allowed(node_id: str) -> None:
    """Verifies that a node transition is allowed based on the strategic intent ledger."""
    node_id_str = str(node_id)
    
    is_offline = os.environ.get("ANTIGRAVITY_RUNNING_TESTS") == "1" or os.environ.get("SPAO_OFFLINE") == "1"
    if is_offline and not _FORCE_STRATEGIC_VERIFICATION:
        return
        
    parent_path_id = find_parent_path_id(node_id_str)
    if is_offline and not parent_path_id and not _FORCE_STRATEGIC_VERIFICATION:
        return
        
    if not parent_path_id:
        raise ValueError(f"Alignment Failure: Terminal Node #{node_id_str} has no parent Path.")
        
    ledger = load_ledger()
    active_prioritized_paths = set()
    for goal in ledger.get("strategic_goals", []):
        if goal.get("status") == "Active":
            for path_id in goal.get("prioritized_paths", []):
                active_prioritized_paths.add(str(path_id))
                
    if str(parent_path_id) not in active_prioritized_paths:
        raise Exception(f"Transition Blocked: Parent Path #{parent_path_id} of Node #{node_id_str} is not prioritized in the active strategic ledger.")

def verify_path_activation_allowed(path_id: str) -> None:
    """Verifies that a path activation is allowed based on the strategic intent ledger."""
    is_offline = os.environ.get("ANTIGRAVITY_RUNNING_TESTS") == "1" or os.environ.get("SPAO_OFFLINE") == "1"
    if is_offline and not _FORCE_STRATEGIC_VERIFICATION:
        return
        
    path_id_str = str(path_id)
    ledger = load_ledger()
    active_prioritized_paths = set()
    for goal in ledger.get("strategic_goals", []):
        if goal.get("status") == "Active":
            for p in goal.get("prioritized_paths", []):
                active_prioritized_paths.add(str(p))
                
    if path_id_str not in active_prioritized_paths:
        raise Exception(f"Path Activation Blocked: Path #{path_id_str} is not prioritized in the active strategic ledger.")

def main():
    parser = argparse.ArgumentParser(description="Manage the strategic intent ledger.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    subparsers.add_parser("list", help="List all strategic goals.")
    
    add_parser = subparsers.add_parser("add", help="Add a new strategic goal.")
    add_parser.add_argument("--title", help="Goal title.")
    add_parser.add_argument("--gap", help="Collaborative relationship gap (grounding).")
    add_parser.add_argument("--constraints", help="Constraints.")
    add_parser.add_argument("--falsification", help="Falsification signal.")
    add_parser.add_argument("--paths", nargs="*", help="Prioritized path IDs.")
    
    subparsers.add_parser("verify", help="Verify the strategic ledger invariants.")
    
    prioritize_parser = subparsers.add_parser("prioritize", help="Define sequencing of Path IDs for a goal.")
    prioritize_parser.add_argument("id", help="Strategic goal ID (e.g. SG-0001).")
    prioritize_parser.add_argument("paths", nargs="+", help="Ordered Path IDs.")
    
    transition_parser = subparsers.add_parser("transition", help="Transition status of a goal.")
    transition_parser.add_argument("id", help="Strategic goal ID (e.g. SG-0001).")
    transition_parser.add_argument("status", choices=["Active", "Draft", "Achieved", "Falsified"], help="Target status.")
    transition_parser.add_argument("notes", nargs="?", help="Notes (required for Falsified).")
    
    args = parser.parse_args()
    
    if args.command == "list":
        cmd_list()
    elif args.command == "add":
        cmd_add(args)
    elif args.command == "verify":
        cmd_verify()
    elif args.command == "prioritize":
        cmd_prioritize(args)
    elif args.command == "transition":
        cmd_transition(args)

if __name__ == "__main__":
    main()
