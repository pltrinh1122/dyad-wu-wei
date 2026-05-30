# Retrospective: Node 930 Specification Clarification

## Context & Correction
During the review of the Node 930 installer specification, the Operator clarified that the installer-spec must be more explicit regarding its baseline assumptions:
1. **Prerequisite Core Retrieval**: The spec did not explicitly state that the Operator must first fetch or clone the core `dyad-wu-wei` engine repository from GitHub before executing the installer.
   - *Resolution*: Updated the installer specification `kb/WHAT-0930-dyad-wu-wei-installer-spec.md` to add an explicit "Assumptions & Prerequisites" section.

## Codified Insight
1. **Explicit Operational Assumptions**: All bootstrap and installer specifications must document the prerequisite manual setup (such as cloning the core runtime and configuring paths) to eliminate environmental ambiguity and align expectations between Operator and Agent.
