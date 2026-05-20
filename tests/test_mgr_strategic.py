import os
import unittest
from unittest.mock import patch, MagicMock
import tempfile
import yaml
from orchestrator import mgr_strategic
from orchestrator.mgr_nba import NBAManager

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
            "operator_problem": "CI fails randomly due to unmocked network calls.",
            "constraints": "CI runners are unauthenticated and do not have GitHub tokens.",
            "falsification_signal": "Mock drift causes real bugs to bypass local test suite."
        }
        errors = mgr_strategic.validate_goal(goal)
        self.assertEqual(len(errors), 0)

    def test_validate_goal_invalid_grounding(self):
        goal = {
            "title": "Robust Tests",
            "operator_problem": "",
            "constraints": "CI runners are unauthenticated.",
            "falsification_signal": "Mock drift occurs."
        }
        errors = mgr_strategic.validate_goal(goal)
        self.assertTrue(any("Grounding error" in e for e in errors))

    def test_validate_goal_invalid_constraint_verb(self):
        goal = {
            "title": "Robust Tests",
            "operator_problem": "CI fails randomly.",
            "constraints": "We must fix the unauthenticated runners.",
            "falsification_signal": "Mock drift occurs."
        }
        errors = mgr_strategic.validate_goal(goal)
        self.assertTrue(any("contains action verb 'fix'" in e for e in errors))

    def test_validate_goal_invalid_falsifiability(self):
        goal = {
            "title": "Robust Tests",
            "operator_problem": "CI fails randomly.",
            "constraints": "CI runners are unauthenticated.",
            "falsification_signal": ""
        }
        errors = mgr_strategic.validate_goal(goal)
        self.assertTrue(any("Falsifiability error" in e for e in errors))

    def test_save_and_load_ledger(self):
        data = {
            "strategic_goals": [
                {
                    "id": "SG-0001",
                    "title": "Goal 1",
                    "operator_problem": "Problem 1",
                    "constraints": "Constraints 1",
                    "falsification_signal": "Signal 1",
                    "status": "Active",
                    "prioritized_paths": [368]
                }
            ]
        }
        mgr_strategic.save_ledger(data)
        
        # Check files exist
        self.assertTrue(os.path.exists(self.ledger_path))
        self.assertTrue(os.path.exists(self.ledger_path + ".sha256"))
        self.assertTrue(os.path.exists(self.ledger_path.replace(".yml", ".md")))
        
        loaded = mgr_strategic.load_ledger()
        self.assertEqual(len(loaded["strategic_goals"]), 1)
        self.assertEqual(loaded["strategic_goals"][0]["id"], "SG-0001")

    @patch("skills.github_client.list_issues_by_label")
    @patch("skills.github_client.get_issue_labels")
    def test_verify_command(self, mock_labels, mock_list):
        # 1. Valid goal, no unmapped open paths
        data = {
            "strategic_goals": [
                {
                    "id": "SG-0001",
                    "title": "Goal 1",
                    "operator_problem": "Problem 1",
                    "constraints": "Constraints 1",
                    "falsification_signal": "Signal 1",
                    "status": "Active",
                    "prioritized_paths": [368]
                }
            ]
        }
        mgr_strategic.save_ledger(data)
        
        mock_list.return_value = [{"number": 368, "title": "Path 368"}]
        mock_labels.return_value = ["backlog", "path"]
        
        # Should run without sys.exit
        mgr_strategic.cmd_verify()

    @patch("skills.github_client.list_issues_by_label")
    @patch("skills.github_client.get_issue_labels")
    def test_nba_reordering(self, mock_labels, mock_list):
        # Setup strategic ledger with prioritized paths
        data = {
            "strategic_goals": [
                {
                    "id": "SG-0001",
                    "title": "Goal 1",
                    "operator_problem": "Problem 1",
                    "constraints": "Constraints 1",
                    "falsification_signal": "Signal 1",
                    "status": "Active",
                    "prioritized_paths": [368]
                }
            ]
        }
        mgr_strategic.save_ledger(data)
        
        mock_list.return_value = [
            {"number": 362, "title": "Path 362"},
            {"number": 368, "title": "Path 368"},
            {"number": 355, "title": "Path 355"}
        ]
        
        nba = NBAManager()
        # Mock active path as None to test global switching logic reordering
        with patch("orchestrator.mgr_frontier.read_active_path", return_value=None):
            result = nba.evaluate("dummy_frontier.md")
            
        recs = result["recommendations"]
        self.assertEqual(len(recs), 3)
        # 368 must be moved to the first place
        self.assertEqual(recs[0]["number"], 368)
        self.assertEqual(recs[1]["number"], 362)
        self.assertEqual(recs[2]["number"], 355)

if __name__ == "__main__":
    unittest.main()
