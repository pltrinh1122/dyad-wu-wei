import fcntl
import os
import contextlib
import threading

_locks = threading.local()

@contextlib.contextmanager
def lock_file(filepath: str):
    """
    Context manager to acquire an exclusive lock on a file using fcntl.
    A separate lock file (filepath + '.lock') is used to avoid mutating the target file's metadata.
    This lock is reentrant within the same thread.
    """
    if not hasattr(_locks, 'acquired'):
        _locks.acquired = {}
        
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
