import yaml
import sys

with open("artifacts/strategic_intent.yml", "r") as f:
    data = yaml.safe_load(f)

mappings = {
    "SG-0001": [1517],
    "SG-0003": [1567, 1642],
    "SG-0004": [1633],
    "SG-0005": [1534, 1561, 1585, 1593, 1602, 1612],
    "SG-0006": [1547]
}

for goal in data.get("strategic_goals", []):
    gid = goal.get("id")
    if gid in mappings:
        for path_id in mappings[gid]:
            if path_id not in goal.get("prioritized_paths", []):
                goal["prioritized_paths"].append(path_id)

class Dumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)

with open("artifacts/strategic_intent.yml", "w") as f:
    yaml.dump(data, f, default_flow_style=False, sort_keys=False, Dumper=Dumper)
