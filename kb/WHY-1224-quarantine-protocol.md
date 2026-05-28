# WHY-1224: Quarantine Protocol for External Requirement Intakes

## 1. Context & Problem Statement
When external entities (such as other human operators or agent dyads like the Healer) submit requirements directly to the repository via GitHub Issues, they bypass the local Strategic Prioritization Gate (SG-0001) and Containment Gate (SG-0002). 

Without isolation, an agent running in the repository might automatically ingest, prioritize, and execute arbitrary external requirements. This could lead to:
* Unintended codebase mutations that violate security or testing invariants.
* Path alignment drift away from the prioritizations established in `artifacts/strategic_intent.yml`.
* Cognitive overload on the Operator due to un-triageable backlog growth.

## 2. Proposed Mechanism (The Quarantine)
To preserve boundary integrity, we establish the **Quarantine Protocol**:
1. **Quarantine State**: All external intakes submitted via GitHub Issues must carry a specific label (such as `status:triage` or `status: quarantine`) or no execution labels at all.
2. **Backlog Exclusion**: The `bin/backlog list` and `bin/node sync` commands only scan and display issues that explicitly carry the `backlog` label. Quarantined issues are invisible to the active planning pipeline.
3. **Transition Enforcement Gate**: The `bin/node plan-start` and checkout routines will raise a validation exception if an operator/agent attempts to initiate a node that does not possess the `backlog` label.
4. **Promotion by Operator**: The quarantine is a one-way gate. Only the human Operator has the authority to promote an issue from `status:triage` to `backlog` by manually updating the GitHub labels.

*This alignment decision is mapped to Node 1225 for planning and Node 1226 for implementation.*
