import re
with open('kernel/daemon_knowledge_accrual.py', 'r') as f:
    content = f.read()

inject_ext = '''
    kb_dir = os.path.join(repo_root, "kb")
    injection = knowledge_accrual_skill.build_contextual_prompt_injection(active_path_str, kb_dir)

    # DDOP Extension: Inject Domain Dao Digest if active node belongs to a domain
    try:
        active_node_str = agent_frontier.read_active_node(frontier_yml_path)
        if active_node_str and active_node_str != "None":
            node_id = active_node_str.split(":")[0].replace("Node ", "").strip()
            from drivers import github_client
            labels = github_client.get_issue_labels(node_id)
            domain_id = None
            for label in labels:
                if isinstance(label, str) and label.startswith("domain:"):
                    domain_id = label.split(":")[1]
                    break
            if domain_id:
                import yaml
                dyad_config_path = os.path.join(repo_root, "dyad-wu-wei.yml")
                if os.path.exists(dyad_config_path):
                    with open(dyad_config_path, 'r') as cf:
                        dyad_config = yaml.safe_load(cf) or {}
                        domain_config = dyad_config.get("domains", {}).get(domain_id)
                        if domain_config and domain_config.get("domain_dao_digest"):
                            digest_path = os.path.join(repo_root, domain_config["domain_dao_digest"])
                            if os.path.exists(digest_path):
                                with open(digest_path, 'r', encoding="utf-8") as df:
                                    injection += "\n\n<!-- DOMAIN DAO DIGEST START -->\n"
                                    injection += df.read() + "\n"
                                    injection += "<!-- DOMAIN DAO DIGEST END -->\n"
    except Exception as e:
        print(f"Warning: Failed to inject domain digest: {e}")
'''

content = re.sub(
    r'\s*kb_dir = os\.path\.join\(repo_root, "kb"\)\s*injection = knowledge_accrual_skill\.build_contextual_prompt_injection\(active_path_str, kb_dir\)',
    inject_ext,
    content
)

with open('kernel/daemon_knowledge_accrual.py', 'w') as f:
    f.write(content)
print("Patched daemon_knowledge_accrual.py")
