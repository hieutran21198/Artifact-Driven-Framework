# Runbooks

Step-by-step ways to change [software knowledge](../../software-knowledge/README.md).
The rules they follow are in [Knowledge](../knowledge.md); a runbook never
restates them. Each one points at the reference pass (the `book` and `member`
artifacts) as a sample.

| Runbook | Use it when |
| --- | --- |
| [Change the system](system.md) | A system-wide requirement, actor, container or term is new or changes. |
| [Add or change a goal](goal.md) | A business need is new, or its success criteria change. |
| [Add or change a flow](flow.md) | Behavior crosses artifacts or containers. |
| [Change an artifact rule](artifact-rule.md) | A rule, the model or the lifecycle of one domain changes. |
| [Add or change a contract](contract.md) | An endpoint is new or changes. |
| [Describe a client](client.md) | A client starts to need something from an artifact's responses, or stops needing it. |
| [Start an artifact](new-artifact.md) | A domain gets its first knowledge. |
| [Report a release](release.md) | Before a release reaches production. |
| [Handle a reported defect](defect.md) | Someone reports wrong behavior. |
| [Check the docs](check.md) | Before every pull request that changes docs. |

Work top down: system, goal, then flow, then artifact and contract. Every runbook ends
with [Check the docs](check.md).

Return to [Artifact Driven](../README.md).
