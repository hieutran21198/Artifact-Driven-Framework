# Move or split knowledge

Use when a fact moves to another owner, such as rules moving from one
artifact to a new one, when a goal, a flow or an artifact splits in two,
or when a page changes path without changing ownership.

## Files

1. The page that owns the fact now, and the page that will own it
2. Every page that [impact](../../../../scripts/README.md#impact) lists for each
   moved ID

## Steps

1. A move changes no behavior. If the meaning changes too, make the move first
   and the change after it, on its own branch. Before editing, run impact on
   each moved ID.
2. Check each moved rule against [the layers](../knowledge.md#layers) and
   [Flow rules](../knowledge.md#flow-rules). Choose ownership by business
   responsibility and decision authority, not by where inputs come from.
   Settle unclear boundaries with the owners before moving a fact. Keep
   domain policy separate from coordination, and do not allocate a Flow-rule
   ID until its adoption checks pass.
3. For a path-only move with unchanged ownership and meaning, keep the ID.
   For an ownership move, define the fact at its authoritative destination
   with a new ID and remove the old definition. Never reuse an old ID
   ([the life of an ID](../knowledge.md#the-life-of-an-id)).
4. Update all active references to the destination: pages, links, flows,
   contracts, diagrams, tooling and tests. Remove obsolete material; keep no tombstones, aliases or ledgers.
5. Record any dependent implementation needed on the issue. Implement it
   after knowledge approval and merge; keep existing supported behavior.
6. The reviewer checks that the destination carries each moved fact's meaning
   unchanged and that no active reference needs the old location or ID.
   Apply [Done](../done.md) to each affected part. Git history preserves the
   earlier definitions.

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
