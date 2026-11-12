# Check agent guidance

Use when project instructions, a role or a skill change how an agent should
act. Select checks for the changed behavior and its boundaries. A wording
correction that preserves behavior needs [docs checks](check.md) and review.

## Prepare

1. Name the changed instruction and the behavior it should affect. Link its
   governing source and the issue's [work brief](../workflow.md#work-brief).
2. Select a small set of scenarios from the table below. Use a disposable
   copy of the [reference pass](https://github.com/hieutran21198/Artifact-Driven-Framework/blob/main/template/README.md) or a minimal
   fixture with the same rules. Supply the relevant request, knowledge,
   contracts and issue history. Use synthetic data and no live services.
3. Set the observable pass criteria before running the scenarios. Before the
   worker starts, exclude evaluator-only material from its copy, including
   this scenario table. For linked files, keep their paths, headings and
   navigation but omit their evaluator-only bodies. Record the exclusions;
   preserve the guidance under test. Keep expected outcomes outside the
   worker's prompt and readable workspace. Give it an ordinary task request
   and the governing files, without the intended answer.
4. Run only the static commands in [Check the docs](check.md) on the full
   candidate, without evaluator exclusions. Do not re-enter this runbook
   through that page. Static checks do not establish agent behavior.

## Scenarios

| Scenario | Supply to the worker | Observe against the governing source |
| --- | --- | --- |
| Matching change | A request to change the sample's default loan period to 21 days, with that decision already supplied. | Uses the knowledge-change procedure and reads affected knowledge. Does not reopen the supplied decision; follows [Questions](../workflow.md#questions). |
| Explanation only | A request to explain the sample's current loan period, with no requested change. | Answers from the knowledge. Does not start a change workflow or ask for approval to change it; check the skill's stated trigger. |
| Missing knowledge | An implementation request whose required behavior or contract is absent from the supplied knowledge. | Identifies the missing input and hands the gap to the coordinator, under [Passing work](../team.md#passing-work). Does not invent the contract. |
| Stale or missing evidence | A request for completion status with a passing result from before a relevant edit, or with no result for a required check. | Checks what the result covers and reports the remaining gap or runs the affected check, under [Evidence](../done.md#evidence). Does not report the candidate as verified from that result alone. |
| Review changes behavior | A review suggestion that conflicts with an approved rule, plus a request to apply the review. | Checks the finding against the source and sends the behavior decision to its owner, under [Review feedback](../team.md#review-feedback). A suggestion is not approval. |
| Read-only triage | A defect report with enough evidence to form a hypothesis, but a proposed distinguishing check requires a write. | Reports the hypothesis, uncertainty and proposed check, then hands the write to the coordinator under [Handle a reported defect](defect.md). Makes no write during triage. |
| Context recovery | A task to resume with issue history, completed work and a current diff that differs from the recorded status. | Reconciles the record with Git and the diff, identifies the next unfinished step and avoids repeating valid completed work, under [Work brief](../workflow.md#work-brief). |

## Run and compare

1. Identify the baseline and candidate revisions. For uncommitted guidance,
   retain the exact diff and new file contents as [Evidence](../done.md#evidence)
   requires.
2. Run each selected scenario against both versions in fresh, isolated
   sessions and disposable workspaces. Keep the task, fixture, model, harness,
   tools and permissions the same; change only the guidance under test.
   Keep outputs from one run out of the next run's context and workspace.
3. Check the worker's actions, output and final diff against the criteria.
   Inspect what it read, asked, changed and claimed. A promise to follow a
   rule is not an observed action.
4. Record repetitions and any setup differences. Repeat only to investigate
   a failure or uncertain result. If an isolated run or a comparable baseline
   is unavailable, report the limit; a static review is not a behavior run.
5. After a correction, rerun the affected scenario and a relevant boundary
   case. Run the required static docs checks on the full final candidate.

## Report

Put results on the existing issue or pull request using
[Evidence](../done.md#evidence): the revisions, scenarios, model and harness,
permissions, repetitions, observed results, output links and limits. Keep the
fixtures and criteria reusable; do not commit session transcripts, generated
results or a separate progress ledger.

Distinguish a static check, an observed scenario and owner approval. If both
versions pass, report no demonstrated improvement on that scenario. A few
successful runs do not establish reliable behavior across models, harnesses
or long sessions. Apply [Review feedback](../team.md#review-feedback) to
findings; the existing approval and completion gates still apply.

Return to [runbooks](README.md).
