## Goal
Anchor the process invariant in DYAD.md to always ground with the remote repo before asserting PR status.

## Meta-Index

## Agent Retrospective

### Continue
- Utilizing targeted bugfix PRs for systemic issues (like the github_client.py fix) alongside process governance updates.
- Following the SPAOR transaction rollbacks closely to preserve state integrity.

### Stop
- Relying on implicit `gh` repository resolution without an active SPAO workspace directory in root contexts.

### Start
- Enforcing explicit repository contexts for `gh` commands across all execution boundaries.
