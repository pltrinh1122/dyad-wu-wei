import os
import re
import yaml
import statistics
import unittest
from unittest.mock import patch

from orchestrator.nba_scorer import NBAScorer, GranularNBAScorer

class TestScoringABTest(unittest.TestCase):
    
    def test_nba_scoring_ab_test_evaluation(self):
        # 1. Load open backlog paths from frontier_state.yml
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        frontier_path = os.path.join(repo_root, "artifacts", "frontier_state.yml")
        self.assertTrue(os.path.exists(frontier_path), f"{frontier_path} not found")
        
        with open(frontier_path, "r") as f:
            frontier_data = yaml.safe_load(f)
            
        issue_cache = {}
        open_paths = []
        
        for node in frontier_data.get("nodes", []):
            name = node.get("name", "")
            status = node.get("status", "")
            if status == "Backlog" and "Path " in name:
                match = re.search(r"Path\s+(\d+)", name)
                if match:
                    num = match.group(1)
                    issue_cache[num] = {
                        "number": int(num),
                        "title": name,
                        "body": node.get("learnings", ""),
                        "labels": ["backlog", "path"],
                        "state": "OPEN"
                    }
                    open_paths.append(num)
            
        # Ensure we have some open paths
        self.assertGreater(len(open_paths), 0, "No open backlog paths found in frontier_state.yml")
        
        # 2. Mock github_client to read from issue_cache
        def mock_get_issue_details(issue_id):
            issue_id_str = str(issue_id)
            if issue_id_str in issue_cache:
                return issue_cache[issue_id_str]
            # Fallback
            return {"number": int(issue_id), "title": f"Mock Issue {issue_id}", "body": "", "state": "CLOSED"}
            
        def mock_get_issue_labels(issue_id):
            issue_id_str = str(issue_id)
            if issue_id_str in issue_cache:
                return issue_cache[issue_id_str]["labels"]
            return []
            
        def mock_list_issues_by_label(label):
            return [
                {"number": int(issue_id), "title": issue_cache[issue_id]["title"], "url": ""}
                for issue_id in open_paths if label in issue_cache[issue_id]["labels"]
            ]
            
        # Patches
        with patch("skills.github_client.get_issue_details", side_effect=mock_get_issue_details), \
             patch("skills.github_client.get_issue_labels", side_effect=mock_get_issue_labels), \
             patch("skills.github_client.list_issues_by_label", side_effect=mock_list_issues_by_label), \
             patch("orchestrator.mgr_strategic.github_client.get_issue_details", side_effect=mock_get_issue_details):
             
            # 3. Instantiate Scorers
            control_scorer = NBAScorer()
            treatment_scorer = GranularNBAScorer()
            
            control_scores = []
            treatment_scores = []
            
            output_lines = []
            def report_print(msg):
                print(msg)
                output_lines.append(msg)
                
            report_print("\n" + "="*80)
            report_print(f"Executing A/B Test on {len(open_paths)} Open Backlog Paths:")
            report_print("="*80)
            report_print(f"{'Path ID':<10} | {'Title':<45} | {'Control (A)':<12} | {'Treatment (B)':<12}")
            report_print("-"*80)
            
            for path_id in open_paths:
                title = issue_cache[path_id]["title"]
                
                res_a = control_scorer.calculate_score(path_id)
                res_b = treatment_scorer.calculate_score(path_id)
                
                control_scores.append(res_a["score"])
                treatment_scores.append(res_b["score"])
                
                short_title = title[:42] + "..." if len(title) > 45 else title
                report_print(f"#{path_id:<9} | {short_title:<45} | {res_a['score']:<12} | {res_b['score']:<12}")
                
            # 4. Calculate Discernment Index (D)
            d_a = statistics.pstdev(control_scores)
            d_b = statistics.pstdev(treatment_scores)
            
            report_print("="*80)
            report_print(f"Control Group (A) Discernment Index (D_A): {d_a:.6f}")
            report_print(f"Treatment Group (B) Discernment Index (D_B): {d_b:.6f}")
            report_print("="*80)
            
            # Hypothesis verification
            null_rejected = d_b > d_a
            report_print(f"Hypothesis Test Results:")
            report_print(f"  Null Hypothesis H_0: D_B <= D_A")
            report_print(f"  Alternative Hypothesis H_1: D_B > D_A")
            report_print(f"  Result: {'REJECT H_0 (Falsified!)' if null_rejected else 'ACCEPT H_0'}")
            report_print("="*80)
            
            # Topological Feasibility check
            # Find highest scoring path under Treatment Group (B)
            scored_paths = [
                (open_paths[i], treatment_scores[i], issue_cache[open_paths[i]])
                for i in range(len(open_paths))
            ]
            scored_paths.sort(key=lambda x: x[1], reverse=True)
            
            top_path_id, top_score, top_details = scored_paths[0]
            top_dep = treatment_scorer.calculate_score(top_path_id)["components"]["dependency"]
            
            report_print(f"Top-Ranked Path: #{top_path_id} (Score: {top_score}) - {top_details['title']}")
            report_print(f"Topological Feasibility (C_dep == 1.0): {top_dep == 1.0}")
            report_print("="*80)
            
            # Write to file
            with open("/tmp/ab_test_output.txt", "w") as out_f:
                out_f.write("\n".join(output_lines) + "\n")
            
            # Assertion verifications
            self.assertTrue(null_rejected, f"Falsification failed: D_B ({d_b:.6f}) is not greater than D_A ({d_a:.6f})")
            self.assertEqual(top_dep, 1.0, f"Top ranked path #{top_path_id} is blocked by open dependencies")
