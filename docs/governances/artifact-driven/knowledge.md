# Knowledge

How [software knowledge](../../software-knowledges/README.md) is organized.
The [reference pass](../../software-knowledges/goals/borrow-a-book.md), from system
down to the `book` and `member` artifacts, shows every rule on this page. Where
this page names a `SYS` ID, it is the ID of the reference pass; a project
keeps the same requirements under its own IDs.

## Layers

| Layer | Holds | Code it matches | Tests that prove it |
| --- | --- | --- | --- |
| System | Purpose, actors, services, clients, external systems, system-wide requirements, glossary, shared contract components | — | — |
| Goal | A business outcome: the need, the actor, success criteria and constraints. No behavior. | The product | End-to-end tests, starting at the trigger: a request, a webhook or a worker run |
| Flow | Behavior that crosses artifacts, services or clients: trigger, steps, failure branches, each transaction, the outcome | Application commands and queries, in each service the flow crosses | Command and unit of work tests in each service |
| Artifact | One domain: model, rules, lifecycle, contract, and what each client needs from it | The domain package of the service that serves it | Domain unit tests |

- Artifacts are the nodes and flows the edges between them. Knowledge that
  touches two or more artifacts belongs to a flow.
- A goal is a set of flows that reach one outcome. "Goal" means a product goal;
  delivery goals stay on issues.
- An artifact is one business domain from the
  [domain map](../../architecture/domain-map.md). It is a unit of knowledge
  ownership, not a module wall in the code.

## Services

The knowledge holds for one service or for many.

