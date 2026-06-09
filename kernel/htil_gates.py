import os
import yaml

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'artifacts', 'htil_gates.yml')

def load_gates():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)
    return config.get('gates', {})

def is_engaged(gate_name):
    """
    Returns True if the specified HTIL gate is currently engaged (blocking),
    and False if the Agent is permitted to proceed autonomously.
    """
    gates = load_gates()
    # Default to True for safety if gate not explicitly defined
    return gates.get(gate_name, True)

def check_nba_handoff():
    return is_engaged('HTIL_GATE_NBA_HANDOFF')

def check_plan_review():
    return is_engaged('HTIL_GATE_PLAN_REVIEW')

def check_pr_merge():
    return is_engaged('HTIL_GATE_PR_MERGE')

def check_backlog_mutation():
    return is_engaged('HTIL_GATE_BACKLOG_MUTATION')
