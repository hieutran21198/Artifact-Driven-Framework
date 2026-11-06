# Applications

The client applications, each as a Git submodule. Each one has its own README
and build instructions. Fill in one row per client; the directory name is the
client name in [artifact-driven.json](../artifact-driven.json), so its client
pages are `<directory>.md`.

| Directory | Repository | Purpose | Stack |
| --- | --- | --- | --- |
| — | — | — | — |

Read the clients to learn how they call the backend: request shape, response
decoding, error handling and the API version they use. Do not commit to these
repositories; client changes go out as written handoffs.

Add a client:

```sh
git submodule add <repository URL> apps/<name>
git submodule set-branch --branch <branch> apps/<name>
```

Initialise the submodules after cloning:

```sh
git submodule update --init
```

Each submodule follows the branch where work happens:

| Directory | Branch |
| --- | --- |
| — | — |

Pull the latest commits with:

```sh
git submodule update --remote
```

When the working branch of a client changes, update it with
`git submodule set-branch`.

Return to the [project contents](../README.md).
