# WHY-0051: Runtime Path Scoring CLI Design

## 1. CLI Commands & Options

We will implement path scoring as a new command in the runtime orchestrator `orchestrator/mgr_rt.py`.

```python
def score_paths(start_id: str = None, end_id: str = None):
    """
    Computes NBA score details for paths.
    If start_id and end_id are provided:
      Scores all Path issues between start_id and end_id (inclusive).
    Else:
      Scores all open Path issues in the backlog.
    """
    ...
```

This logic will be exposed via the command `./bin/rt score-paths`:
* Option `--start`: start issue ID.
* Option `--end`: end issue ID.

## 2. Calculation and Reporting Logic

1. Query all issue numbers matching the criteria (either open backlog paths, or paths in the inclusive range `[start_id, end_id]`).
2. Run `NBAScorer.calculate_score` on each path.
3. Generate a Markdown table summarizing the results with columns:
   * **Path**
   * **Score**
   * **Dependency Component**
   * **Axiom Component**
   * **Strategic Component**
   * **Risk Component**
4. Print the total sum of all scores.
5. Print references to the scoring methodology and mathematical rubrics.
