# Domain map

The domains of the framework and the service that serves each one. Each domain
is one artifact in the
[software knowledge](../software-knowledges/artifacts/README.md) and one part
of the code of its service, such as a package under `internal/domain` of a Go
service. The [services](../../services/README.md) page names each service and
its code. A new domain, or a domain that moves to another service, is an
architecture change first.

| Domain | Service | Holds | Existing code that moves into it |
| --- | --- | --- | --- |
| `workspace` | `install` | What a new workspace holds, and where install takes it from | — |
| `configuration` | `scripts` | The root of a workspace and the settings in `artifact-driven.json` | — |
| `repository` | `scripts` | The folders and Markdown pages of a workspace, and their links | — |
| `knowledge` | `scripts` | Knowledge IDs, operations and the citations between units | — |
| `introduction` | `landing` | The landing page: its story, its reader cards and its links | — |
| `test` | `scripts` | Which knowledge IDs the test files of a part name, and how strongly each is proved | — |
| `tracker` | `tracker` | The project tracker: the workspace and ref it shows, what it reads, what it shows first, and what the browser keeps | — |

External systems are used through the service that uses them, not as domains:

| Adapter | Used for | Existing code that moves into it |
| --- | --- | --- |
| GitHub | `install` downloads the framework at a ref; `tracker` reads workspaces and the repositories of their parts | — |
| Pyodide on jsDelivr | `tracker` runs the code of `scripts` in the browser | — |

Return to [architecture](README.md).
