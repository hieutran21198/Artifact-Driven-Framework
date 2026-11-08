# Glossary

Each term is defined once, here. Other pages use it without restating it.

| Term | Meaning |
| --- | --- |
| Framework | The rules, the scripts and `install.sh` that this repository releases. |
| Workspace | A repository that `install.sh` creates for one project. It holds the project's knowledge and runs its own copy of the scripts. |
| Sample | The knowledge of a small library lending service, from system down to client needs, that a new workspace starts with. |
| Shared files | The files every workspace gets as the framework has them: the rules, the agent resources, the scripts and the README of each place where parts are cloned. |
| Knowledge folder | The folder of a workspace that holds its system, goals, flows and artifacts, as its configuration names. |
| Configuration | The file `artifact-driven.json` at the root of a workspace. |
| Root | The folder of a workspace that holds its configuration. |
| Knowledge ID | The ID of a system requirement, a goal criterion, a flow scenario or an artifact rule. |
| Prefix | The part of a knowledge ID before its number, such as `KN` or `G-GATE`. |
| Withdrawn ID | A knowledge ID whose row says `Withdrawn` in place of its text. |
| Operation | An `operationId` of a contract, a trigger under `x-triggers` or a command under `x-commands`. |
| Unit | One thing in the knowledge that cites or is cited: a row with a knowledge ID, an operation, a contract schema, a section of a client page, or a page. |
| Citation | A unit that names another unit: a knowledge ID, an operation in backticks, a schema by `$ref`, or a link from a page to a page of a lower layer. |
| Open question | One item under `## Open questions` of a knowledge page. |
| Part | A service, a client or the end-to-end tests of a workspace, as the configuration names them. |
| Test file | A file of a part that the part's tests setting selects. |
| Named | A knowledge ID is named when a test file holds it in its text. |
| Check | A script that finds broken knowledge or broken tests and fails when it finds them. |
| Gate | The checks that a pull request into the default branch must pass. |
| Blast radius | What a change to one unit affects, counted by kind. |
| Landing page | The canonical reading path at `index.html`, which introduces the framework and leads to its reference details and the separate tracker. |
| Compatibility entrypoint | A former reading-page URL that leads to the matching topic or reference in the canonical reading path, including when it has an old hash link. |
| Project tracker | The page `tracker/index.html` of the framework, which shows the coverage and the knowledge site of a workspace at a ref, for readers who do not read the repository. |
| Coverage | The share of the knowledge IDs a goal relies on that tests name. |

Return to [system](README.md).
