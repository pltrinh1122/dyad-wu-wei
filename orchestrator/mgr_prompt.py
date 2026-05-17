import sys
import yaml
import os
import time
import uuid
import argparse
from datetime import datetime, timezone

def get_backlog_file():
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(repo_dir, "artifacts", "prompt_backlog.yml")

def load_data(backlog_file):
    data = {"prompts": []}
    if os.path.exists(backlog_file):
        with open(backlog_file, "r") as f:
            loaded = yaml.safe_load(f)
            if loaded and "prompts" in loaded:
                data = loaded
    return data

def save_data(backlog_file, data):
    os.makedirs(os.path.dirname(backlog_file), exist_ok=True)
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

def main():
    parser = argparse.ArgumentParser(description="Prompt Queue Manager")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Add command
    parser_add = subparsers.add_parser("add", help="Add a new prompt to the queue")
    parser_add.add_argument("prompt_text", help="The text of the prompt")

    # List command
    parser_list = subparsers.add_parser("list", help="List prompts in the queue")
    parser_list.add_argument("--all", action="store_true", help="Show all prompts, including consumed")

    args = parser.parse_args()

    if args.command == "add":
        add_prompt(args.prompt_text)
    elif args.command == "list":
        list_prompts(args.all)

if __name__ == "__main__":
    main()
