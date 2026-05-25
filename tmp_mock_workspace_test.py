import os
import sys

# Ensure we can import from the core repo
core_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, core_dir)

from kernel.daemon_workspace import init_workspace

workspace_dir = os.path.join(core_dir, ".workspace")

print(f"Setting up mock workspace at {workspace_dir}...")
# Use the local path instead of URL to avoid network clone if possible,
# or just a lightweight public repo.
# Actually, the repo must be a valid git URL or local path.
local_repo = core_dir
try:
    init_workspace(local_repo)
except Exception as e:
    print(f"Error during init_workspace: {e}")
    sys.exit(1)

print("Verifying workspace structure...")
assert os.path.exists(os.path.join(workspace_dir, "GEMINI.md")), "GEMINI.md missing"
assert os.path.exists(os.path.join(workspace_dir, "kb")), "kb/ missing"
assert os.path.exists(os.path.join(workspace_dir, "artifacts")), "artifacts/ missing"

print("Bootstrapping invariant mock: generating strategic_intent.yml...")
intent_path = os.path.join(workspace_dir, "artifacts", "strategic_intent.yml")
with open(intent_path, "w") as f:
    f.write("mock_telos: Verify Model 1 Redirection\n")
assert os.path.exists(intent_path)

print("Workspace verification complete. Blast radius contained to .workspace/")
