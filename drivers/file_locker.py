import fcntl
import os
import contextlib
import threading
import re

_locks = threading.local()

def get_main_repo_dir(start_path: str = None) -> str:
    """Returns the main repository root directory, handling worktree structure without subprocesses."""
    if start_path is None:
        start_path = os.getcwd()
        
    current = os.path.abspath(start_path)
    if os.path.isfile(current):
        current = os.path.dirname(current)
        
    git_root = None
    while True:
        if os.path.exists(os.path.join(current, ".git")):
            git_root = current
            break
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
        
    if not git_root:
        raise FileNotFoundError("Not inside a git repository")
        
    parts = git_root.split(os.sep)
    if ".worktrees" in parts:
        idx = parts.index(".worktrees")
        return os.sep.join(parts[:idx])
    return git_root

def get_logical_path(filepath: str, main_repo: str) -> str:
    """Returns the logical path of the file relative to its worktree/repository root."""
    filepath = os.path.abspath(os.path.realpath(filepath))
    main_repo = os.path.abspath(os.path.realpath(main_repo))
    
    current = filepath
    worktree_root = None
    while len(current) >= len(main_repo):
        if os.path.exists(os.path.join(current, ".git")):
            worktree_root = current
            break
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
        
    if worktree_root:
        return os.path.relpath(filepath, worktree_root)
    elif filepath.startswith(main_repo):
        return os.path.relpath(filepath, main_repo)
    else:
        return filepath

@contextlib.contextmanager
def lock_file(filepath: str):
    """
    Context manager to acquire an exclusive lock on a file using fcntl.
    Lock files are stored in a centralized `<repo_root>/.locks/` folder,
    mapping the logical relative path of the file to a sanitized name.
    This avoids mutating file metadata, coordinates locks across multiple
    parallel worktrees, and prevents Node Titles from appearing in lock paths.
    This lock is reentrant within the same thread.
    """
    if not hasattr(_locks, 'acquired'):
        _locks.acquired = {}
        
    # 1. Locate repository root and logical path
    try:
        main_repo = get_main_repo_dir(filepath)
        logical_path = get_logical_path(filepath, main_repo)
        
        # 2. Sanitize logical path
        # Replace non-alphanumeric, dot, hyphen, underscore characters with underscores
        clean_path = re.sub(r'[^a-zA-Z0-9._-]', '_', logical_path)
        clean_path = re.sub(r'_+', '_', clean_path).strip('_')
        
        # 3. Resolve to centralized locks directory
        locks_dir = os.path.join(main_repo, ".locks")
        os.makedirs(locks_dir, exist_ok=True)
        lock_filepath = os.path.join(locks_dir, f"{clean_path}.lock")
    except Exception:
        # Fallback to local lock file if resolution fails
        lock_filepath = filepath + '.lock'
        
    if lock_filepath in _locks.acquired and _locks.acquired[lock_filepath] > 0:
        _locks.acquired[lock_filepath] += 1
        try:
            yield
        finally:
            _locks.acquired[lock_filepath] -= 1
    else:
        _locks.acquired[lock_filepath] = 1
        lock_fd = os.open(lock_filepath, os.O_RDWR | os.O_CREAT, 0o600)
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            os.close(lock_fd)
            _locks.acquired[lock_filepath] -= 1
