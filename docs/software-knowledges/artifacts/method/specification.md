# Method specification

The behavior of the page that shows how a team works with the framework, from
a goal to an artifact. It holds no knowledge of any service or flow.

## Model

The page has three parts in this order: the steps to break a requirement
down, the method behind them, and who does what at each step, as one lane for
each person - the product owner, the solution architect and the developer -
and a column for the diagram and the tests of each step.

## Rules

| ID | Rule | Error |
| --- | --- | --- |
| MTH-1 | The page lists in order the steps to break a requirement down, from the goal to the test that names a rule, each with an example from the sample and a small diagram of that example, such as a sequence for a flow, and a diagram that splits one requirement sentence into the parts of each step. It uses only common technical words. | — |
| MTH-2 | After the steps, the page names the method behind them - domains first, contracts first, a diagram for every layer - and shows how it relates to Domain-Driven Design. Each step that follows a known method carries its name as a label. | — |
| MTH-3 | After the method, the page shows, for each step and on the sample's example, what the product owner, the solution architect and the developer each write, read and decide, and what passes from one to another. Who decides is who approves in the governance: the product owner a goal, the owner of each service the flows, artifacts and contracts it serves. | — |
| MTH-4 | Below the lanes, the page gives the word each person already uses for a layer: a user story for a goal's need, acceptance criteria for its success criteria, a use case for a flow, and a bounded context for an artifact. | — |
| MTH-5 | Withdrawn: moved to SYS-8. | — |
| MTH-6 | Withdrawn: moved to SYS-8. | — |
| MTH-7 | Beside the lanes, each step shows the diagram its layer has and the tests that prove it, as the knowledge rules and Done ask: end-to-end tests for a goal's criteria, tests in each service for a flow's scenarios, domain unit tests for an artifact's rules. A label marks a way of writing those tests that the page suggests and the rules do not ask for, such as BDD for scenarios, TDD for rules and contract tests for what an app reads. | — |
| MTH-8 | Withdrawn. Each step names the known practice it uses (MTH-2); a separate list of practices added nothing. | — |
| MTH-9 | Before the step that writes the goal, the page shows how a vague need is made clear, on the sample's example: what holds today, the options with the IDs each one keeps, changes or adds, then the questions about the option chosen. Each step of the page links the runbook that holds its steps. | — |

Return to [Method](README.md).
