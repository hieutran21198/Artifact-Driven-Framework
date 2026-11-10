# Add or change a flow

Use when behavior crosses artifacts, services or clients.

Sample: [Borrow a book](https://github.com/hieutran21198/Artifact-Driven-Framework/blob/main/template/docs/software-knowledges/flows/borrow-book.md).

## Files

1. `flows/<flow>.md` in the knowledge folder
2. The goals that use the flow

The operations the flow calls go in the contract of the artifact that receives
each call ([contract](contract.md)).

## Steps

1. Identify the owner of each policy and coordination promise using
   [Flow rules](../knowledge.md#flow-rules). Do not choose from data sources
   alone. Ask owners about unresolved boundaries on the issue. Before any
   proposed Flow-rule allocation, complete
   [Flow-rule adoption](check.md#flow-rule-adoption). Use the local
   Coordination rules section first; extract a shared specification only for
   established reuse. Keep scenarios as proof, not rule definitions.
2. Write the header: the artifacts it crosses, the contracts of the
   operations it calls, its trigger and its outcome. The header names no goal: the goal names the flow. A flow a
   worker runs names its
   trigger in backticks, as the contract declares it (`overdueCheck`), and for
   a schedule its time and time zone.
3. Write the steps in order. Say who acts in each step (an actor, a client,
   a service, or a worker of a service on a schedule or a trigger), which
   artifact it uses, and which steps run in one transaction. A transaction
   stays inside one service. Where a client or a service calls a service,
   name the call by intent first ("the client asks for the book");
   the contract gives it an `operationId` ([contract](contract.md)), and the
   step then names it. Cite artifact rules by ID; do not restate them. A step
   states no condition of its own: a region, a role or a limit is a rule,
   cited by ID. Calls to other services and to external systems come after
   the transaction; say what happens when they fail, what the caller receives
   then, and how the same call twice gives the same result. Each call to
   another service gets a scenario where it fails and one where it repeats. For a worker or a webhook, say what happens when
   the same trigger arrives twice (SYS-8). A scheduled worker's scenarios
   cover a run with nothing to do, a failed send, and a run that repeats.
4. Draw a `sequenceDiagram`: clients and each service as participants,
   artifacts as participants inside the service that serves them, `rect`
   around each transaction, `alt` for each failure.
5. Write the scenarios as a table with IDs `F-<FLOW>-<n>`: given, when, then,
   and the artifact rules and system requirements each one covers. After
   Flow-rule adoption, also cite the local or shared Flow rules it proves.
   The When names
   the `operationId` the scenario calls, or the trigger that starts a worker,
   in backticks, so that
   [impact](../../../../scripts/README.md#impact) can trace it. Every goal
   criterion the flow serves needs at least one scenario: add the scenario's
   ID to the Proven by column of that criterion on the goal page. When
   changing a flow, add new IDs and keep old ones; mark a dropped scenario as withdrawn
   instead of deleting it ([the life of an ID](../knowledge.md#the-life-of-an-id)).
   Removing one operation from a scenario that names others keeps the ID; a
   scenario left with no operation is withdrawn.
6. Ask about behavior the flow does not define yet
   ([questions](../workflow.md#questions)). What is still open when the branch
   merges goes under `## Open questions`
   ([open questions](../knowledge.md#open-questions)).
7. If a needed rule is missing, resolve its ownership first. For an artifact
   rule, use [artifact rule](artifact-rule.md). For a Flow rule, apply the
   adoption gate and authoring method above; do not force it into an artifact
   or hide it in a scenario.
8. Link relevant existing design as [design links](../knowledge.md#design-links)
   requires. Identify the client and relevant step or scenario. Verify the
   actual destination; keep visual detail with its owner. If no relevant
   design exists, do not create a placeholder link or require one.

Then [check the docs](check.md).

Return to [runbooks](README.md).
