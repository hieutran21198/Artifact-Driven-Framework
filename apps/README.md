# Applications

The client applications, each a separate clone that this workspace ignores,
with its own README and build instructions. Fill in one row per client; the
directory name is the client name in
[artifact-driven.json](../artifact-driven.json), where its tests are set.

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
owner reviews each change to the contract of an operation the client calls
([contracts](../docs/governances/artifact-driven/knowledge.md#contracts)).
When the branch where work happens changes, switch the clone and update the
table.

Return to the [project contents](../README.md).
