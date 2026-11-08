# Project tracker

[index.html](index.html) shows, for one workspace at one branch, tag or
commit, the coverage of each goal and then the
[knowledge site](../scripts/README.md#knowledge-site), with no Python, no clone
and no server of its own. Open it from any static host that also serves
[scripts](../scripts/README.md), such as the GitHub Pages of this repository
or `python3 -m http.server` at its root. What it does is the knowledge of the
[tracker artifact](../docs/software-knowledges/artifacts/tracker/specification.md)
and of the flow [View a workspace](../docs/software-knowledges/flows/view-workspace.md).

## Use it

1. Open **Settings**. Under **Tokens**, set each read-only GitHub token you
   need, by a name. Under **Workspaces**, add a repository with its branch and
   a token, or none; or add a folder on this computer. Settings shows whether
   it can connect to each workspace, to the repository of each part, and with
   each token. A part whose tests are in another repository picks its own
   token there.
2. On the workspace page, pick the workspace, its branch, tag or commit, and
   the ref of each part whose tests are in another repository. Press **Load**:
   the page reads the refs, downloads the files it does not keep, and runs
   this repository's scripts on them in the browser with
   [Pyodide](https://pyodide.org). Picking alone reads nothing.
3. To try another `artifact-driven.json`, change it under the workspace's
   parts in Settings. It is used in this browser only, and the workspace page
   says so above the coverage.
4. To read a workspace from disk, copy its **Clone script** under its parts
   in Settings, run it in any folder with your own git access, and add the
   clone as a folder. It clones the workspace and each part's repository at
   the refs picked, and holds no token.

When the browser uses a directory input instead of a kept folder handle, each
later **Load** asks you to choose the same folder again. This includes files
added or removed since the previous read. Cancelling keeps the previous build.
Browsers with folder handles reread the folder directly.

**Sources of this build**, above the coverage, shows the resolved commits,
effective configuration, analyzer identity and each part's test-read outcome.
For a local folder it identifies working-copy files, with any Git label as
context only. These details belong to the displayed build, not pending picks.

The tracker keeps downloaded workspace files separate from its trusted Python
analyzer and generated output. Workspace Python files are read as test text,
not imported. File paths that escape the workspace or alias another staged
file stop that load.

A repository read with no token is downloaded from `raw.githubusercontent.com`,
which does not count against GitHub's limit of 60 API calls an hour without a
token; a load then needs only the commit and the file tree from the API.

An address such as `tracker/?workspace=owner/repo&ref=main` opens and loads
that workspace. Settings lists what the browser keeps, and where.

## Embedded site

The knowledge site runs in a sandboxed frame with scripts enabled and an
opaque origin. It cannot access tracker settings, storage, tokens or the
parent document, or navigate the parent (TRK-14).

Each rendered document gets a new frame and an identifier. A small message
exchange reports its content height and the visible viewport position, and
lets its section links request a scroll within that document. Both
sides validate the sender, message type, document identifier and bounded
numeric fields. It carries no credentials. The tracker scrolls as one page;
the frame reports expanded controls as well as normal content.

## Check changes

There is no build step or runtime package installation. See
[browser test setup](../tests/README.md), then run:

```sh
python3 -m unittest discover -s tests/tracker -t . -v
```

Return to the [project contents](../README.md).
