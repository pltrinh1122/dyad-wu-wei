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
        """Dynamically evaluates and surfaces the next best action using nba_evaluator skill."""
        from skills import nba_evaluator
        repository = config.get("repository", "pltrinh1122/agent-antigravity")
        frontier_file = config.get("frontier_file", None)

        result = nba_evaluator.evaluate(repository=repository, frontier_file=frontier_file)

        mode_label = "📍 Path Continuation" if result["mode"] == "path_continuation" else "🔀 Path Switch Recommended"
        print(f"\n🎯 Next-Best-Action ({mode_label}):")
        print(f"  {result['message']}")
        if result["recommended"]:
            for item in result["recommended"]:
                print(f"  → #{item['number']}: {item['title']}")
        else:
            print("  (No pending backlog items found.)")
