# Artifact Driven

Artifact Driven is how a team builds software from knowledge: write and agree
the knowledge first, then build the code that implements it, and keep the code
traceable to the knowledge it implements.

- [Knowledge](knowledge.md): the layers of software knowledge, what each one
  holds, how they cite each other, and the diagrams and contracts they carry.
- [Workflow](workflow.md): from an issue to merged knowledge and code.
- [Team](team.md): the roles that do each step, and how work passes between
  them.
- [Done](done.md): what a change needs before it counts as done.
- [Runbooks](runbooks/README.md): step-by-step ways to change the knowledge.

## Where things live

| Information | Lives in |
| --- | --- |
| Established knowledge: system, goals, flows, artifacts, contracts | [Software knowledge](../software-knowledge/README.md) in this repository |
| Code and tests | The code repository |
| The need, the plan, tasks, status and discussion | Issues, with status Todo, In Progress or Done |
| Review, approval and check results | The pull request |

Each fact has one home. Do not keep plans, task lists or status in the
repository, and do not copy knowledge into issues; link to it.

## Local use

Read the [project instructions](../../AGENTS.md) first. A change to this
governance is its own reviewed pull request. Past issues, pull requests and Git
history keep their original meaning.

Return to [documentation](../README.md).
