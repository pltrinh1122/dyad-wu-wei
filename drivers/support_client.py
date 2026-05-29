"""
Support Client — Stateless skill for filing and tracking external project support tickets.

Files GitHub issues on the DZ-CIL repository using the support-external template.
This skill is invoked by bin/support and is designed for use from external project
workstations with read-only DZ-CIL clones.

Full lifecycle: file → status → list → remediation tracking.
Per WHY-1372: Full-Cycle External Support Ticket Status Tracking.
"""
import argparse
import subprocess
import sys
import json


VALID_TYPES = {
    "amendment": "Amendment — Domain Dao Digest rule correction, addition, or removal",
    "escalation": "Escalation — Blocking question requiring Operator guidance",
    "tooling": "Tooling — New skill, wrapper, or infrastructure needed in DZ-CIL",
    "retro": "Retrospective — Session learnings to flow back to the engine Dao",
    "bug": "Bug — DZ-CIL toolchain issue encountered during external project work",
}

# The DZ-CIL repo where support tickets are filed.
# This is intentionally hardcoded — support tickets always target the engine repo.
DZ_CIL_REPO = "pltrinh1122/dz-cil"


def _labels_to_phase(labels, state):
    """Map GitHub issue labels + state to a human-readable lifecycle phase.

    Per WHY-1372 §2.1:
    - support, no backlog       → 📥 Received
    - status:triage             → 🔍 Under Review
    - backlog                   → 📋 Accepted / Queued
    - status: in-progress       → 🔧 In Progress
    - Closed                    → ✅ Resolved
    """
    label_names = {l.lower() for l in labels}

    if state == "CLOSED":
        return "✅ Resolved"
    if "status: in-progress" in label_names or "status:in-progress" in label_names:
        return "🔧 In Progress"
    if "backlog" in label_names:
        return "📋 Accepted / Queued"
    if "status:triage" in label_names or "triage" in label_names:
        return "🔍 Under Review"
    return "📥 Received"


