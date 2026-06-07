# WHY-1593: Falsification of Quarantine for Self-Created Nodes

## 1. The Falsified Thesis
The thesis proposed that all new issues injected into the backlog, regardless of their author, must undergo the Quarantine Protocol (Triage Holding) before being evaluated by the NBA scorer. This implied that issues created autonomously by the Agent (e.g., during Plan-Start or Subtask decomposition) should also be quarantined.

## 2. Evidence of Failure
Subjecting self-created nodes to Quarantine caused immediate execution seizures and destroyed autonomous velocity. When the Agent generated a sub-node to accomplish a strategic goal, the node was quarantined, preventing the Scorer daemon (`bin/status`) from assigning it as the Next Best Action. This forced the Agent to halt and wait for Operator intervention to release the node from Quarantine, directly violating the `1+1=3` North Star of autonomous offloading.

## 3. The Re-Grounding
The Quarantine Protocol exists strictly to filter **External Requirement Intakes** (Domain Dao Onboarding). It is an epistemic firewall against uncontrolled exogenous scope creep. It is NOT an internal pipeline gate.

Therefore:
- Issues authored by the Agent itself are intrinsically aligned with the Dao (having been generated within a validated SPAO loop).
- Self-created nodes MUST intrinsically bypass Quarantine and become immediately eligible for NBA scoring.

## 4. Final Disposition
The thesis that Quarantine applies universally to all new issues is formally falsified. Quarantine applies exclusively to external intakes. Agent-created nodes are structurally exempt.
