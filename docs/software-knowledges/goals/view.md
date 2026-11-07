# Goal: Follow a project in the browser

## Need

Stakeholders, product owners and solution architects who do not read the
repository follow a project from a link: for each goal, how much of what it
relies on tests name, and how its flows and artifacts link, at any branch,
tag or commit. They install, clone and run nothing.

- Actor: Stakeholder, Product owner and Solution architect
  ([context](../system/context.md)).
- Follows: SYS-1, SYS-4, SYS-6 ([requirements](../system/requirements.md)).

## Success criteria

| ID | Criterion | Proven by |
| --- | --- | --- |
| G-VIEW-1 | A reader opens a link to the project tracker and sees, first, the coverage of each goal of the workspace, then how its goals, flows and artifacts link, with nothing to install, clone or run. | F-VIEW-1, F-VIEW-2 |
| G-VIEW-2 | A reader picks a workspace, any branch, tag or commit of it, and the ref of each part whose tests are in another repository, then loads them and sees the knowledge and coverage of those refs. Loading again downloads only what changed since. | F-VIEW-3, F-VIEW-4, F-VIEW-11 |
| G-VIEW-3 | The coverage a reader sees is the coverage `measureCoverage` prints for the same knowledge and tests, the page says that it counts only the IDs a test names, and it names each part whose tests it could not read. | F-VIEW-5, F-VIEW-6, F-VIEW-12 |
| G-VIEW-4 | A reader reads a private repository, of the workspace or of a part, with a read-only token they name once and pick where it is needed. A token leaves the browser only to GitHub and is gone when the tab closes. | F-VIEW-7, F-VIEW-12 |
| G-VIEW-5 | A solution architect sees a workspace from a folder on their computer, with the parts cloned in it, cloned by a script the tracker gives for the refs picked. | F-VIEW-8, F-VIEW-16 |
| G-VIEW-6 | A repository, ref or folder that cannot be read is reported with the reason, and the rest of the page keeps working. | F-VIEW-9 |
| G-VIEW-7 | The page reads on a phone, also when the phone uses a dark theme. | F-VIEW-10 |
| G-VIEW-8 | Before reading a workspace, a reader sees whether the tracker can connect to it, to each of its parts' repositories and with each token, and what to do when it cannot. | F-VIEW-13 |
| G-VIEW-9 | A reader tries a change to the configuration of a workspace in the tracker, sees whether it is valid and what it builds, and the workspace stays unchanged. | F-VIEW-14, F-VIEW-15 |

## Flows

```mermaid
flowchart LR
    learn([Learn the framework]) --> view([View a workspace])
```

1. [Learn the framework](../flows/learn-framework.md)
2. [View a workspace](../flows/view-workspace.md)

Return to [goals](README.md).
