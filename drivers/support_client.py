"""
Support Client — Stateless skill for filing external project support tickets.

Files GitHub issues on the DZ-CIL repository using the support-external template.
This skill is invoked by bin/support and is designed for use from external project
workstations with read-only DZ-CIL clones.
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


def main():
    parser = argparse.ArgumentParser(
        description="DZ-CIL External Project Support Line",
        prog="bin/support",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # file subcommand
    file_parser = subparsers.add_parser("file", help="File a support ticket")
    file_parser.add_argument(
        "--type", required=True, choices=VALID_TYPES.keys(),
        help="Ticket type",
    )
    file_parser.add_argument(
        "--project", required=True,
        help="Short project identifier (e.g., 'fl', 'acme-api')",
    )
    file_parser.add_argument(
        "--blocking", action="store_true", default=False,
        help="Flag this as blocking current work",
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

    # list subcommand
    list_parser = subparsers.add_parser("list", help="List open support tickets")
    list_parser.add_argument(
        "--project", default="",
        help="Filter by project identifier",
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

    elif args.command == "list":
        label_filter = "support"
        cmd = [
            "gh", "issue", "list",
            "--repo", DZ_CIL_REPO,
            "--label", label_filter,
            "--state", "open",
            "--json", "number,title,labels,createdAt",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        issues = json.loads(result.stdout or "[]")

        if args.project:
            issues = [i for i in issues if f"[{args.project}]" in i.get("title", "")]

        if not issues:
            print("📋 No open support tickets.")
        else:
            print(f"📋 Open Support Tickets ({len(issues)}):\n")
            for issue in issues:
                print(f"  #{issue['number']}: {issue['title']}")
                print(f"    Created: {issue['createdAt']}")
                print()


if __name__ == "__main__":
    main()
