# WHAT-1399: Epistemic Retrospective Synthesis - Node 1398

## 1. Intent
To formally synthesize the epistemic learning derived from the `retro-1398.md` post-failure retrospective, ensuring that the system's operational guidelines robustly protect against similar lexical guard failures in the future.

## 2. Context
During the Dyad Practice harmonization task (Node 1398), the agent inserted generative content that contained deprecated ontology (`align` and `dao`). This triggered a Lexical Guard failure during the testing phase because the agent did not proactively cross-reference the generated text with the terms cataloged in `kb/semantic_ledger.yml`.

## 3. Specification
- **The Generative Invariant**: Agents engaged in generative content creation, structural documentation, or template updates must perform a mandatory pre-flight cross-reference against `kb/semantic_ledger.yml`.
- **Lexical Tracing**: A Lexical Guard violation during the local testing phase is considered a definitive symptom of a failure to map generated text to the system's active ontology.
- **System Integration**: This invariant has been integrated into `HOW-0005-terminology-lifecycle.md` under the Wu-wei Execution Loop to explicitly mandate the mapping behavior before the test harness phase is reached.

## 4. Evaluation
- Test suites (`test_lexical_guard.py`) will automatically enforce this invariant by blocking the reflection of nodes that contain deprecated terms.
- The `HOW-0005` integration completes the synthesis loop for this retrospective.
