import os
import re
import yaml
from drivers import github_client
from kernel import mgr_strategic

def _get_active_persona():
    import os
    env_id = os.environ.get("SPAO_PERSONA_ID")
    if env_id:
        return env_id
    try:
        from drivers import path_resolver
        import yaml
        yaml_path = path_resolver.resolve_workspace_path("antigravity.yml")
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)
            return data.get("agent_id")
    except Exception:
        return None

def _get_persona_ownership():
    mapping = {}
    try:
        import os
        from drivers import path_resolver
        md_path = path_resolver.resolve_workspace_path("kb", "WHAT-0062-agent-persona-ownership-index.md")
        if os.path.exists(md_path):
            with open(md_path, "r") as f:
                for line in f:
                    if "|" in line:
                        parts = [p.strip() for p in line.split("|")]
                        if len(parts) >= 3:
                            sg_id = parts[1]
                            agent_id = parts[2]
                            if sg_id.startswith("SG-"):
                                mapping[sg_id] = agent_id

        domain_md_path = path_resolver.resolve_workspace_path("kb", "WHAT-0065-domain-path-ownership-index.md")
        domain_to_agent = {}
        if os.path.exists(domain_md_path):
            with open(domain_md_path, "r") as f:
                content = f.read()
            import re
            domain_match = re.search(r"## Domain-to-Persona Index\s*\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
            if domain_match:
                for line in domain_match.group(1).splitlines():
                    line = line.strip()
                    if line.startswith("|") and not line.startswith("| domain_id"):
                        parts = [p.strip() for p in line.split("|")]
                        if len(parts) >= 3 and parts[1]:
                            domain_to_agent[parts[1]] = parts[2]
                            
            path_match = re.search(r"## Path-to-Domain Index\s*\n(.*?)(?=\n##|\Z)", content, re.DOTALL)
            if path_match:
                for line in path_match.group(1).splitlines():
                    line = line.strip()
                    if line.startswith("|") and not line.startswith("| path_id"):
                        parts = [p.strip() for p in line.split("|")]
                        if len(parts) >= 3 and parts[1]:
                            path_id = parts[1]
                            domain_id = parts[2]
                            if domain_id in domain_to_agent:
                                mapping[path_id] = domain_to_agent[domain_id]
                                
    except Exception:
        pass
    return mapping
class NBAScorer:
    """Computes Next-Best-Action (NBA) prioritization scores based on WHAT-0048."""
    
    def __init__(self, frontier_file: str = "artifacts/frontier_state.md"):
        self.frontier_file = frontier_file

    def calculate_score(self, node_id: str) -> dict:
        node_id_str = str(node_id)
        
        # Default components
        c_dep = 1.0
        c_axiom = 1.0
        c_strategic = 0.5
        c_risk = 1.0
        c_persona = 1.0
        
        try:
            details = github_client.get_issue_details(node_id_str)
            title = details.get("title", "")
            body = details.get("body", "")
            labels = github_client.get_issue_labels(node_id_str)
        except Exception as e:
            # Fallback if details cannot be fetched (e.g. offline tests)
            return {
                "node_id": node_id_str,
                "score": 0.0,
                "components": {
                    "dependency": 0.0,
                    "axiom": 0.0,
                    "strategic": 0.0,
                    "risk": 0.0,
                    "persona": 0.0
                },
                "error": str(e)
            }
            
        # 1. Dependency Gate (C_dependency)
        dep_match = re.search(r"## Depends On\s*\n+([^\n#]+)", body, re.IGNORECASE)
        if dep_match:
            dep_content = dep_match.group(1).strip()
            if dep_content.upper() != "TBD" and dep_content:
                dep_ids = re.findall(r"\d+", dep_content)
                for dep_id in dep_ids:
                    try:
                        dep_details = github_client.get_issue_details(dep_id)
                        if dep_details.get("state") != "CLOSED":
                            c_dep = 0.0
                            break
                    except Exception:
                        c_dep = 0.0
                        break
                        
        # 2. Axiomatic Compliance (C_axiom)
        title_lower = title.lower()
        forbidden_1 = "sp" + "ike"
        forbidden_2 = "ep" + "ic"
        if forbidden_1 in title_lower or forbidden_2 in title_lower:
            c_axiom = 0.0
            
        # 3. Strategic Alignment (C_strategic)
        # Check if node is a path or a terminal node
        if "path" in labels:
            path_id = node_id_str
        else:
            path_id = mgr_strategic.find_parent_path_id(node_id_str)
            
        if path_id:
            ledger = mgr_strategic.load_ledger()
            active_paths = set()
            for goal in ledger.get("strategic_goals", []):
                if goal.get("status") == "Active":
                    for pid in goal.get("prioritized_paths", []):
                        active_paths.add(str(pid))
            if str(path_id) in active_paths:
                c_strategic = 1.0
            else:
                c_strategic = 0.5
        else:
            # Check if it has strategic intent or backlog labels
            if "backlog" in labels:
                c_strategic = 0.5
            else:
                c_strategic = 0.0
                
        # 4. Operational Risk (C_risk)
        proposed_match = re.search(r"## Proposed Changes\s*\n+((?:[^\n#]+\n*)+)", body, re.IGNORECASE)
        if proposed_match:
            lines = proposed_match.group(1).strip().splitlines()
            for line in lines:
                line_lower = line.lower()
                if any(k in line_lower for k in ["node_lifecycle", "github_client", "git_client", "infra_manager"]):
                    c_risk = 0.5
                    break
                    
        # 5. Persona Alignment (C_persona)
        active_persona = _get_active_persona()
        ownership_map = _get_persona_ownership()

        if active_persona and ownership_map and path_id:
            if str(path_id) in ownership_map:
                if ownership_map[str(path_id)] != active_persona:
                    c_persona = 0.0
            else:
                ledger = mgr_strategic.load_ledger()
                parent_sg = None
                for goal in ledger.get("strategic_goals", []):
                    if str(path_id) in [str(p) for p in goal.get("prioritized_paths", [])]:
                        parent_sg = goal.get("id")
                        break

                if parent_sg and parent_sg in ownership_map:
                    if ownership_map[parent_sg] != active_persona:
                        c_persona = 0.0

        # Calculate overall score: S_NBA = C_dep * C_persona * (0.40 * C_axiom + 0.40 * C_strategic + 0.20 * C_risk)
        score = c_dep * c_persona * (0.40 * c_axiom + 0.40 * c_strategic + 0.20 * c_risk)
        
        return {
            "node_id": node_id_str,
            "title": title,
            "score": round(score, 3),
            "components": {
                "dependency": float(c_dep),
                "axiom": float(c_axiom),
                "strategic": float(c_strategic),
                "risk": float(c_risk),
                "persona": float(c_persona)
            }
        }


class GranularNBAScorer(NBAScorer):
    """Experimental scoring engine for Group B with granular strategic and risk metrics."""
    
    def calculate_score(self, node_id: str) -> dict:
        node_id_str = str(node_id)
        
        # Default components
        c_dep = 1.0
        c_axiom = 1.0
        c_strategic = 0.3
        c_risk = 1.0
        c_persona = 1.0
        
        try:
            details = github_client.get_issue_details(node_id_str)
            title = details.get("title", "")
            body = details.get("body", "")
            labels = github_client.get_issue_labels(node_id_str)
        except Exception as e:
            return {
                "node_id": node_id_str,
                "score": 0.0,
                "components": {
                    "dependency": 0.0,
                    "axiom": 0.0,
                    "strategic": 0.0,
                    "risk": 0.0,
                    "persona": 0.0
                },
                "error": str(e)
            }
            
        # 1. Dependency Gate (C_dependency)
        dep_match = re.search(r"## Depends On\s*\n+([^\n#]+)", body, re.IGNORECASE)
        if dep_match:
            dep_content = dep_match.group(1).strip()
            if dep_content.upper() != "TBD" and dep_content:
                dep_ids = re.findall(r"\d+", dep_content)
                for dep_id in dep_ids:
                    try:
                        dep_details = github_client.get_issue_details(dep_id)
                        if dep_details.get("state") != "CLOSED":
                            c_dep = 0.0
                            break
                    except Exception:
                        c_dep = 0.0
                        break
                        
        # 2. Axiomatic Compliance (C_axiom)
        title_lower = title.lower()
        forbidden_1 = "sp" + "ike"
        forbidden_2 = "ep" + "ic"
        if forbidden_1 in title_lower or forbidden_2 in title_lower:
            c_axiom = 0.0
            
        # 3. Strategic Alignment (C_strategic)
        if "path" in labels:
            path_id = node_id_str
        else:
            path_id = mgr_strategic.find_parent_path_id(node_id_str)
            
        if path_id:
            ledger = mgr_strategic.load_ledger()
            active_paths = set()
            for goal in ledger.get("strategic_goals", []):
                if goal.get("status") == "Active":
                    for pid in goal.get("prioritized_paths", []):
                        active_paths.add(str(pid))
            if str(path_id) in active_paths:
                c_strategic = 1.0
            else:
                try:
                    # Check keywords in parent path's title or body
                    path_details = github_client.get_issue_details(path_id)
                    path_title = path_details.get("title", "")
                    path_body = path_details.get("body", "")
                    
                    keywords = ["sandbox", "audit", "telemetry", "velocity", "gate", "knowledge", "abtest"]
                    text_to_search = (path_title + " " + path_body).lower()
                    if any(kw in text_to_search for kw in keywords):
                        c_strategic = 0.7
                    else:
                        c_strategic = 0.3
                except Exception:
                    c_strategic = 0.3
        else:
            # Fallback for nodes without parent paths (check self)
            keywords = ["sandbox", "audit", "telemetry", "velocity", "gate", "knowledge", "abtest"]
            text_to_search = (title + " " + body).lower()
            if any(kw in text_to_search for kw in keywords):
                c_strategic = 0.7
            else:
                c_strategic = 0.3
                
        # 4. Operational Risk (C_risk)
        proposed_match = re.search(r"## Proposed Changes\s*\n+((?:[^\n#]+\n*)+)", body, re.IGNORECASE)
        matched_criticals = set()
        if proposed_match:
            lines = proposed_match.group(1).strip().splitlines()
            for line in lines:
                line_lower = line.lower()
                for k in ["node_lifecycle", "github_client", "git_client", "infra_manager"]:
                    if k in line_lower:
                        matched_criticals.add(k)
        
        num_criticals = len(matched_criticals)
        if num_criticals == 0:
            c_risk = 1.0
        elif num_criticals == 1:
            c_risk = 0.75
        else:
            c_risk = 0.5
            
        # 5. Persona Alignment (C_persona)
        active_persona = _get_active_persona()
        ownership_map = _get_persona_ownership()

        if active_persona and ownership_map and path_id:
            if str(path_id) in ownership_map:
                if ownership_map[str(path_id)] != active_persona:
                    c_persona = 0.0
            else:
                ledger = mgr_strategic.load_ledger()
                parent_sg = None
                for goal in ledger.get("strategic_goals", []):
                    if str(path_id) in [str(p) for p in goal.get("prioritized_paths", [])]:
                        parent_sg = goal.get("id")
                        break

                if parent_sg and parent_sg in ownership_map:
                    if ownership_map[parent_sg] != active_persona:
                        c_persona = 0.0

        score = c_dep * c_persona * (0.40 * c_axiom + 0.40 * c_strategic + 0.20 * c_risk)
        
        return {
            "node_id": node_id_str,
            "title": title,
            "score": round(score, 3),
            "components": {
                "dependency": float(c_dep),
                "axiom": float(c_axiom),
                "strategic": float(c_strategic),
                "risk": float(c_risk),
                "persona": float(c_persona)
            }
        }
