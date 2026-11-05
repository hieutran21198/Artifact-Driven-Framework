# Artifact Driven

A framework for building software from knowledge, with AI agents doing the
work and one person approving it.

Write and agree the knowledge first, then build the code that implements it,
and keep the code traceable to the knowledge. The knowledge has four layers,
each citing only the layers below it:

| Layer | Holds | ID |
| --- | --- | --- |
| System | Purpose, actors, containers, system-wide requirements, glossary, shared contract parts | `SYS-n` |
| Goal | A business outcome and its success criteria | `G-<GOAL>-n` |
| Flow | Behavior across artifacts, as testable scenarios that each name an operation | `F-<FLOW>-n` |
| Artifact | One domain: model, rules, lifecycle, OpenAPI contract, and what each client needs from its responses | `<PREFIX>-n` |

Every fact has one owner and an ID; other pages cite the ID. Because every
citation points down, scripts can trace a change in both directions: what a
rule affects, and what a goal relies on.

## Contents

- [Documentation](docs/README.md)
  - [Artifact Driven](docs/artifact-driven/README.md): the knowledge rules,
    the workflow, the team of agents, the definition of done (D1 to D7) and
    the runbooks.
  - [Software knowledge](docs/software-knowledge/README.md): the reference
    pass, a small library lending service written from system down to client
    needs. Every rule of the framework shows in it.
  - [Diagrams](docs/diagrams/README.md): which Mermaid diagrams to draw and
    how.
- [Scripts](scripts/README.md): the structure, docs and test checks, the
  impact analysis and the bilingual knowledge site, set up by
  [artifact-driven.json](artifact-driven.json).
- [Agent resources](.agents/README.md): one agent per role and the skills
  they use. Claude Code reads them through [.claude](.claude/README.md).
- [Project instructions](AGENTS.md): a template for the project's agent
  instructions.

## Try it

From this folder, with Git and Python 3:

```sh
python3 scripts/check_structure.py
python3 scripts/check_docs.py
python3 scripts/impact.py --stats
python3 scripts/impact.py BK-3
python3 scripts/impact.py --fragile
python3 scripts/site.py
```

`site.py` writes `build/site/index.html`. Open it, pick the goal and analyze.

## Apply it to a project

1. **Copy the framework** into the project repository, or into a separate
   knowledge repository next to the code: `docs/`, `scripts/`, `.agents/`,
   `.claude/`, `AGENTS.md`, `artifact-driven.json` and the `.gitignore`
   lines. Keep the folder layout; the pages link to each other by relative
   path.
2. **Configure** [artifact-driven.json](artifact-driven.json): the knowledge
   folder, the folders the docs check skips (such as checked-out client or
   service code), the clients that get client pages, where the tests live,
   where the site finds backend routes, and the site title. [Scripts](scripts/README.md#configuration)
   describes each key.
3. **Replace the reference pass.** Write the project's own system pages
   first: context, requirements, glossary and the shared contract parts. Keep
   the `book` and `member` pages and the `Borrow a book` goal as samples until
   the first real goal, flow and artifact exist, then delete them and point
   the runbooks' samples at the real pages.
4. **Fill in the template.** Complete [AGENTS.md](AGENTS.md) with the
   project's repositories, code standards and deploy procedure. Add a code
   skill for the implementer and the read-only commands the defect
   investigator may run.
5. **Start from one goal.** Pick one business outcome, write its goal, its
   flows and the artifacts they cross, with contracts and client pages, by the
   [runbooks](docs/artifact-driven/runbooks/README.md). Run the checks after
   each step.
6. **Work by the workflow.** Every change starts as an issue and goes through
   knowledge, contract, code and review as [Workflow](docs/artifact-driven/workflow.md)
   and [Team](docs/artifact-driven/team.md) say. The one person in the loop
   approves: knowledge by merging its branch
   ([approval of knowledge](docs/artifact-driven/README.md#approval-of-knowledge)),
   code by approving its pull request.

## Requirements

Python 3.9 or later and Git. `npx @redocly/cli lint` checks the contracts and
needs Node.js.
