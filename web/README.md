# Knowledge viewer

[index.html](index.html) shows the [knowledge site](../scripts/README.md#knowledge-site)
of one or more projects that use this framework, with no Python, no clone and
no server of its own. Open it from any static host that also serves
[scripts](../scripts/README.md), such as the GitHub Pages of this repository
or `python3 -m http.server` at its root.

1. Enter a GitHub token if a project is private: a fine-grained token with
   read-only access to the contents of those repositories. The page keeps it
   in the browser tab and sends it only to `api.github.com`.
2. List the projects, one `owner/repo` or `owner/repo@branch` per line.
3. Press **Reload**. For each project, the page reads the branch's current
   commit, takes `artifact-driven.json` and the knowledge folder through the
   GitHub API, and runs this repository's `site.py` on them in the browser
   with [Pyodide](https://pyodide.org). It shows one tab per project.

Each file is cached in the browser by its Git blob SHA, which changes when its
content changes, so the cache never goes stale. A reload asks GitHub only for
the branch's commit and its file tree, and downloads only the files that
changed. The page loads Pyodide from jsDelivr; everything else stays in the
browser.

Under the tabs, **Rule coverage** shows, for each goal, the criteria,
scenarios and rules that a test names, as `impact.py --coverage` does. The page
reads the tests of each service, client and end-to-end suite whose `tests`
setting names a `repository` ([configuration](../scripts/README.md#configuration)).
Coverage tells whether each rule is in the code, not whether the project is
right: a rule counts as covered when a test names its ID, whether or not the
test passes, the code does what the rule says, or the rule is right for the
business. The API coverage of the site, which reads routes from the code, is
left out.

Return to the [project contents](../README.md).
