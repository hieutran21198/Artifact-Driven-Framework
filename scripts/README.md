# Scripts

Small commands that check and read the software knowledge. They need Python 3
only, with no additional packages, and change no file except the site output.
Run them from the repository root or any folder under it.

## Configuration

[project.py](project.py) reads `artifact-driven.json` from the repository
root. The root is the nearest folder, from the current folder up, that holds
that file. Every key is optional.

| Key | Holds | Default |
| --- | --- | --- |
| `knowledge` | The knowledge folder, relative to the root | `docs/software-knowledge` |
| `skip` | Folder names whose Markdown the docs check skips, such as checked-out client or service code | `.git`, `node_modules`, `build` |
| `clients` | The client pages an artifact may have: file name without `.md`, mapped to the name the site shows | none |
| `routes` | Where the site finds the backend routes for API coverage: `folders` (relative to the root), `glob`, and `pattern`, a regular expression with the named groups `method` and `path` | none: the site leaves API coverage out |
| `tests` | Where the tests live: `folder` (relative to the root) and `glob`, the test files under it | none, `**/*_test.*` |
| `site` | `title` of the site and `output`, the file it writes | `Software knowledge`, `build/site/index.html` |

A `routes` setting for a backend that documents its handlers with
`swagger:operation` comments looks like this:

```json
"routes": {
  "folders": ["src/api"],
  "glob": "**/*.go",
  "pattern": "swagger:operation (?P<method>GET|POST|PUT|PATCH|DELETE) (?P<path>\\S+)"
}
```

## Structure check

Run [check_structure.py](check_structure.py):

```sh
python3 scripts/check_structure.py
```

The check needs Git. It checks each directory represented by tracked or
untracked, non-ignored files, including intermediate directories and the
repository root. Each needs `README.md`. Ignored generated directories, Git
internals and the contents of submodules are outside the check.

The command prints missing READMEs and exits with status 1 when it finds any.
It exits with status 0 on success and status 2 if Git cannot supply the file list.
It does not check Markdown navigation links.

## Docs check

Run [check_docs.py](check_docs.py):

```sh
python3 scripts/check_docs.py
```

It checks every Markdown file outside the `skip` folders for broken relative
links and missing heading anchors. In the knowledge folder it checks that
every cited ID is defined, once, and not withdrawn; that every scenario that is
not withdrawn names an `operationId` or a trigger under `x-triggers`; and that
every operation and trigger is named by a scenario. It lists the problems and
exits with status 1 when it finds any.

## Test check

Run [check_tests.py](check_tests.py) on the checkout of a code change:

```sh
python3 scripts/check_tests.py [tests folder]
```

It reads the test files that the `tests` setting names, or those under the
folder given, and reports a test that names a knowledge ID the knowledge does
not define, or a withdrawn one. It looks only at IDs whose prefix the
knowledge uses. Without a folder or a `tests` setting it exits with status 2.

## Impact

Run [impact.py](impact.py) to see what in the software knowledge depends on an
ID, an `operationId` or a response field. With the reference pass:

```sh
python3 scripts/impact.py BK-3
python3 scripts/impact.py getBook
python3 scripts/impact.py due_at
python3 scripts/impact.py --down G-BORROW-1
python3 scripts/impact.py --stats
python3 scripts/impact.py --stats MBR-4
```

It follows the citations: rule IDs in tables, `operationId`s in backticks,
`$ref`s in contracts, schema properties, and links from a goal to its flows and
from a flow to its artifacts. `--down` lists what a goal criterion, a scenario
or a page relies on instead.

`--stats` counts instead of listing. With no argument it prints the size of
each goal (criteria, flows, scenarios, rules, operations, artifacts and client
pages it relies on) and the blast radius of each requirement, rule and
operation (the flows, scenarios, operations and client pages a change to it
affects), largest first. With an argument it prints both counts for that goal
(such as `G-BORROW`), ID or operation. A rule with no scenario shows 0
scenarios: a gap in the flows.

`--fragile [tests folder]` ranks the 20 nodes a change would break most and
that are proved least: requirements, rules, operations and schemas, by reach
times weakness. With a tests folder, or the `tests` setting, a rule no test
names counts as weaker:

```sh
python3 scripts/impact.py --fragile
```

`--coverage [tests folder]` gives, for each goal, the share of the scenarios
and rules it relies on that a test names by ID (D3 of Done), and lists the
ones no test names. Without a folder it uses the `tests` setting.
`--questions` lists, for each goal, the open questions that cite an ID or an
operation the goal relies on; a goal with open questions is not ready to
build:

```sh
python3 scripts/impact.py --coverage tests
python3 scripts/impact.py --questions
```

A worker trigger declared under `x-triggers` counts as an operation, a client
page heading that names a payload schema cites that schema, and a heading that
names a rule ID (`### BK-4`) cites that rule. A scenario that names no
operation, trigger or rule is invisible to it.

## Knowledge site

Run [site.py](site.py) to build one HTML page of the software knowledge and
its metrics:

```sh
python3 scripts/site.py
python3 scripts/site.py --routes src/api
```

It writes the `site.output` file, which should be ignored by Git. The page
shows the overview of the whole project and a guide to reading it. Pick up to
three goals, or all goals, and analyze: the page then shows, for those goals
only, the counts, the API coverage (when `routes` is set), each goal with its
criteria and scenarios, an impact explorer, the blast radius table, the gaps,
and what each client needs from the responses. It reads in English or
Vietnamese. [site.html](site.html) is its template. It reuses `impact.py` and
loads nothing from the network. Each `--routes` folder replaces the folders of
the `routes` setting; the `glob` and `pattern` still come from it.

Return to the [repository contents](../README.md).
