import sys
import argparse
from skills import git_client

def main():
    parser = argparse.ArgumentParser(description="Git Client API CLI Wrapper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    parser_add = subparsers.add_parser("add", help="Stage files")
    parser_add.add_argument("files", nargs="+", help="Files to stage")

    # commit
    parser_commit = subparsers.add_parser("commit", help="Commit changes")
    parser_commit.add_argument("-m", "--message", required=True, help="Commit message")

    # push
    parser_push = subparsers.add_parser("push", help="Push changes")
    parser_push.add_argument("branch", nargs="?", help="Branch to push (optional)")
    parser_push.add_argument("-f", "--force", action="store_true", help="Force push")

    # restore
    parser_restore = subparsers.add_parser("restore", help="Restore files")
    parser_restore.add_argument("files", nargs="+", help="Files to restore")

    # worktree
    parser_wt = subparsers.add_parser("worktree", help="Worktree commands")
    wt_sub = parser_wt.add_subparsers(dest="subcommand", required=True)
    
    parser_wt_add = wt_sub.add_parser("add", help="Add worktree")
    parser_wt_add.add_argument("branch", help="Branch name")
    parser_wt_add.add_argument("path", help="Worktree path")
    parser_wt_add.add_argument("base", nargs="?", default="main", help="Base commit/branch")

    parser_wt_remove = wt_sub.add_parser("remove", help="Remove worktree")
    parser_wt_remove.add_argument("path", help="Worktree path")
    parser_wt_remove.add_argument("-f", "--force", action="store_true", help="Force remove")

    args = parser.parse_args()

    if args.command == "add":
        git_client.add(args.files)
    elif args.command == "commit":
        git_client.commit(args.message)
    elif args.command == "push":
        branch = args.branch if args.branch else git_client.get_current_branch()
        git_client.push(branch, force=args.force)
    elif args.command == "restore":
        git_client.restore(args.files)
    elif args.command == "worktree":
        if args.subcommand == "add":
            git_client.worktree_add(args.branch, args.path, args.base)
        elif args.subcommand == "remove":
            git_client.worktree_remove(args.path, force=args.force)

if __name__ == "__main__":
    main()
