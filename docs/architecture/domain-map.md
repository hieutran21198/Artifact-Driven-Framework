# Domain map

The domains of the backend. Each domain is one artifact in the
[software knowledge](../software-knowledges/artifacts/README.md) and one
package under `internal/domain`. A new domain is an architecture change first.

| Domain | Holds | Existing code that moves into it |
| --- | --- | --- |
| `book` | The reference pass: books in the collection and their loans | — |
| `member` | The reference pass: members and whether they may borrow | — |

Replace the reference rows with the project's domains. Where code predates
this structure, name the packages that move into each domain.

External systems become adapters under `adapter/<vendor>`, not domains:

| Adapter | Used for | Existing code that moves into it |
| --- | --- | --- |
| — | — | — |

Return to [architecture](README.md).
