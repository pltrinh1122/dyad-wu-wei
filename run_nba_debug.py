import os
from drivers import github_client
from kernel import agent_frontier

repo_root = "/mnt/shared_data/dzw/dyad-wu-wei"
frontier_file = os.path.join(repo_root, "artifacts", "frontier_state.yml")

state = agent_frontier.load_state(frontier_file)
all_nodes = state.get("nodes", [])
import re
active_ids = set()
for n in all_nodes:
    if n.get("status") not in ("Completed", "Backlog", "Cancelled"):
        match = re.search(r"(?:Node |#)(\d+)", n.get("name", ""))
        if match:
            active_ids.add(str(match.group(1)))

print("Active IDs in frontier:", active_ids)

backlog_items = github_client.list_issues_by_label("backlog")
backlog_items = [item for item in backlog_items if "path" not in item.get("labels", [])]

print("Backlog items count:", len(backlog_items))
for item in backlog_items:
    print(" -", item.get("number"), item.get("title"))

filtered = [item for item in backlog_items if str(item.get("number", "")) not in active_ids]
print("Filtered count:", len(filtered))

