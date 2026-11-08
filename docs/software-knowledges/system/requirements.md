# Requirements

Requirements that every goal, flow and artifact of the framework follows. A
goal cites them by ID.

| ID | Requirement |
| --- | --- |
| SYS-1 | The scripts need Python 3 and its standard library only. `install.sh` needs POSIX `sh`, `curl` and `tar` only. A workspace installs no package to use the framework. |
| SYS-2 | Every script runs from the root of a workspace or from any folder under it, and reads the same workspace from each. |
| SYS-3 | A check exits with status 0 when it finds no problem, with 1 when it finds a problem, and with 2 when it cannot run. In one run it reports every problem it finds, one per line on standard error, and names the file of each problem that has one. |
| SYS-4 | The scripts read the workspace and change no file in it, except the page that the knowledge site writes. `install.sh` changes nothing outside the folder it creates. |
| SYS-5 | A new version of the framework keeps the commands, their arguments, the configuration keys and the knowledge forms that workspaces use. Knowledge that passes the checks of one version passes the checks of the next. |
| SYS-6 | The scripts read the knowledge and the tests as text, by the forms the knowledge rules give. They never run the code or the tests of a workspace. |
| SYS-7 | Framework-generated HTML treats workspace content as data, including configuration, names, paths, knowledge text and diagrams. In embedded JSON, HTML text, attributes and rendered diagrams, that content cannot create executable markup, event handlers or script URLs, escape its data context, or cause requests to destinations it supplies. The knowledge site retains its controls and diagram rendering; when a diagram cannot render, its source remains readable as text. This holds both for the standalone site and for the site embedded in the tracker. |
| SYS-8 | `index.html` is the canonical reading path for What it is, Knowledge, A change, Checks and Start. Readers can open each topic by a stable hash link and read without autoplay, including with reduced motion. The former `framework.html`, `how-we-work.html` and `agents.html` URLs, including their old hash links, lead to the matching canonical topic or reference; linked reference details open. Without a known fragment, each former URL uses its default destination: framework files, knowledge, or the worked change, respectively. Existing landing-page hash links remain usable. The reading path has a light theme, including on a dark-theme system, needs no horizontal scrolling at 360 px, needs no build and loads no script from another host. Its top and foot provide topic links and a link to the separate project tracker. Every name, file and ID it shows exists in the framework or its sample. |

## Released versions

A workspace runs the scripts it installed and takes a new version when its
team chooses ([context](context.md#supported-client-versions)). SYS-5 protects
the workspaces that take it.

## Open questions

- How a change that cannot keep SYS-5 is released and announced to the
  workspaces, and how long the old form stays valid (SYS-5).

Return to [system](README.md).
