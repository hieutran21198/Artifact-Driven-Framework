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

- a rule restated instead of cited, or a layer citing a layer above it;
- a new ID that fails a question of [before adding a fact](../knowledge.md#before-adding-a-fact),
  such as a rule about layout, or one that another ID could hold;
- an open item on the issue that holds a goal ([questions](../workflow.md#questions));
- a diagram that adds a fact the text does not hold;
- a page that answers an open question a page below it leaves open;
- a flow step or scenario that states a condition no cited ID holds, such as
  a region, a role or a limit.

Return to [runbooks](README.md).
