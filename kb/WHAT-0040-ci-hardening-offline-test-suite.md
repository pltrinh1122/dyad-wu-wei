# WHAT-0040: CI Hardening — Technical Specification for Hermetic Offline Test Suite Enforcement

## Technical Design
To prevent any live GitHub CLI (`gh`) calls during test execution, the testing harness is decoupled from the actual GitHub servers using a mock-first search path strategy.

```
                  +-----------------------+
                  |    pytest Session     |
                  +-----------+-----------+
                              |
                     (Injects PATH stub)
                              v
                  +-----------+-----------+
                  | PATH = tests/fixtures |
                  +-----------+-----------+
                              |
                    (Intercepts gh calls)
                              v
                  +-----------+-----------+
                  |    tests/fixtures/gh   |
                  +-----------+-----------+
                              |
                     (Matched Patterns)
                              v
             +----------------+----------------+
             |                                 |
     [Pattern Matched]                 [Pattern Unmatched]
             v                                 v
   Return Mocked JSON JSON             Return Empty Response
   & Exit 0                            & Warn to Stderr
```

## Technical Specifications

### 1. Global PATH-Injection Fixture (`tests/conftest.py`)
A pytest session-scoped, auto-use fixture must prepend `tests/fixtures/` to the `PATH` environment variable.

```python
import os
import pytest

_FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

@pytest.fixture(autouse=True, scope="session")
def stub_gh_cli():
    """Inject tests/fixtures/ into PATH at the session level to redirect all gh calls."""
    original_path = os.environ.get("PATH", "")
    os.environ["PATH"] = _FIXTURES_DIR + os.pathsep + original_path
    yield
    os.environ["PATH"] = original_path
```

### 2. Module Cleanups
All module-level implementations of `stub_gh_cli` (such as in `tests/test_bash_wrappers.py`) must be removed to avoid redundant modifications to `os.environ["PATH"]`.

### 3. Fixture Executable Specifications (`tests/fixtures/gh`)
The `tests/fixtures/gh` executable must be a valid bash/shell script with execute permissions (`chmod +x`). It must capture all input arguments and match them using case/pattern structures.

Required matched subcommand signatures:
- `issue list` with options `--state`, `--limit`, `--json`
- `issue view` with option `--json` (returning state, title, and/or body)
- `issue close`, `issue reopen`, `issue comment`, `issue edit`, `issue create`
- `pr create`, `pr list`, `pr view`
- `api graphql`
- `auth status`
