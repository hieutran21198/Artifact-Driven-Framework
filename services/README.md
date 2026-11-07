# Services

The parts of the framework that the team builds and releases. Unlike the
services of a workspace, they live in this repository, not in separate
clones. The service name is the one in the
[domain map](../docs/architecture/domain-map.md) and in
[artifact-driven.json](../artifact-driven.json).

| Service | Code | Tests | Owner | Stack |
| --- | --- | --- | --- | --- |
| `scripts` | [scripts](../scripts/README.md) | `tests/scripts` | `hieutran21198` | Python 3 |
| `install` | [install.sh](../install.sh) | `tests/install` | `hieutran21198` | POSIX `sh` |
| `landing` | [index.html](../index.html) | — | `hieutran21198` | One HTML file, no build |

The [domain map](../docs/architecture/domain-map.md) says which service serves
each domain. A new workspace gets the empty table of
[template](../template/services/README.md) in place of this page.

## Change a service

The implementer follows the [workflow](../docs/governances/artifact-driven/workflow.md)
and these instructions in place of a stack skill:

- Each service keeps the [system requirements](../docs/software-knowledges/system/requirements.md),
  such as what it may need to run (SYS-1) and what it may change (SYS-4).
- `scripts` reads [artifact-driven.json](../artifact-driven.json) through
  `project.py`.
- Tests use `unittest` and run with
  `python3 -m unittest discover -s tests -t .`. A test is named after the ID
  it proves, such as `test_SYS_1_...`, and its docstring names the ID, such
  as `SYS-1`. A test of `install` runs `install.sh` with `AD_SOURCE` into a
  temporary folder.
- Tests stay under `tests/`, which `install.sh` never copies, so a workspace
  does not get them.

Return to the [project contents](../README.md).
