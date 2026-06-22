import unittest
from unittest.mock import patch, mock_open
from kernel.daemon_nba import NBADaemon

class TestNBADaemon(unittest.TestCase):
    
    @patch("drivers.github_client.list_issues_by_label")
    @patch("kernel.daemon_strategic.get_ledger_path")
    @patch("os.path.exists")
    def test_evaluate_next_best_rub(self, mock_exists, mock_get_ledger, mock_list):
        mock_exists.return_value = True
        mock_get_ledger.return_value = "strategic_intent.yml"
        
        yaml_content = """
strategic_goals:
- id: SG-1
  status: Active
  title: Important Synergistic Partnership
  collaborative_gap: Automation hard-caps output because agent limited
"""
        
        mock_list.return_value = [
            {"number": "100", "title": "Random Issue", "body": "Nothing special here."},
            {"number": "101", "title": "Synergistic automation", "body": "Fix the automation output."}
        ]
        
        nba = NBADaemon()
        with patch("builtins.open", mock_open(read_data=yaml_content)):
            result = nba.evaluate("dummy_frontier.md")
            
        self.assertEqual(result["type"], "next_best_rub")
        self.assertEqual(len(result["recommendations"]), 2)
        # 101 should score higher because it has 'synergistic', 'automation', 'output'
        self.assertEqual(result["recommendations"][0]["number"], "101")
        self.assertEqual(result["recommendations"][1]["number"], "100")

    @patch("drivers.github_client.list_issues_by_label")
    @patch("kernel.daemon_nba.agent_frontier.load_state")
    def test_evaluate_locked_node(self, mock_load, mock_list):
        mock_load.return_value = {
            "active_agents": {
                "agent-x": {
                    "current_active_node": "Node 100"
                }
            }
        }
        mock_list.return_value = [
            {"number": 100, "title": "Locked Task"},
            {"number": 101, "title": "Open Task"}
        ]
        
        nba = NBADaemon()
        with patch("os.path.exists", return_value=False):
            result = nba.evaluate("dummy_frontier.md")
            
        self.assertEqual(result["type"], "next_best_rub")
        self.assertEqual(len(result["recommendations"]), 1)
        self.assertEqual(result["recommendations"][0]["number"], 101)

if __name__ == "__main__":
    unittest.main()
