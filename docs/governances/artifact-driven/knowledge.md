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
| Artifact | An agreed knowledge ownership boundary: model, rules, lifecycle and public operation contract | The domain package of the service that serves it | Domain unit tests |

### Content by type

| Type | Allowed content | Keep elsewhere |
| --- | --- | --- |
| System | Purpose, actors, service/client responsibilities, external systems, glossary and requirements that apply system-wide | Domain rules in their Artifact; interaction steps in Flow; health-check details in the owning API or operational docs |
| Goal | Business outcome, actor, success criteria, constraints and links to the scenarios that prove them | Delivery tasks on issues; step-by-step behavior in Flow |
| Flow | Trigger, participating actors/artifacts, interaction steps, transaction boundaries, failure outcomes, scenarios and owned coordination rules | Domain policy in Artifact; API signatures and payloads in the receiving Artifact's contract |
| Artifact specification | Domain model, invariants, business rules and lifecycle | Service deployment/layout in architecture or infrastructure; cross-domain orchestration in Flow |
| Artifact contract | Public operations received, schemas published, inputs, outputs, errors and owned triggers | Narrative coordination in Flow; implementation signatures in code |
| System contract | Shared schema components, such as authentication and error shapes | Domain operations and payloads in their Artifact contracts |
| Design | Screens, copy, layout and UI states in the client-owned design; Flow may link for navigation | Do not copy visual details into knowledge rules |
| Architecture | Domain/service mapping, structural choices and their rationale | Product behavior in knowledge; delivery progress on issues |
| Governance and runbooks | Reusable development, review and operational procedures | Do not place these procedures in product knowledge |
| Issue or pull request | Change plan, questions, owner review/approval, evidence, blockers and results | Current rules stay in knowledge; history stays in Git |

