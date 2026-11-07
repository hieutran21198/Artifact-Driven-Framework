# Requirements

Requirements that every goal, flow and artifact of the framework follows. A
goal cites them by ID.

| ID | Requirement |
| --- | --- |
| SYS-1 | The scripts need Python 3 and its standard library only. `install.sh` needs POSIX `sh`, `curl` and `tar` only. A workspace installs no package to use the framework. |
| SYS-2 | Every script runs from the root of a workspace or from any folder under it, and reads the same workspace from each. |
| SYS-3 | A check exits with status 0 when it finds no problem, and with a status other than 0 when it finds a problem or cannot run. In one run it reports every problem it finds, one per line on standard error, and names the file of each problem that has one. |
| SYS-4 | The scripts read the workspace and change no file in it, except the page that the knowledge site writes. `install.sh` changes nothing outside the folder it creates. |
| SYS-5 | A new version of the framework keeps the commands, their arguments, the configuration keys and the knowledge forms that workspaces use. Knowledge that passes the checks of one version passes the checks of the next. |
| SYS-6 | The scripts read the knowledge and the tests as text, by the forms the knowledge rules give. They never run the code or the tests of a workspace. |

## Released versions

A workspace runs the scripts it installed and takes a new version when its
team chooses ([context](context.md#supported-client-versions)). SYS-5 protects
the workspaces that take it.

## Open questions

- How a change that cannot keep SYS-5 is released and announced to the
  workspaces, and how long the old form stays valid (SYS-5).

Return to [system](README.md).
