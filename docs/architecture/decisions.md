# Decisions

Why the knowledge and the code of a workspace are shaped the way they are:
each decision, what it was chosen over, and what it costs. The how-we-work
page labels each step with the practice it uses; this page says why that
practice. Two more decisions are in the
[governance decisions](../governances/artifact-driven/decisions.md): the
contract format, and asking before writing. Revisit a decision when its
"Revisit when" comes true, and record the new one here.

## One artifact for each domain

**Decision.** The knowledge is split into artifacts, one for each business
domain in the [domain map](domain-map.md). Each artifact is served by one
service. Inside a service, the domains have no module walls between them.

**Context.** A rule needs one owner who approves a change to it, and a reader
needs one place to find it. When the knowledge is split by screen or by
service, a rule shows up wherever it is used.

**Options.**

| Option | For | Against |
| --- | --- | --- |
| One artifact for each domain (chosen) | Each rule has one home and one owner; the code is split the same way | The team agrees on the domain boundaries first; a wrong boundary moves IDs later |
| One page for each feature or screen | Matches how a product owner talks about the product | A rule that two features use is written twice |
| One page for each service | Matches what is deployed | A domain that moves to another service moves its knowledge; a service with many domains becomes one long page |
| Full tactical Domain-Driven Design: aggregates, domain events, modules | A rich model of each domain | Walls and events inside one service add code that a service of this size does not need ([architecture](README.md#direction)) |

**Costs.** The domain map must be kept. A boundary that changes follows the
[move runbook](../governances/artifact-driven/runbooks/move.md).

**Revisit when** one domain must be served by more than one service.

## Flows written as examples

**Decision.** Behavior that crosses artifacts is a flow. Its scenarios are rows
of Given, When and Then. Each row names the operation it calls and cites the
rules it covers.

**Context.** A product owner checks behavior without reading code, and a
developer writes a test from the same text.

**Options.**

| Option | For | Against |
| --- | --- | --- |
| Examples in a table (chosen) | The business can read each row; one test for each row; the checks find a row that names no operation | A long flow has many rows |
| Use cases in free text | Fast to write | Nothing to point a test or a check at |
| Feature files run by a tool, such as Cucumber | The examples run as tests | A runner and step code for each language; the scripts would have to run tests |

**Costs.** Every scenario names an operation, a trigger or a command, or the
docs check fails.

**Revisit when** a team wants its examples to run as tests and accepts a runner
for each stack.

## Contracts before code

**Decision.** Every operation that a client or another service calls is
written in a contract, and its owner approves it, before the code is written.

**Context.** Services and apps are built at the same time by different people.
A released app cannot be changed when a response changes under it.

**Options.**

| Option | For | Against |
| --- | --- | --- |
| Contract first (chosen) | Both sides build at once; a breaking change shows in review, before release | The shape is decided before anyone has tried the code |
| Code first, contract generated from it | The contract always matches the code | Whoever writes code first decides the shape; a break shows only after release |
| No contract, only what each app reads | Less to write | No single shape to check a change against |

**Costs.** A change of shape is a knowledge change first. The file format is a
separate decision ([OpenAPI](../governances/artifact-driven/decisions.md#openapi-holds-every-contract-also-what-is-not-http)).

**Revisit when** one team builds every client and service and ships them
together.

## Test styles are suggested, not required

**Decision.** The rules ask for two things only: each test names the ID it
proves, and each layer is proved by its kind of test (end-to-end for a goal,
service tests for a flow, unit tests for a rule). BDD, TDD and contract tests
are suggestions, and the how-we-work page marks them so.

**Context.** Each part has its own stack and its own habits. The scan needs only
the ID in the test.

**Options.**

| Option | For | Against |
| --- | --- | --- |
| Require only the ID and the kind of test (chosen) | Works with any test framework and any habit | How good the tests are depends on the team |
| Require one style, such as BDD everywhere | Every part looks the same | A tool for every stack; a team that tests well another way breaks the rule |

**Costs.** A test that names an ID but checks little still counts. The reviewer
reads the tests, not only the count.

**Revisit when** reviews keep finding tests that name an ID and do not check it.

## Knowledge as files in the repository

**Decision.** The knowledge is Markdown and OpenAPI files in a Git repository.
It changes on branches, is reviewed like code, and the scripts check it.

**Context.** The knowledge changes with the code and must be reviewed by the
same people. Coding agents read files.

**Options.**

| Option | For | Against |
| --- | --- | --- |
| Files in Git (chosen) | The same review, history and checks as the code; agents and scripts read it; no licence | A reader who does not use Git reads it through the knowledge site or the project tracker |
| A wiki | Anyone edits it | No review before a change, no checks; it falls behind the code |
| A requirements tool | Links between requirements built in | A cost, a second place to keep, and agents cannot read it easily |

**Costs.** A product owner who does not use Git reads through the knowledge
site, and approves on the pull request, or on the issue when the knowledge has
no pull requests ([approval of knowledge](../governances/artifact-driven/README.md#approval-of-knowledge)).

**Revisit when** the people who approve knowledge cannot review it in a pull
request or on the site.

## IDs named in tests, read as text

**Decision.** Each rule, scenario and criterion has an ID. The test that proves
it names the ID. The scripts find the IDs by reading the files; they never
build or run the tests.

**Context.** Coverage and impact must work for every language of every part,
without its build tools.

**Options.**

| Option | For | Against |
| --- | --- | --- |
| The ID in the test's text (chosen) | Any language; no build; fast | A named ID is not a passing test: coverage counts names, not results |
| Links kept in a test-management tool | Results and links in one place | A second place to keep; links are made by hand and fall behind |
| Run the tests and read their reports | Knows which tests pass | Needs the toolchain of every stack; slow |

**Costs.** Coverage says which IDs a test names, not that the code is right.
The pages that show coverage say so.

**Revisit when** a team needs pass or fail in its coverage. Then the results of
CI feed it; the scripts still do not run tests.

## One owner for each fact, citations point down

**Decision.** Each fact has one page that owns it; every other page cites its
ID. A goal cites flows, a flow cites artifacts, and never the other way.

**Context.** Two copies of a fact drift apart. A change must find everything
that relies on the fact it changes.

**Options.**

| Option | For | Against |
| --- | --- | --- |
| One owner, cite down (chosen) | A change edits one page; the impact traces up from the cited ID | A reader follows links to read a whole flow |
| Copy a fact where it is needed | Each page reads on its own | Copies drift, and the impact cannot find them |
| Links both ways | Each page lists who uses it | A rule changes when a goal that uses it changes |

**Costs.** Readers follow links to read a whole flow.

**Revisit when** readers cannot follow a change without opening many pages.
Then the knowledge site shows the cited text; the pages still do not copy it.

Return to [architecture](README.md).
