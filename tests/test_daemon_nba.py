import unittest
from unittest.mock import patch, MagicMock
from kernel.daemon_nba import NBADaemon

class TestNBADaemon(unittest.TestCase):
    
    @patch("kernel.daemon_nba.agent_frontier.read_active_path")
    @patch("kernel.daemon_nba.agent_frontier.extract_path_id")
    @patch("drivers.github_client.get_issue_details")
    @patch("drivers.gh_graph_skill.get_next_nodes")
    def test_evaluate_path_continuation(self, mock_get_next, mock_get_details, mock_extract, mock_read):
        mock_read.return_value = "**Refactor and Promote NBA Evaluator (#242)**"
        mock_extract.return_value = "242"
        mock_get_details.return_value = {"title": "Path 242", "body": "some body"}
        mock_get_next.return_value = [{"id": "245", "title": "Implement daemon_nba"}]
        
        nba = NBADaemon()
        result = nba.evaluate("dummy_frontier.md")
        
        self.assertEqual(result["type"], "path_continuation")
        self.assertEqual(result["path_id"], "242")
        self.assertEqual(len(result["recommendations"]), 1)
        self.assertEqual(result["recommendations"][0]["id"], "245")

    @patch("kernel.daemon_nba.agent_frontier.read_active_path")
    @patch("drivers.github_client.list_issues_by_label")
    def test_evaluate_path_switching(self, mock_list, mock_read):
        mock_read.return_value = None # No active path
        mock_list.return_value = [{"number": "100", "title": "Global Task"}]
        
        nba = NBADaemon()
        result = nba.evaluate("dummy_frontier.md")
        
        self.assertEqual(result["type"], "path_switching")
        self.assertEqual(len(result["recommendations"]), 1)
        self.assertEqual(result["recommendations"][0]["number"], "100")

if __name__ == "__main__":
    unittest.main()
