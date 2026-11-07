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

An address such as `tracker/?workspace=owner/repo&ref=main` opens and loads
that workspace. Settings lists what the browser keeps, and where.

Return to the [project contents](../README.md).
