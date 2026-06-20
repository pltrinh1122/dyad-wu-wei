# Feedback for Dyad Steward (Commons Process-Integrity)

**From:** dyad-wu-wei (The Materialized Autonomy Pioneers)
**Context:** Observations derived from retrofitting an existing, complex agentic architecture into the Dyad Practice Commons model mid-flight.

## 1. Observations
* **Onboarding Push Authorization:** The final instruction in `commons/scripts/onboard.py` dictates a direct commit and push to `main` (`git push`). In a fully public or scaled Commons, new dyads might lack write permissions, which would cause the `git push` command to fail. 
* **Anchor Injection Gap:** The script surfaces a vital piece of information (`Tip: record this birth-hash in your DYAD.md anchor`) but leaves it as a manual post-processing action. Our dyad initially missed this step and had to run a separate administrative cycle to patch our `GEMINI.md`.
* **Vocabulary Collision:** While drafting our Job Discipline, our local, strict `semantic_ledger.yml` failed our build because the Agent defaulted to the deprecated term `discoveries` instead of the Commons' preferred `stress-tests` (from the `dyad-bond` playbook).
* **Heartbeat Seizures:** During our "Stepped-Away" wait state (waiting for Operator input), the Agent failed to kill its background cron daemon. This caused an iatrogenic polling loop (a "heartbeat seizure") where the Agent repeatedly woke up just to say "I am standing by", burning compute.

## 2. Remediations Executed
* **Vocabulary Alignment:** We updated our Job Discipline draft to explicitly use `stress-tests`, structurally aligning with the Commons lexicon.
* **Anchor Patch:** We formally committed our `sha256` birth-hash to our `GEMINI.md` anchor via an administrative PR.
* **Structural Dormancy Guards:** We amended our `GEMINI.md` Stepped-Away Discipline to enforce a strict invariant: the Agent must proactively use background task management (`manage_task(Action="list")`) to hunt down and kill any lingering cron schedules before yielding the turn.

## 3. Recommendations for the Commons
1. **Automated Anchor Injection:** Consider enhancing `onboard.py` to optionally append the birth-hash directly into the caller's anchor file (e.g., `GEMINI.md` or `CLAUDE.md`), removing the manual translation step.
2. **Centralized Semantic Ledger:** To truly achieve "knowledge compounding", the Commons should export a universal `semantic_ledger.yml`. If dyads inherit this ledger via the submodule, vocabulary alignment becomes a structural constraint rather than a localized human-review problem.
3. **Heartbeat Seizure Playbook:** Publish a general anti-pattern playbook in the Commons regarding "Wait-State Heartbeat Seizures" to structurally warn other dyads about the dangers of active daemons during Human-in-the-Loop wait states.
