# WHY-0003: Terminal vs Non-Terminal Node Abstraction

## 1. The Phenomenon
Currently, the Antigravity system defines execution units as either `Activity` or `Probe`. While these categorizations are highly effective for task-oriented software development (SDLC), they are overly domain-specific. 

If we attempt to reuse this exact SPAO (Sense, Plan, Act, Observe, Reflect) meta-orchestration infrastructure for non-SDLC domains (e.g., `agent-travel` for booking flights or itineraries), terms like "Activity" or "Probe" break domain immersion and do not logically map to the tasks being performed (e.g., "Booking", "Investigation", "Reservation").

## 2. Graph-Theoretic Formalization
To generalize the infrastructure, we must elevate the abstraction to pure graph theory. All units of execution within a workflow graph can be categorized into two absolute base primitives:

### 2.1. Non-Terminal Nodes (Composite/Internal Nodes)
- **Definition**: A node that decomposes into smaller sub-nodes. It does not execute functional logic directly but serves as an aggregator or parent container.
- **Current Mapping**: In Antigravity, this is analogous to a `Path` (which groups multiple Activities/Probes).
- **Domain Agnostic Mapping**: In `agent-travel`, this could be a "Trip Itinerary" (e.g., "Plan trip to Japan"), which decomposes into flights, hotels, and tours.

### 2.2. Terminal Nodes (Leaf/Execution Nodes)
- **Definition**: A node that executes concrete, atomic logic and has no children. It represents a final point of execution that must be resolved.
- **Current Mapping**: In Antigravity, an `Activity` (mutates logic) or a `Probe` (investigates logic) are both just specific implementations of a Terminal Node.
- **Domain Agnostic Mapping**: In `agent-travel`, a "Flight Booking" or "Visa Investigation" are concrete Terminal Nodes.

## 3. The Base Abstraction Architecture
By re-architecting the system to recognize `TerminalNode` and `NonTerminalNode` as the fundamental base classes, we achieve ultimate reusability:

1. **The SPAO Contract is tied to the Base Node**: The SPAO loop (`bin/node plan`, `checkout`, `reflect`), locking mechanisms (GitHub Labels), and frontier state tracking apply globally to the `TerminalNode` abstraction, regardless of its domain implementation.
2. **Domain-Specific Typing**: `Activity` and `Probe` become mere string labels or subclasses injected by the domain configuration. The core orchestrator (`mgr_node`) no longer cares *what* the node is, only that it is a `TerminalNode` requiring execution.

## 4. Conclusion
Adopting the Terminal vs Non-Terminal abstraction perfectly decouples the orchestration engine from the SDLC domain. It allows the Antigravity infrastructure to be dropped into any generic problem space (`agent-travel`, `agent-research`, `agent-finance`) simply by defining new domain-specific labels that inherit from the universal Terminal Node contract.
