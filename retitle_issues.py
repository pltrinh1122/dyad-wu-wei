import sys
import re

sys.path.append("/mnt/shared_data/dzw/dyad-wu-wei/.worktrees/node/1487-retitle-backlog")
from drivers.github_client import get_open_issues, rename_issue_title, update_issue_body

def replace_text(text):
    if not text:
        return text
    # Replace exact case matches
    text = text.replace("DZ-CIL", "Wu-wei Dyad")
    text = text.replace("dz-cil", "dyad-wu-wei")
    text = text.replace("Dz-cil", "Dyad-wu-wei")
    return text

def main():
    issues = get_open_issues()
    print(f"Found {len(issues)} open issues.")
    for issue in issues:
        number = issue["number"]
        old_title = issue["title"]
        old_body = issue["body"]
        
        new_title = replace_text(old_title)
        new_body = replace_text(old_body)
        
        updated = False
        if new_title != old_title:
            print(f"Updating title for {number}: {old_title} -> {new_title}")
            rename_issue_title(number, new_title)
            updated = True
            
        if new_body != old_body:
            print(f"Updating body for {number}")
            update_issue_body(number, new_body)
            updated = True
            
        if updated:
            print(f"Successfully updated #{number}")

if __name__ == "__main__":
    main()
