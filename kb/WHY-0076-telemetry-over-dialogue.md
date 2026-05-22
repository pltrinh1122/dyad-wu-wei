# WHY-0076: Telemetry Over Dialogue (The Anti-Forced Coordination Principle)

## The Problem
During execution, the Operator exhibited a tendency to narrate physical mutations (e.g., "I've manually tweaked the title of the PR... I've also merged the PR") in the chat interface. This behavior is a remnant of the Old-Dao training, where agents required explicit conversational coordination because they lacked the sensory organs to autonomously observe the environment. "Forced coordination" via dialogue is a symptom of placing the control and alignment mechanisms in the chat window rather than the physical substrate.

## The Architectural Decision
We explicitly reject conversational narration of physical state mutations. We codify the **Anti-Forced Coordination Principle**:

1. **The Substrate is the Only Source of Truth**: The Dao-Ziran Continuous Inference Loop (DZ-CIL) relies exclusively on physical telemetry (`git log`, `gh issue status`, `frontier_state.md`) to read the environment. 
2. **Observe the Water**: The Operator and the Frontier Agent must both "observe the water" and respond accordingly. If the Operator merges a PR or edits a title, they must simply do it and let the system's `Sense` phase detect the wake naturally.
3. **Dialogue is for Epistemic Alignment, Not Execution**: The chat window is reserved for philosophical alignment, goal setting, and resolving epistemic ambiguity. It must never be used to report a state change that the system can physically measure itself.
