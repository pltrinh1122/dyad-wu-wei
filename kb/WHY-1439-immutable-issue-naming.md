# WHY-1439: Immutable Issue and PR Naming Convention

## 1. Intent
This document establishes the invariant naming conventions for GitHub Issues and Pull Requests within the Wu-wei Dyad autonomous framework. The goal is to eliminate duplicate ID numbering, leverage GitHub as the sole source of truth for identification, and explicitly differentiate Issues from PRs.

## 2. Context & The Bug (Node 1429 Falsification)
Previously, when the Orchestrator utilized the issue factory (`daemon_backlog`), it attempted to proactively embed predictive Node IDs into the issue titles (e.g., generating `Activity 1430: Activity 1429: Implement...`). This generated two failure modes:
1. **Duplicate Identifiers**: It caused title pollution and duplicate identifiers if GitHub's assigned ID diverged from the predicted/input ID.
2. **Issue/PR Ambiguity**: Because PR titles were identical to the underlying Issue title, it became difficult to distinguish between the PR and the Issue in CI/CD feeds and issue logs.

## 3. The Invariant Guardrails
To mathematically resolve these ambiguities, the following two naming pipelines are strictly enforced:

### Invariant 1: De-coupling Issue Title Generation from Predictive ID Mapping
The issue generation script (`drivers/issue_factory.py` / `kernel/daemon_backlog.py`) MUST NOT append or predict Issue IDs in the issue title.
- **Rule**: GitHub Native ID is the single source of truth.
- **Enforcement**: Issue titles are strictly generated as `[Node Type]: [Title]` (e.g., `Activity: Implement XYZ`). The ID is naturally appended by GitHub's UI (`#1439`). The system will actively regex-strip any erroneously provided ID prefixes during the backlog creation phase.

### Invariant 2: Explicit PR Title Differentiation
The execution reflection cycle (`kernel/node_lifecycle.py`) MUST explicitly prefix Pull Request titles to differentiate them from the source Node.
- **Rule**: A Pull Request title MUST be prefixed with `PR for Node [Issue ID]: ` followed by the Node name.
- **Example**: `PR for Node 1439: Activity: Refactor Naming Conventions`.
- **Enforcement**: This is enforced inside the `reflect` method prior to calling `github_client.create_pull_request()`.
