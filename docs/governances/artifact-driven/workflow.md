# Workflow

From an issue to merged knowledge and code. [Team](team.md) says which role
does each step.

## Steps

1. **Issue.** An issue states the need: a new goal, a change to one, a
   defect, a change the owner of a part reports, a change an external system forces,
   a production incident, a data fix, or a change that keeps behavior. It
   links the knowledge it touches. The coordinator reads the request and
   existing decisions, then resolves material gaps ([questions](#questions)).
   Status: Todo. The last four follow their own sections below.
2. **Knowledge.** On a branch of the knowledge repository, write the change
   from the top down: goal criteria, then flows, then artifact rules and
   contracts. When the area has no goal or flow yet, write a minimal goal and
   flow first, because clients and testers check behavior by flow. The
   coordinator prepares any needed implementation plan with that knowledge before
   requesting owner review, using the existing issue or pull request. Follow
   [Handoffs](#handoffs) for its scope. The reviewer reports there and the owners
   of the parts it touches approve ([approval of knowledge](README.md#approval-of-knowledge)).
   Status: In Progress.
3. **Code.** In the repository of each part the change touches, implement the
   approved knowledge: each service its contract, the rules of the artifacts
   it serves and its steps of the flows; each client its steps of the flows,
   against the contracts of the operations they call. Tests name the IDs they prove. Each part opens its own pull request
   that links the issue and the knowledge merge commit.
4. **Merge, deploy and release.** Merge each pull request and deploy each
   service, following its deploy procedure: a service that others call first,
   then the services that call it, then the clients. Release each client as
   its owner decides.
5. **Close.** When the change meets [Done](done.md), close the issue. Status:
   Done.

## Plan from the outcome and current system

Start with the user's outcome, intended users or readers, supplied decisions
and explicit scope limits. Read the relevant System → Goal → Flow → Artifact
knowledge, architecture and contracts before choosing files to change. For a
rewrite, design the explanation from the system's purpose and responsibilities;
the old file layout and validation bindings do not determine that design.

Compare that intent with the implementation and affected consumers. Trace
requests, responses and failures through callers, handlers and downstream
operations. Inspect relevant runtime and deployment configuration, local entry
points and shared implementations. Source shows what is implemented; it does
not prove what is deployed or decide what the product ought to do. Separate
agreed responsibility, current behavior, proposals and unresolved decisions.
A partial implementation neither narrows a component's purpose nor proves
that its planned capabilities exist.

Use the comparison to identify the owning boundaries, dependencies and
contradictions. Check who relies on a changed operation, rule, field or page,
including consumers outside the edited files. Explain consequences for their
behavior, compatibility and error handling. Impact scripts help find these
consumers; they do not replace reading them. Inspect enough of the affected
system to support the decision, without expanding into an unrelated audit.

Recommend the smallest change that meets the outcome. Compare materially
different alternatives and their consequences when a choice remains; reuse
settled decisions. Apply [KISS](../../principles/kiss/README.md),
[DRY](../../principles/dry/README.md) and
[YAGNI](../../principles/yagni/README.md) before adding a mechanism. For example,
a missing responsibility in the docs alone does not justify a new service or
registry. Use [Questions](#questions) for uncertainty that changes the design.
Continue independent work while the affected decision stays open.

Keep the plan and source differences on the existing issue or pull request.
Respect work the user explicitly deferred: record its consequences and the
needed follow-up, without performing it or claiming completion. In the scoped
change, repair contradictions and references the change creates or leaves in
its governing explanation. Do not preserve stale wording merely to satisfy an
existing check; a deferred or failed check remains visible under
[Done](done.md#evidence).

## Handoffs

For a knowledge change that requires implementation, include a concise plan in
the existing issue or pull request before requesting owner review. Derive it from
the relevant System → Flow → Artifact knowledge: affected parts and contracts,
integration work, dependency order and checks that will verify the change.
State unresolved decisions rather than treating them as approved. The plan
prepares implementation; it does not authorize unapproved behavior.

Reuse that plan for the implementation handoff. Do not create a new issue, pull
request, repository file, ledger or approval gate solely to hold it.

Give the next role the scope, relevant knowledge and decisions, expected
output and checks. Reuse the request and existing issue or pull request;
no separate brief or progress entry is needed for each step. For steps that
share a file or contract, resolve incompatible inputs before execution.

Record material decisions, blockers and final results on the issue or pull
request. After a handoff or context loss, compare that record with Git and the
current diff before resuming. Do not repeat completed work or treat a status
alone as evidence. Do not add a plan or task ledger to the repository.

## Questions

Ideas, options and questions stay on the issue. The knowledge takes only what
is settled. For a need that is still vague, [shape](runbooks/shape.md) gives
the steps.

1. **Read and reuse decisions.** Read the request, the issue, linked knowledge
   and relevant project conventions before asking. Use answers and approvals
   already supplied within their scope; do not reopen them merely because a
   new step starts.
2. **Ask about material gaps.** Group independent questions into one request
   when their answers change behavior, scope, ownership, a contract or how
   success is checked. Ask in sequence only when a question depends on a
   previous answer. Use concrete situations and say what the answers change.
   State what is unknown, what was checked, the viable options and your
   recommendation. Do not turn an assumption into an agreed rule or ask again
   for a documented fact. A deterministic change within the approved scope
   proceeds without a new design conversation. An answer becomes a draft criterion, scenario or rule.
3. **List what is left.** What that person cannot settle now, or what
   another owner must decide, goes on the issue as a checklist item: the
   question, the IDs it touches and who answers it. When it is answered, tick
   it, write the answer under it, and change the knowledge.
4. **At the merge.** An item still open that names a criterion of a goal, or
   an ID or operation the goal relies on, holds that goal: the branch is not
   merged until it is answered. Every other open item moves to
   `## Open questions` of the page it touches ([open questions](knowledge.md#open-questions)).

## Release report

Before a release reaches production, the product owner and the stakeholders
get a report:

1. **Changes.** For each part in the release, the issues and pull requests
   between the commit that runs in production and its release candidate.
2. **Knowledge.** The full set of knowledge the release touches, from the top:
   the system requirements, then each goal, its flows, and the artifacts and
   contracts they cite. Export it from the knowledge commit that the release
   implements.
3. **Tests.** The checks each pull request records ([Done](done.md)), by the
   IDs they prove.
4. **Limits.** What the pull requests record as not covered, and the parts the
   release depends on that are not released yet, such as a client in store
   review.

[Report a release](runbooks/release.md) gives the steps. The report goes on
the release issue. Tag the knowledge commit with the release name so the
knowledge of each release can be found again.

## Parallel branches

Several issues may be in progress at once, each with one coordinator and one
knowledge branch. The owners of the parts they touch merge one knowledge
branch at a time, in the order they agree. Before a branch is merged, the coordinator merges the latest
default branch into it, runs the checks and impact again for every ID and
operation the branch changes, and asks the reviewer to look again when the
default branch changed a page the branch also changes.

## Small changes

A change that touches at most one artifact or one adapter of one service, or
one client only, makes no breaking change ([contract](runbooks/contract.md)), removes no operation
and crosses no flow may put steps 2 and 3 in one round: write the knowledge
and the code together and review both before merging.

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
3. Within two working days, write any missing rule, scenario and contract,
   and record on the issue what was done out of order.
4. After a data leak, record on the issue which data and which users were
   exposed. The product owner decides whether users or a regulator must be
   told.

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
- Closing an issue is not approval. Approval is the owners' merge of a
  knowledge branch, or an owner's approval of a pull request.
- A removal, a breaking change and a conflict with running code need the
  decision of the owners of the parts they touch, on the issue, before the
  knowledge branch is merged.
- Push, merge and deploy only when asked.

Return to [Artifact Driven](README.md).
