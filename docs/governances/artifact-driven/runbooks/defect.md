# Handle a reported defect

Use when someone reports wrong behavior, or when knowledge work finds code
that breaks an approved ID.

The defect investigator gathers read-only evidence and reports it. The
coordinator gives experiments that change files or state, and the fix, to the
authorized implementer. Production mitigation follows the
[incident procedure](../workflow.md#an-incident); it need not wait for a
complete root-cause analysis.

## Steps

1. Get the evidence first: the request, response, logs, data and deployed
   commit from the environment where it happened, with personal data masked.
   Reproduce or observe the failure. Compare recent changes and a working
   case; trace the input and output at the boundary where behavior diverges.
2. Find the knowledge the defect breaks: a goal criterion, a flow scenario or
   an artifact rule. Write its ID on the issue, with the scenarios to test
   again that [impact](../../../../scripts/README.md#impact) lists for it.
3. If the knowledge says the reported behavior is correct, it is not a defect:
   answer on the issue and stop, or open a goal change
   ([goal](goal.md)).
4. State a supported hypothesis, the evidence for it, what remains uncertain
   and the smallest check that would distinguish it from another cause.
   Name the part that breaks the ID: a service, or a client that misses its
   step of a flow or misreads the contract of an operation it calls. The fix
   goes to that part's implementer, or, when nobody doing the change has
   access to it, as a handoff to its owner on the issue, citing the ID and the
   `operationId`.
5. If no ID covers the behavior, the knowledge has a gap. Add the rule or the
   scenario first ([artifact rule](artifact-rule.md), [flow](flow.md)), on a
   knowledge branch merged before the fix, or reviewed with the fix in one
   round during an [incident](../workflow.md#an-incident). The code pull
   request links the issue and the knowledge merge commit. When the area has no goal or
   flow yet, write a minimal goal and flow first ([goal](goal.md)).
6. The implementer records the failing test that names the ID, makes the
   smallest supported fix, then records the passing result and affected
   checks as [evidence](../done.md#evidence). If the result contradicts the
   hypothesis, investigate that result before another fix. A client's test
   names the scenario of the step it missed, or the rule the operation
   serves.
7. Close the issue only when [Done](../done.md) holds.

Return to [runbooks](README.md).
