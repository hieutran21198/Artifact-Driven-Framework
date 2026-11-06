# Add or change a flow

Use when behavior crosses artifacts, services or clients.

Sample: [Borrow a book](../../../software-knowledges/flows/borrow-book.md).

## Files

1. `flows/<flow>.md` in the knowledge folder
2. `flows/<flow>.openapi.yaml`, when the flow owns an endpoint, sends a
   payload that is not an HTTP response, or is started by a trigger
   ([contract](contract.md))
3. `flows/README.md`
4. The goals that use the flow, and the knowledge map

## Steps

1. Write the header: the artifacts it crosses, its contract, its trigger and
   its outcome. The header names no goal: the goal names the flow. A flow a
   worker runs names its
   trigger in backticks, as the contract declares it (`overdueCheck`), and for
   a schedule its time and time zone.
2. Write the steps in order. Say who acts in each step (an actor, a client,
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
3. Draw a `sequenceDiagram`: clients and each service as participants,
   artifacts as participants inside the service that serves them, `rect`
   around each transaction, `alt` for each failure.
4. Write the scenarios as a table with IDs `F-<FLOW>-<n>`: given, when, then,
   and the artifact rules and system requirements each one covers. The When names
   the `operationId` the scenario calls, or the trigger that starts a worker,
   in backticks, so that
   [impact](../../../../scripts/README.md#impact) can trace it. Every goal
   criterion the flow serves needs at least one scenario: add the scenario's
   ID to the Proven by column of that criterion on the goal page. When
   changing a flow, add new IDs and keep old ones; mark a dropped scenario as withdrawn
   instead of deleting it ([the life of an ID](../knowledge.md#the-life-of-an-id)).
   Removing one operation from a scenario that names others keeps the ID; a
   scenario left with no operation is withdrawn.
5. List behavior the flow does not define under `## Open questions`
   ([open questions](../knowledge.md#open-questions)).
6. If a step needs a rule an artifact does not have, add it first:
   [artifact rule](artifact-rule.md).

Then [check the docs](check.md).

Return to [runbooks](README.md).
