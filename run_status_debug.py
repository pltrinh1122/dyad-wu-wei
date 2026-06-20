import os
import sys
from kernel.daemon_nba import NBADaemon

repo_root = "/mnt/shared_data/dzw/dyad-wu-wei"
frontier_path = os.path.join(repo_root, "artifacts", "frontier_state.yml")

nba = NBADaemon(repository="pltrinh1122/dyad-wu-wei")
result = nba.evaluate(frontier_file=frontier_path, local_mode=False)

print(result)
