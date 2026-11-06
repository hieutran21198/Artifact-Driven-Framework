# Move or split knowledge

Use when a fact moves to another owner, such as rules moving from one
artifact to a new one, or when a goal, a flow or an artifact splits in two.

## Files

1. The page that owns the fact now, and the page that will own it
2. Every page that [impact](../../../../scripts/README.md#impact) lists for each
   moved ID
3. The knowledge map and the indexes

## Steps

1. A move changes no behavior. If the meaning changes too, make the move first
   and the change after it, on its own branch.
2. For each fact, add it to its new owner with a new ID, and turn the old row
   into `Withdrawn: moved to <new ID>.`
   ([the life of an ID](../knowledge.md#the-life-of-an-id)).
3. Check each moved rule against [the layers](../knowledge.md#layers). A rule
   that needs the data of another artifact becomes a flow step and scenario,
   not an artifact rule.
4. Run impact on each old ID and point every citation at the new ID: flows,
   contracts, client pages and diagrams.
5. Open an issue for the tests that name an old ID. They are renamed in the
   same release as the move.
6. The reviewer checks that each withdrawn ID's meaning is carried, unchanged,
   by its new ID. D3 to D7 of [Done](../done.md) do not apply unless tests are
   renamed.

Past issues, pull requests and release reports keep the old IDs. A release
report is read at its knowledge tag.

Then [check the docs](check.md).

Return to [runbooks](README.md).
