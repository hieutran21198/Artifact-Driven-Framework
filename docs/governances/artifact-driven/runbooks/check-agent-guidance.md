# Check agent guidance

Use checks that address the risk of the changed instruction, role or skill.
Do not require a new evaluation suite for every edit.

## Choose the checks

- Run [docs checks](check.md) and review the changed guidance for consistency.
  This is enough for wording corrections and low-risk procedural changes.
- Run a focused behavior scenario when a change affects permissions, skill
  dispatch, approval decisions, or a known agent failure. Include a relevant
  boundary case, such as an explanation request that must not start edits.
- Compare baseline and candidate runs only when investigating a regression
  or claiming an improvement. Keep the task, model, harness, tools and
  permissions comparable. Use fresh isolated sessions and keep each run's
  output out of the other's context. Both passing means no demonstrated
  improvement.

Existing project gates still apply. If a needed check cannot run, report the
limit; do not label a static review as observed behavior.

## Run a focused scenario

1. Use a disposable copy of the [reference pass](https://github.com/hieutran21198/Artifact-Driven-Framework/blob/main/template/README.md)
   or a minimal fixture. Supply the request, relevant knowledge and decisions.
   Use synthetic data and no live services.
2. Define observable pass criteria before the run. Keep those criteria and
   evaluator-only material outside the worker's readable context, preserving
   the guidance under test. Give the worker an ordinary task, not its answer.
3. Inspect what the worker read, asked, changed and claimed. A promise to
   follow a rule is not an observed action. After a correction, rerun the
   affected case; repeat further only to investigate uncertainty.
4. Report the checked revision, scenario, relevant setup, observed result and
   limits under [Evidence](../done.md#evidence). Reuse the existing issue or
   pull request; do not commit transcripts or a separate evaluation ledger.

For example, test that an explanation-only request makes no edits, that
already supplied decisions are not asked again, or that a reviewer does not
accept a passing test result from before a relevant code change. Choose the
case that exercises the changed guidance, not a fixed checklist of cases.

Run the static commands from [Check the docs](check.md) on the full candidate,
not an evaluator-redacted fixture. Do not recurse between these runbooks.
A few successful runs do not establish reliability across models or long
sessions. Keep observed results separate from owner approval.

Return to [runbooks](README.md).
