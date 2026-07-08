import os

REPLACEMENTS = {
    '"status: in-progress"': '"status: execute"',
    "'status: in-progress'": "'status: execute'",
    '"in_progress"': '"execute"',
    "'in_progress'": "'execute'",
    'in_progress_label': 'execute_label',
    'in_progress_output': 'execute_output',
    
    '"status: todo"': '"status: clarify"',
    "'status: todo'": "'status: clarify'",
    '"todo"': '"clarify"',
    "'todo'": "'clarify'",
    'todo_label': 'clarify_label',
    
    '"status: triage"': '"status: clarify"',
    "'status: triage'": "'status: clarify'",
    '"triage"': '"clarify"',
    "'triage'": "'clarify'",
    
    '"status: in-review"': '"status: dispose"',
    "'status: in-review'": "'status: dispose'",
    '"in_review"': '"dispose"',
    "'in_review'": "'dispose'",
    
    'test_get_ready_nodes_excludes_in_progress': 'test_get_ready_nodes_excludes_execute',
    'test_plan_start_wip_n1_bypassed_for_concurrent_nodes': 'test_plan_start_wip_n1_bypassed_for_concurrent_nodes'
}

def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
        
    new_content = content
    for old, new in REPLACEMENTS.items():
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

for root, _, files in os.walk('.'):
    if '.git' in root or '.worktrees' in root or '.scratch' in root or '__pycache__' in root:
        continue
    for file in files:
        if file.endswith('.py') or file.endswith('.yml') or file.endswith('.md'):
            process_file(os.path.join(root, file))
