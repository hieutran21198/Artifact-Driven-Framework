# Context

Artifact Driven lets a team build software from knowledge: goals, flows and
artifacts with IDs, which scripts check and trace, and which tests name. It is
a set of rules, a workspace a project installs, and the tools that read the
knowledge.

```mermaid
flowchart LR
    architect([Solution architect])
    dev([Implementer])
    agent([Coding agent])

    subgraph framework [Artifact Driven]
        install[install.sh]
        scripts[scripts: checks, impact, site]
        viewer[knowledge viewer]
    end

    github[(GitHub)]
    pyodide[(Pyodide on jsDelivr)]

    architect & dev & agent --> scripts
    architect --> viewer
    install -- "downloads the workspace" --> github
    viewer -- "reads repositories" --> github
    viewer -- "loads Python" --> pyodide
```

## Actors

| Actor | Uses |
| --- | --- |
| Solution architect | Writes and reviews the knowledge; reads impact and coverage across workspaces |
| Implementer | Builds a service or a client from the knowledge; names knowledge IDs in tests |
| Coding agent | Writes knowledge and code by the runbooks, and runs the checks |

## Parts

| Part | Holds |
| --- | --- |
| `install.sh` | Creates a workspace from the shared files and the sample |
| `scripts` | The structure, docs and test checks, impact analysis and the knowledge site |
| Knowledge viewer | The knowledge site of several workspaces in the browser |

## Supported client versions

A workspace runs the scripts it installed. A new version of the framework does
not change a workspace until the workspace takes it.

Return to [system](README.md).
