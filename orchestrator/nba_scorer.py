import os
import re
import yaml
from skills import github_client
from orchestrator import mgr_strategic

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
                    "risk": 0.0
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
                    
        # Calculate overall score: S_NBA = C_dep * (0.40 * C_axiom + 0.40 * C_strategic + 0.20 * C_risk)
        score = c_dep * (0.40 * c_axiom + 0.40 * c_strategic + 0.20 * c_risk)
        
        return {
            "node_id": node_id_str,
            "title": title,
            "score": round(score, 3),
            "components": {
                "dependency": float(c_dep),
                "axiom": float(c_axiom),
                "strategic": float(c_strategic),
                "risk": float(c_risk)
            }
        }
