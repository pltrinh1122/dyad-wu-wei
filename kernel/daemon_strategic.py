from kernel.daemon_telemetry import record_execution
import os
import sys
import yaml
import hashlib
import argparse
import re
from drivers import path_resolver
from drivers import github_client

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

    print("🔍 Verifying active prioritized path harmonizations on GitHub...")
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
        path_items = github_client.list_issues_by_label("path")
    except Exception as e:
        print(f"Warning: Failed to fetch path issues: {e}")
        return None

    for item in path_items:
        num = str(item.get("number"))
        try:
            details = github_client.get_issue_details(num)
            body = details.get("body", "")
            
            pattern = re.compile(r"-\s+\[\s*x?\s*\]\s*(?:(?:Node|Activity|Discovery)\s+|#)" + re.escape(str(node_id)) + r"\b", re.IGNORECASE)
            if pattern.search(body):
                return num
        except Exception as e:
            print(f"Warning: Failed to fetch issue details for path node {num}: {e}")
            continue
            
    return None

from drivers.markdown_parser import parse_md_table

def _is_pure_ziran(path_id: str, ledger: dict) -> bool:
    """Returns True if the path is unassigned to any domain or SG (Pure Ziran)."""
    # Check if in any SG
    for goal in ledger.get("strategic_goals", []):
        if str(path_id) in [str(p) for p in goal.get("prioritized_paths", [])]:
            return False
            
    # Check if in WHAT-0065
    what_0065_path = path_resolver.resolve_workspace_path("kb", "WHAT-0065-domain-path-ownership-index.md")
    if os.path.exists(what_0065_path):
        rows = parse_md_table(what_0065_path)
        for r in rows:
            if "path_id" in r and str(r["path_id"]) == str(path_id):
                return False
                
    return True

