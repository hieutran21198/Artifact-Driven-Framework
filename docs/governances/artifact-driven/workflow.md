# Workflow

From an issue to merged knowledge and code. [Team](team.md) says which role
does each step.

## Steps

1. **Issue.** An issue states the need: a new goal, a change to one, a
   defect, a change an app team reports, a change an external system forces,
   a production incident, a data fix, or a change that keeps behavior. It
   links the knowledge it touches. Status: Todo. The last four follow their
   own sections below.
2. **Knowledge.** On a branch of the knowledge repository, write the change
   from the top down: goal criteria, then flows, then artifact rules and
   contracts. When the area has no goal or flow yet, write a minimal goal and
   flow first, because clients and testers check behavior by flow. The
   reviewer reports on the issue and the approver approves
   ([approval of knowledge](README.md#approval-of-knowledge)).
   Status: In Progress.
3. **Code.** In the code repository, implement the approved knowledge: the
   contract, the domain rules and the flows. Tests name the IDs they prove.
   Open a pull request that links the issue and the knowledge merge commit.
4. **Merge and deploy.** Merge the code pull request and deploy, following the
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

## Parallel branches

Several issues may be in progress at once, each with one coordinator and one
branch. The approver merges one knowledge branch at a time, in the order the
approver chooses. Before a branch is merged, the coordinator merges the latest
default branch into it, runs the checks and impact again for every ID and
operation the branch changes, and asks the reviewer to look again when the
default branch changed a page the branch also changes.

## Small changes

A change that touches at most one artifact or one adapter, makes no breaking
change ([contract](runbooks/contract.md)), removes no operation and crosses no
flow may put steps 2 and 3 in one round: write the knowledge and the code
together and review both before merging.

## A defect

1. Find the ID the defect breaks: a goal criterion, a flow scenario or an
   artifact rule.
2. If no ID covers the behavior, the knowledge has a gap: add the rule or
   scenario first.
3. Add a test that names the ID and fails, then fix the code.

## An incident

When production leaks personal or internal data, or is down, fix it first:

1. Collect the evidence on the issue ([handle a defect](runbooks/defect.md)),
   with personal data masked.
2. The fix starts from the commit that runs in production. Its test names the
   closest existing ID. The knowledge change, if one is needed, and the code
   are reviewed in one round.
3. Within two working days, write any missing rule, scenario and client need,
   and record on the issue what was done out of order.
4. After a data leak, record on the issue which data and which users were
   exposed. The approver decides whether users or a regulator must be told.

The knowledge change merges into the default branch and appears in the next
release report.

## A change an external system forces

A change that an external system forces on a deadline, such as a provider
changing how it signs its webhook, may write only the flow and the scenarios
it changes, with no goal. The issue records the missing goal. The contract
copies what the system documents ([knowledge](knowledge.md#contracts)).

## A change that keeps behavior

A change that keeps every response, request and rule, such as an index, a
query rewrite or a dependency upgrade, needs no knowledge; D1 of
[Done](done.md) says why. A change that lets a response lag, such as a cache,
adds a scenario saying how stale the response may be.

## A data fix

A change to stored data with no change to the code follows
[fix stored data](runbooks/data-fix.md).

## Rules

- Knowledge leads. Code that changes behavior without matching knowledge is
  incomplete.
- Closing an issue is not approval. Approval is the approver's merge of a
  knowledge branch, or the approval of a pull request.
- A removal, a breaking change and a conflict with running code need the
  approver's decision on the issue before the knowledge branch is merged.
- Push, merge and deploy only when asked.

Return to [Artifact Driven](README.md).
