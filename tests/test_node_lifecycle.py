import os
import tempfile
import yaml
import pytest
from unittest import mock
from kernel.node_lifecycle import load_node_status_config, load_node_classification_config, BaseNode, TerminalNode

def test_load_node_status_config_success():
    mock_yaml_content = {
        "node_attributes": {
            "status": {
                "in_progress": "status: in-progress"
            },
            "classification": {
                "backlog": "backlog"
            }
        }
    }
    with mock.patch("os.path.exists", return_value=True):
        with mock.patch("builtins.open", mock.mock_open(read_data=yaml.dump(mock_yaml_content))):
            status_config = load_node_status_config()
            assert status_config.get("in_progress") == "status: in-progress"

            class_config = load_node_classification_config()
            assert class_config.get("backlog") == "backlog"

def test_load_node_status_config_not_found():
    with mock.patch("os.path.exists", return_value=False):
        status_config = load_node_status_config()
        assert status_config == {}

        class_config = load_node_classification_config()
        assert class_config == {}

@mock.patch("kernel.node_lifecycle.github_client.remove_label")
@mock.patch("kernel.node_lifecycle.github_client.get_issue_labels")
@mock.patch("kernel.node_lifecycle.load_node_status_config")
@mock.patch("kernel.node_lifecycle.github_client.add_label")
def test_base_node_set_status(mock_add_label, mock_load_config, mock_get_labels, mock_remove_label):
    mock_load_config.return_value = {
        "todo": "status: todo",
        "in_progress": "status: in-progress"
    }
    mock_get_labels.return_value = ["status: todo", "backlog"]
    
    node = BaseNode("100")
    node.set_status("in_progress")
    
    mock_add_label.assert_called_once_with("100", "status: in-progress")
    mock_remove_label.assert_called_once_with("100", "status: todo")

@mock.patch("kernel.node_lifecycle.load_node_status_config")
def test_base_node_set_status_invalid(mock_load_config):
    mock_load_config.return_value = {"in_progress": "status: in-progress"}
    node = BaseNode("100")
    with pytest.raises((ValueError, SystemExit), match="Status key 'invalid' is not defined in node.yml"):
        node.set_status("invalid")

@mock.patch("kernel.node_lifecycle.load_node_classification_config")
@mock.patch("kernel.node_lifecycle.github_client.add_label")
def test_base_node_set_classification(mock_add_label, mock_load_config):
    mock_load_config.return_value = {"backlog": "backlog"}
    node = BaseNode("100")
    node.set_classification("backlog")
    mock_add_label.assert_called_once_with("100", "backlog")

@mock.patch("kernel.node_lifecycle.load_node_classification_config")
def test_base_node_set_classification_invalid(mock_load_config):
    mock_load_config.return_value = {"backlog": "backlog"}
    node = BaseNode("100")
    with pytest.raises((ValueError, SystemExit), match="Classification key 'invalid' is not defined in node.yml"):
        node.set_classification("invalid")

@mock.patch("kernel.node_lifecycle.github_client.get_issue_labels")
def test_base_node_metadata_properties(mock_get_labels):
    mock_get_labels.return_value = ["loop:spao", "area:metasystem", "kind:infra"]
    node = BaseNode("390")
    assert node.loop == "spao"
    assert node.area == "metasystem"
    assert node.kind == "infra"

@mock.patch("kernel.node_lifecycle.github_client.get_issue_labels")
def test_get_worktree_path(mock_get_labels):
    from drivers import path_resolver
    base_dir = path_resolver.get_core_dir()
    
    # SPAO loop
    mock_get_labels.return_value = ["loop:spao"]
    node = BaseNode("390")
    assert node.get_worktree_path("node/390-test") == os.path.join(base_dir, ".worktrees", "spao", "node/390-test")

    # SDLC loop
    mock_get_labels.return_value = ["loop:sdlc"]
    node = BaseNode("390")
    assert node.get_worktree_path("node/390-test") == os.path.join(base_dir, ".worktrees", "sdlc", "node/390-test")

    # Default loop
    mock_get_labels.return_value = []
    node = BaseNode("390")
    assert node.get_worktree_path("node/390-test") == os.path.join(base_dir, ".worktrees", "node/390-test")

