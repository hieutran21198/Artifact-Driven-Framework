---
name: defect-triage
description: Triage a reported defect - gather evidence before any fix, find the goal criterion, flow scenario or artifact rule it breaks, and say whether the knowledge has a gap. Use when someone reports a bug, wrong behavior, a client complaint or a production incident.
---

# Defect triage

Follow [Handle a reported defect](../../../docs/governances/artifact-driven/runbooks/defect.md). This skill adds how to gather
evidence safely.

## Evidence first

- Reproduce or observe before you explain. Read the request, the response,
  the logs and the data from the environment where it happened.
- Use read-only access only: the project's read-only queries of logs and
  infrastructure, and SQL `SELECT`. The project instructions name the
  environments and how to reach them.
- Find the commit that runs in that environment before reading code; the
  default branch may differ from what is deployed.
- Never change data, configuration or code while triaging.

## Report

1. What happened, with the evidence and where it came from.
2. The ID it breaks, or "gap" with the rule or scenario that is missing, and
   the scenarios to test again that `python3 scripts/impact.py <ID>` lists.
3. The likely cause, and how sure you are.
4. The proposed next step: a knowledge change, a code fix, or "not a defect".
