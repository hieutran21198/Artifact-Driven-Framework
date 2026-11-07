# Domain map

The domains of the product and the service that serves each one. Each domain
is one artifact in the
[software knowledge](../software-knowledges/artifacts/README.md) and one
package under `internal/domain` of its service. A new domain, or a domain that
moves to another service, is an architecture change first.

| Domain | Service | Holds | Existing code that moves into it |
| --- | --- | --- | --- |

Where code predates this structure, name the packages that move into each
domain.

External systems become adapters under `adapter/<vendor>` of the service that
uses them, not domains:

| Adapter | Used for | Existing code that moves into it |
| --- | --- | --- |
| — | — | — |

Return to [architecture](README.md).