def file_support_ticket(
    ticket_type: str,
    project_id: str,
    description: str,
    blocking: bool = False,
    digest_rule_ids: str = "",
    session_id: str = "",
) -> str:
    """
    Files a support ticket on the DZ-CIL repo.

    Args:
        ticket_type: One of: amendment, escalation, tooling, retro, bug
        project_id: Short identifier for the external project
        description: The support request description
        blocking: Whether this blocks current work
        digest_rule_ids: Related digest rule IDs (optional)
        session_id: Conversation/session ID for traceability (optional)

    Returns:
        The URL of the created issue.

    Raises:
        ValueError: If ticket_type is invalid.
        subprocess.CalledProcessError: If gh CLI fails.
    """
    if ticket_type not in VALID_TYPES:
        raise ValueError(
            f"Invalid ticket type '{ticket_type}'. Must be one of: {', '.join(VALID_TYPES.keys())}"
        )

    type_label = VALID_TYPES[ticket_type]
    blocking_label = "Yes — cannot proceed without resolution" if blocking else "No — can continue, will batch with next session"

    title = f"[SUPPORT] [{project_id}] {ticket_type}: {description[:80]}"

    body_parts = [
        f"**Ticket Type**: {type_label}",
        f"**Project**: {project_id}",
        f"**Blocking**: {blocking_label}",
    ]
    if digest_rule_ids:
        body_parts.append(f"**Related Digest Rules**: {digest_rule_ids}")
    if session_id:
        body_parts.append(f"**Session ID**: {session_id}")

    body_parts.append(f"\n## Request\n\n{description}")

    body = "\n".join(body_parts)

    cmd = [
        "gh", "issue", "create",
        "--repo", DZ_CIL_REPO,
        "--title", title,
        "--body", body,
        "--label", "support,external-project",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    url = result.stdout.strip()
    return url


def get_ticket_status(ticket_number: int) -> dict:
    """
    Query the full lifecycle status of a support ticket.

    Args:
        ticket_number: The GitHub issue number.

    Returns:
        Dict with keys: number, title, state, phase, created_at, updated_at,
        labels, comments, url.
    """
    cmd = [
        "gh", "issue", "view", str(ticket_number),
        "--repo", DZ_CIL_REPO,
        "--json", "number,title,state,labels,createdAt,updatedAt,comments,url",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)

    labels = [l["name"] for l in data.get("labels", []) if isinstance(l, dict)]
    state = data.get("state", "UNKNOWN")

    return {
        "number": data.get("number"),
        "title": data.get("title", ""),
        "state": state,
        "phase": _labels_to_phase(labels, state),
        "labels": labels,
        "created_at": data.get("createdAt", ""),
        "updated_at": data.get("updatedAt", ""),
        "comments": data.get("comments", []),
        "url": data.get("url", ""),
    }


def list_support_tickets(project_filter: str = "", state: str = "open") -> list:
    """
    List support tickets, optionally filtered by project.

    Args:
        project_filter: Filter by project identifier (e.g., 'fl').
        state: Issue state filter ('open', 'closed', 'all').

    Returns:
        List of ticket dicts with number, title, phase, created_at.
    """
    cmd = [
        "gh", "issue", "list",
        "--repo", DZ_CIL_REPO,
        "--label", "support",
        "--state", state,
        "--json", "number,title,labels,createdAt,state",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    issues = json.loads(result.stdout or "[]")

    if project_filter:
        issues = [i for i in issues if f"[{project_filter}]" in i.get("title", "")]

    tickets = []
    for issue in issues:
        labels = [l["name"] for l in issue.get("labels", []) if isinstance(l, dict)]
        issue_state = issue.get("state", "UNKNOWN")
        tickets.append({
            "number": issue["number"],
            "title": issue["title"],
            "phase": _labels_to_phase(labels, issue_state),
            "created_at": issue.get("createdAt", ""),
        })
    return tickets


def main():
    parser = argparse.ArgumentParser(
        description="DZ-CIL External Project Support Line — File, track, and query support tickets.",
        prog="bin/support",
        epilog="""Examples:
  %(prog)s file --type bug --project fl "NBA scorer recommends completed paths"
  %(prog)s file --type amendment --project fl --blocking --rules INV-024 "Rule INV-024 conflicts with Flutter conventions"
  %(prog)s status 1233
  %(prog)s list
  %(prog)s list --project fl --state all
  %(prog)s --help
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # file subcommand
    file_parser = subparsers.add_parser(
        "file",
        help="File a new support ticket on DZ-CIL",
        description="Create a support ticket on the DZ-CIL repository. The ticket will be labeled 'support' and 'external-project' for tracking.",
    )
    file_parser.add_argument(
        "--type", required=True, choices=VALID_TYPES.keys(),
        help="Ticket type: amendment (rule fix), escalation (blocking question), tooling (new skill), retro (session learnings), bug (toolchain issue)",
    )
    file_parser.add_argument(
        "--project", required=True,
        help="Short project identifier (e.g., 'fl', 'acme-api')",
    )
    file_parser.add_argument(
        "--blocking", action="store_true", default=False,
        help="Flag this as blocking current work (escalates priority)",
    )
    file_parser.add_argument(
        "--rules", default="",
        help="Related digest rule IDs (e.g., 'INV-024,CONV-008')",
    )
    file_parser.add_argument(
        "--session", default="",
        help="Session/conversation ID for traceability",
    )
    file_parser.add_argument(
        "description", help="Support request description",
    )

    # status subcommand
    status_parser = subparsers.add_parser(
        "status",
        help="Check the status of a support ticket",
        description="Query the full lifecycle status of a specific support ticket by issue number.",
    )
    status_parser.add_argument(
        "ticket_number", type=int,
        help="GitHub issue number of the support ticket",
    )

    # list subcommand
    list_parser = subparsers.add_parser(
        "list",
        help="List support tickets",
        description="List all support tickets, optionally filtered by project and state.",
    )
    list_parser.add_argument(
        "--project", default="",
        help="Filter by project identifier (e.g., 'fl')",
    )
    list_parser.add_argument(
        "--state", default="open", choices=["open", "closed", "all"],
        help="Filter by ticket state (default: open)",
    )

    args = parser.parse_args()

    if args.command == "file":
        url = file_support_ticket(
            ticket_type=args.type,
            project_id=args.project,
            description=args.description,
            blocking=args.blocking,
            digest_rule_ids=args.rules,
            session_id=args.session,
        )
        print(f"✅ Support ticket filed: {url}")

    elif args.command == "status":
        ticket = get_ticket_status(args.ticket_number)
        print(f"🎫 Support Ticket #{ticket['number']}")
        print(f"   Title:   {ticket['title']}")
        print(f"   Phase:   {ticket['phase']}")
        print(f"   State:   {ticket['state']}")
        print(f"   Created: {ticket['created_at']}")
        print(f"   Updated: {ticket['updated_at']}")
        print(f"   Labels:  {', '.join(ticket['labels'])}")
        print(f"   URL:     {ticket['url']}")

        comments = ticket.get("comments", [])
        if comments:
            print(f"\n📝 Comments ({len(comments)}):")
            for c in comments:
                author = c.get("author", {}).get("login", "unknown")
                body = c.get("body", "").strip()
                created = c.get("createdAt", "")
                # Show first 200 chars of each comment
                preview = body[:200] + ("..." if len(body) > 200 else "")
                print(f"   [{created}] @{author}: {preview}")

            # Check for remediation in closing comment
            if ticket["state"] == "CLOSED" and comments:
                last_comment = comments[-1].get("body", "")
                if "## Remediation" in last_comment or "Pull Instructions" in last_comment:
                    print("\n🔧 Remediation Instructions Found:")
                    # Extract the remediation section
                    for line in last_comment.split("\n"):
                        line = line.strip()
                        if line.startswith("- **") or line.startswith("**"):
                            print(f"   {line}")
        else:
            print("\n📝 No comments yet.")

    elif args.command == "list":
        tickets = list_support_tickets(
            project_filter=args.project,
            state=args.state,
        )

        if not tickets:
            print("📋 No support tickets found.")
        else:
            print(f"📋 Support Tickets ({len(tickets)}):\n")
            for t in tickets:
                print(f"  #{t['number']}: {t['title']}")
                print(f"    Phase: {t['phase']} | Created: {t['created_at']}")
                print()


if __name__ == "__main__":
    main()
