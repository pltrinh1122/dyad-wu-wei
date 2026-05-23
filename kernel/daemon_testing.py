import os
import sys
import subprocess
import argparse
import re
import yaml
from typing import List

class TestManager:
    """Manages the execution and orchestration of the test suite."""

    def __init__(self, repo_root: str = None):
        from drivers import path_resolver
        if repo_root is None:
            repo_root = path_resolver.get_workspace_dir()
        self.repo_root = os.path.abspath(repo_root)
        self.config_path = os.path.join(self.repo_root, "orchestrator/test_config.yml")
        self.config = self._load_config()

    def _load_config(self) -> dict:
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return yaml.safe_load(f)
        return {"guardrails": {"patch_density": {"threshold": 10, "strict": False}}}

    def audit_patch_density(self, targets: List[str]) -> bool:
        """Audits the patch density of targeted test files."""
        threshold = self.config.get("guardrails", {}).get("patch_density", {}).get("threshold", 10)
        strict = self.config.get("guardrails", {}).get("patch_density", {}).get("strict", False)
        
        violations = []
        
        # Resolve all test files in targets
        test_files = []
        for target in targets:
            abs_target = os.path.abspath(os.path.join(self.repo_root, target))
            if os.path.isfile(abs_target):
                test_files.append(abs_target)
            elif os.path.isdir(abs_target):
                for root, _, files in os.walk(abs_target):
                    for f in files:
                        if f.startswith("test_") and f.endswith(".py"):
                            test_files.append(os.path.join(root, f))
        
        for filepath in test_files:
            with open(filepath, "r") as f:
                content = f.read()
            
            patches = re.findall(r"@patch\(['\"]([^'\"]+)['\"]\)", content)
            count = len(patches)
            
            if count > threshold:
                violations.append((os.path.relpath(filepath, self.repo_root), count))
        
        if violations:
            print("\n🚨 Patch Density Violation Detected!")
            print(f"Threshold: {threshold} patches per file")
            for file, count in violations:
                print(f"  - {file}: {count} patches")
            
            if strict:
                print("❌ Aborting tests due to strict guardrail enforcement. Use fixtures in conftest.py instead.")
                return False
        
        return True

    def run(self, targets: List[str] = None) -> int:
        """Executes pytest for the given targets."""
        if not targets:
            targets = ["tests/"]

        # 1. Audit Phase
        if not self.audit_patch_density(targets):
            return 1

        # 2. Execution Phase
        env = os.environ.copy()
        env["PYTHONPATH"] = self.repo_root
        env["ANTIGRAVITY_RUNNING_TESTS"] = "1"

        pytest_exe = self._resolve_pytest()
        
        print(f"🚀 Running tests: {' '.join(targets)}")
        result = subprocess.run(
            [pytest_exe] + targets,
            env=env,
            cwd=self.repo_root,
            capture_output=True,
            text=True
        )
        
        # Write captured stdout and stderr to physical output streams
        sys.stdout.write(result.stdout)
        sys.stderr.write(result.stderr)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print(f"❌ Test suite failed with exit code {result.returncode}")
            
            # Post-failure diagnostics parsing & rule synthesis (SG-0005)
            try:
                from drivers import knowledge_accrual_skill
                import json
                from datetime import datetime, timezone
                
                failures = knowledge_accrual_skill.parse_test_failure_diagnostics(result.stdout)
                if failures:
                    audit_dir = os.path.join(self.repo_root, "artifacts", "audit")
                    os.makedirs(audit_dir, exist_ok=True)
                    
                    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                    fail_file = os.path.join(audit_dir, f"test-fail-{timestamp}.json")
                    with open(fail_file, "w", encoding="utf-8") as f:
                        json.dump({
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "failures": failures
                        }, f, indent=4)
                    print(f"Recorded test failures to {fail_file}")
                    
                    # Update audit_config.yml with synthesized rules
                    config_path = os.path.join(self.repo_root, "infra", "audit-daemon", "audit_config.yml")
                    if os.path.exists(config_path):
                        try:
                            with open(config_path, "r", encoding="utf-8") as f:
                                config_data = yaml.safe_load(f) or {}
                            
                            if "rules" not in config_data:
                                config_data["rules"] = []
                                
                            rules_updated = False
                            for failure in failures:
                                new_rule = knowledge_accrual_skill.synthesize_rule(failure)
                                if new_rule:
                                    existing_ids = {r.get("id") for r in config_data["rules"] if isinstance(r, dict)}
                                    if new_rule["id"] not in existing_ids:
                                        config_data["rules"].append(new_rule)
                                        rules_updated = True
                                        print(f"Synthesized new rule: {new_rule['id']} for term: {new_rule.get('pattern')}")
                                        
                            if rules_updated:
                                with open(config_path, "w", encoding="utf-8") as f:
                                    yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)
                                print("Updated audit_config.yml with synthesized rules.")
                        except Exception as ex:
                            print(f"Warning: Failed to update audit_config.yml with synthesized rules: {ex}")
            except Exception as e:
                print(f"Warning: Failed to execute knowledge accrual hooks: {e}")
            
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

from kernel.daemon_telemetry import record_execution

@record_execution(stage="act")
def main():
    parser = argparse.ArgumentParser(description="SPAO Test Manager")
    parser.add_argument("targets", nargs="*", help="Test files or directories to run")
    
    args = parser.parse_args()
    
    manager = TestManager()
    sys.exit(manager.run(args.targets))

if __name__ == "__main__":
    main()
