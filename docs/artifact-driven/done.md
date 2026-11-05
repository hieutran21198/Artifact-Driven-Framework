# Done

A change is done when every item applies and holds. Record on the pull request
which checks ran and what they did not cover.

| ID | Item |
| --- | --- |
| D1 | **Knowledge.** The goal, flows, artifacts and contracts the change touches are written and merged. |
| D2 | **Consistency.** Knowledge, contract, code and tests agree. Every cited ID exists. |
| D3 | **Tests.** Each changed rule and scenario has a test that names its ID and passes. A changed goal criterion has an end-to-end test, or the pull request says why not. |
| D4 | **Checks.** The checks in [Check the docs](runbooks/check.md) and the code repository's own checks pass, including the OpenAPI lint for changed contracts. |
| D5 | **Review.** The pull requests are approved by someone other than the author. |
| D6 | **Delivery.** The code is merged and deployed to the environment the issue names, and someone checked it there. |

D6 covers the backend. When a client must ship a release to use the change,
the handoff and that delivery go on their own issue.

An item that does not apply says why on the pull request. A failed or skipped
check stays visible; do not mark it done.

Return to [Artifact Driven](README.md).