@mock.patch("kernel.node_lifecycle.git_client.diff_names")
@mock.patch("kernel.node_lifecycle.github_client.get_issue_labels")
def test_validate_spao_purity_success(mock_get_labels, mock_diff_names):
    mock_get_labels.return_value = ["loop:spao"]
    mock_diff_names.return_value = ["kb/WHAT-0034.md", "artifacts/frontier_state.md", "GEMINI.md"]
    
    node = TerminalNode("390")
    # Should not raise any exception
    node._validate_spao_purity(worktree_path="/some/dir")
    mock_diff_names.assert_called_once_with("main", cwd="/some/dir")

@mock.patch("kernel.node_lifecycle.git_client.diff_names")
@mock.patch("kernel.node_lifecycle.github_client.get_issue_labels")
def test_validate_spao_purity_failure(mock_get_labels, mock_diff_names):
    mock_get_labels.return_value = ["loop:spao"]
    mock_diff_names.return_value = ["skills/path_resolver.py", "kb/WHAT-0034.md"]
    
    node = TerminalNode("390")
    with pytest.raises((Exception, SystemExit), match="SPAO PR Purity Violation"):
        node._validate_spao_purity(worktree_path="/some/dir")
    mock_diff_names.assert_called_once_with("main", cwd="/some/dir")

@mock.patch("kernel.node_lifecycle.github_client.get_issue_labels")
@mock.patch("subprocess.run")
@mock.patch("kernel.node_lifecycle.github_client.get_issue_details")
def test_plan_finish_spec_check_failure(mock_get_details, mock_run, mock_get_labels):
    mock_get_details.return_value = {"title": "Discovery 386: Plan - Test Issue", "body": "Goal"}
    mock_get_labels.return_value = []
    mock_run.return_value = mock.MagicMock(returncode=0, stdout="skills/path_resolver.py")
    
    node = TerminalNode("390")
    with pytest.raises((Exception, SystemExit), match="SPEC file violation"):
        node.plan_finish("dummy body")

@mock.patch("kernel.node_lifecycle.subprocess.run")
@mock.patch("kernel.node_lifecycle.git_client")
@mock.patch("kernel.node_lifecycle.github_client")
@mock.patch("kernel.node_lifecycle.agent_frontier")
@mock.patch("kernel.node_lifecycle.daemon_nba")
@mock.patch("kernel.node_lifecycle.TerminalNode.get_worktree_path")
@mock.patch("kernel.daemon_knowledge_accrual.enforce_reflection_hook")
def test_reflect_success(mock_enforce, mock_get_worktree_path, mock_nba, mock_frontier, mock_gh, mock_git, mock_subprocess):
    from drivers import path_resolver
    mock_get_worktree_path.return_value = os.path.join(path_resolver.get_core_dir(), ".worktrees/node/390-test")
    mock_frontier.read_active_path.return_value = None
    mock_nba.NBADaemon.return_value.evaluate.return_value = {"type": "continue"}
    mock_gh.get_issue_labels.return_value = []
    mock_git.get_git_common_dir.return_value = ".git"
    mock_git.check_merge_conflicts.return_value = False
    
    node = TerminalNode("390")
    
    with mock.patch("kernel.node_lifecycle.FlowTransaction") as mock_tx:
        node.reflect("frontier.md", "node-390", "learnings", ["invariants"], "commit-msg", "node/390-test", stage="all")
        
    from drivers import path_resolver
    expected_worktree = os.path.abspath(os.path.join(path_resolver.get_core_dir(), ".worktrees/node/390-test"))
    mock_git.add.assert_called_once_with(["."], cwd=expected_worktree)
    mock_git.commit.assert_called_once_with("commit-msg", cwd=expected_worktree)
    mock_git.push.assert_called_once_with("node/390-test", cwd=expected_worktree)

@mock.patch("kernel.node_lifecycle.subprocess.run")
@mock.patch("kernel.node_lifecycle.git_client")
@mock.patch("kernel.node_lifecycle.github_client")
@mock.patch("kernel.node_lifecycle.agent_frontier")
@mock.patch("kernel.node_lifecycle.daemon_nba")
@mock.patch("kernel.node_lifecycle.TerminalNode.get_worktree_path")
@mock.patch("kernel.daemon_knowledge_accrual.enforce_reflection_hook")
def test_reflect_empty_pr_blocked(mock_enforce, mock_get_worktree_path, mock_nba, mock_frontier, mock_gh, mock_git, mock_subprocess):
    from drivers import path_resolver
    mock_get_worktree_path.return_value = os.path.join(path_resolver.get_core_dir(), ".worktrees/node/390-test")
    mock_git.get_git_common_dir.return_value = ".git"
    
    # Simulate an empty PR with no workspace changes and no commits ahead of main
    mock_git.status_porcelain.return_value = ""
    mock_git.diff_names.return_value = []
    
    node = TerminalNode("390")
    
    with mock.patch("kernel.node_lifecycle.FlowTransaction") as mock_tx:
        with pytest.raises((Exception, SystemExit), match="Reflection Blocked: No file changes detected"):
            node.reflect("frontier.md", "node-390", "learnings", ["invariants"], "commit-msg", "node/390-test", stage="all")

