import os
import re
import json
import subprocess
import yaml
from skills import github_client
from skills import frontier_editor
from orchestrator import mgr_prompt

def is_verbose() -> bool:
    """Checks if verbose mode is triggered by the operator."""
    return os.environ.get("SPAO_VERBOSE") in ("1", "true", "TRUE") or os.environ.get("SPOA_VERBOSE") in ("1", "true", "TRUE")

def load_node_status_config() -> dict:
    """Loads the node status mapping from node.yml."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "node.yml")
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config.get("node_attributes", {}).get("status", {})

def load_node_classification_config() -> dict:
    """Loads the node classification mapping from node.yml."""
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "node.yml")
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config.get("node_attributes", {}).get("classification", {})

def log_stage_advancement(stage: str, status: str, details: str = "") -> None:
    """Prints a beautiful H1 banner representing SPAO loop stage advancement when verbose is active."""
    if not is_verbose():
        return
    stage_colors = {
        "sense": "🔍 SENSE",
        "plan": "📋 PLAN",
        "act": "⚡ ACT",
        "observe": "👀 OBSERVE",
        "reflect": "💾 REFLECT"
    }
    stage_label = stage_colors.get(stage.lower(), stage.upper())
    
    print("\n" + "═"*60)
    print(f" 🔄 SPAO Loop Stage  ►  {stage_label}")
    print(f" 📌 Status           ►  {status}")
    if details:
        print(f" 📝 Details          ►  {details}")
    print("═"*60 + "\n")

class BaseNode:
    """Abstract base class for all Antigravity Nodes."""
    def __init__(self, issue_id: str):
        self.issue_id = str(issue_id)
        
    @property
    def gh_labels(self):
        return github_client.get_issue_labels(self.issue_id)
        
    def add_gh_label(self, label: str):
        github_client.add_label(self.issue_id, label)
        
    def update_body(self, body: str):
        github_client.update_issue_body(self.issue_id, body)
        
    def close(self, comment: str):
        github_client.close_issue(self.issue_id, comment)

    def set_status(self, status_key: str) -> None:
        """Translates a logical status key into a physical label using node.yml."""
        status_config = load_node_status_config()
        if status_key not in status_config:
            raise ValueError(f"Status key '{status_key}' is not defined in node.yml")
        self.add_gh_label(status_config[status_key])

    def set_classification(self, classification_key: str) -> None:
        """Translates a logical classification key into a physical label using node.yml."""
        class_config = load_node_classification_config()
        if classification_key not in class_config:
            raise ValueError(f"Classification key '{classification_key}' is not defined in node.yml")
        self.add_gh_label(class_config[classification_key])

class NonTerminalNode(BaseNode):
    """Represents a composite or path node."""
    pass

class TerminalNode(BaseNode):
    """Represents an actionable, execution-level leaf node."""
    
    def __init__(self, issue_id: str):
        super().__init__(issue_id)
        
    def plan_start(self) -> None:
        in_progress_label = load_node_status_config().get("in_progress", "status: in-progress")
        if in_progress_label in self.gh_labels:
            raise Exception(f"Node #{self.issue_id} is already in progress by another thread!")
            
        self.set_status("in_progress")
        log_stage_advancement("plan", "Plan-Start Executed", f"Acquired lock on Node #{self.issue_id} for multi-phase planning.")

    def plan_finish(self, body: str) -> str:
        log_stage_advancement("plan", "Formulating Implementation Contract", f"Locking Node Contract into Issue #{self.issue_id}")
        
        res = subprocess.run(["gh", "issue", "view", self.issue_id, "--json", "title"], capture_output=True, text=True, check=True)
        current_title = json.loads(res.stdout)["title"]
        
        prefix = f"Node {self.issue_id}:"
        if not current_title.startswith(prefix):
            new_title = f"{prefix} {current_title}"
            github_client.rename_issue_title(self.issue_id, new_title)
            
        self.update_body(body)
        
        issue_url = f"https://github.com/pltrinh1122/agent-antigravity/issues/{self.issue_id}"
        log_stage_advancement("plan", "Plan Phase Completed", f"Node issue #{self.issue_id} successfully planned. Transitioning to Act phase.")
        return issue_url

    def checkout(self, branch_name: str) -> None:
        if not re.match(r"^node/\d+-[a-z0-9-]+$", branch_name):
            raise ValueError("Branch name MUST follow the standard: node/<id>-<kebab-case>")
            
        self.set_status("in_progress")
                
        log_stage_advancement("act", "Initializing Execution Worktree", f"Creating git worktree at .worktrees/{branch_name}")
        
        worktree_path = os.path.join(".worktrees", branch_name)
        os.makedirs(os.path.dirname(worktree_path), exist_ok=True)
        
        subprocess.run(["git", "worktree", "add", "-b", branch_name, worktree_path, "main"], check=True)
        
        print(f"\nWorktree established. Please `cd {worktree_path}` to begin work.")

    def reflect(self, frontier_file: str, node_name: str, learnings: str, invariants: list[str], commit_msg: str, branch_name: str) -> None:
        if not re.match(r"^node/\d+-[a-z0-9-]+$", branch_name):
            raise ValueError("Branch name MUST follow the standard: node/<id>-<kebab-case>")

        log_stage_advancement("reflect", "Initiating Reflect Phase", f"Closing Issue #{self.issue_id}, updating ledger, and preparing branch: '{branch_name}'")

        self.close("Node completed via Flow-State Manager. Moving to PR.")
        
        # Enforce Path Invariant: Evaluate the active path and close it if 0 activities remain
        from skills import nba_evaluator
        repository = "pltrinh1122/agent-antigravity"  # Hardcoded for now, could be dynamic
        nba_result = nba_evaluator.evaluate(repository=repository, frontier_file=frontier_file)
        
        if nba_result["mode"] == "path_switching" and nba_result["active_path"] is not None:
            active_path_str = nba_result["active_path"]
            path_number_match = re.search(r"Path (\d+):", active_path_str, re.IGNORECASE)
            if path_number_match:
                path_issue_id = path_number_match.group(1)
                github_client.close_issue(path_issue_id, "Path Invariant Enforced: Automatically closed because the final child Activity has been completed.")
                log_stage_advancement("reflect", "Path Invariant Enforced", f"Automatically closed parent {active_path_str}")
                frontier_editor.set_active_path(frontier_file, "None")
        
        frontier_editor.complete_active_node(frontier_file, node_name, learnings, invariants)
        
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)
        
        pr_body = f"Resolves #{self.issue_id}\n\n{learnings}"
        
        pr_url = github_client.create_pull_request(node_name, pr_body)
        
        log_stage_advancement("reflect", "Reflect Phase Completed", f"PR successfully created. Entering Observe phase under HARD HITL block.")

    @classmethod
    def clean_if_merged(cls, branch_name: str):
        """Cleans up the local worktree and branch if it has been merged."""
        wt_path = os.path.join(".worktrees", branch_name)
        if os.path.exists(wt_path):
            subprocess.run(["git", "worktree", "remove", "-f", wt_path])
        subprocess.run(["git", "branch", "-D", branch_name])
