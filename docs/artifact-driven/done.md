# Done

A change is done when every item applies and holds. Record which checks ran
and what they did not cover on the code pull request, and for a knowledge
change on the issue.

| ID | Item |
| --- | --- |
| D1 | **Knowledge.** The goal, flows, artifacts and contracts the change touches are written and merged. |
| D2 | **Consistency.** Knowledge, contract, code and tests agree. Every cited ID exists, in the docs and in the tests (`check_tests.py`). |
| D3 | **Tests.** Each changed rule and scenario has a test that names its ID and passes. A changed goal criterion has an end-to-end test, or the pull request says why not. A quality scenario is proved by a measurement in the environment the issue names, recorded by ID with its method, load and result. |
| D4 | **Checks.** The checks in [Check the docs](runbooks/check.md) and the code repository's own checks pass, including the OpenAPI lint for changed contracts. |
| D5 | **Review.** A reviewer who is not the author reported on the change, and the approver approved it: the code pull request is approved, and the knowledge branch is merged. When the approver is the author, the reviewer agent's report stands in for a second person, and the pull request or the issue says so. |
| D6 | **Delivery.** The code is merged and deployed to the environment the issue names, and someone checked it there: for a worker, by firing its trigger with a short time; for a webhook, with a call from the external system's sandbox; for a data fix, by the count of rows that break the rule, which is zero. The pull request says how. |
| D7 | **Configuration.** The secrets and parameters the change needs exist in each target environment before the deploy. The pull request lists them by name, never by value. |

D6 and D7 cover the backend and the infrastructure it needs. When a client
must ship a release to use the change, the handoff and that delivery go on
their own issue.

An item that does not apply says why on the pull request or the issue. A
failed or skipped check stays visible; do not mark it done.

Return to [Artifact Driven](README.md).
