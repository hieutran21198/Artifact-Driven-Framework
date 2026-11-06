# General

The coding standard for backend code, across languages.

## Scope

The scope is code in the structure of the backend that the
[architecture](../../architecture/README.md) describes: `internal/domain`,
`internal/app` and `internal/adapter`. Code that predates that structure is
excluded until it moves into it. Generated code, third-party code and repository tooling are excluded.
A language standard adds rules for its language mechanisms.

## Rule conventions

These conventions apply to the General and Go rule sets. A language
standard adds a mechanism and cites the general rule instead of copying it.
Use the selected standards during implementation and review. Cite the rule ID
when reporting a violation; the canonical text stays in its owning standard.

### Precedence

Established requirements, specifications and decisions govern product behavior.
Selected coding standards govern how code is written; local package conventions
and reviewer preferences do not override them. A conflict with an approved
contract is a defect in the standard. Preserve the contract and resolve the
standard through an explicit reviewed change. A skill supplies a procedure and
references rules; it does not override or duplicate them.

### Levels and IDs

| Level | Meaning |
| --- | --- |
| `MUST` | Mandatory; compliance or an authorized recorded exception is required before merge. |
| `MUST NOT` | Forbidden; compliance or an authorized recorded exception is required before merge. |
| `SHOULD` | Expected; a deviation states its reason on the issue or pull request. |
| `MAY` | Permitted; the standard states no preference. |

Each rule has an ID, one of these levels and a concise statement. Add rationale
or an example only when needed. IDs use `<prefix>-<number>`: `GEN` for general
and `GO` for Go. Headings group numbers by concern.

Keep IDs stable. Do not reuse or renumber them. When a rule moves or is retired,
keep a traceable replacement or retirement reference; leave number gaps empty.
A new rule takes the next free number in its family. Preserve existing citations
when changing these standards. Record substantive meaning changes explicitly in
the issue or pull request rather than silently changing a cited contract.

### Changes and exceptions

Change a selected standard on a dedicated branch, obtain authorized review and
resolve affected code or approved exceptions before adopting it. Keep one
canonical rule; check language references when a general rule changes. Git
history preserves knowledge revisions. Do not add a version or changelog;
execution evidence and migration tasks belong to the issue or pull request.

A local exception uses the tool's ignore directive at the code position, with
the rule ID and reason. It needs the project's authorized review. For example:

```go
//lint:ignore ST1005 GO-406: the upstream contract fixes this wording.
var ErrUpstream = errors.New("Upstream rejected the request")
```

A standing exception is reviewed enduring knowledge. Use the owning standard's
register with rule, scope, reason, owner and review date; link the authorizing
issue or pull request when recording a real exception. Review by that date and renew
it or remove the deviation. Empty tables below are templates, not claims that a
project has no exceptions. Tool suppression alone is not approval. An exception
to a code convention cannot override a governing security or product contract.

## Design and boundaries (GEN-1xx)

| ID | Level | Rule |
| --- | --- | --- |
| GEN-101 | MUST | A module, package or component has one responsibility, and its name states it. |
| GEN-102 | MUST | Dependencies point toward the domain. Do not create a dependency cycle. |
| GEN-103 | MUST | Expose only the API that a caller outside the unit needs. |
| GEN-104 | MUST | Minimize shared mutable state. |
| GEN-105 | MUST | A constructor or a factory returns a valid object and validates its input. |
| GEN-106 | MUST NOT | Add an abstraction without a present need. |
| GEN-107 | MUST | Move code that a second consumer needs to one package that both import. Do not copy it. |
| GEN-108 | MUST | The default path completes the common task with no setup. |
| GEN-109 | MUST NOT | Remove a capability to simplify the default. Expose it through a documented opt-in. |

GEN-102 states the dependency direction; it does not install an architecture
pattern. GEN-106 agrees with the
[KISS principle](../../principles/kiss/README.md). GEN-108 and GEN-109 define default behavior and opt-in capability.

## Naming and documentation (GEN-2xx)

| ID | Level | Rule |
| --- | --- | --- |
| GEN-201 | MUST | Use a name that a reader of the domain understands. Do not abbreviate a term that the domain does not define. |
| GEN-202 | MUST NOT | Create a catch-all module named `util`, `utils`, `common`, `helpers` or `shared`. |
| GEN-203 | MUST | Document every public interface that a consumer can call. |
| GEN-204 | MUST | Write a comment about the reason, not about the mechanics. |
| GEN-205 | MUST NOT | Keep commented-out code. |
| GEN-206 | SHOULD | Keep a function to one intent and to the size of one screen. |

A name for a helper states the thing that the helper helps with. Put `retry`
next to the retry policy, not in a `utils` module.

## Failure handling (GEN-3xx)

| ID | Level | Rule |
| --- | --- | --- |
| GEN-301 | MUST | Handle a failure or propagate it. Never discard it without a comment that states why that is safe. |
| GEN-302 | MUST NOT | Log a failure and propagate the same failure. |
| GEN-303 | MUST NOT | Terminate the process for an expected failure. Reserve a process exit for a failure that prevents startup. |
| GEN-304 | MUST | Add the operation context once, at the layer that knows the operation. |
| GEN-305 | MUST | Bound every retry and wait between the attempts. Retry only a failure that can succeed on a later attempt. |

The two failure forms differ in their reader:

- Wrong: the operation reports `failed`, and the reader cannot tell which
  operation failed.
- Right: the operation reports `save order 1234: connection refused`.

