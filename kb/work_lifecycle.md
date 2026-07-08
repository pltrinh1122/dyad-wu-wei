# The Work Lifecycle: Singular Staging & Live Swarm Command

This diagram illustrates the unified intake architecture, explicitly separating the Pre-Agentic Intake Queue from Active Swarm Steering. It demonstrates how raw ideas funnel through the `staging` queue and are formalizied by the Strategist, while the Operator exercises real-time command-and-control over the executing swarm via Live Chat.

```mermaid
graph TD
    %% ----------------------------------------------------
    %% 1. The Pre-Agentic Staging Area (Intake)
    %% ----------------------------------------------------
    subgraph Staging[Pre-Agentic Staging Area]
        User[Operator] -->|gh issue create| RawIdea[Raw Idea / Bug Request]
        RawIdea -.->|Apply Label| StagingLabel((Label: staging))
        StagingLabel --> StagingQueue[(Singular 'staging' Queue)]
    end

    %% ----------------------------------------------------
    %% 2. The Execution Gate & Harmonization (The Rub)
    %% ----------------------------------------------------
    subgraph Triage[Strategist Harmonization]
        StagingQueue -->|Triggers| HTILGate{HTIL Gate:<br/>Staging Queue Empty?}
        HTILGate -->|No| Block[Halt Execution Floor<br/>StagingAreaBlockedError]
        Block --> PullStaging[Strategist pulls 'staging' issues]
        
        PullStaging --> GenPath[bin/backlog new path<br/>Generate DAG]
        GenPath --> CloseStaging(Close 'staging' Issue)
        CloseStaging --> HTILGate
    end

    %% ----------------------------------------------------
    %% 3. The Execution Factory Floor
    %% ----------------------------------------------------
    subgraph Factory[Execution Factory Floor]
        HTILGate -->|Yes| NBA[daemon_nba.py<br/>Selects Next-Best-Action]
        GenPath -.->|Produces Nodes| Backlog[Nodes with 'status: backlog']
        Backlog --> NBA
        
        NBA --> PlanStart[plan-start acquires lock<br/>Applies 'status: execute']
        
        PlanStart --> ExecHarmonize[Harmonize Node]
        ExecHarmonize --> ExecPlan[Plan Node]
        ExecPlan --> ExecAct[Act Node]
        ExecAct --> ExecReflect[Reflect Node]
        ExecReflect -->|Closes Node| Done((Node Completed))
    end

    %% ----------------------------------------------------
    %% 4. Active Swarm Command (Live Chat)
    %% ----------------------------------------------------
    subgraph ActiveSteering[Live Chat Command & Control]
        Chat[Operator Live Chat] -->|Real-Time Directive| Frontier[Frontier Agent]
        Frontier -->|Active Management| Kill[manage_subagents kill]
        Frontier -->|Context Injection| Send[send_message to sub-agent]
        
        Kill -.->|Terminates| ExecAct
        Send -.->|Steers| ExecAct
    end

    %% Connections across subgraphs
    Done -.->|Fetch Next Node| HTILGate

    %% Styling
    classDef raw fill:#f9f2f4,stroke:#333,stroke-width:1px;
    classDef trigger fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    classDef execute fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    classDef gate fill:#ffebee,stroke:#d32f2f,stroke-width:2px;
    classDef staging fill:#e3f2fd,stroke:#1976d2,stroke-width:2px;
    classDef command fill:#e1bee7,stroke:#8e24aa,stroke-width:2px;

    class User,RawIdea raw;
    class StagingQueue,StagingLabel staging;
    class HTILGate,Block gate;
    class PullStaging,GenPath,CloseStaging trigger;
    class Factory,Backlog,NBA,PlanStart,ExecHarmonize,ExecPlan,ExecAct,ExecReflect,Done execute;
    class Chat,Frontier,Kill,Send command;

```

## Key Architectural Principles

1. **The Singular Intake Queue:** The `staging` GitHub Issue label is strictly the Pre-Agentic Intake Queue. It holds unstructured bugs and feature requests awaiting formal DAG translation by the Strategist.
2. **The Passive Gate:** The engine cannot pull new nodes into execution if the `staging` queue is non-empty, guaranteeing that Operator intent is codified before allocating resources.
3. **Active Swarm Steering:** The legacy Prompt mechanism is retired. Real-time steering, course correction, and emergency braking of actively executing nodes are handled exclusively via **Live Chat**, where the asynchronous Frontier Agent can instantaneously terminate or message executing sub-agents.
