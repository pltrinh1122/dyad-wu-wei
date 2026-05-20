import os
import sys
import subprocess
import argparse
from typing import List

class TestManager:
    """Manages the execution and orchestration of the test suite."""

    def __init__(self, repo_root: str = "."):
        self.repo_root = os.path.abspath(repo_root)

    def run(self, targets: List[str] = None) -> int:
        """Executes pytest for the given targets."""
        if not targets:
            targets = ["tests/"]

        env = os.environ.copy()
        env["PYTHONPATH"] = self.repo_root
        env["ANTIGRAVITY_RUNNING_TESTS"] = "1"

        pytest_exe = self._resolve_pytest()
        
        print(f"🚀 Running tests: {' '.join(targets)}")
        result = subprocess.run(
            [pytest_exe] + targets,
            env=env,
            cwd=self.repo_root
        )
        
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print(f"❌ Test suite failed with exit code {result.returncode}")
            
        return result.returncode

    def _resolve_pytest(self) -> str:
        """Dynamically resolves the pytest executable."""
        venv_dir = os.environ.get("VIRTUAL_ENV")
        if venv_dir and os.path.exists(os.path.join(venv_dir, "bin/pytest")):
            return os.path.join(venv_dir, "bin/pytest")
        
        # Priority 2: System-specific path from testing_harness
        if os.path.exists("/home/pt/actions-runner/venv/bin/pytest"):
            return "/home/pt/actions-runner/venv/bin/pytest"
            
        # Priority 3: Local venv
        if os.path.exists(os.path.join(self.repo_root, ".venv/bin/pytest")):
            return os.path.join(self.repo_root, ".venv/bin/pytest")

        return "pytest"

def main():
    parser = argparse.ArgumentParser(description="SPAO Test Manager")
    parser.add_argument("targets", nargs="*", help="Test files or directories to run")
    
    args = parser.parse_args()
    
    manager = TestManager()
    sys.exit(manager.run(args.targets))

if __name__ == "__main__":
    main()
