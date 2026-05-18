import subprocess
import json

# Fetch current body
res = subprocess.run(['gh', 'issue', 'view', '10', '--json', 'body'], capture_output=True, text=True, check=True)
current_body = json.loads(res.stdout)['body']

# The new nodes to append
new_nodes = """
- [x] Activity 108: Refactor prompt backlog to YAML (#108)
- [x] Activity 113: List items in prompt queue (#113)
- [x] Activity 109: Link consumed prompts to PR bodies (#109)
- [x] Probe 125: Architectural Evaluation of Hot-Fix Workflow (#125)
- [x] Activity 127: Implement bin/rt formal primitive (#127)
- [x] Activity 124: Add prompt-processing hook into GEMINI.md SPAO instructions (#124)
- [x] Activity 122: Implement file-locking mechanism for shared artifacts (#122)
- [x] Activity 121: Implement git worktree management for orthogonal parallelism (#121)
- [x] Activity 134: Implement universal --help and -h support for all bin/ CLI adapters (#134)
- [x] Activity 136: Execute Architectural Migration of sync-clean to bin/node sync (#136)
- [x] Activity 137: Implement prompt delete CLI command (#137)
- [x] Activity 140: Implement Architectural TTY Hard-Gate (#140)
- [x] Activity 143: Implement prompt clean CLI command (#143)
- [x] Activity 146: Add meta-rule to GEMINI for gh issue mapping (#146)
- [x] Activity 145: Implement GitHub Label-Based Node Locking (#145)
- [x] Probe 149: Triage GitHub API Eventual Consistency on Issue State (#149)
- [x] Activity 150: Mitigate GitHub API Eventual Consistency (#150)
- [x] Activity 154: Add invariant check for closed PR before branch cleanup (#154)
- [x] Probe 153: Architectural Evaluation of Terminal vs Non-Terminal Node Abstraction (#153)
- [x] Node 157: Implement Soft-Locking for Node Checkout (#157)
- [x] Probe 159: Evaluate node plan-start and plan-finish commands (#159)
- [ ] Probe 163: Audit State Inconsistencies (#163)
"""

if "- [x] Activity 108" not in current_body:
    # Append to the list
    new_body = current_body.strip() + "\n" + new_nodes.strip() + "\n"
    subprocess.run(['gh', 'issue', 'edit', '10', '--body', new_body], check=True)
    print("Issue #10 successfully updated with new nodes.")
else:
    print("Issue #10 already contains the new nodes.")
