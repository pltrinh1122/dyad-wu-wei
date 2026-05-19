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
        repository = config.get("repository", "pltrinh1122/agent-antigravity")
        frontier_file = config.get("frontier_file", "artifacts/frontier_state.md")

        nba = NBAManager(repository=repository)
        result = nba.evaluate(frontier_file=frontier_file)

        if result["type"] == "error":
            print(f"\n❌ Next-Best-Action Error: {result['message']}")
            return

        mode_label = "📍 Path Continuation" if result["type"] == "path_continuation" else "🔀 Path Switch Recommended"
        print(f"\n🎯 Next-Best-Action ({mode_label}):")
        
        if result["type"] == "path_continuation":
            print(f"  Continuing Path {result['path_id']}: {result['path_title']}")
        elif result["type"] == "path_switching":
            if not result["recommendations"]:
                print("  No pending work in current Path. Recommending next best from global backlog.")
            else:
                print("  Path exhausted or not detected. Recommending next best from global backlog:")

        if result["recommendations"]:
            for item in result["recommendations"]:
                # gh_graph_skill returns 'id' and 'title', github_client returns 'number' and 'title'
                issue_id = item.get("id") or item.get("number")
                print(f"  → #{issue_id}: {item['title']}")
        else:
            print("  (No recommendations found.)")
