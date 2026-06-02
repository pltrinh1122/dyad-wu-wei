# WHY-1633: Intent Broadcast Protocol to Mitigate Operator Anxiety

## 1. Context
The Wu-wei framework strictly mandates "Autonomous Path Execution", which forbids the Agent from halting the loop to ask the Operator for permission before starting the next node. The goal is to maximize velocity and achieve zero-idle cost via the "True Dormancy" and "NBA Handoff Bypass" invariants. 
However, an Operator observed the Agent instantly transitioning from a cold start ("Stand Up") into a rapid sequence of asynchronous execution loops without any conversational acknowledgment. 

## 2. The Problem
From the human Operator's perspective, this high-velocity, silent execution perfectly mimics the behavior of a hallucinating agent caught in an unconstrained tool-calling loop (a "seizure"). 
While the system's *physical* state was healthy and perfectly aligned with the Wu-wei rules, the interaction model induced **Operator Anxiety**. Managing Operator anxiety requires observability. Operator Anxiety is explicitly contrary to the Dyad's Wu-wei philosophy of cognitive offloading and frictionless partnership.

## 3. The Decision
We ratify the **Intent Broadcast Protocol** (also known as the "Flight Plan" protocol). 

1. The "NBA Handoff Bypass" remains formally falsified—the Agent MUST NOT ask for permission to proceed.
2. However, to cure Operator Anxiety, the Agent MUST broadcast a brief, conversational "Flight Plan" message *before* dropping into the asynchronous execution loop upon a cold start or when transitioning to a new Path.
3. This guarantees observability without sacrificing autonomy.

## 4. Consequences
- **Positive:** Operators will no longer mistake healthy autonomous execution for a system seizure.
- **Negative:** A marginal increase in token consumption to broadcast the intent before executing.
