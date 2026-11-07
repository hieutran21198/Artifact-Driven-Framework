# Flow: View a workspace

A reader who does not read the repository opens the project tracker and sees,
for one workspace at one ref, the coverage of each goal and how its goals,
flows and artifacts link.

- Crosses: [tracker](../artifacts/tracker/README.md), served by the `tracker`
  service, and [configuration](../artifacts/configuration/README.md),
  [knowledge](../artifacts/knowledge/README.md) and
  [test](../artifacts/test/README.md), whose code of the `scripts` service the
  tracker runs in the browser.
- Contract: `openWorkspace`, `listRefs`, `setToken`,
  `addWorkspace`, `removeWorkspace`, `addFolder`, `checkSettings`,
  `changeConfiguration`, `restoreConfiguration`, `copyCloneScript`,
  `exportSettings` and `importSettings` in the
  [tracker contract](../artifacts/tracker/openapi.yaml), and
  `measureCoverage` in the
  [measure coverage contract](measure-coverage.openapi.yaml).
- Trigger: a reader follows a link to the tracker, such as the one on the
  landing page (`openTracker`) or one a team sends with the workspace and the
  ref in it.
- Outcome: the reader sees the coverage of each goal, then the knowledge
  site, of the workspace at the ref; or the reason a part could not be read.

## Steps

1. Once, in the settings, the reader names each token needed with
   `setToken`, and adds each workspace with `addWorkspace`: a repository, a
   branch, and a token or none (TRK-6, TRK-7). The tracker checks the
   workspace, the repositories of the parts its configuration names and the
   tokens, and shows what it cannot connect to and why (TRK-11); the reader picks a token for a
   private part there. `checkSettings` checks them again. To try another
   configuration, the reader changes it with `changeConfiguration`; the
   tracker validates it and uses it in place of the workspace's until
   `restoreConfiguration` (TRK-12). To read a workspace from disk instead,
   the reader copies its clone script with `copyCloneScript`, runs it, and
   adds the clone with `addFolder` (TRK-13, TRK-8).
2. The page opens and calls `openWorkspace` with the workspace and the ref
   the address names, or the ones chosen before, or the repository of the
   framework (TRK-1, TRK-7).
3. For a repository, the tracker asks GitHub for the commit of the ref and
   its file tree, and downloads the configuration, the knowledge folder and
   the files it does not keep yet (TRK-2, TRK-5). For each part whose tests
   setting names a repository (CFG-6), it reads that repository's test files
   the same way (TRK-4). Each repository is read with the token picked for
   it, if any (TRK-6). For a folder added with `addFolder`, the
   tracker reads the files on disk (TRK-8).
4. The tracker loads Pyodide from jsDelivr once per page load, and runs the
   scripts of the framework on the files: the coverage as `measureCoverage`
   prints it, then the knowledge site (TRK-2, TRK-3). It keeps the build for
   the workspace and the ref (TRK-5).
5. The page shows the coverage, its sentence on what coverage means, and the
   knowledge site (TRK-3). Each part, repository or file it could not read is
   listed with the reason (TRK-9).
6. The reader picks another ref, or the ref of a part, from the lists that
   `listRefs` gives, and calls `openWorkspace` again with Load. Picking alone
   builds nothing (TRK-1); a load downloads only what changed (TRK-5).
7. The reader moves the settings to another browser with `exportSettings` and
   `importSettings` (TRK-7).

GitHub is called with no write, so a call that repeats gives the same result.
When a call fails, the tracker reports it and builds what it could read
(TRK-9).

```mermaid
sequenceDiagram
    actor Reader
    participant Page as tracker service
    participant GitHub
    participant Pyodide as Pyodide on jsDelivr

    Reader->>Page: setToken(name, value)
    Reader->>Page: addWorkspace(repository, branch, token)
    Page->>GitHub: the repository, its parts' repositories, each token
    Page-->>Reader: what it can connect to, and why not
    Reader->>Page: Open link, or pick and Load
    Page->>Page: openWorkspace(workspace, refs)
    alt build kept
        Page-->>Reader: coverage, then the site
    else
        Page->>GitHub: commit and file tree of the ref
        alt cannot read
            GitHub-->>Page: error
            Page-->>Reader: the reason, other parts still build
        else
            Page->>GitHub: changed files, tests of each part
            Page->>Pyodide: load once
            Page->>Page: measureCoverage, then the site
            Page-->>Reader: parts left out, coverage, then the site
        end
    end
    Reader->>Page: listRefs, pick another ref or a part's ref
    Reader->>Page: Load: openWorkspace(workspace, refs)
```

## Scenarios

