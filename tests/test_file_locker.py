import os
import threading
import time
import pytest
from skills import file_locker

def test_get_main_repo_dir_standard(tmp_path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    
    assert file_locker.get_main_repo_dir(str(tmp_path)) == str(tmp_path)
    
    nested = tmp_path / "subdir" / "another"
    nested.mkdir(parents=True)
    assert file_locker.get_main_repo_dir(str(nested)) == str(tmp_path)

def test_get_main_repo_dir_worktree(tmp_path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    
    wt_dir = tmp_path / ".worktrees" / "node" / "123-some-activity"
    wt_git = wt_dir / ".git"
    wt_git.mkdir(parents=True)
    
    assert file_locker.get_main_repo_dir(str(wt_dir)) == str(tmp_path)

def test_get_main_repo_dir_not_in_git(tmp_path):
    with pytest.raises(FileNotFoundError):
        file_locker.get_main_repo_dir(str(tmp_path))

def test_get_logical_path(tmp_path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    
    main_repo = str(tmp_path)
    filepath = str(tmp_path / "skills" / "some_file.py")
    assert file_locker.get_logical_path(filepath, main_repo) == os.path.join("skills", "some_file.py")

def test_get_logical_path_worktree(tmp_path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    
    wt_dir = tmp_path / ".worktrees" / "node" / "123-some-activity"
    wt_git = wt_dir / ".git"
    wt_git.mkdir(parents=True)
    
    main_repo = str(tmp_path)
    filepath = str(wt_dir / "skills" / "some_file.py")
    
    assert file_locker.get_logical_path(filepath, main_repo) == os.path.join("skills", "some_file.py")

def test_lock_file_sanitization(tmp_path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    
    test_file = tmp_path / "some@invalid#name.txt"
    with file_locker.lock_file(str(test_file)):
        expected_lock = tmp_path / ".locks" / "some_invalid_name.txt.lock"
        assert expected_lock.exists()

def test_lock_file_fallback(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.touch()
    
    with file_locker.lock_file(str(test_file)):
        expected_lock = tmp_path / "test.txt.lock"
        assert expected_lock.exists()

def test_lock_file_reentrancy(tmp_path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    
    test_file = tmp_path / "test.txt"
    
    with file_locker.lock_file(str(test_file)):
        with file_locker.lock_file(str(test_file)):
            pass

def test_lock_file_concurrency(tmp_path):
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    
    test_file = tmp_path / "test.txt"
    test_file.touch()
    
    events = []
    
    def worker():
        with file_locker.lock_file(str(test_file)):
            events.append("acquired")
            time.sleep(0.1)
            events.append("releasing")
            
    with file_locker.lock_file(str(test_file)):
        t = threading.Thread(target=worker)
        t.start()
        time.sleep(0.05)
        events.append("main_held")
        
    t.join()
    assert events == ["main_held", "acquired", "releasing"]
