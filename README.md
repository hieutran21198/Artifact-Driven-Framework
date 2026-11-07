# Artifact Driven

A framework for a whole team building software from knowledge: each person
owns their part, a service or a client, and people and AI agents do the work
together. The knowledge has four layers, each citing only the layers below it:

| Layer | Holds | ID |
| --- | --- | --- |
| System | Purpose, actors, services, clients, system-wide requirements, glossary, shared contract parts | `SYS-n` |
| Goal | A business outcome and its success criteria | `G-<GOAL>-n` |
| Flow | Behavior across artifacts, as testable scenarios that each name an operation, a trigger or a command | `F-<FLOW>-n` |
| Artifact | One domain: model, rules, lifecycle, OpenAPI contract, and what each client needs | `<PREFIX>-n` |

Every fact has one owner and an ID; other pages cite the ID. Because every
citation points down, scripts can trace a change in both directions: what a
rule affects, and what a goal relies on.

## Create a workspace

A project gets its own workspace, with the rules, the scripts and a sample to
start from. The installer needs `curl` and `tar`:

```sh
curl -fsSL https://raw.githubusercontent.com/hieutran21198/Artifact-Driven-Framework/main/install.sh | sh -s -- my-workspace
```

To read the script before it runs, or to take a fixed version, download it and
pass a branch, tag or commit as the second argument:

```sh
curl -fsSLO https://raw.githubusercontent.com/hieutran21198/Artifact-Driven-Framework/main/install.sh
sh install.sh my-workspace <ref>
```

The new workspace holds the shared files of this repository and, in place of
its knowledge, the sample of [template](template/README.md): a small library
lending service written from system down to client needs. Its README says what
to do next.

## Read the repository

This repository is the framework, and the framework manages itself with its
own knowledge. Every directory has a `README.md` that explains its purpose.

1. [install.sh](install.sh): creates a workspace.
2. [Template](template/README.md): the sample a new workspace starts from,
   and the files of a workspace that differ from this repository's.
3. [Documentation](docs/README.md): the rules of
   [Artifact Driven](docs/governances/artifact-driven/README.md), the
   architecture, standards, principles, and the framework's own
   [software knowledge](docs/software-knowledges/README.md).
4. [Scripts](scripts/README.md): the checks, the impact analysis and the
   knowledge site, set up by [artifact-driven.json](artifact-driven.json).
5. [Contributing](CONTRIBUTING.md): make and check a change.
6. [Project instructions](AGENTS.md): instructions for coding agents.
   [CLAUDE.md](CLAUDE.md) points Claude Code at them.
7. [Agent resources](.agents/README.md): the agent team and its skills.
8. [Claude Code](.claude/README.md): links Claude Code reads.
9. [Services](services/README.md), [applications](apps/README.md) and
   [end-to-end tests](e2e/README.md): where a workspace clones its parts.
10. [index.html](index.html): the landing page of the framework.

## Check a change

Run the checks here, and on a workspace the installer creates from this copy:

```sh
python3 scripts/check_structure.py
python3 scripts/check_docs.py
rm -rf /tmp/ad-check && AD_SOURCE=. sh install.sh /tmp/ad-check
cd /tmp/ad-check && git init -q && python3 scripts/check_structure.py && python3 scripts/check_docs.py
```

`AD_SOURCE` copies from a local copy instead of GitHub; use a clean one, since
it copies untracked files too.
