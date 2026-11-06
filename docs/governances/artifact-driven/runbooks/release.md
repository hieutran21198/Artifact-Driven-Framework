# Report a release

Use before a release reaches production, to give the product owner and the
stakeholders the report that
[Workflow](../workflow.md#release-report) describes.

## Steps

1. Find the commit that runs in production and the release candidate. List
   the issues and pull requests between them.
2. From those pull requests, collect the IDs their tests prove and the goals
   those IDs serve. List apart the pull requests that change production data
   or prove no ID, so the readers see them too.
3. For each goal, run [impact](../../../../scripts/README.md#impact) downward
   (`python3 scripts/impact.py --down <goal criterion ID>`) to list the
   requirements, flows, rules, operations and contracts the goal relies on.
   That set is the knowledge part of the report.
4. Collect what the pull requests record as not covered, and the handoffs
   still open on their issues.
5. Tag the knowledge commit that the release implements with the release
   name.
6. Post the report on the release issue: changes, knowledge, tests by ID, and
   limits.

Return to [runbooks](README.md).
