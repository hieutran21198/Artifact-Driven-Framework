# Handle a reported defect

Use when someone reports wrong behavior.

## Steps

1. Get the evidence first: the request, the response, the logs and the data, from
   the environment where it happened. Do not patch before the cause is clear.
2. Find the knowledge the defect breaks: a goal criterion, a flow scenario or
   an artifact rule. Write its ID on the issue, with the scenarios to test
   again that [impact](../../../scripts/README.md#impact) lists for it.
3. If the knowledge says the reported behavior is correct, it is not a defect:
   answer on the issue and stop, or open a goal change
   ([goal](goal.md)).
4. If the backend meets the ID and the client is wrong, write the handoff for
   the app team on the issue, citing the ID and the client page.
5. If no ID covers the behavior, the knowledge has a gap. Add the rule or the
   scenario first ([artifact rule](artifact-rule.md), [flow](flow.md)), in the
   same pull request as the fix or before it. When the area has no goal or
   flow yet, write a minimal goal and flow first ([goal](goal.md)).
6. The code fix comes with a test that names the ID and fails before the fix.
7. Close the issue only when [Done](../done.md) holds.

Return to [runbooks](README.md).
