# Artifact Driven workspace

A workspace for a whole team building software from knowledge: each person
owns their part, a service or a client, and people and AI agents do the work
together. It holds for one backend or for many services. It was created by the
[Artifact Driven](https://github.com/hieutran21198/Artifact-Driven-Framework)
installer. The services and the client applications stay
in their own repositories and are cloned here; this workspace holds the
knowledge around them: software knowledge, architecture, standards and agent
guidance.

Write and agree the knowledge first, then build the code that implements it,
and keep the code traceable to the knowledge. The knowledge has four layers:

| Layer | Holds | ID |
| --- | --- | --- |
| System | Purpose, actors, services, clients, system-wide requirements, glossary, shared contract parts | `SYS-n` |
| Goal | A business outcome and its success criteria | `G-<GOAL>-n` |
| Flow | Behavior across artifacts, as testable scenarios that each name an operation, a trigger or a command | `F-<FLOW>-n` |
| Artifact | One domain: model, rules, lifecycle, OpenAPI contract, and what each client needs | `<PREFIX>-n` |

Every fact has one owner and an ID; other pages cite the ID. Follow the
[knowledge rules](docs/governances/artifact-driven/knowledge.md#citations) for
dependency direction and Flow-rule adoption prerequisites. The scripts trace
supported knowledge IDs in both directions: what a rule affects,
and what a goal relies on.

## Read the repository

Treat the project as a book. This README is its contents page. Every directory
has a `README.md` that explains its purpose and links to its contents.

1. [Contributing](CONTRIBUTING.md): make and check a change.
2. [Project instructions](AGENTS.md): instructions for coding agents.
   [CLAUDE.md](CLAUDE.md) points Claude Code at them.
3. [Documentation](docs/README.md): architecture, software knowledge,
   governances, infrastructure, standards and principles.
4. [Services](services/README.md): the services, one or many, as separate
   clones.
5. [Applications](apps/README.md): the client applications, as separate clones.
6. [End-to-end tests](e2e/README.md): the tests of the goals, as a separate
   clone.
7. [Scripts](scripts/README.md): the checks, the impact analysis and the
   knowledge site, set up by [artifact-driven.json](artifact-driven.json).
8. [Agent resources](.agents/README.md): the agent team and its skills.
9. [Claude Code](.claude/README.md): links Claude Code reads.

The [software knowledge](docs/software-knowledges/README.md) holds a reference
pass: a small library lending service, written from system down to client
needs. Every rule of [Artifact Driven](docs/governances/artifact-driven/README.md)
shows in it. Try the scripts on it:

```sh
python3 scripts/check_structure.py
python3 scripts/check_docs.py
python3 scripts/impact.py --stats
python3 scripts/impact.py BK-3
python3 scripts/site.py
```

`site.py` writes `build/site/index.html`. Open it, pick the goal and analyze.

## Start a new project

1. **Start the repository** and name the workspace: rename the title of this
   README and of the knowledge site (`site.title` in
   [artifact-driven.json](artifact-driven.json)).

   ```sh
   git init
   ```

2. **Clone the services and the clients**, one or many of each, and fill in
   the tables in [services](services/README.md) and
   [applications](apps/README.md), with the owner of each:

   ```sh
   git clone <service repository URL> services/<service>
   git clone -b <working branch> <client repository URL> apps/<client>
   ```

   List the clients under `clients` and the services under `services` in
   [artifact-driven.json](artifact-driven.json), with the same names as their
   folders, and point each service's `routes` and `tests` at its code
   ([configuration](scripts/README.md#configuration)).
3. **Describe the system.** Rewrite the pages in
   [system](docs/software-knowledges/system/README.md): context, actors,
   services, clients, requirements, glossary, supported client versions and the
   shared contract parts. Fill in the
   [domain map](docs/architecture/domain-map.md), the
   [infrastructure](docs/infrastructure/README.md) pages and the deploy table
   in [Contributing](CONTRIBUTING.md).
4. **Write the first goal** by the
   [runbooks](docs/governances/artifact-driven/runbooks/README.md): the goal,
   its flows, the artifacts they cross, their contracts and the client pages.
   Run the checks after each step.
5. **Remove the reference pass** once the first real goal, flow and artifact
   exist: delete the `book`, `member` and `notice` artifacts, the `Borrow a
   book` goal and its flows, and the `lending` and `notification` rows in
   [services](services/README.md), the domain map, the context and
   [artifact-driven.json](artifact-driven.json); then point the runbooks'
   samples and the architecture examples at the real pages.
6. **Work by the workflow.** Every change starts as an issue and goes through
   knowledge, contract, code and review as
   [Workflow](docs/governances/artifact-driven/workflow.md) and
   [Team](docs/governances/artifact-driven/team.md) say. The owner of each part
   a change touches approves it: knowledge by merging its branch
   ([approval of knowledge](docs/governances/artifact-driven/README.md#approval-of-knowledge)),
   code by approving its pull request.

## Get started on a clone

Clone the services and the clients as [services](services/README.md) and
[applications](apps/README.md) show, then check the structure:

```sh
python3 scripts/check_structure.py
```

The check reads tracked and untracked, non-ignored files. It reports any
directory that has content but no `README.md`.

The scripts need Python 3.9 or later and Git. `npx @redocly/cli lint` checks
the contracts and needs Node.js.
