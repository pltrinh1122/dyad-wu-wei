import unittest
from unittest.mock import patch, MagicMock
import os
from orchestrator.mgr_rt import execute_score_paths

class TestMgrRT(unittest.TestCase):

    @patch("orchestrator.nba_scorer.GranularNBAScorer.calculate_score")
    @patch("skills.github_client.list_issues_by_label")
    @patch("builtins.print")
    def test_execute_score_paths_default(self, mock_print, mock_list, mock_calc):
        mock_list.return_value = [{"number": "480", "title": "Test Path 480"}]
        mock_calc.return_value = {
            "score": 0.8,
            "components": {
                "dependency": 1.0,
                "axiom": 1.0,
                "strategic": 0.5,
                "risk": 1.0
            }
        }
        
        # Run execution
        execute_score_paths()
        
        # Verify calls
        mock_list.assert_called_once_with("path")
        mock_calc.assert_called_once_with("480")
        
        # Verify file output
        report_path = "/home/pt/.gemini/antigravity-cli/brain/26a5d234-9e33-4b59-8f27-719b4738d389/nba_historical_scores_report.md"
        self.assertTrue(os.path.exists(report_path))
        
        with open(report_path, "r") as f:
            content = f.read()
            self.assertIn("# NBA Historical Decision Scoring Report", content)
            self.assertIn("| #480 | Test Path 480 | 0.800 | 1.0 | 1.0 | 0.5 | 1.0 |", content)

if __name__ == "__main__":
    unittest.main()
