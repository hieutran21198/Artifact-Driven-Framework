---
name: software-knowledge
description: Plan, add, change or review proposed software knowledge - system responsibilities, a goal, a flow, an artifact rule or an OpenAPI contract. Use for requested knowledge rewrites and changes to requirements, specifications or contracts before implementation. Explanation-only questions about existing knowledge do not start this change workflow.
---

# Software knowledge

Change the knowledge first; code follows it. The rules are in
[Knowledge](../../../docs/governances/artifact-driven/knowledge.md). The steps are in the
runbooks. This skill picks the runbook and does not restate either.

For planning, follow
[Plan from the outcome and current system](../../../docs/governances/artifact-driven/workflow.md#plan-from-the-outcome-and-current-system)
and prepare the [handoff](../../../docs/governances/artifact-driven/workflow.md#handoffs)
before owner review. For an independent review, use the
[reviewer brief](../../agents/reviewer.md); review does not start authoring.

## Pick the runbook

| The change | Runbook |
| --- | --- |
| A need that is new or still vague | [shape](../../../docs/governances/artifact-driven/runbooks/shape.md) |
| A business need or its success criteria | [goal](../../../docs/governances/artifact-driven/runbooks/goal.md) |
| Behavior that crosses artifacts, services or clients | [flow](../../../docs/governances/artifact-driven/runbooks/flow.md) |
| A rule, the model or the lifecycle of one domain | [artifact rule](../../../docs/governances/artifact-driven/runbooks/artifact-rule.md) |
| An endpoint | [contract](../../../docs/governances/artifact-driven/runbooks/contract.md) |
| A system-wide requirement, actor or term | [system](../../../docs/governances/artifact-driven/runbooks/system.md) |
| A release report for the client | [release](../../../docs/governances/artifact-driven/runbooks/release.md) |
| The first knowledge of a domain | [new artifact](../../../docs/governances/artifact-driven/runbooks/new-artifact.md) |

A change that spans several rows runs them top down: goal, flow, artifact rule,
contract.

## Always

1. Read the request, the issue and the pages it links. Read the sample the
   runbook names.
   Before changing an existing ID, operation or field, run
   `python3 scripts/impact.py <it>` to see what depends on it.
2. Use [Questions](../../../docs/governances/artifact-driven/workflow.md#questions)
   to resolve material gaps before writing. Reuse supplied decisions.
3. For cross-boundary rules, follow
   [Flow rules](../../../docs/governances/artifact-driven/knowledge.md#flow-rules)
   to settle ownership and check adoption before allocating a Flow-rule ID.
   For visual references, follow
   [design links](../../../docs/governances/artifact-driven/knowledge.md#design-links).
4. Follow the runbook step by step. Before adding an ID, apply
   [before adding a fact](../../../docs/governances/artifact-driven/knowledge.md#before-adding-a-fact).
5. Run [Check the docs](../../../docs/governances/artifact-driven/runbooks/check.md) and report each check's result.
6. Report what changed, the IDs added or changed, for each new ID the IDs it
   was checked against, and the questions still open on the issue.

Do not commit to client repositories, and do not push, merge or deploy.
