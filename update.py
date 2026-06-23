import re

with open("kernel/daemon_nba.py", "r") as f:
    content = f.read()

replacement = """            active_path = None
            try:
                active_path = agent_frontier.read_active_path(frontier_file)
            except Exception:
                pass

            if not top_items:
                nba_type = "idle"
            elif active_path:
                nba_type = "path_continuation"
            else:
                nba_type = "path_switching"

            return {
                "type": nba_type,
                "recommendations": top_items
            }"""

content = re.sub(
    r'            return \{\n                "type": "next_best_rub",\n                "recommendations": top_items\n            \}',
    replacement,
    content,
    count=1
)

with open("kernel/daemon_nba.py", "w") as f:
    f.write(content)

with open("tests/test_daemon_nba.py", "r") as f:
    content2 = f.read()

content2 = re.sub(r'"next_best_rub"', r'"path_switching"', content2)

with open("tests/test_daemon_nba.py", "w") as f:
    f.write(content2)

