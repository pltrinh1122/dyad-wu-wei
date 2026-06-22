import subprocess
import json
import re

def main():
    labels_to_create = [
        {"name": "type: intent", "color": "e6e6fa", "description": "Raw operator intent"},
        {"name": "type: path", "color": "bfdadc", "description": "Autonomous Path execution context"},
        {"name": "type: node", "color": "f9d0c4", "description": "Active execution node (Plan/Act/Reflect)"}
    ]
    
    for lbl in labels_to_create:
        print(f"Creating label: {lbl['name']}")
        subprocess.run(["gh", "label", "create", lbl['name'], "--color", lbl['color'], "--description", lbl['description'], "--force"], check=False)

    print("Fetching open issues...")
    result = subprocess.run(
        ["gh", "issue", "list", "--state", "open", "--json", "number,title,labels", "--limit", "300"],
        capture_output=True, text=True, check=True
    )
    issues = json.loads(result.stdout)

    for issue in issues:
        number = issue["number"]
        title = issue["title"]
        labels = [l["name"] for l in issue.get("labels", [])]
        
        target_label = None
        
        if title.startswith("Path:"):
            target_label = "type: path"
        elif re.match(r'^(Plan|Act|Reflect|Node)\b', title):
            target_label = "type: node"
        else:
            target_label = "type: intent"
            
        if target_label and target_label not in labels:
            print(f"Applying '{target_label}' to Issue #{number} ({title})")
            subprocess.run(["gh", "issue", "edit", str(number), "--add-label", target_label], check=True)
        else:
            print(f"Issue #{number} already has '{target_label}'")

if __name__ == "__main__":
    main()
