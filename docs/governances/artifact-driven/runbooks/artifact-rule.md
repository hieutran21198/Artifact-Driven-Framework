# Change an artifact rule

Use when a rule, the model or the lifecycle of one domain changes.

Sample: [book specification](../../../software-knowledges/artifacts/book/specification.md).

## Files

1. `artifacts/<artifact>/specification.md` in the knowledge folder
2. `openapi.yaml` of the artifact, when the rule shows in the contract
3. The client pages that cite the rule
4. The flows that cite the rule

## Steps

1. Add the rule to the rules table with the next free ID, using the prefix in
   the artifact's README. Never reuse or renumber an ID; mark a dropped rule as
   withdrawn ([the life of an ID](../knowledge.md#the-life-of-an-id)).
2. Name the error the rule returns, if any. Write a value the rule depends
   on, a table of regions when it differs by region, and whether a change
   applies to existing records
   ([rules with values](../knowledge.md#rules-with-values)).
3. Update the `classDiagram` when a behavior is added or removed, and the
   `stateDiagram-v2` when the lifecycle changes.
4. Keep the page free of services, clients and flows: no screens, no endpoints, no
   "during checkout".
5. Run [impact](../../../../scripts/README.md#impact) on the rule's ID (`python3 scripts/impact.py <ID>`) and update
   every scenario, operation and client page it lists.
6. If the contract changes, follow [contract](contract.md).

Then [check the docs](check.md).

Return to [runbooks](README.md).
