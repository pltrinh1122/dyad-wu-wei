# WHAT-1315: Headless GH_TOKEN Fallback Specification

## Specification
The credentials lookup protocol inside the GitHub client adapter must implement an automated fallback mechanism:

1. **Environment lookup**:
   Check if `GH_TOKEN` or `GITHUB_TOKEN` is present in the current environment dictionary. If so, use them directly.

2. **File lookup**:
   If neither environment variable is set, check for a local `.env` file at the repository root.
   If the `.env` file is present, parse it to extract the value for `GH_TOKEN` or `GITHUB_TOKEN`.
   
3. **Subprocess execution environment**:
   Inject the extracted token into the environment dictionary of the executed subprocess (such as gh-commands or git-commands).

## Implementation Details
The helper function `_run_gh` in `drivers/github_client.py` is updated to implement this protocol before invoking any remote-bound processes.

All Git and GitHub integration references in documentation must use hyphenated terminology (such as git-checkout and gh-pr-list).
