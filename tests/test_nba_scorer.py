import unittest
from unittest.mock import patch, MagicMock
from orchestrator.nba_scorer import NBAScorer

class TestNBAScorer(unittest.TestCase):
    
    @patch("skills.github_client.get_issue_details")
    @patch("skills.github_client.get_issue_labels")
    @patch("orchestrator.mgr_strategic.find_parent_path_id")
    @patch("orchestrator.mgr_strategic.load_ledger")
    def test_calculate_score_clean(self, mock_load, mock_find, mock_labels, mock_details):
        mock_details.side_effect = lambda issue_id: {
            "483": {"title": "Activity 483: Reflect", "body": "## Depends On\n482"},
            "482": {"state": "CLOSED"}
        }[str(issue_id)]
        mock_labels.return_value = ["activity"]
        mock_find.return_value = "480"
        mock_load.return_value = {
            "strategic_goals": [
                {
                    "status": "Active",
                    "prioritized_paths": [480]
                }
            ]
        }
        
        scorer = NBAScorer()
        res = scorer.calculate_score("483")
        
        self.assertEqual(res["score"], 1.0)
        self.assertEqual(res["components"]["dependency"], 1.0)
        self.assertEqual(res["components"]["axiom"], 1.0)
        self.assertEqual(res["components"]["strategic"], 1.0)
        self.assertEqual(res["components"]["risk"], 1.0)

    @patch("skills.github_client.get_issue_details")
    @patch("skills.github_client.get_issue_labels")
    def test_calculate_score_blocked_dependency(self, mock_labels, mock_details):
        mock_details.side_effect = lambda issue_id: {
            "483": {"title": "Activity 483: Reflect", "body": "## Depends On\n482"},
            "482": {"state": "OPEN"}
        }[str(issue_id)]
        mock_labels.return_value = ["activity"]
        
        scorer = NBAScorer()
        res = scorer.calculate_score("483")
        
        self.assertEqual(res["score"], 0.0)
        self.assertEqual(res["components"]["dependency"], 0.0)

    @patch("skills.github_client.get_issue_details")
    @patch("skills.github_client.get_issue_labels")
    def test_calculate_score_axiom_violation(self, mock_labels, mock_details):
        forbidden_title = "Sp" + "ike 483: Align on NBA"
        mock_details.return_value = {"title": forbidden_title, "body": ""}
        mock_labels.return_value = ["activity"]
        
        scorer = NBAScorer()
        res = scorer.calculate_score("483")
        
        # c_axiom is 0.0, c_strategic is 0.0 (no parent/backlog), c_risk is 1.0
        # Score = 1.0 * (0.4 * 0.0 + 0.4 * 0.0 + 0.2 * 1.0) = 0.2
        self.assertEqual(res["score"], 0.2)
        self.assertEqual(res["components"]["axiom"], 0.0)

if __name__ == "__main__":
    unittest.main()
