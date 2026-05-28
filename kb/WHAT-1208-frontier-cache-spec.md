# WHAT-1208: local frontier cache specification

## Cache File Location
The cached state will be persisted in JSON format at:
`artifacts/cache/github_state_cache.json`

## Cache Payload Schema
```json
{
  "timestamp": 1782547200,
  "ttl_seconds": 60,
  "open_prs": [
    {
      "number": 1231,
      "title": "Example PR Title",
      "headRefName": "node/1230-document-intake-readme",
      "url": "https://github.com/pltrinh1122/dz-cil/pull/1231"
    }
  ],
  "open_issues": [
    {
      "number": 1208,
      "title": "Example Issue Title",
      "body": "Issue Body...",
      "labels": ["status:active", "backlog"]
    }
  ],
  "issue_labels": {
    "1208": ["status:active", "backlog"]
  }
}
```

## interface for Cache Checks in `github_client`
1. `get_cached_open_prs()`: Checks if the cache exists and the timestamp is within `ttl_seconds`. If valid, returns the cached list. Otherwise, triggers a remote check and updates the cache.
2. `get_cached_issue_labels(issue_id)`: Checks the cache for the issue labels. If not found or cache is stale, performs a remote query and updates the cache.
3. `invalidate_cache()`: Programmatically forces cache invalidation, forcing subsequent reads to perform live remote queries.

All Git and GitHub integrations must use hyphenated terminology (such as git-checkout and gh-pr-list) in documentation.
