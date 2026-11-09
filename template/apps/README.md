# Applications

The client applications, each a separate clone that this workspace ignores,
with its own README and build instructions. Fill in one row per client; the
directory name is the client name in
[artifact-driven.json](../artifact-driven.json), so its client pages are
`<directory>.md`.

| Directory | Repository | Owner | Branch where work happens | Stack |
| --- | --- | --- | --- | --- |
| `web/` | — | — | — | — |
| `mobile/` | — | — | — | — |

Clone each client after cloning the workspace, on the branch where work
happens:

```sh
git clone -b <branch> <repository URL> apps/<name>
```

Each client's changes are made, reviewed and merged in its own repository by
its implementer, and approved by its owner
([team](../docs/governances/artifact-driven/team.md#parts-and-owners)). Its
owner keeps its client pages ([client](../docs/governances/artifact-driven/runbooks/client.md)).
When the branch where work happens changes, switch the clone and update the
table.

For design ownership and links from a Flow, follow
[Design links](../docs/governances/artifact-driven/knowledge.md#design-links).
After cloning, record the actual design location in each client's README.
Do not link to a sample design path in a client that has not been cloned.

Return to the [project contents](../README.md).