@mock.patch("kernel.node_lifecycle.github_client.get_issue_labels")
@mock.patch("kernel.node_lifecycle.FlowTransaction")
@mock.patch("kernel.node_lifecycle.load_node_status_config")
@mock.patch("kernel.node_lifecycle.github_client.get_issue_details")
@mock.patch("kernel.node_lifecycle.TerminalNode._verify_state_purity")
@mock.patch("kernel.node_lifecycle.TerminalNode._validate_orthogonal_scope")
@mock.patch("kernel.node_lifecycle.TerminalNode.set_status")
@mock.patch("kernel.node_lifecycle.agent_frontier.append_active_node")
@mock.patch("kernel.daemon_knowledge_accrual.run_kb_check")
def test_plan_start_dependency_violation(mock_kb_check, mock_append, mock_set_status, mock_validate_scope, mock_verify_purity, mock_get_details, mock_load_config, mock_tx, mock_get_labels):
    mock_load_config.return_value = {"in_progress": "status: in-progress"}
    mock_get_labels.return_value = ["backlog"]
    
    def side_effect(issue_id):
        if str(issue_id) == "390":
            return {
                "title": "Discovery 390: Plan - title",
                "body": "## Goal\nSome goal\n\n## Depends On\nNode 380",
                "state": "OPEN"
            }
        elif str(issue_id) == "380":
            return {
                "title": "Discovery 380: Harmonize - title",
                "body": "Some body",
                "state": "OPEN"
            }
        return {}
        
    mock_get_details.side_effect = side_effect
    
    node = TerminalNode("390")
    
    with pytest.raises((Exception, SystemExit), match="Dependency Violation: Node #390 depends on Node #380, which is still open"):
        node.plan_start("dummy_frontier.md")


@mock.patch("kernel.node_lifecycle.github_client.get_issue_labels")
@mock.patch("kernel.node_lifecycle.FlowTransaction")
@mock.patch("kernel.node_lifecycle.load_node_status_config")
@mock.patch("kernel.node_lifecycle.github_client.get_issue_details")
@mock.patch("kernel.node_lifecycle.TerminalNode._verify_state_purity")
@mock.patch("kernel.node_lifecycle.TerminalNode._validate_orthogonal_scope")
@mock.patch("kernel.node_lifecycle.TerminalNode.set_status")
@mock.patch("kernel.node_lifecycle.agent_frontier.append_active_node")
@mock.patch("kernel.daemon_knowledge_accrual.run_kb_check")
def test_plan_start_dependency_satisfied(mock_kb_check, mock_append, mock_set_status, mock_validate_scope, mock_verify_purity, mock_get_details, mock_load_config, mock_tx, mock_get_labels):
    mock_load_config.return_value = {"in_progress": "status: in-progress"}
    mock_get_labels.return_value = ["backlog"]
    
    def side_effect(issue_id):
        if str(issue_id) == "390":
            return {
                "title": "Discovery 390: Plan - title",
                "body": "## Goal\nSome goal\n\n## Depends On\nNode 380",
                "state": "OPEN"
            }
        elif str(issue_id) == "380":
            return {
                "title": "Discovery 380: Harmonize - title",
                "body": "Some body",
                "state": "CLOSED"
            }
        return {}
        
    mock_get_details.side_effect = side_effect
    
    node = TerminalNode("390")
    
    node.plan_start("dummy_frontier.md")
    mock_set_status.assert_called_with("in_progress")


def test_log_stage_advancement():
    from kernel.node_lifecycle import log_stage_advancement
    import sys
    with mock.patch("sys.stdout") as mock_stdout, mock.patch("kernel.node_lifecycle.is_verbose", return_value=True):
        log_stage_advancement("sense", "Status Detail", "Extra details")
        assert mock_stdout.write.called
        mock_stdout.flush.assert_called()


