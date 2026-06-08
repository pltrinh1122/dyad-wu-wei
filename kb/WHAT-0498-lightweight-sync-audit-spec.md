# WHAT-0498: Lightweight Sync Audit Spec

## 1. Technical Strategy

To implement the `WHY-0497` philosophy, the `audit_daemon.py` must support a new `--lightweight` runtime flag. When this flag is provided, the daemon will filter its rule evaluation pipeline, executing only the subset of rules marked `lightweight: true` in `infra/audit-daemon/audit_config.yml`.

The `bin/node sync` (`kernel/daemon_node.py`) command will be modified to pass this `--lightweight` flag during the SPAO loop transition, dramatically reducing latency on the hot path while maintaining critical structural integrity safeguards.

## 2. Changes to Configuration (`infra/audit-daemon/audit_config.yml`)

Modify the rule definitions in the YAML configuration to explicitly tag lightweight rules:

*   Add `lightweight: true` to structurally critical rules:
    *   `stale_pointer_check` (type: `stale_active_node`)
    *   `frontier-integrity` (type: `frontier_integrity`)
*   All other rules (e.g., `seizure_detector`, `semantic_immune_system`, `backlog_hygiene_auditor`, `pr_merged_monitor`) remain implicitly `lightweight: false` and will only execute during full (cold path) audits.

## 3. Changes to Execution Engine (`drivers/audit_daemon.py`)

Modify `main(args=None)`:

1.  **Argument Parsing**: Add `--lightweight` to `argparse` configuration.
    ```python
    parser.add_argument("--lightweight", action="store_true", help="Run only rules marked as lightweight: true")
    ```
2.  **Rule Filtering**: Before entering the execution loop, filter `rules_to_evaluate`:
    ```python
    if parsed_args.lightweight:
        rules_to_evaluate = [r for r in rules_to_evaluate if r.get("lightweight") is True]
    ```

## 4. Changes to Sync Invocation (`kernel/daemon_node.py`)

Modify `sync_and_clean_node(remote_mode: bool = True)` (approx. Line 356):

1.  Append `--lightweight` to the `audit_cmd` arguments list so that the sync process exclusively runs the fast structural tier.
    ```python
    audit_cmd.append("--lightweight")
    ```

## 5. Verification

1.  **Test Updates**: Modify or add tests in `tests/test_audit_daemon.py` to assert that `--lightweight` correctly filters rule execution based on the configuration payload.
2.  **Performance Verification**: The local execution of `bin/node sync` must exhibit lower execution latency by skipping network calls or expensive file I/O scans.
