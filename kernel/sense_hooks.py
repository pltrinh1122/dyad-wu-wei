import yaml
import os
from kernel import agent_frontier

class HookDaemon:
    """Manages the execution of configurable Sense hooks."""
    
    def __init__(self, config_path="antigravity.yml"):
        self.config_path = config_path
        self.hooks = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            return []
        with open(self.config_path, "r") as f:
            config = yaml.safe_load(f)
        return config.get("sense_hooks", [])

    def execute_all(self, local_mode=False):
        """Iterates over all configured hooks and executes them."""
        for hook_config in self.hooks:
            hook_type = hook_config.get("type")
            if hook_type == "prompt_queue":
                self.execute_prompt_queue_hook(hook_config)
            elif hook_type == "next_best_action":
                self.execute_next_best_action_hook(hook_config, local_mode=local_mode)
            else:
                print(f"Warning: Unknown hook type '{hook_type}'")

    def execute_prompt_queue_hook(self, config):
        """Surfaces pending operator prompts from a configurable file path."""
        location = config.get("location", "artifacts/prompt_backlog.yml")
        from kernel.daemon_prompt import list_prompts
        print()
        list_prompts(all_prompts=False, backlog_file=location)

    def execute_next_best_action_hook(self, config, local_mode=False):
        """Dynamically evaluates and surfaces the next best action using NBADaemon kernel."""
        from kernel.daemon_nba import NBADaemon
        from drivers import issue_factory
        repository = config.get("repository", "pltrinh1122/agent-antigravity")
        frontier_file = config.get("frontier_file", "artifacts/frontier_state.md")

        nba = NBADaemon(repository=repository)
        result = nba.evaluate(frontier_file=frontier_file, local_mode=local_mode)

        if result["type"] == "error":
            print(f"\n❌ Next-Best-Action Error: {result['message']}")
            return

        # History Extraction
        last_step = agent_frontier.read_last_completed_node(frontier_file)
        if last_step:
            history_info = f"\033[1;30m(Last Step: {last_step})\033[0m"
        else:
            history_info = ""

        mode_label = "📍 Path Continuation" if result["type"] == "path_continuation" else "🔀 Path Switch Recommended"
        
        path_info = ""
        if result["type"] == "path_continuation":
            path_info = f"  \033[1;34m{result['path_title']}\033[0m"
        elif result["type"] == "path_switching":
            if not result["recommendations"]:
                path_info = "  (Global backlog empty)"
            else:
                path_info = "  (Switching to Global Backlog)"

        recommendations_list = ""
        if result["recommendations"]:
            from kernel.nba_scorer import GranularNBAScorer
            scorer = GranularNBAScorer(frontier_file=frontier_file)
            lines = []
            for item in result["recommendations"]:
                issue_id = item.get("id") or item.get("number")
                title = item['title']
                
                # Calculate score
                try:
                    score_data = scorer.calculate_score(issue_id)
                    score_val = score_data.get("score", 0.0)
                    comps = score_data.get("components", {})
                    score_str = f" \033[1;36m[Score: {score_val:.3f} | dep={comps.get('dependency', 0.0)}, ax={comps.get('axiom', 0.0)}, str={comps.get('strategic', 0.0)}, rsk={comps.get('risk', 0.0)}]\033[0m"
                except Exception:
                    score_str = ""
                
                # Semantic Styling
                if "Discovery" in title:
                    styled_title = f"\033[1;33m{title}\033[0m" # Bold Yellow
                elif "Activity" in title:
                    styled_title = f"\033[1;32m{title}\033[0m" # Bold Green
                else:
                    styled_title = title
                    
                lines.append(f"  → #{issue_id}: {styled_title}{score_str}")
            recommendations_list = "\n".join(lines)
        else:
            recommendations_list = "  (No recommendations found.)"

        # Construct raw content for framing
        content_lines = [
            f"🎯 \033[1;36mNext-Best-Action\033[0m (\033[1;35m{mode_label}\033[0m)",
            history_info,
            path_info,
            recommendations_list
        ]
        
        # Clean up empty lines
        content_lines = [l for l in content_lines if l.strip()]

        # Framing Logic (Simplified for terminal width)
        print("\n┌──────────────────────────────────────────────────────────┐")
        for line in content_lines:
            # We don't pad to the right perfectly because of ANSI escape codes 
            # calculating visible length is non-trivial without a dedicated library.
            # We'll just print the line with a left border.
            print(f"│ {line}")
        print("└──────────────────────────────────────────────────────────┘")
