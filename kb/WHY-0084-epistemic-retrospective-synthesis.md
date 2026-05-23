# WHY-0084: Epistemic Retrospective Synthesis

## Meta-Architecture
**Domain:** Knowledge Accrual  
**Scope:** Retrospective Synthesis and Terminal Output  
**Enforced By:** Node 810 (Alignment)  

## The Epistemic Gap
Under SG-0005 (The Meta-Learning Imperative), agents are forced to generate fragmented `retro-*.md` artifacts whenever they encounter a test failure or execution block. These files are correctly stored in `artifacts/audit/`. However, reading them individually places a high cognitive burden on the Operator. The artifacts are piece-meal, and the lessons they contain are isolated in the file system rather than surfaced actively during development cycles. 

## The Synthesis Imperative
To close the loop on SG-0005 and align with the Synergistic Human-Agent Partnership (SG-0002), we must implement a deterministic, low-latency mechanism to aggregate and synthesize these learnings. The Operator should not be required to go digging for systemic issues. The system must present its synthesized lessons proactively.

We align on the following architectural capability:
1. **The Aggregation Mechanism (`bin/node retro`)**: We will introduce a new CLI command that specifically targets un-synthesized `retro-*.md` files.
2. **Terminal Summarization**: The command will output a synthesized CLI view showing the top recurring structural lessons grouped by semantic similarity (e.g., "Mock Patching Oversights", "Git Conflict Patterns").
3. **Knowledge Base Mutation**: The synthesized insights will be injected directly into a dedicated primitive (e.g. `artifacts/operational_insights.md`) to serve as a high-density, centralized ledger of Agentic failures and corrections.

## Alignment Outcome
By consolidating piece-meal retrospectives into grouped, structural lessons, we relieve the Operator of manual synthesis. This ensures that the system's failures actively shape its future execution policies, accelerating the velocity of inner-loop corrections.
