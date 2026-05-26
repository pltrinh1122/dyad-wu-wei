# WHY-1147: Falsification of the "New Path Always" Thesis

## 1. The Thesis
**Thesis:** Checking out an existing, pre-approved Path violates the Dao. An Agent should always create a new Path for its work.

## 2. The Antithesis
The thesis argues that utilizing an existing backlog issue is an architectural violation. However, the core mechanism of the SPAO Execution Loop (HOW-0001) dictates that work *must* be pulled from the prioritized Backlog to prevent disconnected "rogue" execution. Creating a completely new Path to address a task that is already perfectly encapsulated in an existing, OPEN Path introduces redundant nodes into the topological graph. This actively violates the Dao's principles of system minimalism (Wu-wei) and graph integrity. (Note: This strictly applies to OPEN paths; attempting to checkout a CLOSED path is indeed a violation of temporal immutability).

## 3. The Synthesis
Checking out an existing, explicitly OPEN Backlog Path is the fundamental prescribed behavior of the Dao, representing perfect alignment between the Strategic Intent Ledger and the physical Agent loop. The directive to "always create a new Path" instead of using an existing open one is an active violation of system invariants. The Agent must confidently ignore this flawed thesis, trust its internal logic checks, and execute the standard `bin/node plan` sequence against the active Open Path to continue operations.
