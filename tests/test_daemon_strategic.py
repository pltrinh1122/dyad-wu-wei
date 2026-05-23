import os
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import yaml
from kernel import daemon_strategic
from kernel.daemon_nba import NBAManager

class TestMgrStrategic(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.ledger_path = os.path.join(self.temp_dir.name, "strategic_intent.yml")
        os.environ["SPAO_STRATEGIC_LEDGER_PATH"] = self.ledger_path

    def tearDown(self):
        self.temp_dir.cleanup()
        if "SPAO_STRATEGIC_LEDGER_PATH" in os.environ:
            del os.environ["SPAO_STRATEGIC_LEDGER_PATH"]

    def test_validate_goal_valid(self):
        goal = {
            "title": "Robust Tests",
            "collaborative_gap": "CI fails randomly due to unmocked network calls.",
            "constraints": "CI runners are unauthenticated and do not have GitHub tokens.",
            "falsification_signal": "Mock drift causes real bugs to bypass local test suite."
        }
        errors = daemon_strategic.validate_goal(goal)
        self.assertEqual(len(errors), 0)

    def test_validate_goal_invalid_grounding(self):
        goal = {
            "title": "Robust Tests",
            "collaborative_gap": "",
            "constraints": "CI runners are unauthenticated.",
            "falsification_signal": "Mock drift occurs."
        }
        errors = daemon_strategic.validate_goal(goal)
        self.assertTrue(any("Grounding error" in e for e in errors))

    def test_validate_goal_invalid_constraint_verb(self):
        goal = {
            "title": "Robust Tests",
            "collaborative_gap": "CI fails randomly.",
            "constraints": "We must fix the unauthenticated runners.",
            "falsification_signal": "Mock drift occurs."
        }
        errors = daemon_strategic.validate_goal(goal)
        self.assertTrue(any("contains action verb 'fix'" in e for e in errors))

    def test_validate_goal_invalid_falsifiability(self):
        goal = {
            "title": "Robust Tests",
            "collaborative_gap": "CI fails randomly.",
            "constraints": "CI runners are unauthenticated.",
            "falsification_signal": ""
        }
        errors = daemon_strategic.validate_goal(goal)
        self.assertTrue(any("Falsifiability error" in e for e in errors))

    def test_validate_goal_invalid_materializability(self):
        goal = {
            "title": "AGI Integration",
            "collaborative_gap": "The operator wants an AGI model to automate all repository work.",
            "constraints": "Requires infinite context window and zero latency connection.",
            "falsification_signal": "The agent makes a mistake."
        }
        errors = daemon_strategic.validate_goal(goal)
        self.assertTrue(any("Materializability error" in e for e in errors))
        self.assertTrue(any("speculative capabilities" in e for e in errors))


    def test_save_and_load_ledger(self):
        data = {
            "strategic_goals": [
                {
                    "id": "SG-0001",
                    "title": "Goal 1",
                    "collaborative_gap": "Problem 1",
                    "constraints": "Constraints 1",
                    "falsification_signal": "Signal 1",
                    "status": "Active",
                    "prioritized_paths": [368]
                }
            ]
        }
        daemon_strategic.save_ledger(data)
        
        # Check files exist
        self.assertTrue(os.path.exists(self.ledger_path))
        self.assertTrue(os.path.exists(self.ledger_path + ".sha256"))
        self.assertTrue(os.path.exists(self.ledger_path.replace(".yml", ".md")))
        
        loaded = daemon_strategic.load_ledger()
        self.assertEqual(len(loaded["strategic_goals"]), 1)
        self.assertEqual(loaded["strategic_goals"][0]["id"], "SG-0001")

    @patch("drivers.github_client.list_issues_by_label")
    @patch("drivers.github_client.get_issue_labels")
    def test_verify_command(self, mock_labels, mock_list):
        # 1. Valid goal, no unmapped open paths
        data = {
            "strategic_goals": [
                {
                    "id": "SG-0001",
                    "title": "Goal 1",
                    "collaborative_gap": "Problem 1",
                    "constraints": "Constraints 1",
                    "falsification_signal": "Signal 1",
                    "status": "Active",
                    "prioritized_paths": [368]
                }
            ]
        }
        daemon_strategic.save_ledger(data)
        
        mock_list.return_value = [{"number": 368, "title": "Path 368"}]
        mock_labels.return_value = ["backlog", "path"]
        
        # Should run without sys.exit
        daemon_strategic.cmd_verify()

    @patch("drivers.github_client.list_issues_by_label")
    @patch("drivers.github_client.get_issue_labels")
    def test_nba_reordering(self, mock_labels, mock_list):
        # Setup strategic ledger with prioritized paths
        data = {
            "strategic_goals": [
                {
                    "id": "SG-0001",
                    "title": "Goal 1",
                    "collaborative_gap": "Problem 1",
                    "constraints": "Constraints 1",
                    "falsification_signal": "Signal 1",
                    "status": "Active",
                    "prioritized_paths": [368]
                }
            ]
        }
        daemon_strategic.save_ledger(data)
        
        mock_list.return_value = [
            {"number": 362, "title": "Path 362"},
            {"number": 368, "title": "Path 368"},
            {"number": 355, "title": "Path 355"}
        ]
        
        nba = NBAManager()
        # Mock active path as None to test global switching logic reordering
        with patch("kernel.agent_frontier.read_active_path", return_value=None):
            result = nba.evaluate("dummy_frontier.md")
            
        recs = result["recommendations"]
        self.assertEqual(len(recs), 3)
        # 368 must be moved to the first place
        self.assertEqual(recs[0]["number"], 368)
        self.assertEqual(recs[1]["number"], 362)
        self.assertEqual(recs[2]["number"], 355)

    @patch("drivers.github_client.get_issue_details")
    @patch("os.environ.get")
    def test_verify_prioritized_paths_success(self, mock_env_get, mock_details):
        mock_env_get.side_effect = lambda key, default=None: "0" if key in ("ANTIGRAVITY_RUNNING_TESTS", "SPAO_OFFLINE") else os.environ.get(key, default)
        mock_details.return_value = {"number": 368, "state": "OPEN"}
        goals = [{"status": "Active", "prioritized_paths": [368]}]
        res = daemon_strategic.verify_prioritized_paths(goals)
        self.assertTrue(res)
        mock_details.assert_called_once_with("368")

    @patch("drivers.github_client.get_issue_details")
    @patch("os.environ.get")
    def test_verify_prioritized_paths_closed(self, mock_env_get, mock_details):
        mock_env_get.side_effect = lambda key, default=None: "0" if key in ("ANTIGRAVITY_RUNNING_TESTS", "SPAO_OFFLINE") else os.environ.get(key, default)
        mock_details.return_value = {"number": 368, "state": "CLOSED"}
        goals = [{"status": "Active", "prioritized_paths": [368]}]
        res = daemon_strategic.verify_prioritized_paths(goals)
        self.assertFalse(res)

    @patch("drivers.github_client.get_issue_details")
    @patch("os.environ.get")
    def test_verify_prioritized_paths_missing(self, mock_env_get, mock_details):
        mock_env_get.side_effect = lambda key, default=None: "0" if key in ("ANTIGRAVITY_RUNNING_TESTS", "SPAO_OFFLINE") else os.environ.get(key, default)
        mock_details.side_effect = Exception("Issue not found")
        goals = [{"status": "Active", "prioritized_paths": [368]}]
        res = daemon_strategic.verify_prioritized_paths(goals)
        self.assertFalse(res)

    def test_verify_node_transition_allowed_success(self):
        data = {
            "strategic_goals": [
                {
                    "id": "SG-0001",
                    "status": "Active",
                    "prioritized_paths": [416]
                }
            ]
        }
        daemon_strategic.save_ledger(data)
        
        daemon_strategic._FORCE_STRATEGIC_VERIFICATION = True
        os.environ["SPAO_PERSONA_ID"] = "agent-sg1"
        daemon_strategic._MOCK_PARENT_PATHS = {"419": "416"}
        os.environ["SPAO_PERSONA_ID"] = "agent-sg1"
        
        try:
            daemon_strategic.verify_node_transition_allowed("419")
        finally:
            daemon_strategic._FORCE_STRATEGIC_VERIFICATION = False
            daemon_strategic._MOCK_PARENT_PATHS = {}

    def test_verify_node_transition_allowed_pure_ziran(self):
        data = {
            "strategic_goals": [
                {
                    "id": "SG-0001",
                    "status": "Active",
                    "prioritized_paths": [412]
                }
            ]
        }
        daemon_strategic.save_ledger(data)
        
        daemon_strategic._FORCE_STRATEGIC_VERIFICATION = True
        os.environ["SPAO_PERSONA_ID"] = "agent-sg1"
        daemon_strategic._MOCK_PARENT_PATHS = {"419": "416"}
        os.environ["SPAO_PERSONA_ID"] = "agent-sg1"
        
        try:
            # Path 416 is not in the ledger, so it is Pure Ziran.
            # Pure Ziran should flow through without being blocked by Strategic Goal constraints.
            daemon_strategic.verify_node_transition_allowed("419")
        finally:
            daemon_strategic._FORCE_STRATEGIC_VERIFICATION = False
            daemon_strategic._MOCK_PARENT_PATHS = {}

    def test_verify_node_transition_allowed_missing_parent(self):
        data = {
            "strategic_goals": [
                {
                    "id": "SG-0001",
                    "status": "Active",
                    "prioritized_paths": [416]
                }
            ]
        }
        daemon_strategic.save_ledger(data)
        
        daemon_strategic._FORCE_STRATEGIC_VERIFICATION = True
        os.environ["SPAO_PERSONA_ID"] = "agent-sg1"
        daemon_strategic._MOCK_PARENT_PATHS = {}
        
        try:
            with self.assertRaises(ValueError) as ctx:
                daemon_strategic.verify_node_transition_allowed("419")
            self.assertIn("Alignment Failure", str(ctx.exception))
        finally:
            daemon_strategic._FORCE_STRATEGIC_VERIFICATION = False

    def test_verify_path_activation_allowed_success(self):
        data = {
            "strategic_goals": [
                {
                    "id": "SG-0001",
                    "status": "Active",
                    "prioritized_paths": [416]
                }
            ]
        }
        daemon_strategic.save_ledger(data)
        
        daemon_strategic._FORCE_STRATEGIC_VERIFICATION = True
        os.environ["SPAO_PERSONA_ID"] = "agent-sg1"
        try:
            daemon_strategic.verify_path_activation_allowed("416")
        finally:
            daemon_strategic._FORCE_STRATEGIC_VERIFICATION = False

    def test_verify_path_activation_allowed_pure_ziran(self):
        data = {
            "strategic_goals": [
                {
                    "id": "SG-0001",
                    "status": "Active",
                    "prioritized_paths": [412]
                }
            ]
        }
        daemon_strategic.save_ledger(data)
        
        daemon_strategic._FORCE_STRATEGIC_VERIFICATION = True
        os.environ["SPAO_PERSONA_ID"] = "agent-sg1"
        try:
            # Path 416 is not in the ledger, so it is Pure Ziran.
            # Pure Ziran should flow through without being blocked by Strategic Goal constraints.
            daemon_strategic.verify_path_activation_allowed("416")
        finally:
            daemon_strategic._FORCE_STRATEGIC_VERIFICATION = False

    def test_find_parent_path_id_success(self):
        import os
        from unittest.mock import MagicMock
        from drivers import github_client
        
        orig_list = github_client.list_issues_by_label
        orig_details = github_client.get_issue_details
        orig_environ = os.environ.get
        
        github_client.list_issues_by_label = MagicMock(return_value=[{"number": 416, "title": "Path: Some Path"}])
        github_client.get_issue_details = MagicMock(return_value={
            "number": 416,
            "title": "Path: Some Path",
            "body": "## Meta-Index\n- [ ] Node 419: Some activity"
        })
        os.environ.get = lambda key, default=None: "0" if key in ("ANTIGRAVITY_RUNNING_TESTS", "SPAO_OFFLINE") else orig_environ(key, default)
        
        try:
            parent_id = daemon_strategic.find_parent_path_id("419")
            self.assertEqual(parent_id, "416")
            github_client.list_issues_by_label.assert_called_once_with("path")
        finally:
            github_client.list_issues_by_label = orig_list
            github_client.get_issue_details = orig_details
            os.environ.get = orig_environ

if __name__ == "__main__":
    unittest.main()

