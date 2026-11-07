# Tests

The tests of the framework's parts, one folder for each part that
[services](../services/README.md) lists. Each test is named after the
knowledge ID it proves, and its docstring names the ID. `install.sh` never
copies this folder, so a workspace does not get it.

Run them from the root:

```sh
python3 -m unittest discover -s tests -t .
```

- [scripts](scripts/README.md): the checks, impact and the site.
- [install](install/README.md): `install.sh`.

Return to the [project contents](../README.md).
