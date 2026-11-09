# Check the docs

Use before a docs branch goes to review, and again on the merge result before
the owners merge it. Run from the repository root. Post the results on the
issue.

```sh
python3 scripts/check_structure.py
python3 scripts/check_docs.py
git -c core.whitespace=-blank-at-eof diff --check
```

Also run these three in CI on each pull request into the default branch: agents
write most changes, and a check that someone must remember to run is skipped.
In CI, pass the complete PR range to the whitespace command instead of checking
the clean working tree. Use a full-history checkout and set `BASE_SHA` and
`HEAD_SHA` to the pull request's base and head commits:

```sh
git -c core.whitespace=-blank-at-eof diff --check "$BASE_SHA...$HEAD_SHA"
```

For staged changes, run:

```sh
git -c core.whitespace=-blank-at-eof diff --cached --check
```

These commands apply the [file conventions](../../../coding-standards/README.md#files-and-prose).
The `-c` option applies to one command; it does not save Git configuration.
Read new, untracked files during review because `git diff` does not include them.

Before a code change is merged, check the IDs its tests name. With no folder
the check reads the tests of every cloned part; pass the folder of the
change's worktree to check only that one:

```sh
python3 scripts/check_tests.py [tests folder]
```

For each changed OpenAPI file:

```sh
npx @redocly/cli lint <knowledge folder>/<path>.yaml
```

| Check | Finds |
| --- | --- |
| `check_structure.py` | A directory without a README |
| `check_docs.py` | A broken link, a missing heading anchor, a knowledge ID that is cited but not defined, defined twice, or withdrawn and still cited; a scenario that names no operation, trigger or command, and one that no scenario names |
| `check_tests.py` | A test that names an ID the knowledge does not define, or a withdrawn ID |
| Git whitespace check above | Trailing whitespace, spaces before tabs in indentation and conflict markers |
| Redocly lint | An invalid contract or a broken `$ref` |

Then read the changed pages once more for what the scripts cannot see:

- a rule restated instead of cited, or an invalid dependency under
  [Citations](../knowledge.md#citations), including Flow-rule chains or goals
  and scenarios used as reusable rules;
- policy ownership inferred only from data sources, or an unresolved owner
  decision written as settled knowledge;
- a design navigation link treated as a rule dependency or execution evidence,
  or copied visual detail that belongs to a client;
- a new ID that fails a question of [before adding a fact](../knowledge.md#before-adding-a-fact),
  such as a rule about layout, or one that another ID could hold;
- an open item on the issue that holds a goal ([questions](../workflow.md#questions));
- a diagram that adds a fact the text does not hold;
- a page that answers an open question a page below it leaves open;
- a flow step or scenario that states a condition no cited ID holds, such as
  a region, a role or a limit.

## Flow-rule adoption

Before allocating any `FR-<SCOPE>-<n>` product ID, verify all of these on the
exact tool version the workspace uses. Record results on the issue:

1. Docs checks recognize local and shared Flow-rule definitions and permitted
   citations, and reject missing, duplicate and withdrawn IDs. They reject
   forbidden dependencies, including Flow-rule chains.
2. Impact analysis follows the rule's dependencies and its consumers in both
   directions without treating links to client-owned design outside the knowledge graph
   as rule dependencies. Preserve dependency handling for links between
   software-knowledge pages.
3. Test-reference checks recognize Flow-rule IDs and reject missing or
   withdrawn references.
4. The knowledge viewer distinguishes rules from scenarios and shows their
   permitted dependencies without turning design references into execution
   evidence.
5. Inventory existing ID forms and namespace collisions, including `FR` used
   as an artifact prefix. Preserve previously accepted workspaces under the
   existing compatibility contract, or obtain the required owner decision
   before enforcement. Do not assume the proposed prefix is globally free.
6. Existing framework and installed-template samples still pass unchanged.

A passing check that does not recognize the proposed namespace is not support.
A docs-only proposal does not establish tool support. If any item is missing
or unverified, keep product IDs and contracts unchanged and report the gap for
separate tooling work. Review the method in prose; do not add temporary IDs,
relax a gate, or rewrite samples to make it appear supported.

Return to [runbooks](README.md).
