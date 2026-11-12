# Domain map

The domains of the product and the service that serves each one. Each domain
is one artifact in the
[software knowledge](../software-knowledges/artifacts/README.md) and one
package under `internal/domain` of its service. A new domain, or a domain that
moves to another service, is an architecture change first.

The rows select this project's domain-to-Artifact and service mapping. They do
not by themselves establish DDD bounded contexts; use the model and language
boundaries described in [Knowledge](../governances/artifact-driven/knowledge.md#layers).

| Domain | Service | Holds | Existing code that moves into it |
| --- | --- | --- | --- |
| `book` | `lending` | The reference pass: books in the collection and their loans | — |
| `member` | `lending` | The reference pass: members and whether they may borrow | — |
| `notice` | `notification` | The reference pass: messages sent to members, once each | — |

These sample boundaries demonstrate document shape, not mandatory product
boundaries. The split between loans and borrowing eligibility is not evidence
that a real product must separate those responsibilities. Choose the project's
boundaries through [knowledge ownership](../governances/artifact-driven/knowledge.md#choose-the-owner).

Replace the reference rows with the project's domains. Where code predates
this structure, name the packages that move into each domain.

External systems become adapters under `adapter/<vendor>` of the service that
uses them, not domains:

| Adapter | Used for | Existing code that moves into it |
| --- | --- | --- |
| — | — | — |

Return to [architecture](README.md).
