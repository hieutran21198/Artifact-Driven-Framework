---
name: software-knowledge
description: Add or change software knowledge - a goal, a flow, an artifact rule, an OpenAPI contract, a client page, or a new artifact - and check it. Use whenever a change touches requirements, specifications or contracts, before any code is written for it.
---

# Software knowledge

Change the knowledge first; code follows it. The rules are in
[Knowledge](../../../docs/governances/artifact-driven/knowledge.md). The steps are in the
runbooks. This skill picks the runbook and does not restate either.

## Pick the runbook

| The change | Runbook |
| --- | --- |
| A business need or its success criteria | [goal](../../../docs/governances/artifact-driven/runbooks/goal.md) |
| Behavior that crosses artifacts or containers | [flow](../../../docs/governances/artifact-driven/runbooks/flow.md) |
| A rule, the model or the lifecycle of one domain | [artifact rule](../../../docs/governances/artifact-driven/runbooks/artifact-rule.md) |
| An endpoint | [contract](../../../docs/governances/artifact-driven/runbooks/contract.md) |
| What a client needs from an artifact's responses | [client](../../../docs/governances/artifact-driven/runbooks/client.md) |
| A system-wide requirement, actor or term | [system](../../../docs/governances/artifact-driven/runbooks/system.md) |
| A release report for the client | [release](../../../docs/governances/artifact-driven/runbooks/release.md) |
| The first knowledge of a domain | [new artifact](../../../docs/governances/artifact-driven/runbooks/new-artifact.md) |

A change that spans several rows runs them top down: goal, flow, artifact rule,
contract, client.

## Always

1. Read the issue and the pages it links. Read the sample the runbook names.
   Before changing an existing ID, operation or field, run
   `python3 scripts/impact.py <it>` to see what depends on it.
2. Follow the runbook step by step.
3. Run [Check the docs](../../../docs/governances/artifact-driven/runbooks/check.md) and report each check's result.
4. Report what changed, the IDs added or changed, and any open question you
   wrote into a page instead of guessing.

Do not commit to client repositories, and do not push, merge or deploy.
