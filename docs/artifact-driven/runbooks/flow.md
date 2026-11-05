# Add or change a flow

Use when behavior crosses artifacts or containers.

Sample: [Borrow a book](../../software-knowledge/flows/borrow-book.md).

## Files

1. `flows/<flow>.md` in the knowledge folder
2. `flows/<flow>.openapi.yaml`, when the flow owns an endpoint
   ([contract](contract.md))
3. `flows/README.md`
4. The goals that use the flow, and the knowledge map

## Steps

1. Write the header: the goal it serves, the artifacts it crosses, its
   contract, its trigger and its outcome.
2. Write the steps in order. Say who acts in each step (an actor, a client,
   the backend, or a worker on a schedule or a trigger), which artifact it
   uses, and which steps run in one transaction. Where a client calls the
   backend, name the call by intent first ("the client asks for the book");
   the contract gives it an `operationId` ([contract](contract.md)), and the
   step then names it. Cite artifact rules by ID; do not restate them.
3. Draw a `sequenceDiagram`: clients and the backend as participants, artifacts
   as participants inside the backend, `rect` around the transaction, `alt` for
   each failure.
4. Write the scenarios as a table with IDs `F-<FLOW>-<n>`: given, when, then,
   and the goal criteria and artifact rules each one covers. The When names
   the `operationId` the scenario calls, or the trigger of a worker, so that
   [impact](../../../scripts/README.md#impact) can trace it. Every goal
   criterion the flow serves needs at least one scenario. When changing a
   flow, add new IDs and keep old ones; mark a dropped scenario as withdrawn
   instead of deleting it.
5. List behavior the flow does not define under "Not covered yet". Write
   behavior only, never status or plans.
6. If a step needs a rule an artifact does not have, add it first:
   [artifact rule](artifact-rule.md).

Then [check the docs](check.md).

Return to [runbooks](README.md).