def _verify_persona(path_id: str, ledger: dict) -> None:
    is_offline = os.environ.get("ANTIGRAVITY_RUNNING_TESTS") == "1" or os.environ.get("SPAO_OFFLINE") == "1"
    if is_offline and not _FORCE_STRATEGIC_VERIFICATION:
        return
        
    spao_persona = os.environ.get("SPAO_PERSONA_ID")
    what_0065_path = path_resolver.resolve_workspace_path("kb", "WHAT-0065-domain-path-ownership-index.md")
    what_0062_path = path_resolver.resolve_workspace_path("kb", "WHAT-0062-agent-persona-ownership-index.md")

    if not spao_persona:
        resolved_owner = None
        # 1. Check WHAT-0065 (Horizontal Domain Override)
        if os.path.exists(what_0065_path):
            try:
                rows = parse_md_table(what_0065_path)
                path_to_domain = {}
                domain_to_owner = {}
                for r in rows:
                    if "path_id" in r and "domain_id" in r:
                        path_to_domain[r["path_id"]] = r["domain_id"]
                    elif "domain_id" in r and "owner_persona" in r:
                        domain_to_owner[r["domain_id"]] = r["owner_persona"]
                
                domain_id = path_to_domain.get(str(path_id))
                if domain_id:
                    owner = domain_to_owner.get(domain_id)
                    if owner and owner not in ("unassigned", "shared"):
                        resolved_owner = owner
            except Exception:
                pass

        # 2. Fall back to WHAT-0062 (Vertical SG mapping)
        if not resolved_owner:
            sg_id = None
            for goal in ledger.get("strategic_goals", []):
                if str(path_id) in [str(p) for p in goal.get("prioritized_paths", [])]:
                    sg_id = goal.get("id")
                    break
            if sg_id and os.path.exists(what_0062_path):
                try:
                    rows = parse_md_table(what_0062_path)
                    sg_to_owner = {r.get("sg_id"): r.get("owner_persona") for r in rows if "sg_id" in r}
                    owner = sg_to_owner.get(sg_id)
                    if owner and owner not in ("unassigned", "shared"):
                        resolved_owner = owner
                except Exception:
                    pass

        # 3. Fallback inside child workspace
        if not resolved_owner and os.environ.get("SPAO_WORKSPACE_DIR"):
            resolved_owner = "frontier"
            try:
                yaml_path = path_resolver.resolve_workspace_path("dyad-wu-wei.yml")
                if os.path.exists(yaml_path):
                    with open(yaml_path, "r") as f:
                        data = yaml.safe_load(f)
                        resolved_owner = data.get("agent_id") or "frontier"
            except Exception:
                pass
                
        # 4. Root system daemon fallback
        if not resolved_owner and not os.environ.get("SPAO_WORKSPACE_DIR"):
            resolved_owner = "frontier"

        if resolved_owner:
            os.environ["SPAO_PERSONA_ID"] = resolved_owner
            spao_persona = resolved_owner
            print(f"ℹ️  Auto-resolved SPAO_PERSONA_ID to '{spao_persona}' for Path #{path_id}")

    if os.environ.get("SPAO_WORKSPACE_DIR"):
        if not os.path.exists(what_0062_path) or not os.path.exists(what_0065_path):
            print("⚠️  WARNING: Child workspace is missing ownership index files in kb/. Strategic gate sovereign bypass allowed.")
            return

    if not spao_persona:
        raise Exception("Persona Gate Blocked: SPAO_PERSONA_ID environment variable is absent. Cannot verify identity.")

    if _is_pure_ziran(path_id, ledger):
        return # Pure Ziran paths have no structured domain or SG owner; they bypass the gate.

    # 1. Check WHAT-0065 (Horizontal Domain Override)
    if os.path.exists(what_0065_path):
        rows = parse_md_table(what_0065_path)
        path_to_domain = {}
        domain_to_owner = {}
        for r in rows:
            if "path_id" in r and "domain_id" in r:
                path_to_domain[r["path_id"]] = r["domain_id"]
            elif "domain_id" in r and "owner_persona" in r:
                domain_to_owner[r["domain_id"]] = r["owner_persona"]
        
        domain_id = path_to_domain.get(str(path_id))
        if domain_id:
            owner = domain_to_owner.get(domain_id)
            if owner and owner != "unassigned":
                if owner == "shared" or owner == spao_persona:
                    return # Authorized by horizontal override!
                else:
                    raise Exception(f"Persona Gate Blocked: Executing persona '{spao_persona}' does not match horizontal domain owner '{owner}' for Path #{path_id}.")
    
    # 2. Fall back to WHAT-0062 (Vertical SG mapping)
    sg_id = None
    for goal in ledger.get("strategic_goals", []):
        if str(path_id) in [str(p) for p in goal.get("prioritized_paths", [])]:
            sg_id = goal.get("id")
            break
            
    if not sg_id:
        raise Exception(f"Persona Gate Blocked: Path #{path_id} is not associated with any Strategic Goal.")
        
    if os.path.exists(what_0062_path):
        rows = parse_md_table(what_0062_path)
        sg_to_owner = {r.get("sg_id"): r.get("owner_persona") for r in rows if "sg_id" in r}
        owner = sg_to_owner.get(sg_id)
        if not owner:
            sys.exit(f"[🚫 BLOCKED] Persona Gate Blocked: SG {sg_id} is not mapped in WHAT-0062.")
        if owner == "unassigned":
            sys.exit(f"[🚫 BLOCKED] Persona Gate Blocked: SG {sg_id} is 'unassigned'.")
        if owner != "shared" and owner != spao_persona:
            sys.exit(f"[🚫 BLOCKED] Persona Gate Blocked: Executing persona '{spao_persona}' does not match vertical SG owner '{owner}' for Path #{path_id}.")


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
        sys.exit(f"[🚫 BLOCKED] Harmonization Failure: Terminal Node #{node_id_str} has no parent Path. (Is it a Path issue? You cannot execute plan-start on a Path.)")
        
    ledger = load_ledger()
    active_prioritized_paths = set()
    for goal in ledger.get("strategic_goals", []):
        if goal.get("status") == "Active":
            for path_id in goal.get("prioritized_paths", []):
                active_prioritized_paths.add(str(path_id))
                
    if str(parent_path_id) not in active_prioritized_paths:
        if _is_pure_ziran(str(parent_path_id), ledger):
            _verify_persona(str(parent_path_id), ledger)
            return
        print(f"⚠️  WARNING: Parent Path #{parent_path_id} of Node #{node_id_str} is not prioritized in the active strategic ledger.", file=sys.stderr)

    _verify_persona(str(parent_path_id), ledger)

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
        if _is_pure_ziran(path_id_str, ledger):
            _verify_persona(path_id_str, ledger)
            return
        print(f"⚠️  WARNING: Path #{path_id_str} is not prioritized in the active strategic ledger.", file=sys.stderr)

    _verify_persona(path_id_str, ledger)
@record_execution(stage="align")
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
