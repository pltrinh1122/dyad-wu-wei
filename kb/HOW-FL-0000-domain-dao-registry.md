# Domain Dao Registry

> **Purpose**: Index of external project Domain Dao Digests.
> Loaded by the Agent during Sense phase when operating on external projects.
> Referenced from GEMINI.md §7.

## Active Projects

| Project | Digest (DZ-CIL Cache) | Source of Truth | Repo | Version |
|---------|----------------------|-----------------|------|---------|
| Family Legacy | `kb/WHAT-FL-0001-domain-dao-digest.md` | `docs/7_governance/agent_dao/domain_dao_digest.md` | `pltrinh1122/family_legacy` | v0.1 DRAFT |

## Amendment Protocol

1. FL Agent discovers gap during work → files `[FL-SUPPORT]` issue on DZ-CIL repo
2. Operator ratifies amendment
3. Source of truth updated in FL repo via product PR
4. DZ-CIL cache synced via `bin/rt` hotfix or governed node PR
5. Registry version column updated to reflect latest ratified version

## Loading Instructions

When the Agent begins work on an external project:

1. Read this registry to locate the project's digest
2. Load the referenced digest file in full
3. Treat all rules in the digest as operational constraints for the duration of the work session
4. Any corrections discovered during work:
   - **Blocking**: Raise inline in product PR as `⚠️ DIGEST AMENDMENT CANDIDATE`
   - **Non-blocking**: Batch for session-end amendment PR + FL-SUPPORT ticket

## Support Line

- **Template**: `.github/ISSUE_TEMPLATE/support-fl.yml` (see Node 1326 for materialization)
- **Labels**: `fl-support`, `external-project`
- **Ticket Types**: Amendment, Escalation, Tooling, Retrospective, Bug
