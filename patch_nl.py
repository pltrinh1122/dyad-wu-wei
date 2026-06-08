import sys, re
with open('kernel/node_lifecycle.py', 'r') as f:
    content = f.read()

# 1. Add _get_domain_config method to NodeLifecycle class
# We'll inject it before def checkout(
method = '''
    def _get_domain_config(self):
        import yaml
        from drivers import path_resolver, github_client
        labels = github_client.get_issue_labels(self.issue_id)
        domain_id = None
        for label in labels:
            if label.startswith("domain:"):
                domain_id = label.split(":")[1]
                break
        if not domain_id:
            return None
        try:
            main_repo_dir = path_resolver.get_core_dir()
            if ".worktrees" in main_repo_dir.split(os.sep):
                main_repo_dir = main_repo_dir.split(".worktrees")[0]
            import os
            dyad_config_path = os.path.join(main_repo_dir, "dyad-wu-wei.yml")
            if os.path.exists(dyad_config_path):
                with open(dyad_config_path, 'r') as cf:
                    dyad_config = yaml.safe_load(cf) or {}
                    return dyad_config.get("domains", {}).get(domain_id)
        except Exception as e:
            print(f"Warning: Failed to parse dyad-wu-wei.yml for domains. Error: {e}")
        return None

    @record_execution(stage="act")
    def checkout(self, branch_name: str, frontier_file: str = "artifacts/frontier_state.md") -> None:
        domain_config = self._get_domain_config()
        if not os.environ.get("SPAO_WORKSPACE_DIR") and not re.match(r"^node/\\d+-[a-z0-9-]+$", branch_name):
            if not (domain_config and domain_config.get("branch_prefix") and branch_name.startswith(domain_config["branch_prefix"])):
                raise ValueError(f"Branch name MUST follow the standard: node/<id>-<kebab-case> or domain prefix")
'''
content = re.sub(r'\s*@record_execution\(stage="act"\)\s*def checkout\(self, branch_name: str, frontier_file: str = "artifacts/frontier_state\.md"\) -> None:\s*if not os\.environ\.get\("SPAO_WORKSPACE_DIR"\) and not re\.match\(r"\^node/\\\\d\+-\[a-z0-9-\]\+\\$", branch_name\):\s*raise ValueError\("Branch name MUST follow the standard: node/<id>-<kebab-case>"\)', method, content)

# 2. Modify reflect CI Validation
# Find:
#                 run_tests_script = os.path.join(worktree_dir, "bin", "run-tests")
#                 if not os.path.exists(run_tests_script):
#                     run_tests_script = os.path.join(main_repo, "bin", "run-tests")
#                 subprocess.run([run_tests_script], cwd=worktree_dir, check=True)
ci_block = '''
                domain_config = self._get_domain_config()
                if domain_config and domain_config.get("validation_hook"):
                    run_tests_script = domain_config["validation_hook"]
                    print(f"Running domain-specific validation hook: {run_tests_script}")
                    # hook might be a script path or command, handle appropriately
                    import shlex
                    subprocess.run(shlex.split(run_tests_script), cwd=worktree_dir, check=True)
                else:
                    run_tests_script = os.path.join(worktree_dir, "bin", "run-tests")
                    if not os.path.exists(run_tests_script):
                        run_tests_script = os.path.join(main_repo, "bin", "run-tests")
                    subprocess.run([run_tests_script], cwd=worktree_dir, check=True)
'''
content = re.sub(
    r'\s*run_tests_script = os\.path\.join\(worktree_dir, "bin", "run-tests"\)\s*if not os\.path\.exists\(run_tests_script\):\s*run_tests_script = os\.path\.join\(main_repo, "bin", "run-tests"\)\s*subprocess\.run\(\[run_tests_script\], cwd=worktree_dir, check=True\)',
    ci_block,
    content
)

# 3. Modify reflect HTIL Bypass for auto_approve_labels
# Find:
#             modified_files = git_client.diff_names("origin/main", cwd=worktree_dir)
#             is_autonomous_merge = True
#             if any(f in sacred_files for f in modified_files):
#                 is_autonomous_merge = False
htil_block = '''
            modified_files = git_client.diff_names("origin/main", cwd=worktree_dir)
            is_autonomous_merge = True
            if any(f in sacred_files for f in modified_files):
                is_autonomous_merge = False
            
            domain_config = self._get_domain_config()
            if domain_config and domain_config.get("auto_approve_labels"):
                labels = github_client.get_issue_labels(self.issue_id)
                if any(label in domain_config["auto_approve_labels"] for label in labels):
                    is_autonomous_merge = True
'''
content = re.sub(
    r'\s*modified_files = git_client\.diff_names\("origin/main", cwd=worktree_dir\)\s*is_autonomous_merge = True\s*if any\(f in sacred_files for f in modified_files\):\s*is_autonomous_merge = False',
    htil_block,
    content
)

with open('kernel/node_lifecycle.py', 'w') as f:
    f.write(content)
print("Patched kernel/node_lifecycle.py")
