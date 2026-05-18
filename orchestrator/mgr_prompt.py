import sys
from skills.file_locker import lock_file
import yaml
import os
import time
import uuid
import argparse
from datetime import datetime, timezone
from skills.tty_gate import require_operator_approval

def get_backlog_file():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(repo_dir, "artifacts", "prompt_backlog.yml")

def load_data(backlog_file):
    data = {"prompts": []}
    with lock_file(backlog_file):
        if os.path.exists(backlog_file):
            with open(backlog_file, "r") as f:
                loaded = yaml.safe_load(f)
                if loaded and "prompts" in loaded:
                    data = loaded
    return data

def save_data(backlog_file, data):
    os.makedirs(os.path.dirname(backlog_file), exist_ok=True)
    with lock_file(backlog_file):
        with open(backlog_file, "w") as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)

def add_prompt(prompt_text):
    backlog_file = get_backlog_file()
    data = load_data(backlog_file)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    prompt_id = "p-" + str(int(time.time())) + "-" + str(uuid.uuid4())[:4]

    new_prompt = {
        "id": prompt_id,
        "timestamp": timestamp,
        "text": prompt_text,
        "status": "pending"
    }

    data["prompts"].append(new_prompt)
    save_data(backlog_file, data)
    print(f"Prompt queued to {backlog_file}")

def consume_prompts(prompt_ids_str, pr_url):
    backlog_file = get_backlog_file()
    data = load_data(backlog_file)
    prompt_ids = [p.strip() for p in prompt_ids_str.split(",")]
    
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    consumed_count = 0
    for p in data.get("prompts", []):
        if p["id"] in prompt_ids and p.get("status") == "pending":
            p["status"] = "consumed"
            p["consumed_by_pr"] = pr_url
            p["read_timestamp"] = timestamp
            consumed_count += 1
            
    if consumed_count > 0:
        save_data(backlog_file, data)
    print(f"Consumed {consumed_count} prompt(s).")

def list_prompts(all_prompts=False):
    backlog_file = get_backlog_file()
    data = load_data(backlog_file)
    prompts = data.get("prompts", [])
    
    if not all_prompts:
        prompts = [p for p in prompts if p.get("status") == "pending"]

    print(f"📋 Prompt Queue ({len(prompts)} item(s) pending):")
    for p in prompts:
        status_icon = " " if p.get("status") == "pending" else "x"
        print(f"  [{status_icon}] {p['id']} ({p['timestamp']}): {p['text']}")

def delete_prompt(prompt_id):
    backlog_file = get_backlog_file()
    data = load_data(backlog_file)
    prompts = data.get("prompts", [])
    
    target = next((p for p in prompts if p["id"] == prompt_id), None)
    if not target:
        print(f"Error: Prompt {prompt_id} not found.")
        sys.exit(1)
        
    print(f"Prompt {prompt_id}:")
    print(f"  Status: {target.get('status')}")
    print(f"  Text: {target.get('text')}")
    
    if require_operator_approval(f"Are you sure you want to delete this prompt? [y/N]: "):
        data["prompts"] = [p for p in prompts if p["id"] != prompt_id]
        save_data(backlog_file, data)
        print(f"\nPrompt {prompt_id} deleted.")
    else:
        print("\nDeletion cancelled.")

def main():
    parser = argparse.ArgumentParser(description="Prompt Queue Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new prompt to the queue")
    parser_add.add_argument("prompt_text", help="The text of the prompt")

    # List command
    parser_list = subparsers.add_parser("list", help="List prompts in the queue")
    parser_list.add_argument("--all", action="store_true", help="Show all prompts, including consumed")

    # Consume command
    parser_consume = subparsers.add_parser("consume", help="Consume prompts")
    parser_consume.add_argument("prompt_ids", help="Comma-separated list of prompt IDs")
    parser_consume.add_argument("pr_url", help="URL of the PR that consumed the prompts")

    # Delete command
    parser_delete = subparsers.add_parser("delete", help="Delete a prompt from the queue")
    parser_delete.add_argument("prompt_id", help="ID of the prompt to delete")

    args = parser.parse_args()

    if args.command == "add":
        add_prompt(args.prompt_text)
    elif args.command == "list":
        list_prompts(args.all)
    elif args.command == "consume":
        consume_prompts(args.prompt_ids, args.pr_url)
    elif args.command == "delete":
        delete_prompt(args.prompt_id)

if __name__ == "__main__":
    main()
