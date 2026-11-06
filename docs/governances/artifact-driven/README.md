# Artifact Driven

Artifact Driven is how a team builds software from knowledge: write and agree
the knowledge first, then build the code that implements it, and keep the code
traceable to the knowledge it implements.

- [Knowledge](knowledge.md): the layers of software knowledge, what each one
  holds, how they cite each other, and the diagrams and contracts they carry.
- [Workflow](workflow.md): from an issue to merged knowledge and code.
- [Team](team.md): the parts the team builds and their owners, the roles that
  do each step, and how work passes between them.
- [Done](done.md): what a change needs before it counts as done.
- [Runbooks](runbooks/README.md): step-by-step ways to change the knowledge.

## Where things live

| Information | Lives in |
| --- | --- |
| Established knowledge: system, goals, flows, artifacts, contracts | [Software knowledge](../../software-knowledges/README.md) in the knowledge repository |
| Code and tests | The repository of each service and client |
| The need, the plan, tasks, status and discussion | Issues, with status Todo, In Progress or Done |
| Review, approval and check results | Code: the pull request of each part. Knowledge: as [Approval of knowledge](#approval-of-knowledge) says |

Each fact has one home. Do not keep plans, task lists or status in the
repository, and do not copy knowledge into issues; link to it.

## Approval of knowledge

The knowledge may live in a local Git repository with no remote, so a
knowledge change may have no pull request. Then:

- Each change is a branch named after its issue.
- The reviewer's report and the check results go on the issue.
- The owners of the parts it touches approve; one of them merges the branch
  into the default branch. The merge commit names the issue, and the issue
  links the merge commit.
- Each code pull request links the issue and the knowledge merge commit.

When the knowledge repository has pull requests, the knowledge change is a
pull request instead, and the owners approve and merge it there.

## Local use

Read the [project instructions](../../../AGENTS.md) first. A change to this
governance is its own reviewed branch. Past issues, pull requests and Git
history keep their original meaning.

Return to [governances](../README.md).
