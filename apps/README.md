# Applications

The client applications, each a separate clone that this workspace ignores,
with its own README and build instructions. Fill in one row per client; the
directory name is the client name in
[artifact-driven.json](../artifact-driven.json), so its client pages are
`<directory>.md`.

| Directory | Repository | Owner | Branch where work happens | Stack |
| --- | --- | --- | --- | --- |

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

Return to the [project contents](../README.md).
