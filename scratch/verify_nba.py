from orchestrator.sense_hooks import HookManager
import os

# Mock the configuration to ensure NBA hook is triggered
os.environ["SPAO_VERBOSE"] = "1"
hm = HookManager()
# Manually trigger the NBA hook
hm.execute_next_best_action_hook({"type": "next_best_action"})
