---
name: backend-service
description: Build and extend the Go backend through its domain, use case and adapter structure. Use for endpoints, domain behavior, transactions, migrations and provider integration. Does not authorize commits to client repositories or deployment.
---

# Backend service

Implement backend behavior through the project's established architecture.
Resolve project paths against the current worktree root. Project contracts and
selected standards remain authoritative; this skill supplies an implementation
procedure, not a second architecture or rule catalog.

## Establish the boundary

Read `AGENTS.md`, the backend's own instructions (its `AGENTS.md` or `CLAUDE.md`
under `services/`, when it has them), the
[architecture](../../../docs/architecture/README.md) and the scope of the issue
before editing. Follow the
[Artifact Driven](../../../docs/governances/artifact-driven/README.md) workflow
and its gates; do not create local change or task files. Issue closure is not
approval.

Implement only approved knowledge. Read the goal, flow and artifact pages the
issue links, and the OpenAPI contract of every endpoint you touch, in
`docs/software-knowledges/`. If the code needs behavior the knowledge does not
hold, stop and report the gap instead of inventing it. Name each test after the
rule or scenario ID it proves, such as `BK-5` or `F-BORROW-3`.

Check how the clients call the endpoint (request shape, response decoding,
version) before changing it; the client pages of the artifact say where.

Read the [coding standards entry point](../../../docs/coding-standards/README.md)
and the [General](../../../docs/coding-standards/general/README.md) and
[Go](../../../docs/coding-standards/golang/README.md) guidance. Confirm which rules
the project has adopted; availability alone is not adoption. Inspect nearby code,
tests and local exceptions. Cite governing rule IDs instead of copying a second
rule catalog. Read infrastructure rules only when infrastructure is in scope.
Report missing or conflicting authority before affected implementation rather
than inventing conventions.

Map the change to the responsibilities present in the affected service:

| Boundary | Responsibility |
| --- | --- |
| Domain | Invariants, lifecycle transitions, validated values, business policy and established domain ports |
| Application | Use-case orchestration, transaction/UoW ports, authorization and provider coordination |
| Transport | Request decoding, authentication integration, DTOs and public error/status mapping |
| Persistence | Storage models, domain mapping, queries, locks and atomic persistence operations |
| Transaction/UoW | Transaction ownership and writers bound to the same transaction/context |
| Provider adapter | SDK/protocol translation and safe provider outcomes |
| Process entry point | Configuration, construction and start |

Use local package names. In the structure, Domain is `internal/domain`,
Application is `internal/app/command` and `internal/app/query` with transfer
objects in `internal/app/dto`, Transport is `internal/adapter/http`,
Persistence is `internal/adapter/db/repo` and Provider adapter is
`internal/adapter/<vendor>`. A command writes through a domain `Writer`; a
query reads through a domain `Reader` and changes nothing. See the
[architecture](../../../docs/architecture/README.md). Do not add a layer that the
change does not need.

## Domain and transaction work

For a service using domain models, locate its package layout, interface-placement,
aggregate and persistence contracts before changing their boundaries. Preserve
validated construction and stored-value restoration conventions where present.
Put lifecycle decisions in domain behavior; persistence enforces the resulting
conditions rather than deciding business limits, expiry or eligibility. Atomic
queries may enforce domain-supplied conditions. Add no aggregate/event framework
without a present requirement. Respect the governing port-placement convention;
resolve a conflict with GO-202 explicitly instead of inventing an exception.

Where a UoW exists, reuse it. Repositories receive its transaction handle and do
not open independent transactions. Expose only transaction-scoped writers the use case needs. Preserve
established repository naming and compile-time port assertions. A pure query
reuses the reader/read-only context rather than adding a write UoW or aggregate
lifecycle solely for the read.

Keep provider calls outside database transactions. For behavior that spans remote
I/O, use short claim and final-commit transactions when the established workflow
requires them. Re-read protected state under its lock and evaluate expiry after
lock acquisition. Preserve contract-defined idempotency, resolved identity and
stale-owner conditions across retries. Distinguish a rejection that must commit
accounting from a failure that must roll back; an invalid attempt can still
consume an existing quota reservation. Do not add quotas, leases, queues or
outboxes when the current behavior does not require them.

## Implement and verify

Locate local HTTP, persistence and concurrency guidance for the affected boundary.
Trace caller cancellation and deadlines through use case, transaction, repository
and provider. Socket timeouts alone do not establish database/provider operation
deadlines. Bound work using the contract and existing defaults without adding an
unused configuration option.

Apply selected rules for constructors, naming, exported documentation, errors and
formatting. Preserve error causes where required; if a governing security contract
forbids exposing a sensitive cause, sanitize at that boundary and record/review
the exception as required. Do not log a secret to explain failure. Keep new
SDK/dependency choices scoped, pinned and justified.

Select checks from observable behavior and the affected contracts:

- Domain checks exercise policy and transitions without a database or provider.
- Transaction/UoW integration checks prove commit, rollback and shared writer
  binding where those mechanisms apply.
- Provider/port checks verify remote calls run outside database transactions.
- Concurrency checks use barriers and fault injection for relevant races,
  including stale work and lost commit/response recovery; do not synchronize
  tests with sleeps.
- API and migration checks cover authentication, isolation and compatibility
  against appropriate real dependencies or an explicitly identified emulator.

Run applicable Go gates and existing service checks with the pinned toolchain and
compatible analysis tools. Distinguish reachable vulnerability findings from
unimported/module-only advisories and retain both with the issue or pull request.
Report tool/environment limits; emulator success does not prove live behavior.

Prepare affected API, persistence, configuration and flow knowledge for review
with the result. Attach evidence and review outcomes to the issue or pull
request. In existing checks, assess layer ownership, transaction
boundaries, failure/retry behavior and selected KISS/writing guidance. Return
scoped changes, check results and remaining gates. This skill grants no extra
publication, deployment or cloud permissions.
