# WHAT-0052: NBA Scoring Granularity A/B Test Plan

This document defines the experimental design, hypotheses, metrics, and execution plan for an A/B test comparing coarse and granular NBA scoring models.

## 1. Experimental Design

To evaluate whether greater scoring granularity increases prioritization discernment, we establish a controlled A/B testing environment:

* **Control Group (A)**: The coarse baseline scoring engine (current `NBAScorer`).
* **Treatment Group (B)**: An experimental scoring engine incorporating granular metrics:
  * **Strategic Value ($C_{\text{Strategic}}$)**: Refined from binary to tiered (`1.0` for prioritized active paths, `0.6` for general backlog paths matching active goals, `0.3` for others).
  * **Operational Risk ($C_{\text{Risk}}$)**: Refined from binary to a scale (`1.0` down to `0.5`) based on the complexity/count of proposed modifications.

## 2. Hypothesis Definition

* **Null Hypothesis ($H_0$)**: The granular scoring model (B) does not yield higher score differentiation or improved topological ranking compared to the coarse model (A).
  $$H_0: D_B \le D_A$$
* **Alternative Hypothesis ($H_1$)**: The granular scoring model (B) yields higher score differentiation (greater Discernment Index) and a topologically valid prioritization compared to the coarse model (A).
  $$H_1: D_B > D_A$$

## 3. Controlled Metrics

1. **Discernment Index (D)**: The standard deviation of the score distribution across all evaluated backlog paths:
   $$D = \sqrt{\frac{1}{N} \sum_{i=1}^N (S_i - \bar{S})^2}$$
   * A higher $D$ indicates greater discernment (less uniformity).
2. **Topological Feasibility**: Boolean check indicating whether the top-ranked path is free of unclosed dependencies.

## 4. Execution Plan

We will implement an automated A/B test harness (`tests/test_scoring_ab_test.py` or a CLI script) that:
1. Instantiates both scoring models.
2. Scores all open backlog paths.
3. Computes the Discernment Index ($D$) and topological feasibility for both groups.
4. Outputs the comparative results and formally accepts or rejects the null hypothesis.

## 5. Detailed Implementation Specifications

### 5.1 Strategic Value ($C_{\text{Strategic}}$) Tiered Rules
* Score = `1.0`: If the path is prioritized inside `strategic_intent.yml`.
* Score = `0.7`: If the path matches keywords associated with active strategic goals (e.g., "sandbox", "audit", "telemetry", "velocity", "gate", "knowledge", "abtest") in its title or body.
* Score = `0.3`: If no keyword match and not prioritized.

### 5.2 Operational Risk ($C_{\text{Risk}}$) Complexity Rules
* Score = `1.0`: If the path does not propose changes to any critical modules.
* Score = `0.75`: If the path proposes changes to exactly 1 critical module (e.g., `git_client`, `github_client`, `node_lifecycle`, `infra_manager`).
* Score = `0.5`: If the path proposes changes to 2 or more critical modules.

