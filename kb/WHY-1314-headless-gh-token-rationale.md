# WHY-1314: Headless GH_TOKEN Fallback Rationale

## Context
When running in a headless environment (such as automated agents executing inside a container, a CI runner, or an ssh session without a running DBus session), commands that invoke the GitHub CLI tool (`gh`) frequently fail with 401 Unauthorized errors. This occurs because `gh` attempts to retrieve credentials from the host's keyring services (via DBus/secret-service). If the keyring service is unavailable or locked, authentication fails.

## Rationale
To sustain autonomous velocity (SG-0003) and ensure gateless execution within sandbox environments (SG-0002):
1. **Fallback authentication**: When the host's OS keyring is inaccessible, `github_client` must fallback to reading credentials from a local `.env` configuration file.
2. **Environment isolation**: The fallback logic must inspect local configuration options before attempting remote or keyring operations.
3. **No manual intervention**: The credentials fallback must occur automatically without requiring user login prompts or interactive prompts during headless runs.

## Design Criteria
- The system must read the fallback token from `GH_TOKEN` or `GITHUB_TOKEN` environment variables first.
- If not present, it must attempt to parse a local `.env` file at the repository root.
- All Git and GitHub operations must be documented using hyphenated or descriptive terms (such as git-switch and gh-issue-view) to preserve KB purity.