@mock.patch("kernel.node_lifecycle.git_client")
@mock.patch("kernel.node_lifecycle.github_client")
@mock.patch("kernel.node_lifecycle.agent_frontier")
@mock.patch("kernel.daemon_knowledge_accrual.enforce_reflection_hook")
def test_branch_naming_regex_enforcement_and_exemption(mock_enforce, mock_frontier, mock_gh, mock_git):
    mock_gh.get_open_prs.return_value = []
    node = TerminalNode("1133")
    
    # 1. Normal mode (SPAO_WORKSPACE_DIR NOT set) - invalid branch name should raise ValueError in checkout
    if "SPAO_WORKSPACE_DIR" in os.environ:
        del os.environ["SPAO_WORKSPACE_DIR"]
        
    with pytest.raises((ValueError, SystemExit), match="Branch name MUST follow the standard: node/.*"):
        node.checkout("custom-branch-name", "dummy_frontier.md")
        
    # 2. Normal mode (SPAO_WORKSPACE_DIR NOT set) - invalid branch name should raise ValueError in reflect
    with pytest.raises((ValueError, SystemExit), match="Branch name MUST follow the standard: node/.*"):
        node.reflect("dummy_frontier.md", "node-1133", "learnings", [], "msg", "custom-branch-name")

    # 3. Workspace mode (SPAO_WORKSPACE_DIR set) - custom branch names should be allowed
    os.environ["SPAO_WORKSPACE_DIR"] = "/tmp/mock-workspace"
    try:
        # Mock dependencies inside checkout to verify it bypasses the regex check and proceeds to other checks
        with mock.patch("kernel.node_lifecycle.FlowTransaction"), \
             mock.patch("kernel.daemon_strategic.verify_node_transition_allowed"), \
             mock.patch.object(node, "_verify_state_purity"), \
             mock.patch.object(node, "set_status"):
            # This should NOT raise ValueError. It might raise other errors if mock is incomplete,
            # but ValueError("Branch name MUST follow...") should not be raised.
            try:
                node.checkout("custom-branch-name", "dummy_frontier.md")
            except (Exception, SystemExit) as e:
                # We expect git/gh calls or other state/PR checks to fail, but not the ValueError
                assert not isinstance(e, ValueError) or "Branch name MUST follow" not in str(e)
                
        # Similarly for reflect in workspace mode
        with mock.patch("kernel.node_lifecycle.FlowTransaction"), \
             mock.patch.object(node, "_verify_state_purity"), \
             mock.patch.object(node, "get_worktree_path", return_value="/tmp/wt"):
            try:
                node.reflect("dummy_frontier.md", "node-1133", "learnings", [], "msg", "custom-branch-name")
            except (Exception, SystemExit) as e:
                assert not isinstance(e, ValueError) or "Branch name MUST follow" not in str(e)
    finally:
        del os.environ["SPAO_WORKSPACE_DIR"]


@mock.patch("kernel.node_lifecycle.subprocess.run")
@mock.patch("kernel.node_lifecycle.daemon_nba")
@mock.patch("kernel.node_lifecycle.agent_frontier")
@mock.patch("kernel.node_lifecycle.FlowTransaction")
@mock.patch("kernel.node_lifecycle.github_client")
@mock.patch("kernel.node_lifecycle.git_client")
@mock.patch("kernel.daemon_knowledge_accrual.enforce_reflection_hook")
def test_reflect_admin_bypass_conditions(mock_enforce, mock_git, mock_gh, mock_tx, mock_frontier, mock_nba, mock_subprocess):
    mock_frontier.read_active_path.return_value = None
    mock_nba.NBADaemon.return_value.evaluate.return_value = {"type": "continue"}
    mock_git.get_git_common_dir.return_value = ".git"
    mock_git.check_merge_conflicts.return_value = False
    
    node = TerminalNode("390")
    
    # Case 1: Zero modifications (not modified_files) -> should bypass
    mock_git.diff_names.return_value = []
    node.reflect("frontier.md", "node-390", "learnings", [], "msg", "node/390-test")
    mock_gh.admin_merge_pull_request.assert_called_once()
    mock_gh.admin_merge_pull_request.reset_mock()
    
    # Case 2: Only non-template artifacts/ modifications -> should bypass
    mock_git.diff_names.return_value = ["artifacts/frontier_state.md", "artifacts/some_log.txt"]
    node.reflect("frontier.md", "node-390", "learnings", [], "msg", "node/390-test")
    mock_gh.admin_merge_pull_request.assert_called_once()
    mock_gh.admin_merge_pull_request.reset_mock()
    
    # Case 3: kb/ modifications -> should NOT bypass
    mock_git.diff_names.return_value = ["artifacts/frontier_state.md", "kb/WHY-0001.md"]
    node.reflect("frontier.md", "node-390", "learnings", [], "msg", "node/390-test")
    mock_gh.admin_merge_pull_request.assert_not_called()

    # Case 4: artifacts/ template modifications -> should NOT bypass
    mock_git.diff_names.return_value = ["artifacts/frontier_state.md", "artifacts/job-discipline-template.md"]
    node.reflect("frontier.md", "node-390", "learnings", [], "msg", "node/390-test")
    mock_gh.admin_merge_pull_request.assert_not_called()
    
    # Case 5: Code changes -> should NOT bypass
    mock_git.diff_names.return_value = ["kernel/node_lifecycle.py", "artifacts/frontier_state.md"]
    node.reflect("frontier.md", "node-390", "learnings", [], "msg", "node/390-test")
    mock_gh.admin_merge_pull_request.assert_not_called()

