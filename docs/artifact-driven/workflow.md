# Workflow

From an issue to merged knowledge and code. [Team](team.md) says which role
does each step.

## Steps

1. **Issue.** An issue states the need: a new goal, a change to one, a
   defect, or a change an app team reports. It links the knowledge it touches.
   Status: Todo.
2. **Knowledge.** On a branch of this repository, write the change from the
   top down: goal criteria, then flows, then artifact rules and contracts. When
   the area has no goal or flow yet, write a minimal goal and flow first,
   because clients and testers check behavior by flow. Open a pull request and
   get it approved. Status: In Progress.
3. **Code.** In the code repository, implement the approved knowledge: the
   contract, the domain rules and the flows. Tests name the IDs they prove.
   Open a pull request that links the knowledge pull request.
4. **Merge and deploy.** Merge both pull requests and deploy, following the
   project's deploy procedure.
5. **Close.** When the change meets [Done](done.md), close the issue. Status:
   Done.

## Release report

Before a release reaches production, the client gets a report:

1. **Changes.** The issues and pull requests between the commit that runs in
   production and the release candidate.
2. **Knowledge.** The full set of knowledge the release touches, from the top:
   the system requirements, then each goal, its flows, and the artifacts and
   contracts they cite. Export it from the knowledge commit that the release
   implements.
3. **Tests.** The checks each pull request records ([Done](done.md)), by the
   IDs they prove.
4. **Limits.** What the pull requests record as not covered, and the client
   handoffs still open.

[Report a release](runbooks/release.md) gives the steps. The report goes on
the release issue. Tag the knowledge commit with the release name so the
knowledge of each release can be found again.

## Small changes

A change that touches one artifact, makes no breaking change to a contract
([contract](runbooks/contract.md)) and crosses no flow may put steps 2 and 3 in
one round: write the knowledge and the code together and review both before
merging.

## A defect

1. Find the ID the defect breaks: a goal criterion, a flow scenario or an
   artifact rule.
2. If no ID covers the behavior, the knowledge has a gap: add the rule or
   scenario first.
3. Add a test that names the ID and fails, then fix the code.

## Rules

- Knowledge leads. Code that changes behavior without matching knowledge is
  incomplete.
- Closing an issue is not approval. Approval is on the pull request.
- Push, merge and deploy only when asked.

Return to [Artifact Driven](README.md).
