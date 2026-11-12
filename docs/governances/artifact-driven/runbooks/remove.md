# Remove an operation

Use when an operation, or an old version of it, should leave the service that
serves it.
Removing an operation is breaking (SYS-6 in the reference pass).

## Files

1. The contract that holds the operation
2. The flows whose scenarios name it

## Steps

1. Open an issue. Mark the operation `deprecated: true` in the contract, with
   the operation that replaces it, if any.
2. Get evidence of who still calls it: production logs by path, client
   version and calling service, over at least the last 90 days. The evidence goes on the issue.
3. The owner of the serving service decides on the issue. Remove the
   operation only when no other service and no supported client version
   calls it
   ([supported client versions](../../../software-knowledges/system/context.md#supported-client-versions))
   and the logs show no call for the last 30 days.
4. Before removing it, run [impact](../../../../scripts/README.md#impact)
   on it. Remove it from the contract and update all active references,
   including scenarios, diagrams and tests. Delete a scenario left with no
   operation and update the criteria that cite it. Never reuse its ID.
5. After the deploy, watch the responses for the removed path, and record on
   the issue that nothing still calls it.

Then [check the docs](check.md).

Return to [runbooks](README.md).