## Security (GEN-4xx)

| ID | Level | Rule |
| --- | --- | --- |
| GEN-401 | MUST | Validate and normalize untrusted input at the boundary before the domain uses it. |
| GEN-402 | MUST | Enforce authorization in the service that owns the data. A check in the transport layer alone is not sufficient. |
| GEN-403 | MUST | Use a parameterized query. Never build a query from input with string concatenation. |
| GEN-404 | MUST | Encode output for its sink, such as HTML, SQL, a shell command or a log record. |
| GEN-405 | MUST | Keep certificate and signature verification enabled. Do not disable it to make a connection work. |
| GEN-406 | MUST NOT | Put a secret in source code, in a default configuration value or in a test fixture. |
| GEN-407 | MUST | Give a credential the least privilege that it needs and the shortest lifetime that works. |

## Configuration, resources and timeouts (GEN-5xx)

| ID | Level | Rule |
| --- | --- | --- |
| GEN-501 | MUST | Read configuration from the environment or from the deployment system. Use safe defaults and never a secret default. |
| GEN-502 | MUST | Set a timeout or a deadline on every call that can block, such as a network call, a query or a lock. |
| GEN-503 | MUST | Let a call inherit the deadline and the cancellation of its caller. Detach a call only with a recorded reason. |
| GEN-504 | MUST | Reuse an expensive resource, such as a client, a pool or a connection. |
| GEN-505 | MUST | Release a resource in the scope that acquired it. |

## Observability (GEN-6xx)

| ID | Level | Rule |
| --- | --- | --- |
| GEN-601 | MUST | Emit structured log records with stable, lowercase keys. |
| GEN-602 | MUST NOT | Use console output for operational information. |
| GEN-603 | MUST | Log a cause once, at the boundary that handles it. |
| GEN-604 | MUST NOT | Put a secret, a token or personal data in a log record, a metric label or a trace attribute. |
| GEN-605 | MUST | Correlate the records of one request with a request identifier. |

## Tests (GEN-7xx)

| ID | Level | Rule |
| --- | --- | --- |
| GEN-701 | MUST | Assert the behavior in the contracts, not the implementation of the code under test. |
| GEN-702 | MUST | Make a test deterministic. Do not depend on execution order or on the wall clock. |
| GEN-703 | MUST NOT | Use sleeping as a synchronization mechanism in a test or in production code. |
| GEN-704 | MUST | Run an integration test against the real dependency, in an environment that the test starts. |
| GEN-705 | MUST | Add a test for each new behavior that a caller can observe. |
| GEN-706 | SHOULD | Treat coverage as evidence of exercised behavior, not as a target percentage. |

Unit tests may use fakes. GEN-704 applies to integration tests and does not
require unit tests to make live network calls.

## Dependencies (GEN-8xx)

| ID | Level | Rule |
| --- | --- | --- |
| GEN-801 | MUST | Prefer the platform and its standard library. A third-party dependency needs a reason in the change that adds it. |
| GEN-802 | MUST | Pin dependency versions and commit the lock file. |
| GEN-803 | MUST NOT | Depend on a package that is unmaintained or whose license the project cannot accept. |
| GEN-804 | MUST | Keep the dependencies free of known vulnerabilities. A recorded exception is the only alternative to a fix. |
| GEN-805 | MUST | Review a dependency update with the same care as a code change. |

## Repository hygiene (GEN-9xx)

| ID | Level | Rule |
| --- | --- | --- |
| GEN-901 | MUST | Give each app, service and library a README with install, run, test and build commands. |
| GEN-902 | MUST NOT | Commit build output or installed dependencies. |
| GEN-903 | MUST NOT | Commit a credential file, a private key or a populated environment file. |
| GEN-904 | MUST | Keep a change to its scope. Do not refactor unrelated code in the same change. |

## Gates (GEN-10xx)

| ID | Level | Rule |
| --- | --- | --- |
| GEN-1001 | MUST | Pass every gate that applies to the changed code before a merge. |
| GEN-1002 | MUST | Run the same gates locally and in continuous integration. |
| GEN-1003 | MUST | Record a deliberate skip with the rule ID and the reason in the change. |

These methods describe gates to configure when adopting the standard; they do
not assert that tools or CI are installed. Record actual coverage and limits
with the issue or pull request. A missing required gate is a gap, not a passing check.

| Gate | Method | Relevant rules |
| --- | --- | --- |
| Secret scanning | Scan the change for a credential or a private key. | GEN-406, GEN-903 |
| Dependency audit | Audit the lock file for a known vulnerability. | GEN-804 |
| License check | Compare each dependency license with the project policy. | GEN-803 |
| Lock file check | Confirm that the lock file matches the manifests. | GEN-802 |
| Language gates | Run the gates of the language standard. | Per standard |

## Exceptions register (GEN-11xx)

| ID | Level | Rule |
| --- | --- | --- |
| GEN-1101 | MUST | A standing exception has a row in its owning standard's register with the rule ID, the scope, the reason, the owner and the review date. |
| GEN-1102 | MUST | Review an exception on its review date. Renew it with a new date or remove the deviation. |

| Rule | Scope | Reason | Owner | Review date |
| --- | --- | --- | --- | --- |
| None | — | — | — | — |

## Local use

Read the [project instructions](../../../AGENTS.md) first. A change to this
standard is its own reviewed pull request. Keep run results, progress and
discussion on the issue or pull request. Approved standing exceptions
belong in the register above.

Return to [coding standards](../README.md).
