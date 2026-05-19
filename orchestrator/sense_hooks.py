import yaml
import os

class HookManager:
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

    def execute_all(self):
        """Iterates over all configured hooks and executes them."""
        for hook_config in self.hooks:
            hook_type = hook_config.get("type")
            if hook_type == "prompt_queue":
                self.execute_prompt_queue_hook(hook_config)
            elif hook_type == "next_best_action":
                self.execute_next_best_action_hook(hook_config)
            else:
                print(f"Warning: Unknown hook type '{hook_type}'")

    def execute_prompt_queue_hook(self, config):
        """Surfaces pending operator prompts from a configurable file path."""
        location = config.get("location", "artifacts/prompt_backlog.yml")
        from orchestrator.mgr_prompt import list_prompts
        print()
        list_prompts(all_prompts=False, backlog_file=location)

    def execute_next_best_action_hook(self, config):
        """Dynamically evaluates and surfaces the next best action using NBAManager orchestrator."""
        from orchestrator.mgr_nba import NBAManager
        from skills import issue_factory
        repository = config.get("repository", "pltrinh1122/agent-antigravity")
        frontier_file = config.get("frontier_file", "artifacts/frontier_state.md")

        nba = NBAManager(repository=repository)
        result = nba.evaluate(frontier_file=frontier_file)

        if result["type"] == "error":
            print(f"\n❌ Next-Best-Action Error: {result['message']}")
            return

        mode_label = "📍 Path Continuation" if result["type"] == "path_continuation" else "🔀 Path Switch Recommended"
        
        path_info = ""
        if result["type"] == "path_continuation":
            path_info = f"  \033[1m{result['path_title']}\033[0m"
        elif result["type"] == "path_switching":
            if not result["recommendations"]:
                path_info = "  (Global backlog empty)"
            else:
                path_info = "  (Switching to Global Backlog)"

        recommendations_list = ""
        if result["recommendations"]:
            lines = []
            for item in result["recommendations"]:
                issue_id = item.get("id") or item.get("number")
                lines.append(f"  → #{issue_id}: {item['title']}")
            recommendations_list = "\n".join(lines)
        else:
            recommendations_list = "  (No recommendations found.)"

        banner = issue_factory.render_template("nba_banner", {
            "mode_label": mode_label,
            "path_info": path_info,
            "recommendations_list": recommendations_list
        })
        print("\n" + banner.strip())
