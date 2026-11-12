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

## Check the explanation

1. Separate what you observed from what you infer. State a cause as a
   hypothesis, with the evidence that supports it and any evidence that
   conflicts with it.
2. Name the observation that would support or reject the hypothesis. Choose
   the smallest read-only check that distinguishes it from plausible
   alternatives. Trace the failing request across the relevant boundaries;
   do not infer a cause only from the last error.
3. Compare each check's result with that prediction. If the result
   contradicts the hypothesis, revise it before proposing a fix.
   When the available checks cannot distinguish the causes, report the
   alternatives and the missing evidence.
4. If reproduction or instrumentation needs a write, hand the proposed check
   to the coordinator for the affected owner. Keep triage read-only; an
   implementer can run the authorized check in an isolated environment.

For an [incident](../../../docs/governances/artifact-driven/workflow.md#an-incident),
send the evidence and any urgent mitigation need to the coordinator at once.
State what remains uncertain. Do not wait for a complete diagnosis before
this handoff.

## Report

1. What happened, with the evidence and where it came from.
2. The ID it breaks, or "gap" with the rule or scenario that is missing, and
   the scenarios to test again that `python3 scripts/impact.py <ID>` lists.
3. The likely cause, the checks that support or reject it, and the uncertainty
   or alternatives that remain.
4. The proposed next step: a knowledge change, a code fix, further evidence,
   incident mitigation through its owner, or "not a defect".
