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
        """Dynamically evaluates and surfaces the next best action."""
        # Placeholder for Activity C
        repository = config.get("repository", "pltrinh1122/agent-antigravity")
        print(f"\n📋 Next-Best-Action Hook (repo: {repository}):")
        print("  [Pending Implementation in Activity C]")
