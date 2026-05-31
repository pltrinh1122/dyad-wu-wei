import drivers.github_client as gh
issue = gh.get_issue_details(1355)
body = issue.get("body", "")

new_body = body.replace("### Continue\n-", "### Continue\n- Emphasize the inviolability of execution flow when interacting with unpredictable system harnesses.\n- Use explicit Iatrogenic-Injection Suppression Rules in GEMINI.md rather than trying to engineer around the prompt injection.")
new_body = new_body.replace("### Stop\n-", "### Stop\n- Allowing injected ephemeral prompts to cancel in-flight wait states or asynchronous tasks, leading to execution seizures.")
new_body = new_body.replace("### Start\n-", "### Start\n- Formalizing system-injected messages as pure information rather than directives.")

# Check off nodes
new_body = new_body.replace("- [ ] Node 1356", "- [x] Node 1356")
new_body = new_body.replace("- [ ] Node 1357", "- [x] Node 1357")
new_body = new_body.replace("- [ ] Node 1358", "- [x] Node 1358")

gh.update_issue(1355, body=new_body, state="closed")
print("Successfully updated and closed Path 1355.")
