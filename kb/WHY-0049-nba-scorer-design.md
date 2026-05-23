# WHY-0049: NBA Scorer Implementation Design

## 1. Interface Design

The scoring engine will be implemented in `kernel/nba_scorer.py` under the class `NBAScorer`. 

```python
class NBAScorer:
    def __init__(self, frontier_file: str = "artifacts/frontier_state.md"):
        self.frontier_file = frontier_file

    def calculate_score(self, node_id: str) -> dict:
        """
        Computes the NBA score for a given node.
        Returns a dict containing:
          - "node_id": str
          - "score": float (0.00 to 1.00)
          - "components": {
              "dependency": float,
              "axiom": float,
              "strategic": float,
              "risk": float
            }
        """
        ...
```

## 2. Component Scoring Logic

### 2.1. Dependency Gate ($C_{\text{Dependency}}$)
* The scorer queries the GitHub API for the node's dependencies listed in the issue body.
* If any dependent issue is not `CLOSED`, this component is `0.0`. Otherwise `1.0`.

### 2.2. Axiomatic Compliance ($C_{\text{Axiom}}$)
* Checks if working directory is clean or matches isolation standards.
* Nodes that follow standard lifecycle receive `1.0`. Nodes attempting direct main commits receive `0.0`.

### 2.3. Strategic Alignment ($C_{\text{Strategic}}$)
* Scans `artifacts/strategic_intent.yml` (the active strategic ledger).
* If the node's parent path is prioritized, it receives `1.0`.
* If the path is in the backlog but not prioritized, it receives `0.5`.
* Otherwise, `0.0`.

### 2.4. Operational Risk ($C_{\text{Risk}}$)
* Evaluates risk based on file lock markers or changes to global `kb/` rules.
* Safe, isolated leaf nodes receive `1.0`. Global system modifications receive `0.5` or `0.0`.

## 3. CLI Integration

We will expose the scorer via:
* Direct integration into `./bin/node sync` to output the score of recommended actions.
* A scoring report script that allows querying specific nodes.
