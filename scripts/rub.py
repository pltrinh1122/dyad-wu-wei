#!/usr/bin/env python3
import os
import sys
import json
import argparse
import re

# Add the project root to sys.path so we can import drivers
repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, repo_root)

from drivers import github_client

def parse_dag_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_dag_md(file_path):
    """
    Simple markdown parser:
    # Path: <Title>
    <Body>
    
    ## Node: <Title>
    <Body>
    
    ## Node: <Title>
    <Body>
    """
    path_title = ""
    path_body = []
    nodes = []
    current_node = None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        path_match = re.match(r'^#\s+Path:\s*(.+)$', line, re.IGNORECASE)
        node_match = re.match(r'^##\s+Node:\s*(.+)$', line, re.IGNORECASE)
        
        if path_match:
            path_title = path_match.group(1).strip()
            current_node = None
        elif node_match:
            if current_node:
                nodes.append(current_node)
            current_node = {"title": node_match.group(1).strip(), "body": []}
        else:
            if current_node is not None:
                current_node["body"].append(line)
            else:
                path_body.append(line)
                
    if current_node:
        nodes.append(current_node)
        
    return {
        "title": path_title,
        "body": "".join(path_body).strip(),
        "nodes": [{"title": n["title"], "body": "".join(n["body"]).strip()} for n in nodes]
    }

def main():
    parser = argparse.ArgumentParser(description="DAG Generator: Creates Path and Node issues with orthogonal type labels.")
    parser.add_argument("manifest", help="Path to the manifest file (dag.json or dag.md), or a Path issue ID (e.g., 1234)")
    args = parser.parse_args()

    if args.manifest.isdigit():
        issue_id = args.manifest
        issue_details = github_client.get_issue_details(issue_id)
        if not issue_details or 'title' not in issue_details:
            print(f"Error: Could not fetch details for issue #{issue_id}")
            sys.exit(1)
            
        path_title = issue_details["title"]
        path_id = issue_id
        print(f"Using existing Path #{path_id}: {path_title}")
        
        nodes = [
            {"title": f"[Harmonize] {path_title}", "body": f"[Parent: #{path_id}]"},
            {"title": f"[Plan] {path_title}", "body": f"[Parent: #{path_id}]"},
            {"title": f"[Act] {path_title}", "body": f"[Parent: #{path_id}]"},
            {"title": f"[Reflect] {path_title}", "body": f"[Parent: #{path_id}]"}
        ]
    else:
        if not os.path.exists(args.manifest):
            print(f"Error: Manifest file {args.manifest} not found.")
            sys.exit(1)

        if args.manifest.endswith('.json'):
            dag = parse_dag_json(args.manifest)
        elif args.manifest.endswith('.md'):
            dag = parse_dag_md(args.manifest)
        else:
            print("Error: Manifest must be a .json, .md file, or an issue ID.")
            sys.exit(1)

        path_title = dag.get("title")
        path_body = dag.get("body", "")
        nodes = dag.get("nodes", [])

        if not path_title:
            print("Error: Path title is missing in the manifest.")
            sys.exit(1)

        # In flattened structure, the overarching path is just another node
        print(f"Creating Root Node from Path title: {path_title}")
        root_node_url = github_client.create_issue(
            title=path_title,
            body=path_body,
            labels=["type: node", "backlog"]
        )
        path_id = root_node_url.split('/')[-1]
        print(f"Created Root Node #{path_id}: {root_node_url}")

    created_nodes = []
    for i, node in enumerate(nodes):
        node_title = node.get("title")
        node_body = node.get("body", "")
        if not node_title:
            print(f"Warning: Node {i+1} is missing a title. Skipping.")
            continue
            
        print(f"Creating Node: {node_title}")
        node_url = github_client.create_issue(
            title=node_title,
            body=node_body,
            labels=["type: node", "backlog"]
        )
        node_id = node_url.split('/')[-1]
        print(f"Created Node #{node_id}: {node_url}")
        created_nodes.append((node_id, node_title))

    if created_nodes:
        # Append DAG Linkage (Meta-Index) to the Path's body
        print("Updating Path with Meta-Index linkage...")
        meta_index = "\n\n## Meta-Index\n"
        for nid, ntitle in created_nodes:
            meta_index += f"- [ ] #{nid}: {ntitle}\n"
        
        # Read current path issue to append properly in case GH modified it
        path_details = github_client.get_issue_details(path_id)
        current_body = path_details.get("body", "")
        
        new_body = current_body.strip() + meta_index
        github_client.update_issue_body(path_id, new_body)
        print("Path successfully harmonized with its child nodes.")

if __name__ == "__main__":
    main()