def test_plan_start_quarantine_protocol_violation():
    # Setup mocks to return an issue labeled with "status:triage" (lacking "backlog")
    with mock.patch("kernel.node_lifecycle.github_client.get_issue_labels", return_value=["status:triage"]), \
         mock.patch("kernel.node_lifecycle.FlowTransaction"), \
         mock.patch("kernel.node_lifecycle.github_client.get_open_prs", return_value=[]), \
         mock.patch("kernel.node_lifecycle.TerminalNode._verify_state_purity"), \
         mock.patch("kernel.daemon_knowledge_accrual.run_kb_check"):
        
        node = TerminalNode("9999")
        with pytest.raises((Exception, SystemExit), match="Quarantine Protocol Violation: Node #9999 does not possess the 'backlog' label"):
            node.plan_start("dummy_frontier.md")


@mock.patch("kernel.node_lifecycle.git_client")
@mock.patch("kernel.node_lifecycle.github_client")
def test_clean_if_merged_on_github(mock_gh, mock_git):
    from kernel.node_lifecycle import TerminalNode
    
    # 1. If not merged on GitHub, should skip clean
    mock_gh.get_pr_state_by_branch.return_value = "OPEN"
    TerminalNode.clean_if_merged("node/1234-test")
    mock_git.worktree_remove.assert_not_called()
    mock_git.branch_delete.assert_not_called()
    
    # 2. If merged on GitHub, should perform clean
    mock_gh.get_pr_state_by_branch.return_value = "MERGED"
    mock_git.worktree_remove.reset_mock()
    mock_git.branch_delete.reset_mock()
    
    # Let's mock os.path.exists to return False to avoid actually trying to remove non-existent worktrees
    with mock.patch("os.path.exists", return_value=False):
        TerminalNode.clean_if_merged("node/1234-test")
        
    mock_git.branch_delete.assert_called_once_with("node/1234-test")

def test_plan_start_quarantine_bypass():
    """Test that self-created nodes (Activity/Discovery) are exempt from quarantine."""
    with mock.patch("kernel.node_lifecycle.github_client.get_issue_labels", return_value=["status:triage"]), \
         mock.patch("kernel.node_lifecycle.github_client.get_issue_details", return_value={"title": "Node 999: Activity 999: Implement quarantine survivor"}), \
         mock.patch("kernel.node_lifecycle.github_client.add_label") as mock_add_label, \
         mock.patch("kernel.node_lifecycle.FlowTransaction"), \
         mock.patch("kernel.node_lifecycle.github_client.get_open_prs", return_value=[]), \
         mock.patch("kernel.node_lifecycle.TerminalNode._verify_state_purity"), \
         mock.patch("kernel.daemon_strategic.verify_node_transition_allowed") as mock_verify:
        
        from kernel.node_lifecycle import TerminalNode
        node = TerminalNode("999")
        node.plan_start(frontier_file="artifacts/frontier_state.md")
        
        # Verify backlog label was added autonomously
        mock_add_label.assert_any_call("999", "backlog")
        mock_verify.assert_called_once_with("999")
