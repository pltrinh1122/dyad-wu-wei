from drivers import github_client
import yaml
import os

repo_root = "/mnt/shared_data/dzw/dyad-wu-wei"
backlog_items = github_client.list_issues_by_label("backlog")
backlog_items = [item for item in backlog_items if "path" not in item.get("labels", [])]
backlog_items.sort(key=lambda x: x.get("number", 0))

cache_path = os.path.join(repo_root, "artifacts", "global_backlog.yml")
with open(cache_path, "w", encoding="utf-8") as f:
    yaml.dump({"backlog_items": backlog_items}, f)
print("Cache rebuilt.")
