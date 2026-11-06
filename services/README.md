# Services

The services of the product: one or many, such as one backend API or several
microservices behind an API gateway. Each one is a separate clone that this
workspace ignores, with its own README and agent instructions for building,
running and testing it. Fill in one row per service; the directory name is
the service name in the [domain map](../docs/architecture/domain-map.md) and in
[artifact-driven.json](../artifact-driven.json).

| Directory | Repository | Owner | Serves | Stack |
| --- | --- | --- | --- | --- |
| `lending/` | — | — | The reference pass: `book`, `member` | Go |
| `notification/` | — | — | The reference pass: `notice` | Go |

Clone each service after cloning the workspace:

```sh
git clone <repository URL> services/<name>
```

Each service's changes are made, reviewed and merged in its own repository by
its implementer, and approved by its owner
([team](../docs/governances/artifact-driven/team.md#parts-and-owners)). The
scripts read each service's routes and tests as
[artifact-driven.json](../artifact-driven.json) says.

Return to the [project contents](../README.md).