The restrictions in [Knowledge, not evidence](#knowledge-not-evidence) apply
to every knowledge type. Tables and diagrams follow the same ownership as
text; a link does not make forbidden content appropriate for a knowledge page.

- Artifacts are the nodes and flows the edges between them. Knowledge that
  coordinates artifacts belongs to a flow. Choose a business policy owner by
  responsibility and decision authority, not by the number of data sources.
  Reading external facts alone neither assigns a policy to an artifact nor
  moves it to a flow. Separate the policy from its orchestration; ask the
  affected owners when that boundary is unresolved.
- A goal is a set of flows that reach one outcome. "Goal" means a product goal;
  delivery goals stay on issues.
- A domain is a problem area. A bounded context is the scope in which a model
  and its language have a consistent meaning. An Artifact is an agreed
  knowledge ownership boundary. A service is a deployable part.
- The project explicitly selects the mapping between its domains, bounded
  contexts, Artifacts and services in the
  [domain map](../../architecture/domain-map.md). An Artifact may represent a
  bounded context when that model and language boundary is established; its
  folder or page alone does not establish one. This mapping requires no new
  service or module wall.

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
- A scenario links a rule to an operation: the rule in its Covers column,
  the operation in its When column. A contract need not cite rule IDs.
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
- Delete a dropped fact and update all active references. A path-only move
  keeps its ID when ownership and meaning stay the same. An ownership move
  gives the fact a new ID at its destination; remove the old definition and
  update all active references ([move or split knowledge](runbooks/move.md)).
- Git history keeps prior definitions and decisions. Do not add tombstone
  rows, aliases or migration ledgers. Check history before allocating an ID;
  a deleted ID is never free for reuse.
- `check_docs.py` and impact CLI reports reject withdrawn tombstone rows,
  whether cited or not. Complete the cleanup before merging.

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
   keeps its meaning. When the meaning changes, add the new ID, remove the
   old definition and update every active reference.

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

Knowledge holds the current agreed behavior, model and public interfaces.
It can be agreed before implementation, but it is not a record of delivery.

- Do not store or link historical versions, superseded facts, withdrawn/moved
  markers, change logs, investigation evidence, or owner review/approval
  records in knowledge. History is in Git; discussion, evidence and approvals
  belong on the issue or pull request. Link from those records to knowledge,
  not from knowledge to those records.
- Do not put any migration or cutover procedure, compatibility-transition
  plan, temporary bridge, delivery task or progress status in knowledge.
  Reusable procedures belong in governance or operational runbooks;
  change-specific execution belongs on the issue. This does not remove
  executable database migrations needed to build or upgrade a database.
- Remove stale content when replacing it and update direct references in the
  same change. Do not retain a second source of truth or a chain of redirects.
- Product rules that still apply, such as a supported API version or whether
  a new limit applies to existing records, remain knowledge. State the current
  promise, not the history or steps of reaching it.
- Implementation file/line locations, logs, measured counts and investigation
  dates are evidence, not knowledge. A target that must hold is knowledge;
  a value measured once is evidence.
- Mask personal data in issue/PR evidence: names, emails, phone numbers,
  addresses and user IDs. Never include secret values.

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
| `openapi.yaml` | Operations the artifact receives and public payloads it publishes |

An artifact has no other file and is never split per service or per client.

- Which client calls which `operationId`, when, and what happens when the call
  fails belongs to the flow: each step names its actor and the operation it
  calls. The knowledge tracks a client's use at that level only, not field by
  field.
- The use cases of the serving service and its `Writer` and `Reader`
  interfaces live in its code, as the
  [architecture](../../architecture/README.md) says, not in the knowledge.
- Screens belong to the client's owner at their actual design location, not
  to the knowledge ([design links](#design-links)).

## Contracts

Contracts come first: the OpenAPI contract is written and agreed before the code
that implements it.

- OpenAPI 3.0.3, in YAML, also for what is not HTTP
  ([decision](decisions.md#openapi-holds-every-contract-also-what-is-not-http)).
- `system/openapi.yaml` holds the shared components: the error shape and
  authentication.
- Every operation belongs to the `openapi.yaml` of the artifact whose code
  receives the call; the service that serves the artifact serves it. Flow
  owns coordination specifications, including reusable Markdown under
  `flows/contracts/`; it owns no OpenAPI operation contract. An endpoint only
  other services may call carries
  `x-internal: true`.
- An endpoint whose use case crosses domains, such as a checkout, belongs to
  the artifact that owns its handler and use case, and reuses the schemas of
  other artifacts with `$ref`.
- A payload that is not an HTTP response, such as a push notification, an
  email or a deep link, is a schema under `components` of the artifact that
  sends it to the outside. An email or a file names its format (HTML, CSV)
  and its fields in order in the schema description.
- A trigger that starts a worker, such as a timer or a schedule, is declared
  under `x-triggers` of the artifact whose worker handles it, by name in
  camelCase, with its schedule or time and its input schema. A scenario names
  the trigger as it names an operation. A change keeps the input that
  triggers already scheduled will deliver (SYS-4).
- A command sent to a specific receiver through a queue or a topic belongs
  to that receiver's artifact, under `x-commands`, with its topic and input
  schema.
- A published event describes a fact of the publishing domain. Its public
  payload schema belongs to the publisher's artifact under
  `components/schemas`, with its topic in the description. Each receiver
  declares its handling operation under `x-triggers` in its own artifact
  and uses `$ref` to that schema as input; it does not copy the payload.
  The flow describes what each receiver does. For example, Order owns
  `OrderPlaced`; Billing and Notification each own their handler and
  reference Order's schema. Adding a consumer does not move the event.
- For both kinds of message, the publisher sends after its transaction and
  retries when the send fails; a consumer that receives it twice gets the
  same result (SYS-8). A change keeps what the consumers read (SYS-4).
- A command that is not an HTTP request, such as a CLI command or an action
  in a client's interface, is declared under `x-commands` of the artifact it
  belongs to, by name in camelCase, with its caller and its input and output
  schemas. A scenario names the command as it names an operation. A change
  keeps what callers pass and read (SYS-4).
- An endpoint an external system calls, such as a payment webhook, belongs to
  the artifact that receives and translates its payload. Its contract copies
  the request the external system documents; it is agreed with that
  documentation, not designed, and the issue links the vendor's version of
  it.
- A call or a notice from one domain to another in the same service is a step
  of the flow; its signature stays in code, not in a contract.
- A contract with no endpoint has `paths: {}`.
- `flows/` holds no `openapi.yaml`.
- A change to an existing operation keeps what released clients and calling
  services see (SYS-4, SYS-6 in the reference pass). Every visible change is
  breaking:
  - removing a key or a value, changing a type, or changing the meaning of a
    value;
  - adding an enum value;
  - adding a required request key, removing an accepted value, or tightening
    the validation of a request key;
  - changing who may call the operation, the state changes it allows, or the
    status codes and errors it returns, including a new status such as `429`;
  - removing the operation ([remove an operation](runbooks/remove.md)).

  Only a new optional key is not breaking. Removing data a client must not
  see is not breaking when the key stays with a value its schema already
  allows. Instead of a breaking change, add a new key beside the old one, or a
  new version of the path (`/v2/...`) with an `operationId` that ends in its
  version (`getBookV2`) ([contract](runbooks/contract.md)).
- The owner of each client and service that calls an operation reviews a pull
  request that changes the operation's contract. The flows name those callers.
  Each client owner checks their own decoding in the client's repository.
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
