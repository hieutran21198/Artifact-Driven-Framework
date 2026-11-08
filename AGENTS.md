# Project instructions

## Start with the governing sources

Read the [repository README](README.md), [contributing guide](CONTRIBUTING.md)
and the README of each directory you change. For the code of a service or a
client, also read its own agent instructions under
[services](services/README.md) or [applications](apps/README.md). Before
changing an endpoint, read the client pages of its artifact, and how the
[client applications](apps/README.md) and other services call it. Inspect nearby code and existing checks before choosing a design. Reload
affected instructions after context loss or source changes.

The [architecture](docs/architecture/README.md) is the agreed direction.

## Scope

- Change only the parts the issue and their owners give you
  ([parts and owners](docs/governances/artifact-driven/team.md#parts-and-owners)).
  For a part you cannot access, write a handoff to its owner on the issue.
- Each service is one deployable, split by domain inside it. Do not add module
  walls or events between the domains of one service, or a second module
  inside a service. Services talk only through their contracts: calls and
  published messages.

## Principles and writing

Apply [KISS](docs/principles/kiss/README.md) when choosing or simplifying a
solution. Apply [ASD-STE-100 writing guidance](docs/coding-standards/asd-ste-100/README.md)
to English technical documents while preserving technical meaning.

## Knowledge and delivery

Read [Artifact Driven](docs/governances/artifact-driven/README.md) for how
knowledge leads the code. Follow its
[knowledge rules](docs/governances/artifact-driven/knowledge.md),
[workflow](docs/governances/artifact-driven/workflow.md) and
[definition of done](docs/governances/artifact-driven/done.md).

Keep changes, tasks, progress, discussion and evidence on issues and pull
requests. The repository holds established knowledge and code. Do not create
change or task ledgers in the repository. Issue closure is not approval. A
missing contract, approval or evidence stays an explicit gap; do not invent it
or weaken a gate.

## Standards and skills

Follow the [repository conventions](docs/coding-standards/README.md). For code,
read the [General](docs/coding-standards/general/README.md) and
language standard of the part, such as
[Go](docs/coding-standards/golang/README.md), before implementation and review. Cite rule IDs instead of copying their text.

Work as the [team](docs/governances/artifact-driven/team.md): the main session is
the coordinator and hands each step to its agent in
[.agents/agents](.agents/agents/README.md). The skills are
[software-knowledge](.agents/skills/software-knowledge/SKILL.md) for knowledge
and contracts, [defect-triage](.agents/skills/defect-triage/SKILL.md) for
reported defects, and the skill of each part's stack, such as
[backend-service](.agents/skills/backend-service/SKILL.md) for a Go service.

## Change and verify

Use the branch, scope and commit conventions in [Contributing](CONTRIBUTING.md).
Preserve unrelated work. Keep one authoritative copy of each rule and update
README navigation when adding content.

Before changing an existing knowledge ID, operation or field, run
`python3 scripts/impact.py <it>` to see what depends on it.

Run the [docs checks](docs/governances/artifact-driven/runbooks/check.md) and the checks
appropriate to the changed behavior. Report actual results and limits;
distinguish static checks, runtime observations and human approval.

Push, open a pull request, merge or deploy only when requested.
