# Done

A change is done when every item applies and holds, for every part it
touches. Record which checks ran and what they did not cover on each pull
request, and for a knowledge change on the issue.

| ID | Item |
| --- | --- |
| D1 | **Knowledge.** The goal, flows, artifacts and contracts the change touches are written and merged. |
| D2 | **Consistency.** Knowledge, contracts, code and tests agree. Every cited ID exists, in the docs and in the tests of each part (`check_tests.py`). |
| D3 | **Tests.** Each changed rule and scenario has a test that names its ID and passes, in the part that implements it. A changed goal criterion has an end-to-end test, or the issue says why not. A quality scenario is proved by a measurement in the environment the issue names, recorded by ID with its method, load and result. |
| D4 | **Checks.** The checks in [Check the docs](runbooks/check.md) and each part's own checks pass, including the OpenAPI lint for changed contracts. |
| D5 | **Review.** A reviewer who is not the author reported on the change, and the owner of each part approved its share: each pull request is approved, and the knowledge branch is merged. When an owner is the author, the reviewer agent's report stands in for a second person, and the pull request or the issue says so. |
| D6 | **Services.** Each service the change touches is merged and deployed to the environment the issue names, and someone checked it there: for a worker, by firing its trigger with a short time; for a webhook, with a call from the external system's sandbox; for a call to another service, with that service deployed in the same environment; for a data fix, by the count of rows that break the rule, which is zero. The pull request says how. |
| D7 | **Configuration.** The secrets and parameters the change needs exist in each target environment before the deploy. The pull request lists them by name, never by value. |
| D8 | **Clients.** Each client the change touches calls the operations its flow steps name, decodes their responses as the contract gives them, handles the errors the contract lists, and is released, or is ready for release with its version on the issue. A client that needs a service change ships after that service is deployed. |

When a client cannot ship with the services, the change stays open until its
release, or the client's release gets its own issue that links this one.

An item that does not apply says why on the pull request or the issue. A
failed or skipped check stays visible; do not mark it done.

## Evidence

Record the checked revision, command or method, actual result and remaining
limits on the issue or pull request, following the
[masking rules](knowledge.md#knowledge-not-evidence). Include environment,
dependency or data details when they affect the result. Record secret names,
never values. Link existing check output instead of copying it.

Several checks can share one revision or tested snapshot. For uncommitted
work, keep one identifiable snapshot with its base commit, diff and new files
for the reported batch, not a copy for each result. Before publishing the
result against a commit, verify that its tested contents match that commit.
Do not retain every intermediate check or snapshot as a progress history.

Make only claims that the evidence supports. A passing test does not prove
every requirement, and a review report does not replace a required runtime
check. For a [defect](workflow.md#a-defect), retain the failing result before
the fix and the passing result after it. The
[incident procedure](workflow.md#an-incident) still applies.

Reuse evidence while its checked code, knowledge, dependencies and relevant
environment remain valid. After a change that affects a result, rerun the
affected checks and the mandatory gates for the candidate being reviewed or
merged. Do not rerun an unchanged check only because another agent or message
now reports its result. State which earlier evidence still applies and why;
an uncertain or missing result stays a gap.

Return to [Artifact Driven](README.md).
