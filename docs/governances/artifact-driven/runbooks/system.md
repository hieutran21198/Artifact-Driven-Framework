# Change the system

Use when a system-wide requirement, an actor, a service, a client, an external system
or a glossary term is new or changes.

Sample: [system](../../../software-knowledges/system/README.md).

## Files

1. `system/requirements.md`, `context.md`, `glossary.md` or `openapi.yaml` in
   the knowledge folder
2. The pages that cite a changed `SYS` ID

## Steps

1. Add a requirement with the next free `SYS-<n>` ID. Never reuse or
   renumber an ID; remove a dropped requirement and update its references
   ([the life of an ID](../knowledge.md#the-life-of-an-id)).
2. A requirement names what must hold for every goal, flow and artifact. It
   names groups and principles, not fields; the contract owns the fields.
3. Update the context diagram when an actor, a service, a client or an external
   system changes.
4. Run [impact](../../../../scripts/README.md#impact) on each changed `SYS` ID and update every page it lists.

Then [check the docs](check.md).

Return to [runbooks](README.md).
