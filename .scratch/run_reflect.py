import subprocess
import os

learnings = """### Continue
- Utilizing explicit ask_question multi-turn rub-backs to mechanically lock the operator intent before altering global taxonomies.

### Stop
- Using gh-issues as a passive backlog/staging queue. All issues must now represent live intent bound by the clarify mechanical lock.

### Start
- Relying exclusively on the `clarify -> dispose -> execute -> blocked` lifecycle for DAG nodes.
"""

env = os.environ.copy()
env["GH_REPO"] = "pltrinh1122/dyad-wu-wei"
env["SPAO_WORKSPACE_DIR"] = "/mnt/shared_data/dzw/dyad-wu-wei"

subprocess.run([
    "./bin/node", "reflect",
    "2500",
    "Node 2500: Audit and align GitHub Issues usage with the dyad-chiron interaction workflow.",
    learnings,
    "[]", 
    "refactor: migrate legacy taxonomy to clarify-dispose-execute",
    "node/2500-synergy-audit"
], env=env, check=True)
