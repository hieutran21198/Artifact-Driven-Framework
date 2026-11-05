# Knowledge

How [software knowledge](../software-knowledge/README.md) is organized.
The [reference pass](../software-knowledge/goals/borrow-a-book.md), from system
down to the `book` and `member` artifacts, shows every rule on this page.

## Layers

| Layer | Holds | Code it matches | Tests that prove it |
| --- | --- | --- | --- |
| System | Purpose, actors, containers, external systems, system-wide requirements, glossary, shared contract components | — | — |
| Goal | A business outcome: the need, the actor, success criteria and constraints. No behavior. | The product | End-to-end tests |
| Flow | Behavior that crosses artifacts or containers: trigger, steps, failure branches, the transaction, the outcome | Application commands and queries | Command and unit of work tests |
| Artifact | One domain: model, rules, lifecycle, contract, and how each container uses it | The domain package | Domain unit tests |

- Artifacts are the nodes and flows the edges between them. Knowledge that
  touches two or more artifacts belongs to a flow.
- A goal is a set of flows that reach one outcome. "Goal" means a product goal;
  delivery goals stay on issues.
- An artifact is one business domain. It is a unit of knowledge ownership, not
  a module wall in the code.

## Citations

- System is shared: every layer may cite it.
- Among goals, flows and artifacts, a layer cites only the layers below it: a
  goal cites flows, a flow cites artifacts. An artifact never mentions a flow or
  a goal.
- Each fact has one owner. Other pages cite it by ID and never restate it.
- A contract description cites the rule ID behind a value; it never states a
  rule that has no ID.

| Owner | ID form | Example |
| --- | --- | --- |
| System requirement | `SYS-<n>` | `SYS-4` |
| Goal success criterion | `G-<GOAL>-<n>` | `G-BORROW-2` |
| Flow scenario | `F-<FLOW>-<n>` | `F-BORROW-3` |
| Artifact rule | `<PREFIX>-<n>`, prefix set in the artifact's README | `BK-5` |

IDs never change and are never reused. A test that proves a rule or a scenario
names its ID.

## Knowledge, not evidence

Knowledge says what must hold. It stays true when the code changes and can be
written before the code exists.

- Never write evidence into knowledge: no client code locations (files, lines,
  classes, functions), no observed data (counts, samples, logs), no dates or
  names of an investigation.
- Never write status or plans into knowledge: no "for now", "not implemented
  yet", "later" or "when the app ships". Those belong on the issue.
- A client page says what the backend promises in a response, never what the
  app does with it: "`due_at` is an RFC 3339 time", not "a null hides the
  reminder".
- Evidence goes to the issue or the pull request that the change belongs to.
- When evidence shows that a client depends on something, write the
  dependency as an expectation on the client page, for example
  "`getBook`: `status` is one of the listed values", not where the client
  reads it.

## Artifact files

| File | Holds |
| --- | --- |
| `README.md` | What the artifact owns, its rule prefix, and links |
| `specification.md` | Model, rules and lifecycle; no container or flow |
| `openapi.yaml` | The HTTP contract of the artifact's own endpoints |
| `backend.md` | The domain contract: the `Writer` and `Reader` interfaces and their operations; no packages, types or tables |
| `<client>.md`, one per client in the [configuration](../../scripts/README.md#configuration) | What that client needs from the artifact's responses, by `operationId`; only when it uses the artifact |

An artifact is never split per container. Client pages cite rule IDs and
`operationId`s; they never restate rules. Which client calls which operation,
and when, belongs to the flow: each step names its actor and the operation it
calls. Screens belong to the app team, not to the knowledge. A need on a flow
operation goes on the client page of the artifact that owns the response
schema.

## Contracts

Contracts come first: the OpenAPI contract is written and agreed before the code
that implements it.

- OpenAPI 3.0.3, in YAML.
- `system/openapi.yaml` holds the shared components: the error shape and
  authentication.
- An artifact's `openapi.yaml` holds endpoints of that artifact only.
- An endpoint that crosses artifacts belongs to its flow, in
  `flows/<flow>.openapi.yaml`, and reuses artifact schemas with `$ref`.
- A payload that is not an HTTP response, such as a push notification, an
  email or a deep link, is a schema under `components` of the flow that sends
  it.
- Check with `npx @redocly/cli lint` on the changed files.

## Diagrams

Draw diagrams as the [diagrams standard](../diagrams/README.md) says. A layer
never draws the inside of a lower layer.

| Layer | Diagram |
| --- | --- |
| System | Context: actors, containers, external systems. Knowledge map: goals, flows, artifacts. |
| Goal | The flows that reach the goal, as a `flowchart`. |
| Flow | A `sequenceDiagram`, with `rect` for the transaction and `alt` for failures. A `flowchart` when it branches a lot. |
| Artifact | A `classDiagram` of entities and their behavior methods, without fields. A `stateDiagram-v2` when an entity has a lifecycle. |

Return to [Artifact Driven](README.md).
