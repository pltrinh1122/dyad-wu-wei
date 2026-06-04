# WHAT-0295: Bin Executable Metadata Guard

## 1. Intent
To enforce the integrity of the agentic CLI execution surface (`bin/*` scripts), we must guarantee that all wrapper scripts remain executable (`+x`). If a script loses its executable bit (e.g. through a bad git transaction, manual copy, or operating system file transfer), the engine loops will fail to invoke them, causing hard crashes.

## 2. Rationale
The engine heavily relies on `subprocess.run` calling `./bin/node`, `./bin/status`, etc. A regression in file permissions will break the primary SPAO state machine. A deterministic test (metadata guard) is required to fail local CI immediately if the executable bits are lost, preventing broken changes from being reflected to `main`.

## 3. Implementation Specification
File: `tests/test_bin_executable.py`
Target: A new pytest module that iterates through `bin/` and asserts `os.access(filepath, os.X_OK)` is `True` for all files.

```python
import os
import glob

def test_bin_scripts_are_executable():
    bin_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "bin")
    bin_files = glob.glob(os.path.join(bin_dir, "*"))
    
    assert len(bin_files) > 0, "No files found in bin directory"
    
    for bin_file in bin_files:
        if os.path.isfile(bin_file):
            assert os.access(bin_file, os.X_OK), f"File {bin_file} is missing the executable bit (+x)"
```

## 4. Testing & Validation
- Run `spao test` (or `./bin/run-tests`). 
- The new test MUST pass against the current repository state.
