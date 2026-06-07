# Alignment Contract: Codify The Void of the Metasystem

## Philosophical Stance
1. **The Void**: The Metasystem (agent-meta) is an agnostic executor pipeline. It operates in "The Void", completely unaware of the specific payload it is processing.
2. **Agnostic Payloads**: Whether a node is refactoring python code, writing markdown documentation, or planning a strategic roadmap, the Metasystem's SPAO loop (`status -> plan -> checkout -> act -> reflect`) remains identical and ignorant of the context.
3. **Decoupling**: The engine must never inspect the payload to alter its state machine. If the state machine forks its behavior based on the content of the repository (e.g., "if this is a docs PR, skip testing"), it violates The Void.

## Conclusion
The engine is a dumb, perfectly reliable conveyor belt. The intelligence and context are entirely contained within the payload (the issue descriptions and the agent prompts).
