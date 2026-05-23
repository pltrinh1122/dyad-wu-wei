# WHAT-0093: Decouple Prompt Backlog from Git Tracking Specification

## Context
The operator prompt backlog (`artifacts/prompt_backlog.yml`) stores operator instructions asynchronously. When tracked by Git, it gets reset by branch operations or workspace cleaning, leading to lost instructions. Furthermore, concurrent branches can cause git conflicts.

## Specification
The operator prompt backlog must be decoupled from the Git repository index.

### 1. Git Index Exclusion
- The file `artifacts/prompt_backlog.yml` and its lock file `artifacts/prompt_backlog.yml.lock` must be removed from Git tracking.
- The patterns `artifacts/prompt_backlog.yml` and `artifacts/prompt_backlog.yml.lock` must be added to the repository root `.gitignore` file.

### 2. Auto-Initialization
- The prompt daemon must handle cases where the backlog file does not exist.
- When loading prompts, the daemon must return a default empty list if the file is absent.
- When adding a prompt, the daemon must ensure the target directory and file are created and initialized.
- Status verification checks must gracefully return 0 pending prompts if the file is absent, rather than throwing errors.
