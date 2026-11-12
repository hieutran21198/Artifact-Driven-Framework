# Move or split knowledge

Use when a fact moves to another owner, such as rules moving from one
artifact to a new one, or when a goal, a flow or an artifact splits in two.

## Files

1. The page that owns the fact now, and the page that will own it
2. Every page that [impact](../../../../scripts/README.md#impact) lists for each
   moved ID

## Steps

1. A move changes no behavior. If the meaning changes too, make the move first
   and the change after it, on its own branch.
2. Put each fact in its new owner. Keep its ID when its namespace still fits;
   otherwise allocate a new ID. Follow
   [the life of an ID](../knowledge.md#the-life-of-an-id).
3. Check each moved rule against [the layers](../knowledge.md#layers) and
   [Flow rules](../knowledge.md#flow-rules). Choose ownership by business
   responsibility and decision authority, not by where inputs come from.
   Settle unclear boundaries with the owners before moving a fact. Keep
   domain policy separate from coordination, and do not allocate a Flow-rule
   ID until its adoption checks pass.
4. Run impact on each old ID and point every citation at the new ID: flows,
   contracts and diagrams.
5. Update tests and other active consumers that name an old ID, then remove
   the old row or page. If a consumer cannot be updated, report the blocker
   on the issue instead of leaving stale knowledge behind.
6. The reviewer compares the diff to verify that each moved fact keeps its
   meaning and that no current reference points to the removed location.
   Apply [Done](../done.md) to the affected parts.

Past issues, pull requests and release reports keep the old IDs. A release
report is read at its knowledge tag.

## An artifact moves to another service

The artifact keeps its rules and IDs; the service that serves it changes. It
is an architecture change first: the owners of both services, the gateway
owner and the product owner agree on the issue.

1. Change the service in the [domain map](../../../architecture/domain-map.md).
   For a new service, also add it to
   [context](../../../software-knowledges/system/context.md),
   [services](../../../../services/README.md) and the `services` of
   [artifact-driven.json](../../../../artifact-driven.json). The owner of the
   new service now keeps the artifact.
2. Run impact on each of its rules and operations. Every flow step that used
   the artifact inside one transaction with another artifact of the old
   service now calls the new service after the transaction: write what happens
   when the call fails, and its scenarios ([flow](flow.md)).
3. Keep the operations and their shapes (SYS-4, SYS-6). The gateway routes them
   to the new service; a call that becomes internal gets `x-internal: true`.
4. Moving the stored data is a migration on its own issue: back up the rows,
   make it safe to run twice, and check the count after it runs. Stop writes
   to the artifact in the old service, or copy again, before the gateway
   routes to the new service.

Then [check the docs](check.md).

Return to [runbooks](README.md).
