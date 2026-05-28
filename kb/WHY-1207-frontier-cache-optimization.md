# WHY-1207: local frontier cache optimization and lazy sync

## Context
Executing system commands like `node sync` or status checks involves communicating with the GitHub API to list open issues, PRs, and label statuses. This remote API latency slows down the inner-loop velocity (SG-0003), especially during repetitive offline checkouts and transitions.

## Rationale
To sustain maximum autonomous velocity:
1. **Lazy Synchronization**: Network-bound synchronization via the GitHub API (e.g. fetching labels or issue listings) should be deferred and performed only when transition gates explicitly require fresh remote state (e.g., during plan-start, plan-finish, or reflect).
2. **Local Cache**: Fetch results should be cached locally under `artifacts/` (or in memory) with a short time-to-live (TTL). Commands like status checks or NBA scoring can consume the local cache instead of hitting the API directly.
3. **Optimistic Sync**: When local git-branch structures and commit IDs indicate that no remote mutation has occurred since the last sync, local commands should optimistically bypass network queries.

## Design Criteria
- The local cache must be stored in a structured JSON payload in a non-tracked or selectively tracked file under the `artifacts/` directory.
- The cache must contain timestamps to enforce TTL invalidation.
- The system must remain fully functional offline when cache TTL is valid or force-offline is active.
- Git and GitHub operations must use hyphenated command descriptions (such as git-fetch and gh-issue-view) in documentation to satisfy KB purity.
