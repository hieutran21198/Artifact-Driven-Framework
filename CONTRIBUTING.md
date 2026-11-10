# Contributing

Start with the [repository README](README.md), the
[architecture](docs/architecture/README.md) and
[Artifact Driven](docs/governances/artifact-driven/README.md).

## Change this workspace

1. Work on a dedicated branch. Use `<type>/<short-name>`, for example
   `docs/domain-list`. A knowledge change is a branch named after its issue
   ([approval of knowledge](docs/governances/artifact-driven/README.md#approval-of-knowledge)).
2. Keep the change within its agreed scope. Preserve unrelated files and work.
3. Follow the [repository conventions](docs/coding-standards/README.md).
4. Update the affected READMEs so readers can find the result.
5. Run the [checks](#check-a-change).

## Change a service or a client

The change to each part is made in its clone under
[services](services/README.md) or [applications](apps/README.md), merged in its
own repository and approved by its owner.

1. Branch from the latest default branch. Use `<type>/<issue>-<short-name>`,
   for example `fix/123-return-overdue-book`.
2. Before changing an endpoint, read the flow steps that name it and how the
   [clients](apps/README.md) and other services call it: request shape,
   response decoding, error handling and API version.
3. Add a test for the changed behavior, named after the knowledge ID it
   proves. Runtime code needs a passing test with seeded data before it is
   committed.
4. Merge the latest default branch into the branch, then open the pull
   request. It links the issue and the knowledge merge commit.

Use a short, single-line commit message that names the issue. The project
sets its own commit and release-branch conventions here.

Change only the parts the issue and their owners give you. For a part you
cannot access, write a handoff to its owner on the issue.

## Owners

The owners of the parts that no service or client README lists
([parts and owners](docs/governances/artifact-driven/team.md#parts-and-owners)).
Fill in a person or a group for each:

| Part | Owner |
| --- | --- |
| Goals (product owner) | — |
| End-to-end tests (quality owner), in `e2e/` | — |
| The API gateway | — |
| Tie-breaker when owners disagree | — |

## Deploy and release

Fill in how each part reaches each environment:

| Part | Environment | How |
| --- | --- | --- |
| — | — | — |

The [infrastructure](docs/infrastructure/README.md) pages show what a deploy
runs.

Before a deploy of a part, find the commit of that part that runs in the
target environment and list the changes between it and the candidate. After a deploy, watch the alarms and
the logs.

A hotfix starts from the commit that runs in production, not from the newest
release branch. Keep the fix to the reported defect, deploy only what it
changes, and bring the fix back to the default branch.

Push, merge and deploy only when asked.

## Move existing code into the structure

New code goes into the [structure](docs/architecture/README.md):
`internal/domain`, `internal/app` and `internal/adapter`. Code that predates it
shrinks one use case at a time.

1. Write end-to-end scenarios for the use case. Run them against the existing
   code until they pass. Capture a JSON snapshot of every response.
2. Build the use case in the structure: a command in `app/command` or a query
   in `app/query`, as the
   [architecture](docs/architecture/commands-and-queries.md) describes.
3. Register the new handler on the same route and remove the old
   registration. Rollback is a one-line route swap.
4. Run the same scenarios and snapshots. They must pass byte for byte,
   including null and empty fields, because released clients may parse
   responses by their JSON shape.
5. Delete the old code when no route uses it.

Rules:

- Do not move or rename existing code in bulk. A bulk move breaks `git blame`,
  open pull requests and cherry-picks onto release branches.
- Use cases that write the same tables move together.
- Do not change the schema, API paths, versions or response shapes as part of
  a move.

## Check a change

The checks need Git and Python 3. They use the Python standard library and do
not install packages or change files.
Follow [Check the docs](docs/governances/artifact-driven/runbooks/check.md)
for the structure, docs and whitespace commands, including staged changes and
the complete pull request diff in CI.

For a service or client change, check that its tests name only knowledge IDs
that exist:

```sh
python3 scripts/check_tests.py
```

For a changed OpenAPI contract, lint it:

```sh
npx @redocly/cli lint docs/software-knowledges/<path>.yaml
```

To see what depends on a knowledge ID, an operation or a response field:

```sh
python3 scripts/impact.py <ID|operationId|field>
```

For a change to a part, run the checks in its README and the gates of its
language standard, such as the [Go gates](docs/coding-standards/golang/README.md#gates).

Describe the checks you ran and any remaining limits when handing off a change.

Return to the [contents](README.md).
