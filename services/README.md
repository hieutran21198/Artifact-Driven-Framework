# Services

The backend, as a Git submodule. Its own README and agent instructions explain
how to build, run and test it.

| Directory | Repository | Purpose | Stack |
| --- | --- | --- | --- |
| `backend/` | — | The backend API and workers | Go |

Add the backend:

```sh
git submodule add <repository URL> services/backend
```

Initialise the submodule after cloning:

```sh
git submodule update --init
```

Backend changes are made, reviewed and merged in the backend repository. The
submodule pointer in this workspace changes only when a document needs a
specific backend commit. The scripts read its tests and routes as
[artifact-driven.json](../artifact-driven.json) says.

Return to the [project contents](../README.md).
