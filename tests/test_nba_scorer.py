import unittest
from kernel.nba_scorer import NBAScorer
from drivers import github_client
from kernel import daemon_strategic
import kernel.nba_scorer as nba_scorer_module

class TestNBAScorer(unittest.TestCase):
    def setUp(self):
        self.old_get_issue_details = github_client.get_issue_details
        self.old_get_issue_labels = github_client.get_issue_labels
        self.old_find_parent_path_id = daemon_strategic.find_parent_path_id
        self.old_load_ledger = daemon_strategic.load_ledger
        self.old_get_persona_ownership = nba_scorer_module._get_persona_ownership
        self.old_get_active_persona = nba_scorer_module._get_active_persona

    def tearDown(self):
        github_client.get_issue_details = self.old_get_issue_details
        github_client.get_issue_labels = self.old_get_issue_labels
        daemon_strategic.find_parent_path_id = self.old_find_parent_path_id
        daemon_strategic.load_ledger = self.old_load_ledger
        nba_scorer_module._get_persona_ownership = self.old_get_persona_ownership
        nba_scorer_module._get_active_persona = self.old_get_active_persona

    def test_calculate_score_clean(self):
        github_client.get_issue_details = lambda issue_id: {
            "483": {"title": "Activity 483: Reflect", "body": "## Depends On\n482"},
            "482": {"state": "CLOSED"}
        }[str(issue_id)]
        github_client.get_issue_labels = lambda x: ["activity"]
        daemon_strategic.find_parent_path_id = lambda x: "480"
        daemon_strategic.load_ledger = lambda: {
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

    def test_calculate_score_blocked_dependency(self):
        github_client.get_issue_details = lambda issue_id: {
            "483": {"title": "Activity 483: Reflect", "body": "## Depends On\n482"},
            "482": {"state": "OPEN"}
        }[str(issue_id)]
        github_client.get_issue_labels = lambda x: ["activity"]

        scorer = NBAScorer()
        res = scorer.calculate_score("483")

        self.assertEqual(res["score"], 0.0)
        self.assertEqual(res["components"]["dependency"], 0.0)

    def test_calculate_score_axiom_violation(self):
        forbidden_title = "Sp" + "ike 483: Align on NBA"
        github_client.get_issue_details = lambda issue_id: {"title": forbidden_title, "body": ""}
        github_client.get_issue_labels = lambda x: ["activity"]

        scorer = NBAScorer()
        res = scorer.calculate_score("483")

        self.assertEqual(res["score"], 0.2)
        self.assertEqual(res["components"]["axiom"], 0.0)

    def test_calculate_score_persona_fail_open(self):
        github_client.get_issue_details = lambda issue_id: {"title": "Test", "body": ""}
        github_client.get_issue_labels = lambda x: ["activity"]
        daemon_strategic.find_parent_path_id = lambda x: "480"
        daemon_strategic.load_ledger = lambda: {"strategic_goals": [{"id": "SG-123", "status": "Active", "prioritized_paths": [480]}]}
        nba_scorer_module._get_active_persona = lambda: "agent-platform"
        nba_scorer_module._get_persona_ownership = lambda: {} # WHAT-0062 does not exist or empty

        scorer = NBAScorer()
        res = scorer.calculate_score("483")
        self.assertEqual(res["components"]["persona"], 1.0)

    def test_calculate_score_persona_match(self):
        github_client.get_issue_details = lambda issue_id: {"title": "Test", "body": ""}
        github_client.get_issue_labels = lambda x: ["activity"]
        daemon_strategic.find_parent_path_id = lambda x: "480"
        daemon_strategic.load_ledger = lambda: {"strategic_goals": [{"id": "SG-123", "status": "Active", "prioritized_paths": [480]}]}
        nba_scorer_module._get_active_persona = lambda: "agent-platform"
        nba_scorer_module._get_persona_ownership = lambda: {"SG-123": "agent-platform"}

        scorer = NBAScorer()
        res = scorer.calculate_score("483")
        self.assertEqual(res["components"]["persona"], 1.0)

    def test_calculate_score_persona_mismatch(self):
        github_client.get_issue_details = lambda issue_id: {"title": "Test", "body": ""}
        github_client.get_issue_labels = lambda x: ["activity"]
        daemon_strategic.find_parent_path_id = lambda x: "480"
        daemon_strategic.load_ledger = lambda: {"strategic_goals": [{"id": "SG-123", "status": "Active", "prioritized_paths": [480]}]}
        nba_scorer_module._get_active_persona = lambda: "agent-sg1"
        nba_scorer_module._get_persona_ownership = lambda: {"SG-123": "agent-platform"}

        scorer = NBAScorer()
        res = scorer.calculate_score("483")
        self.assertEqual(res["components"]["persona"], 0.0)
        self.assertEqual(res["score"], 0.0)

    def test_calculate_score_semantic_dispatcher_conflict(self):
        github_client.get_issue_details = lambda issue_id: {"title": "Test", "body": ""}
        github_client.get_issue_labels = lambda x: ["activity"]
        daemon_strategic.find_parent_path_id = lambda x: "480"
        daemon_strategic.load_ledger = lambda: {
            "strategic_goals": [
                {"id": "SG-123", "status": "Active", "prioritized_paths": [480]},
                {"id": "SG-999", "status": "Active", "prioritized_paths": [900]}
            ]
        }
        nba_scorer_module._get_active_persona = lambda: "agent-alpha"
        nba_scorer_module._get_persona_ownership = lambda: {}
        
        from kernel import agent_frontier
        self.old_load_state = getattr(agent_frontier, "load_state", None)
        self.old_resolve_yml_path = getattr(agent_frontier, "resolve_yml_path", None)
        
        agent_frontier.resolve_yml_path = lambda x: "dummy.yml"
        agent_frontier.load_state = lambda x: {
            "active_agents": {
                "agent-beta": {
                    "current_active_path": "#480"  # agent-beta is working on path 480 which is in SG-123
                }
            }
        }
        
        scorer = NBAScorer()
        res = scorer.calculate_score("483")
        
        # Restore mock
        if self.old_load_state:
            agent_frontier.load_state = self.old_load_state
        if self.old_resolve_yml_path:
            agent_frontier.resolve_yml_path = self.old_resolve_yml_path
            
        # c_dep should drop to 0.0 because of the semantic conflict in SG-123
        self.assertEqual(res["components"]["dependency"], 0.0)
        self.assertEqual(res["score"], 0.0)

if __name__ == "__main__":
    unittest.main()
