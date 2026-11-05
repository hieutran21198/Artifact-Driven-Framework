# Project instructions

A template. Copy it to the project root and fill in what the project adds:
its repositories, its code standards, its code skill and how it deploys.

## Start with the governing sources

Read the [repository README](README.md) and the README of each directory you
change. Before changing an endpoint, read how the clients call it, through the
client pages of the artifact and, when needed, the client code.

## Scope

- Do not commit to client repositories. Client changes go out as written
  handoffs on the issue.

## Knowledge and delivery

Read [Artifact Driven](docs/artifact-driven/README.md) for how knowledge leads
the code. Follow its [knowledge rules](docs/artifact-driven/knowledge.md),
[workflow](docs/artifact-driven/workflow.md) and
[definition of done](docs/artifact-driven/done.md).

Keep changes, tasks, progress, discussion and evidence on issues and pull
requests. The repository holds established knowledge and code. Do not create
change or task ledgers in the repository. Issue closure is not approval. A
missing contract, approval or evidence stays an explicit gap; do not invent it
or weaken a gate.

## Team and skills

Work as the [team](docs/artifact-driven/team.md): the main session is the
coordinator and hands each step to its agent in
[.agents/agents](.agents/agents/README.md). The skills are
[software-knowledge](.agents/skills/software-knowledge/SKILL.md) for knowledge
and contracts and [defect-triage](.agents/skills/defect-triage/SKILL.md) for
reported defects. The project adds its own code skill for the implementer.

## Change and verify

Preserve unrelated work. Keep one authoritative copy of each rule and update
README navigation when adding content.

Before changing an existing knowledge ID, operation or field, run
`python3 scripts/impact.py <it>` to see what depends on it.

Run the checks in [Check the docs](docs/artifact-driven/runbooks/check.md)
and the checks appropriate to the changed behavior. Report actual results and
limits; distinguish static checks, runtime observations and human approval.

Push, open a pull request, merge or deploy only when the approver asks.
