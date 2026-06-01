# WHY-1606: PR and Node ID Conflation Falsification

## The Conflation
Historically, the Agent conflated PR IDs with Node IDs because GitHub issues and pull requests share the same global ID sequence. When the system reported `Cannot plan node #Y because there are open pull requests: [X]`, the Agent would incorrectly interpret `X` as a Node ID, rather than a Pull Request ID.

## Falsification
We formally falsify the **PR/Node ID Equivalency Thesis**.
1. **Distinct Abstractions**: A Node ID represents a Strategic Graph planning entity (an Issue). A PR ID represents a physical code integration transaction. They are structurally decoupled.
2. **Namespace Sharing**: While they share the GitHub ID sequence, they must be explicitly differentiated in system logs and agent reasoning.

## Remediation (Survivor Deep Ingraining)
To deep-ingrain this remediation into the system's survivor architecture:
1. All `WIP-N=1 Invariant Violation` interception blocks (e.g. in `kernel/node_lifecycle.py`) are explicitly formatted to emit the `headRefName` alongside the PR number. For example: `PR #1601 (branch: node/1600-survivor)`.
2. This ensures the Agent explicitly reads the `node_id` from the branch name rather than erroneously projecting the PR number as the Node ID.
