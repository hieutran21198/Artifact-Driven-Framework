# Check the docs

Use before every pull request that changes docs. Run from the repository root.

```sh
python3 scripts/check_structure.py
python3 scripts/check_docs.py
git diff --check
```

For each changed OpenAPI file:

```sh
npx @redocly/cli lint <knowledge folder>/<path>.yaml
```

| Check | Finds |
| --- | --- |
| `check_structure.py` | A directory without a README |
| `check_docs.py` | A broken link, a missing heading anchor, a knowledge ID that is cited but not defined, or a scenario that names no operation |
| `git diff --check` | Trailing spaces and conflict markers |
| Redocly lint | An invalid contract or a broken `$ref` |

Then read the changed pages once more for what the scripts cannot see: a rule
restated instead of cited, a layer citing a layer above it, or a diagram that
adds a fact the text does not hold.

Return to [runbooks](README.md).
