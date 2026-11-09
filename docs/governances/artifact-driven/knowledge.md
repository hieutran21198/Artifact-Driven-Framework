# Knowledge

How [software knowledge](../../software-knowledges/README.md) is organized.
The [reference pass](https://github.com/hieutran21198/Artifact-Driven-Framework/blob/main/template/docs/software-knowledges/goals/borrow-a-book.md), from system
down to the `book` and `member` artifacts, shows the established scenario format. Where
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
  coordinates artifacts belongs to a flow. Choose a business policy owner by
  responsibility and decision authority, not by the number of data sources.
  Reading external facts alone neither assigns a policy to an artifact nor
  moves it to a flow. Separate the policy from its orchestration; ask the
  affected owners when that boundary is unresolved.
- A goal is a set of flows that reach one outcome. "Goal" means a product goal;
  delivery goals stay on issues.
- An artifact is one business domain from the
  [domain map](../../architecture/domain-map.md). It is a unit of knowledge
  ownership, not a module wall in the code.

## Services

The knowledge holds for one service or for many.

- Each artifact is served by exactly one service, named in the
  [domain map](../../architecture/domain-map.md) and nowhere else; the
  artifact's README links it. A service may serve several artifacts. The owner of that service
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
- Rule dependencies normally point down: a goal cites flows, a flow cites
  artifacts. An artifact never depends on a flow or a goal, and a flow never
  depends on a goal. Same-layer Flow-rule citations are limited
  to [Flow rules](#flow-rules) and require the adoption checks there.
- A goal criterion names the flow scenarios that prove it, in the Proven by
  column of its row. A scenario names the artifact rules and system
  requirements it covers. It may also cover
  Flow rules after the adoption checks pass. Scenarios prove behavior; they
  are not reusable rule definitions.
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

### Before adding a fact

Add a new ID only when the fact passes all four questions. Otherwise leave it
out, or change the ID that already holds it.

1. **Can a break be seen?** A test, a check or a reviewer can show that the
   product breaks it. A fact that nothing can show broken is design and stays
   out of the knowledge.
2. **Is it behavior?** It states what the product does or promises, not where
   something sits on a page or a screen. "The page links the guide" is
   behavior; "the link is the second item of the menu" is layout.
3. **Does it have no owner yet?** When another page owns it, cite that ID. A
   fact that holds for every service, client or page is a system requirement.
4. **Can no ID be widened to hold it?** Widen an existing ID when the change
   keeps its meaning. When the meaning changes, add the new ID and withdraw the
   old one.

The report of the change names, for each new ID, the IDs it was checked
against.

## Flow rules

Before using this authoring method to allocate product IDs, complete the
[adoption checks](runbooks/check.md#flow-rule-adoption) for docs checks, impact
analysis, test references and the knowledge viewer. Keep existing scenarios,
contracts and IDs unchanged until those checks pass. Record an
unsupported rule need on the issue; do not hide it in a scenario or bypass a
check.

### Choose the owner

First state the business decision and identify who has authority to change
it. Keep domain meaning separate from how the application obtains facts and
coordinates work. A cross-boundary policy does not automatically belong to
Flow; using external facts does not automatically make it an artifact rule
either. Ask the affected owners to settle an unclear boundary on the issue
before writing it as established knowledge.

Choosing a rule owner does not require code or model extraction. Conditions
specific to a use case may stay with their legitimate Flow owner. A separate
policy artifact, service or function needs an actual domain responsibility;
an external input alone does not justify it.

Flow owns coordination promises: ordering, atomicity within one service,
retry and recovery across steps. Cite existing domain rules instead of moving
or copying their business meaning into coordination. A goal states the
outcome, not a reusable rule.

### Choose the home and scope

- Start with `## Coordination rules` in `flows/<flow>.md` for rules owned by
  that flow.
- Use `flows/contracts/<interaction>.md` only when multiple flows genuinely
  reuse the same coordination promise. Reuse an existing suitable page first.
  This is a shared Flow specification, not an OpenAPI transport contract.
  Do not create the directory or extract a page for hypothetical reuse.
- State the scope and responsible owner. Each rule row has an ID, a testable
  rule statement and explicit dependencies. Name the interaction or steps the
  scope covers, including limits and failure outcomes when they matter.
- The ID form is `FR-<SCOPE>-<n>`, separate from scenario IDs
  `F-<FLOW>-<n>`. A scope names one local flow or shared interaction, not a
  goal. Check that the scope is unique before allocation; after adoption,
  apply [the life of an ID](#the-life-of-an-id).

### Citations and proof

After adoption, a flow's steps and scenarios may cite local Flow rules or
shared Flow rules at the same layer. A scenario's Covers column names the
rules it proves. This exception does not allow one flow to treat another
flow's scenario as a reusable rule.

A Flow rule may depend on artifact rules and system requirements. It must
not depend on another Flow rule, a scenario or a goal. Do not build Flow-rule
chains. Keep the dependency list explicit and cite facts without restating
them. Goals continue to name scenarios in Proven by; a rule definition alone
is not proof. Tests name the rule or scenario they prove.

## Design links

When relevant design exists, a Flow links to the client-owned design material
outside the software-knowledge graph for navigation. Name the
owning client and, when useful, the step or scenario it illustrates. Screens,
copy and layout stay with that client's owner at their actual location, such
as the client repository or a design tool. Do not copy them into knowledge,
require a new design folder or ID namespace, or require design for every Flow.
Technical choices and their rationale stay in architecture decisions.

Such a design link is not a rule dependency, an approval or execution
evidence. Keep it separate from Covers, Proven by and rule dependency lists.
Verify that it points to the intended design; if access or location is unknown,
ask the owner on the issue rather than inventing a link. This does not change
how links between software-knowledge pages establish dependencies or the
citation direction those pages must follow ([Citations](#citations)).

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

Except for a conflict with running code (above), a question is asked before it
is written: it reaches a page only when its branch merges with it still open
([questions](workflow.md#questions)).

## Artifact files

| File | Holds |
| --- | --- |
| `README.md` | What the artifact owns, its rule prefix, a link to the domain map for the service that serves it, and links |
| `specification.md` | Model, rules and lifecycle; no service, client or flow |
| `openapi.yaml` | The HTTP contract of the artifact's own endpoints, internal ones included |
| `service.md` | The domain contract the serving service provides: the `Writer` and `Reader` interfaces and their operations; no packages, types or tables. Only when the service has such interfaces, as a service with a database does |
| `<client>.md`, one per client in the [configuration](../../../scripts/README.md#configuration) | What that client needs from the artifact, by `operationId`, by payload schema, or by rule ID for a need no response carries; only when it uses the artifact |

An artifact is never split per service or per client. Client pages cite rule IDs and
`operationId`s; they never restate rules. Which client calls which operation,
and when, belongs to the flow: each step names its actor and the operation it
calls. Screens belong to the client's owner at their actual design location,
not to the knowledge ([design links](#design-links)). A need on a flow
operation goes on the client page of the artifact that owns the response
schema. A need on a flow payload goes on the client page of the artifact the
payload is about, under the name of the payload schema.

## Contracts

Contracts come first: the OpenAPI contract is written and agreed before the code
that implements it.

- OpenAPI 3.0.3, in YAML, also for what is not HTTP
  ([decision](decisions.md#openapi-holds-every-contract-also-what-is-not-http)).
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
- A command that is not an HTTP request, such as a CLI command or an action
  in a client's interface, is declared under `x-commands` of the contract of
  the artifact or flow it belongs to, by name in camelCase, with its caller
  and its input and output schemas. A scenario names the command as it names
  an operation. A change keeps what callers pass and read (SYS-4).
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
| System | Context: actors, clients, services, gateway, external systems. Nobody draws how goals, flows and artifacts link: the [knowledge site](../../../scripts/README.md#knowledge-site) shows it from the links. |
| Goal | The flows that reach the goal, as a `flowchart`. |
| Flow | A `sequenceDiagram` with each service it crosses as a participant, `rect` for each transaction inside one service, and `alt` for failures. A `flowchart` when it branches a lot. |
| Artifact | A `classDiagram` of entities and their behavior methods, without fields. A `stateDiagram-v2` when an entity has a lifecycle. |

Return to [Artifact Driven](README.md).
