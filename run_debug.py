from drivers import github_client
nodes = ["2076", "2077", "2079", "2070", "2071", "2072"]
for node in nodes:
    details = github_client.get_issue_details(node)
    print(node, details.get("state"), details.get("labels"))