| ID | Given | When | Then | Covers |
| --- | --- | --- | --- | --- |
| F-VIEW-1 | An address that names a public workspace and its branch `main` | The reader opens it, which calls `openWorkspace` | The page shows that workspace at `main`: first one coverage line for each goal with the sentence on what coverage means, then the knowledge site | TRK-1, TRK-2, TRK-3 |
| F-VIEW-2 | An address that names no workspace, and no settings in the browser | The reader opens it, which calls `openWorkspace` | The page shows the repository of the framework at its default branch | TRK-1 |
| F-VIEW-3 | A workspace shown at `main`, a branch `feature/renew` that changes one flow, and a part whose tests are in another repository with a branch `feature/renew` | The reader calls `listRefs` for the workspace and for the part, picks `feature/renew` for both, then calls `openWorkspace` with Load | The branches list `main` first; the page shows the knowledge of `feature/renew`, with the changed flow, and the coverage with the part's tests at `feature/renew` | TRK-1, TRK-2, TRK-4 |
| F-VIEW-4 | A workspace loaded at `main`, then at `feature/renew` | The reader picks `main` again, then calls `openWorkspace` with Load, then calls it again after one knowledge file changed on `main` | Picking reads nothing; the first load reads the commit and the file tree only and shows the kept build of `main`; the second downloads only the changed file and builds again | TRK-1, TRK-5 |
| F-VIEW-5 | A workspace and the tests of its parts | The reader calls `openWorkspace`, and a person runs `measureCoverage` in a clone of it at the same ref, with the same parts cloned | The coverage lines are the same | TRK-3, TRK-4, TST-4 |
| F-VIEW-6 | A part whose tests setting names a repository, a test there that fails and names a rule, and a reader who picks `feature/renew` for that part | The reader calls `openWorkspace` | The test files come from that repository at `feature/renew`; the rule counts as covered; no test runs and no file changes | TRK-2, TRK-4, CFG-6, TST-3, SYS-4, SYS-6 |
| F-VIEW-7 | A private workspace, and a token named `team` set with `setToken` | The reader calls `addWorkspace` with the repository and `team`, then `exportSettings`, then closes the tab | The workspace builds; the token was sent only to `api.github.com`; the exported file names `team` and holds no token value; a new tab has no token value, and the workspace there asks for `team` again | TRK-6, TRK-7 |
| F-VIEW-8 | A folder with the workspace, a part cloned in it, a test file under `node_modules`, and `.git/HEAD` naming `feature/renew` | The reader calls `addFolder` with the folder | The page shows the folder's workspace at `feature/renew` with the coverage of the part's tests, and does not read the file under `node_modules` | TRK-8, CFG-4 |
| F-VIEW-9 | A workspace with two parts whose tests name repositories, one of which the token cannot read | The reader calls `openWorkspace` | The page names that part and the reason, and shows the coverage and the site with the other part's tests | TRK-4, TRK-9 |
| F-VIEW-10 | A browser 360 px wide, on a system that uses a dark theme | The reader calls `openWorkspace` | The page stays light and needs no horizontal scrolling | TRK-10 |
| F-VIEW-11 | Settings of an older version in the browser, and a settings file of a newer version | The page loads, then the reader calls `importSettings` with the file | The older settings are migrated and stored; the newer file is shown with a warning and not stored | TRK-7 |
| F-VIEW-12 | A public workspace with a part whose tests setting names a private repository, and no token picked for that part | The reader calls `openWorkspace` | Above the coverage, the page names the part and says that it needs a token; the coverage leaves out its tests; the rest builds | TRK-3, TRK-6, TRK-9 |
| F-VIEW-13 | A token named `old` that GitHub refuses, and a repository that does not exist | The reader calls `checkSettings`, then `addWorkspace` with that repository, then `removeWorkspace` | The token `old` shows as refused; the new workspace shows as not found; after the removal it is gone from the settings and the workspace picker | TRK-11, TRK-7 |
| F-VIEW-14 | A workspace, and a changed configuration that is not valid JSON, then one whose `services` is a list | The reader calls `changeConfiguration` with each | Each is reported, the first with the line where it fails and the second with the key; the tracker builds with neither and keeps the last valid one | TRK-12, CFG-2 |
| F-VIEW-15 | A workspace whose configuration was changed in the tracker to add a part with a tests folder | The reader calls `openWorkspace`, then `restoreConfiguration` | The first build reads the tests of the added part and says, above the coverage, that it uses a configuration changed in this browser; the workspace has no new commit; after the restore the build uses the workspace's configuration again | TRK-12, TRK-4 |
| F-VIEW-16 | A workspace picked at `main`, a part whose tests setting names a private repository and folder `services/lending`, `feature/renew` picked for it, and a token picked for it | The reader calls `copyCloneScript`, runs the script in an empty folder, then calls `addFolder` with the clone | The script clones the workspace at `main` and the part at `feature/renew` into `services/lending`, and holds no token; the folder builds with the part's tests | TRK-13, TRK-6, TRK-8, CFG-6 |

## Open questions

- Whether the tracker shows the API coverage of the site, which reads the
  routes of each service from its code (TRK-2).

Return to [flows](README.md).
