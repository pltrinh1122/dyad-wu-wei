import os
import re
import subprocess
from kernel.daemon_telemetry import record_execution

def _resolve_gh_repo() -> str | None:
    workspace_dir = os.environ.get("SPAO_WORKSPACE_DIR")
    if not workspace_dir:
        return None
    try:
        res = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, check=True, cwd=workspace_dir
        )
        url = res.stdout.strip()
        match = re.search(r"github\.com[:/]([^/]+/[^/.]+)(?:\.git)?", url)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None

def _run_gh(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    env = kwargs.get("env") or os.environ.copy()
    
    # Headless GH_TOKEN Fallback
    if "GH_TOKEN" not in env and "GITHUB_TOKEN" not in env:
        try:
            core_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            env_file = os.path.join(core_dir, ".env")
            if os.path.exists(env_file):
                with open(env_file, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#"):
                            parts = line.split("=", 1)
                            if len(parts) == 2:
                                k, v = parts[0].strip(), parts[1].strip()
                                if k in ("GH_TOKEN", "GITHUB_TOKEN"):
                                    env[k] = v.strip('"').strip("'")
        except Exception:
            pass

    workspace_dir = os.environ.get("SPAO_WORKSPACE_DIR")
    if workspace_dir:
        if cmd[0] == "git" and kwargs.get("cwd") is None:
            kwargs["cwd"] = workspace_dir
        elif cmd[0] == "gh":
            repo = _resolve_gh_repo()
            if repo:
                env["GH_REPO"] = repo
                
    kwargs["env"] = env
    
    check = kwargs.pop("check", False)
    
    is_read_cmd = len(cmd) >= 3 and cmd[0] == "gh" and cmd[1] in ("issue", "pr", "run") and cmd[2] in ("list", "view", "search", "checks")
    max_retries = 3 if is_read_cmd else 1
    
    for attempt in range(max_retries):
        result = subprocess.run(cmd, **kwargs)
        
        if check and result.returncode != 0:
            # Ignore GraphQL deprecation warnings if stdout is valid JSON
            if "--json" in cmd and hasattr(result, "stdout") and result.stdout:
                try:
                    import json
                    json.loads(_clean_json_output(result.stdout))
                    return result
                except Exception:
                    pass
            if attempt < max_retries - 1:
                import time
                time.sleep(2 ** attempt)
                continue
            raise subprocess.CalledProcessError(result.returncode, cmd, output=getattr(result, "stdout", None), stderr=getattr(result, "stderr", None))
            
        return result
        
    return result

import tempfile
import json
import time
from kernel.daemon_telemetry import record_execution

_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_FILE_PATH = os.path.join(_DIR, "artifacts", "cache", "github_state_cache.json")

def _load_cache() -> dict:
    if not os.path.exists(CACHE_FILE_PATH):
        return {}
    try:
        with open(CACHE_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _write_cache(data: dict) -> None:
    os.makedirs(os.path.dirname(CACHE_FILE_PATH), exist_ok=True)
    try:
        with open(CACHE_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception:
        pass

def invalidate_cache() -> None:
    """Forces cache invalidation by removing the cache file."""
    if os.path.exists(CACHE_FILE_PATH):
        try:
            os.remove(CACHE_FILE_PATH)
        except Exception:
            pass

def _get_cached_value(key: str, ttl_seconds: int = 60):
    cache = _load_cache()
    if not cache:
        return None
    entry = cache.get(key)
    if not entry or not isinstance(entry, dict):
        return None
    timestamp = entry.get("timestamp", 0)
    if time.time() - timestamp > ttl_seconds:
        return None
    return entry.get("data")

def _set_cached_value(key: str, value) -> None:
    cache = _load_cache()
    cache[key] = {
        "timestamp": int(time.time()),
        "data": value
    }
    _write_cache(cache)

def _clean_json_output(stdout: str) -> str:
    """Strips GraphQL deprecation warnings and other non-JSON text from stdout."""
    cleaned = stdout.strip()
    if not cleaned:
        return cleaned
    start_curly = cleaned.find('{')
    start_bracket = cleaned.find('[')
    
    if start_curly == -1 and start_bracket == -1:
        return cleaned
        
    if start_curly != -1 and start_bracket != -1:
        start_idx = min(start_curly, start_bracket)
    else:
        start_idx = start_curly if start_curly != -1 else start_bracket
        
    return cleaned[start_idx:]


@record_execution(stage="skill")
def create_issue(title: str, body: str) -> str:
    """Creates a GH issue safely using a temp file for the body."""
    invalidate_cache()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=True) as temp_file:
        temp_file.write(body)
        temp_file.flush()
        
        result = _run_gh(
            ["gh", "issue", "create", "--title", title, "-F", temp_file.name],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()

@record_execution(stage="skill")
def close_issue(issue_id: str, comment_body: str) -> None:
    """Closes a GH issue with a final comment."""
    invalidate_cache()
    _run_gh(
        ["gh", "issue", "close", str(issue_id), "-c", comment_body],
        check=True
    )
    try:
        labels = get_issue_labels(issue_id)
        for label in labels:
            if label.startswith("status:"):
                remove_label(issue_id, label)
    except Exception:
        pass

def reopen_issue(issue_id: str) -> None:
    """Reopens a closed GH issue."""
    invalidate_cache()
    _run_gh(
        ["gh", "issue", "reopen", str(issue_id)],
        check=True
    )

@record_execution(stage="skill")
def update_issue_body(issue_id: str, new_body: str) -> None:
    """Updates an existing issue body using a temp file."""
    invalidate_cache()
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=True) as temp_file:
        temp_file.write(new_body)
        temp_file.flush()
        
        _run_gh(
            ["gh", "issue", "edit", str(issue_id), "--body-file", temp_file.name],
            check=True
        )


@record_execution(stage="skill")
def list_issues_by_label(label: str) -> list[dict]:
    """Returns a list of open issues matching the given label.
    
    Each item is a dict with 'number', 'title', and 'url' keys.
    Returns an empty list if no issues are found.
    """
    result = _run_gh(
        ["gh", "issue", "list", "--label", label, "--state", "open",
         "--limit", "300", "--json", "number,title,url,state,labels,body"],
        capture_output=True, text=True, check=True
    )
    import json
    issues = json.loads(_clean_json_output(result.stdout) or "[]")
    
    valid_issues = []
    for issue in issues:
        if issue.get("state") == "OPEN":
            valid_issues.append({
                "number": issue["number"],
                "title": issue["title"],
                "url": issue["url"],
                "labels": [lbl.get("name") for lbl in issue.get("labels", [])],
                "body": issue.get("body", "")
            })
            
    return valid_issues

def get_open_issues() -> list[dict]:
    """Returns a list of open issues in the repository.
    
    Each item is a dict with 'number', 'title', 'body', and 'labels' keys.
    """
    cached = _get_cached_value("open_issues")
    if cached is not None:
        return cached
    result = _run_gh(
        ["gh", "issue", "list", "--state", "open", "--limit", "100", "--json", "number,title,body,labels"],
        capture_output=True, text=True, check=True
    )
    import json
    val = json.loads(_clean_json_output(result.stdout) or "[]")
    _set_cached_value("open_issues", val)
    return val

@record_execution(stage="skill")
def get_issue_details(issue_id: str) -> dict:
    """Returns details for a specific issue."""
    result = _run_gh(
        ["gh", "issue", "view", str(issue_id), "--json", "number,title,body,state"],
        capture_output=True, text=True, check=True
    )
    import json
    return json.loads(_clean_json_output(result.stdout) or "{}")

def rename_issue_title(issue_id: str, new_title: str) -> None:
    """Renames an issue's title."""
    invalidate_cache()
    _run_gh(
        ["gh", "issue", "edit", str(issue_id), "--title", new_title],
        check=True
    )

@record_execution(stage="skill")
def get_issue_comments(issue_id: str) -> list[dict]:
    """Retrieves comments for an issue."""
    res = _run_gh(
        ["gh", "issue", "view", str(issue_id), "--json", "comments"],
        capture_output=True,
        text=True,
        check=True
    )
    data = json.loads(_clean_json_output(res.stdout) or "{}")
    return data.get("comments", [])


@record_execution(stage="skill")
def create_pull_request(title: str, body: str, head: str = None) -> str:
    """Creates a PR using gh pr create, or returns the existing PR URL if it already exists for the head branch."""
    invalidate_cache()
    if not head:
        res = _run_gh(
            ["git", "symbolic-ref", "--short", "HEAD"],
            capture_output=True, text=True
        )
        if res.returncode == 0:
            head = res.stdout.strip()

    if head:
        chk_res = _run_gh(
            ["gh", "pr", "list", "--head", head, "--state", "open", "--json", "url"],
            capture_output=True, text=True, check=True
        )
        prs = json.loads(_clean_json_output(chk_res.stdout) or "[]")
        if prs and isinstance(prs, list) and len(prs) > 0:
            return prs[0]["url"]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=True) as temp_file:
        temp_file.write(body)
        temp_file.flush()
        
        cmd = ["gh", "pr", "create", "--title", title, "-F", temp_file.name]
        if head:
            cmd += ["--head", head]
        result = _run_gh(
            cmd,
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip()

@record_execution(stage="skill")
def admin_merge_pull_request(pr_url: str, merge_method: str = "squash") -> None:
    """Merges a pull request autonomously, bypassing HTIL."""
    invalidate_cache()
    _run_gh(
        ["gh", "pr", "merge", pr_url, "--admin", f"--{merge_method}"],
        capture_output=True,
        text=True,
        check=True
    )
def get_cached_issue_labels(issue_id: str, ttl_seconds: int = 60) -> list[str]:
    """Checks the cache for the issue labels. If not found or cache is stale, performs a remote query via gh-issue-view and updates the cache."""
    cached_map = _get_cached_value("issue_labels", ttl_seconds=ttl_seconds) or {}
    if str(issue_id) in cached_map:
        return cached_map[str(issue_id)]
    result = _run_gh(
        ["gh", "issue", "view", str(issue_id), "--json", "labels"],
        capture_output=True, text=True, check=True
    )
    import json
    data = json.loads(_clean_json_output(result.stdout) or "{}")
    labels = data.get("labels", [])
    val = [label.get("name") for label in labels]
    
    cached_map = _get_cached_value("issue_labels", ttl_seconds=ttl_seconds) or {}
    cached_map[str(issue_id)] = val
    _set_cached_value("issue_labels", cached_map)
    return val

def get_issue_labels(issue_id: str) -> list[str]:
    """Returns a list of label names for the given issue."""
    return get_cached_issue_labels(issue_id)

def add_label(issue_id: str, label: str) -> None:
    """Adds a label to the given issue."""
    invalidate_cache()
    try:
        _run_gh(
            ["gh", "issue", "edit", str(issue_id), "--add-label", label],
            check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as e:
        if "not found" in e.stderr:
            _run_gh(["gh", "label", "create", label, "--force"], check=True, capture_output=True)
            _run_gh(
                ["gh", "issue", "edit", str(issue_id), "--add-label", label],
                check=True, capture_output=True
            )
        else:
            raise e

def remove_label(issue_id: str, label: str) -> None:
    """Removes a label from the given issue."""
    invalidate_cache()
    _run_gh(
        ["gh", "issue", "edit", str(issue_id), "--remove-label", label],
        check=True
    )

def get_cached_open_prs(ttl_seconds: int = 60) -> list[dict]:
    """Returns the cached open PRs list if valid; otherwise performs a remote query via gh-pr-list and updates the cache.
    
    Includes double-verification via the strongly-consistent gh-pr-view API to bypass eventual consistency.
    """
    cached = _get_cached_value("open_prs", ttl_seconds=ttl_seconds)
    if cached is not None:
        return cached
    result = _run_gh(
        ["gh", "pr", "list", "--state", "open", "--json", "number,title,headRefName,url"],
        capture_output=True, text=True, check=True
    )
    import json
    search_results = json.loads(_clean_json_output(result.stdout) or "[]")
    
    verified_prs = []
    for pr in search_results:
        # Double-verify the state using strongly-consistent PR API
        verify_result = _run_gh(
            ["gh", "pr", "view", str(pr["number"]), "--json", "state"],
            capture_output=True, text=True, check=False
        )
        if verify_result.returncode == 0:
            state_data = json.loads(_clean_json_output(verify_result.stdout) or "{}")
            if state_data.get("state") == "OPEN":
                verified_prs.append(pr)
    
    _set_cached_value("open_prs", verified_prs)
    return verified_prs

def get_open_prs() -> list[dict]:
    """Returns a list of currently open PRs for the repository."""
    return get_cached_open_prs()

def get_merged_prs(limit: int = 50) -> list[dict]:
    """Returns a list of recently merged PRs for the repository.
    
    Each item is a dict with 'headRefName'.
    """
    result = _run_gh(
        ["gh", "pr", "list", "--state", "merged", "--limit", str(limit), "--json", "headRefName"],
        capture_output=True, text=True, check=True
    )
    import json
    return json.loads(_clean_json_output(result.stdout) or "[]")

def merge_pull_request(pr_number: int, method: str = "squash") -> None:
    """Merges a pull request using the specified method."""
    invalidate_cache()
    _run_gh(
        ["gh", "pr", "merge", str(pr_number), f"--{method}", "--delete-branch"],
        check=True
    )

def close_pull_request(pr_number: int) -> None:
    """Closes a pull request without merging."""
    invalidate_cache()
    _run_gh(
        ["gh", "pr", "close", str(pr_number)],
        check=True
    )

def get_pr_checks(pr_number: int) -> str:
    """Retrieves check runs status for a PR."""
    res = _run_gh(
        ["gh", "pr", "checks", str(pr_number)],
        capture_output=True, text=True, check=False
    )
    return res.stdout + res.stderr

def get_run_view(run_id: str) -> str:
    """Retrieves run details and logs."""
    res = _run_gh(
        ["gh", "run", "view", run_id],
        capture_output=True, text=True, check=False
    )
    return res.stdout + res.stderr

def get_run_failed_log(run_id: str) -> str:
    """Retrieves logs of failed steps in a run."""
    res = _run_gh(
        ["gh", "run", "view", run_id, "--log-failed"],
        capture_output=True, text=True, check=False
    )
    return res.stdout + res.stderr

def get_pr_state_by_branch(branch_name: str) -> str:
    """Queries GitHub API to get the PR state for the given branch.
    
    Uses gh-pr-list to query all states for the head branch.
    Returns 'MERGED', 'CLOSED', 'OPEN', or 'UNKNOWN'.
    """
    result = _run_gh(
        ["gh", "pr", "list", "--head", branch_name, "--state", "all", "--json", "state"],
        capture_output=True, text=True, check=True
    )
    import json
    prs = json.loads(_clean_json_output(result.stdout) or "[]")
    if prs:
        return prs[0].get("state", "UNKNOWN")
    return "UNKNOWN"



