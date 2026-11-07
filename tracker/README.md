# Project tracker

[index.html](index.html) shows the [knowledge site](../scripts/README.md#knowledge-site)
and the coverage of the workspaces that use this framework, with no Python,
no clone and no server of its own. Open it from any static host that also serves
[scripts](../scripts/README.md), such as the GitHub Pages of this repository
or `python3 -m http.server` at its root.

## Use it

1. Open **Settings** and list the workspaces, one per line: `owner/repo` for
   a GitHub repository, or **Add local folder** for a folder on this computer.
2. For a private repository, set a read-only GitHub token for its owner. Owner
   `*` is used for any owner without a token of its own.
3. Pick the workspace in the drop-down, and its branch, tag or commit in the
   field next to it, which lists the repository's branches and tags. The page
   builds the site of that workspace at that ref.
4. When the workspace's `tests` settings name a `repository`, the **Tests at**
   row picks the ref of each part's tests, such as a service on the same
   feature branch. Empty means the branch in the setting, or the default one.
5. Press **Reload** to read the ref again; a build is kept until then, so
   switching back and forth does not rebuild.

The page reads `artifact-driven.json` and the knowledge folder of the
workspace, and the tests of each part, then runs this repository's `site.py`
on them in the browser with [Pyodide](https://pyodide.org).

## Local folders

The page reads the folder as it is on disk, with the services and clients
cloned in it; it shows the branch from `.git/HEAD` and cannot switch it. In
Chrome and Edge the page keeps access to the folder between visits; after a
page load, Reload asks once to allow it. Firefox and Safari cannot keep the
access: after each page load, Reload asks to choose the folder again, and the
browser lists every file in it, which takes longer for a big folder. The page
shows this note in those browsers.

## Coverage

Under the site, **Rule coverage** shows, for each goal, the criteria,
scenarios and rules that a test names, as `impact.py --coverage` does. The page
reads the tests of each service, client and end-to-end suite: from the
`repository` its `tests` setting names
([configuration](../scripts/README.md#configuration)), or from its folder in a
local workspace. Coverage tells whether each rule is in the code, not whether
the project is right: a rule counts as covered when a test names its ID,
whether or not the test passes, the code does what the rule says, or the rule
is right for the business. The API coverage of the site, which reads routes
from the code, is left out.

## What the browser keeps

| Kept | Where | For how long |
| --- | --- | --- |
| The configuration: workspaces, chosen refs | `localStorage`, versioned | Until removed; **Export** and **Import** move it to another browser |
| Tokens, one per owner | `sessionStorage` | Until the tab closes; never exported, sent only to `api.github.com` |
| GitHub files, by Git blob SHA | `localStorage` | Never stale: a blob SHA changes when the content changes. A reload asks GitHub for the commit and its tree, and downloads only changed files |
| Local folders (Chrome, Edge) | IndexedDB | Until removed; an imported configuration needs the folder chosen again |

The configuration has a `version`. A newer page migrates an older
configuration when it opens or imports it. An older page shows a newer
configuration but does not save it. The page loads Pyodide from jsDelivr;
everything else stays in the browser.

Return to the [project contents](../README.md).
