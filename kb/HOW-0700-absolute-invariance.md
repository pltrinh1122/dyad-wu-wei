# HOW-0700: Technical Plan for Absolute Invariance

## 1. Objective
This document outlines the technical mechanisms for enforcing "The Absolute Invariance of the Audit Ledger" as codified in `WHAT-0700`. The system must technologically prevent the deletion, modification, or squashing of established audit history.

## 2. Technical Directives

### 2.1. Guarding `artifacts/audit/`
- **Pre-commit / Reflection Hooks**: Ensure no commits attempt to delete or modify existing files in the `artifacts/audit/` directory. Only additions are allowed.
- **Agent Context**: Instruct the Agent in `AGENT.md` that it MUST NEVER modify existing retrospective files, and instead create new delta documents if corrections are needed.

### 2.2. Guarding the Git Graph
- **Force Push Protection**: The primary branch (`main`) MUST have branch protection rules enforced at the GitHub repository level to strictly prohibit force pushes (`git push --force` or `--force-with-lease`).
- **Squash Protection**: Branch protection rules MUST require merge commits (or rebase merges that preserve all commits). "Squash and merge" should be disabled to prevent the destruction of granular node history.

### 2.3. Dao Modification Auditing
- **Deprecation Workflow**: When updating `kb/` or `GEMINI.md`, the old logic should be preserved where necessary or explicitly documented as deprecated in a new node retrospective. The git history provides the true audit trail.

## 3. Implementation Steps
1. **Inject Directive into AGENT.md**: Add explicit language stating the Agent must not modify `artifacts/audit/*` files and must append new reflections instead.
2. **Review Repository Settings**: Document that the Operator MUST configure GitHub branch protection to block force pushes and squashes on `main`.