- Each artifact is served by exactly one service, named in the artifact's
  README. A service may serve several artifacts. The owner of that service
  keeps the artifact ([team](team.md#parts-and-owners)).
- [Context](../../software-knowledges/system/context.md) lists the services,
  the clients and what stands between them, such as an API gateway.
- Each step of a flow names the service that runs it.
- A transaction never spans services. A step that calls another service says
  what happens when the call fails: the caller retries, compensates, or
  leaves the work for the next run. The called operation gives the same
  result when it receives the same call twice (SYS-8 in the reference pass).
- A call between services has a contract, like a call from a client: its
  operation is in the contract of the artifact it serves, marked as internal
  when no client may call it.

## Citations

- System is shared: every layer may cite it.
- Among goals, flows and artifacts, a layer cites only the layers below it: a
  goal cites flows, a flow cites artifacts. An artifact never mentions a flow or
  a goal, and a flow never mentions a goal.
- A goal criterion names the flow scenarios that prove it, in the Proven by
  column of its row. A scenario names only the artifact rules and system
  requirements it covers.
- Each fact has one owner. Other pages cite it by ID and never restate it.
- A contract description cites the rule ID behind a value; it never states a
  rule that has no ID.
- Every statement a test or a data fix can break has an ID. An invariant of
  the model, such as who holds a record, is a row in the rules table, not prose.
- A flow step or scenario states no condition of its own, such as a region,
  a role or a limit; it cites the rule that holds it.

| Owner | ID form | Example |
| --- | --- | --- |
| System requirement | `SYS-<n>` | `SYS-4` |
| Goal success criterion | `G-<GOAL>-<n>` | `G-BORROW-2` |
| Flow scenario | `F-<FLOW>-<n>` | `F-BORROW-3` |
| Artifact rule | `<PREFIX>-<n>`, prefix set in the artifact's README | `BK-5` |

IDs never change and are never reused. A test that proves a rule or a scenario
names its ID.

### The life of an ID

- An ID is fixed when its branch merges into the default branch. Until then it
  is a proposal: when two branches take the same ID, the branch that merges
  second takes the next free ID and renames its citations and tests.
- A goal key is one word of up to eight capital letters, such as `BORROW`.
- A dropped fact keeps its row, with the text replaced by `Withdrawn.` and the
  reason. A moved fact keeps its row as `Withdrawn: moved to MBR-7.` and gets
  a new ID in its new owner ([move or split knowledge](runbooks/move.md)).
- Nothing cites a withdrawn ID except the row that withdraws it.
  `check_docs.py` reports an ID defined twice and a withdrawn ID still cited.

## Rules with values

- A value the business sets, such as a duration, a fee or a limit, is part of
  its rule. When operations may change it without a release, the rule names
  the setting and its default; changing the default is a knowledge change.
- A rule that differs by region (a country, a market, a site) follows the
  system requirement on regions (SYS-7): one ID, a table with a value for each
  region, and the region it uses.
- A rule that changes says whether it applies to existing records or only to
  new ones.
- A quality requirement, such as speed or a rate limit, is a SYS requirement
  when it holds for the whole system, and otherwise a flow scenario whose When
  names the operation and whose Then is a number to meet, such as "p95 under
  800 ms with 50,000 records".

## Knowledge, not evidence

Knowledge says what must hold. It stays true when the code changes and can be
written before the code exists.

- Never write evidence into knowledge: no client code locations (files, lines,
  classes, functions), no observed data (counts, samples, logs), no dates or
  names of an investigation. A target that must hold is knowledge; a number
  measured once is evidence.
- Never write status or plans into knowledge: no "for now", "not implemented
  yet", "later" or "when the app ships". Those belong on the issue.
- A client page says what a service promises in a response, never what the
  client does with it: "`due_at` is an RFC 3339 time", not "a null hides the
  reminder".
- Evidence goes to the issue or the pull request that the change belongs to.
  Evidence never holds personal data: mask names, emails, phone numbers,
  addresses and user IDs before writing it there.
- When evidence shows that a client depends on something, write the
  dependency as an expectation on the client page, for example
  "`getBook`: `status` is one of the listed values", not where the client
  reads it.

## Knowledge and running code

When the running code does something the knowledge would forbid, or the
knowledge would change something released clients rely on, write neither
version as settled:

1. Write an open question on the page, naming the IDs it touches. The evidence
   goes on the issue.
2. The coordinator asks the owners of the parts it touches to choose on the
   issue: the running
   behavior becomes the rule, or the new rule is written and the code change
   gets its own issue, as a breaking change when a supported client relies on
   the behavior (SYS-6).
3. A branch that adds a criterion or a rule with an open conflict is not
   merged until the owners have chosen.

## Open questions

Any knowledge page may end with `## Open questions`: behavior the page does not
define yet, or a decision it waits for. Each question names the IDs it
touches, and holds behavior only, never status or plans. A page above must not
answer a question that a page below leaves open.

## Artifact files

| File | Holds |
| --- | --- |
| `README.md` | What the artifact owns, its rule prefix, the service that serves it, and links |
| `specification.md` | Model, rules and lifecycle; no service, client or flow |
| `openapi.yaml` | The HTTP contract of the artifact's own endpoints, internal ones included |
| `service.md` | The domain contract the serving service provides: the `Writer` and `Reader` interfaces and their operations; no packages, types or tables |
| `<client>.md`, one per client in the [configuration](../../../scripts/README.md#configuration) | What that client needs from the artifact, by `operationId`, by payload schema, or by rule ID for a need no response carries; only when it uses the artifact |

An artifact is never split per service or per client. Client pages cite rule IDs and
`operationId`s; they never restate rules. Which client calls which operation,
and when, belongs to the flow: each step names its actor and the operation it
calls. Screens belong to the client's owner, in the client's repository, not
to the knowledge. A need on a flow
operation goes on the client page of the artifact that owns the response
schema. A need on a flow payload goes on the client page of the artifact the
payload is about, under the name of the payload schema.

## Contracts

Contracts come first: the OpenAPI contract is written and agreed before the code
that implements it.

- OpenAPI 3.0.3, in YAML.
- `system/openapi.yaml` holds the shared components: the error shape and
  authentication.
- An artifact's `openapi.yaml` holds endpoints of that artifact only; the
  service that serves the artifact serves them. An endpoint only other
  services may call carries `x-internal: true`.
- An endpoint that crosses artifacts belongs to its flow, in
  `flows/<flow>.openapi.yaml`, and reuses artifact schemas with `$ref`.
- A payload that is not an HTTP response, such as a push notification, an
  email or a deep link, is a schema under `components` of the flow that sends
  it. An email or a file names its format (HTML, CSV) and its fields in order
  in the schema description.
- A trigger that starts a worker, such as a timer, a schedule or a message
  another service publishes, is declared
  under `x-triggers` of the flow it starts, by name in camelCase, with its
  schedule or time and its input schema. A scenario names the trigger as it
  names an operation. A change keeps the input that triggers already
  scheduled will deliver (SYS-4).
- A message a service publishes to a queue or a topic is a schema under
  `components` of the flow that publishes it, and names its topic in its
  description. Each flow it starts in another service declares it under
  `x-triggers`, by the same name. The publisher sends it after its
  transaction and retries when the send fails; a consumer that receives it
  twice gets the same result (SYS-8). A change keeps what the consumers read
  (SYS-4).
- An endpoint an external system calls, such as a payment webhook, belongs to
  the flow it starts. Its contract copies the request the external system
  documents; it is agreed with that documentation, not designed, and the
  issue links the vendor's version of it.
- A flow contract with no endpoint has `paths: {}`.
- Check with `npx @redocly/cli lint` on the changed files.

## Diagrams

Draw diagrams as the [diagrams standard](../../coding-standards/diagrams/README.md) says. A layer
never draws the inside of a lower layer.

| Layer | Diagram |
| --- | --- |
| System | Context: actors, clients, services, gateway, external systems. Knowledge map: goals, flows, artifacts. |
| Goal | The flows that reach the goal, as a `flowchart`. |
| Flow | A `sequenceDiagram` with each service it crosses as a participant, `rect` for each transaction inside one service, and `alt` for failures. A `flowchart` when it branches a lot. |
| Artifact | A `classDiagram` of entities and their behavior methods, without fields. A `stateDiagram-v2` when an entity has a lifecycle. |

Return to [Artifact Driven](README.md).
