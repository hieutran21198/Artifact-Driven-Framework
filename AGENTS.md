# Project instructions

## Start with the governing sources

Read the [repository README](README.md), [contributing guide](CONTRIBUTING.md)
and the README of each directory you change. For backend code, also read the
backend's own agent instructions under [services](services/README.md). Before
changing an endpoint, read how the [client applications](apps/README.md) call
it. Inspect nearby code and existing checks before choosing a design. Reload
affected instructions after context loss or source changes.

The [architecture](docs/architecture/README.md) is the agreed direction.

## Scope

- Backend only. Do not commit to the client repositories under `apps/`. Client
  changes go out as written handoffs.
- One deployable, split by domain inside it. Do not add bounded contexts,
  module walls, events between domains or a second Go module.

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
[Go](docs/coding-standards/golang/README.md) standards before implementation and
review. Cite rule IDs instead of copying their text.

Work as the [team](docs/governances/artifact-driven/team.md): the main session is
the coordinator and hands each step to its agent in
[.agents/agents](.agents/agents/README.md). The skills are
[software-knowledge](.agents/skills/software-knowledge/SKILL.md) for knowledge
and contracts, [defect-triage](.agents/skills/defect-triage/SKILL.md) for
reported defects, and [backend-service](.agents/skills/backend-service/SKILL.md)
for backend code.

## Change and verify

Use the branch, scope and commit conventions in [Contributing](CONTRIBUTING.md).
Preserve unrelated work. Keep one authoritative copy of each rule and update
README navigation when adding content.

Before changing an existing knowledge ID, operation or field, run
`python3 scripts/impact.py <it>` to see what depends on it.

Run `python3 scripts/check_structure.py`, `git diff --check` and the checks
appropriate to the changed behavior. Report actual results and limits;
distinguish static checks, runtime observations and human approval.

Push, open a pull request, merge or deploy only when requested.
