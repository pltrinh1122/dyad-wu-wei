# WHAT-0041: Technical Specification for Auditing and Hardening Inner-Loop Test Dependencies

## Technical Design
To maintain a 100% hermetic offline testing boundary, we catalog all test files and declare their isolation level. No test file may perform live network requests.

### Catalog of Test Suite Hermeticity

All test files are mapped in the table below:

| Test File | Type | Mocking/Stubbing Mechanism | Network Status |
| :--- | :---: | :--- | :---: |
| `tests/test_audit_daemon.py` | Type A | Mocks system daemons and subprocess calls. | Hermetic |
| `tests/test_bash_wrappers.py` | Type A | Intercepted via global `stub_gh_cli` fixture in `conftest.py`. | Hermetic |
| `tests/test_frontier_editor.py` | Type A | Operates on temporary local files. | Hermetic |
| `tests/test_gh_graph_skill.py` | Type A | Stubs GraphQL API endpoints via unit mocks. | Hermetic |
| `tests/test_git_client.py` | Type A | Uses local scratch git repositories. | Hermetic |
| `tests/test_git_wrapper.py` | Type A | Stubs system-level git calls. | Hermetic |
| `tests/test_github_client.py` | Type A | Unit stubs all GitHub API responses. | Hermetic |
| `tests/test_infra_manager.py` | Type A | Stubs underlying daemons and system-level processes. | Hermetic |
| `tests/test_issue_factory.py` | Type A | Unit stubs GitHub issue generation templates. | Hermetic |
| `tests/test_lexical_guard.py` | Type A | Operates strictly on local file contents. | Hermetic |
| `tests/test_daemon_backlog.py` | Type A | Unit stubs backlog commands and GitHub interactions. | Hermetic |
| `tests/test_daemon_nba.py` | Type A | Unit stubs Next-Best-Action recommendation outputs. | Hermetic |
| `tests/test_daemon_node.py` | Type A | Unit stubs node planning and transition checks. | Hermetic |
| `tests/test_daemon_strategic.py` | Type A | Unit stubs strategic alignment checks. | Hermetic |
| `tests/test_daemon_telemetry.py` | Type A | Stubs telemetry collection and tracking files. | Hermetic |
| `tests/test_node_lifecycle.py` | Type A | Unit stubs node plan, checkout, and reflection methods. | Hermetic |
| `tests/test_path_resolver.py` | Type A | Local filesystem path resolution checks. | Hermetic |
| `tests/test_sense_hooks.py` | Type A | Unit stubs sync commands and git fetch calls. | Hermetic |
| `tests/test_telemetry_decorator.py` | Type A | Local decorator unit testing. | Hermetic |
| `tests/test_transaction.py` | Type A | Local unit tests for transactional flow states. | Hermetic |

## Technical Invariants
1. **Network-Isolated Execution**: All unit and integration tests must run successfully with no external network interfaces or live CLI calls.
2. **Catalog Integrity**: Any new test file added to the repository must be cataloged in this specification as a `Type A` (Hermetic) test before passing review.
