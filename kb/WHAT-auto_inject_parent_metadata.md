# WHAT - Auto-Inject Parent Metadata

## Goal
Update `scripts/rub.py` to accept an issue ID as an argument. The script will fetch the parent issue, automatically generate a standard 4-node DAG (Harmonize/Plan/Act/Reflect), and explicitly inject `[Parent: #<ID>]` into each node's body, eliminating the JSON/MD manifest requirement.

## Implementation Details
1. **Argument Parsing Updates**: 
   Modify `scripts/rub.py`'s argument parsing so that the positional argument `manifest` can also accept an issue ID (e.g., `"1234"`). We'll detect this using `args.manifest.isdigit()`. Update the help text to reflect this change.

2. **Fetch Parent Details**:
   If an ID is provided, use `github_client.get_issue_details(issue_id)` to retrieve the parent Path issue's title.

3. **Generate Standard Nodes**:
   Bypass the manifest parsing and dynamically create the standard node structure:
   - `[Harmonize] <Parent Title>`
   - `[Plan] <Parent Title>`
   - `[Act] <Parent Title>`
   - `[Reflect] <Parent Title>`

4. **Metadata Injection**:
   Set each node's `body` explicitly to `[Parent: #<ID>]` to guarantee strict topological linkage.

5. **Issue Creation & Parent Update**:
   Use the existing node creation loop to push the nodes to GitHub and update the parent issue's body to append the Meta-Index checklist.
