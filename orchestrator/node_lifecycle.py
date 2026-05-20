import os
import re
import json
import subprocess
import yaml
from skills import github_client
from skills import frontier_editor
from orchestrator import mgr_prompt, mgr_backlog, mgr_nba
from orchestrator.mgr_telemetry import TelemetryManager, record_execution

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
    def _validate_orthogonal_scope(self):
        """Validates that the current node does not have an identical footprint to another open node."""
        current_node = github_client.get_issue_details(self.issue_id)
        current_title = current_node.get("title", "")
        current_body = current_node.get("body", "")
        
        def extract_goal(body: str) -> str:
            match = re.search(r"## Goal\n(.*?)(?=\n## |\Z)", body, re.DOTALL | re.IGNORECASE)
            return match.group(1).strip().lower() if match else ""
            
        def extract_core_title(title: str) -> str:
            clean = re.sub(r"^(Node \d+: )?(Activity|Probe|Path)( \d+)?: ", "", title, flags=re.IGNORECASE)
            return clean.strip().lower()

        current_goal = extract_goal(current_body)
        current_core_title = extract_core_title(current_title)
        
        if not current_core_title and not current_goal:
            return
            
        open_issues = github_client.get_open_issues()
        
        for issue in open_issues:
            if str(issue["number"]) == str(self.issue_id):
                continue
                
            other_core_title = extract_core_title(issue.get("title", ""))
            other_goal = extract_goal(issue.get("body", ""))
            
            if current_core_title and current_core_title == other_core_title:
                raise Exception(f"Orthogonal Scope Violation: Node {self.issue_id} has an identical title footprint to Node {issue['number']}")
                
            if current_goal and current_goal == other_goal:
                raise Exception(f"Orthogonal Scope Violation: Node {self.issue_id} has an identical goal footprint to Node {issue['number']}")

    @record_execution(stage="plan")
    def plan_start(self) -> None:
        in_progress_label = load_node_status_config().get("in_progress", "status: in-progress")
        if in_progress_label in self.gh_labels:
            raise Exception(f"Node #{self.issue_id} is already in progress by another thread!")
            
        self._validate_orthogonal_scope()
            
        self.set_status("in_progress")
        
        log_stage_advancement("plan", "Plan-Start Executed", f"Acquired lock on Node #{self.issue_id} for multi-phase planning.")

    @record_execution(stage="plan")
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

    @record_execution(stage="act")
    def checkout(self, branch_name: str) -> None:
        if not re.match(r"^node/\d+-[a-z0-9-]+$", branch_name):
            raise ValueError("Branch name MUST follow the standard: node/<id>-<kebab-case>")
            
        self.set_status("in_progress")
                
        log_stage_advancement("act", "Initializing Execution Worktree", f"Creating git worktree at .worktrees/{branch_name}")
        
        worktree_path = os.path.join(".worktrees", branch_name)
        os.makedirs(os.path.dirname(worktree_path), exist_ok=True)
        
        subprocess.run(["git", "worktree", "add", "-b", branch_name, worktree_path, "main"], check=True)
        
        print(f"\nWorktree established. Please `cd {worktree_path}` to begin work.")

    @record_execution(stage="reflect")
    def reflect(self, frontier_file: str, node_name: str, learnings: str, invariants: list[str], commit_msg: str, branch_name: str) -> None:
        if not re.match(r"^node/\d+-[a-z0-9-]+$", branch_name):
            raise ValueError("Branch name MUST follow the standard: node/<id>-<kebab-case>")
 
        log_stage_advancement("reflect", "Initiating Reflect Phase", f"Closing Issue #{self.issue_id}, updating ledger, and preparing branch: '{branch_name}'")
 
        self.close("Node completed via Flow-State Manager. Moving to PR.")
        
        # Automate Meta-Index Checkbox Synchronization
        active_path_str = frontier_editor.read_active_path(frontier_file)
        if active_path_str:
            path_issue_id = frontier_editor.extract_path_id(active_path_str)
            if path_issue_id:
                backlog = mgr_backlog.BacklogManager()
                backlog.check_off_meta_index(path_issue_id, self.issue_id)
            else:
                print(f"Warning: Failed to extract Path ID from active path string: '{active_path_str}'")
        
        # Enforce Path Invariant: Evaluate the active path and close it if 0 activities remain
        nba = mgr_nba.NBAManager()
        nba_result = nba.evaluate(frontier_file=frontier_file)
        
        if nba_result["type"] == "path_switching" and active_path_str:
            # We had an active path, but NBA now says we should switch (because it's exhausted)
            path_issue_id = frontier_editor.extract_path_id(active_path_str)
            if path_issue_id:
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
