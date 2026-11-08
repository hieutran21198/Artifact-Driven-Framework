# Tests

The tests of the framework's parts, one folder for each part that
[services](../services/README.md) lists. Each test is named after the
knowledge ID it proves, and its docstring names the ID. `install.sh` never
copies this folder, so a workspace does not get it.

## Setup

The command-line checks use Python 3 and Git. Browser checks additionally use
Playwright and Chromium, only for development. Install the
[pinned Python packages](requirements-browser.txt) and Playwright's matching browser:

```sh
python3 -m pip install -r tests/requirements-browser.txt
python3 -m playwright install chromium
```

The harness also accepts a system `chromium` or `ADF_CHROMIUM_PATH` pointing
to a Chromium executable. It starts a loopback HTTP server, so the test
process needs permission to open local sockets. Missing browser dependencies
or a blocked browser launch fail the check rather than silently skip it.
These packages are not part of the static tracker or generated site.

## Run

Run all checks from the root:

```sh
python3 -m unittest discover -s tests -t .
```

- [scripts](scripts/README.md): the checks, impact and the site.
- [install](install/README.md): `install.sh`.
- [tracker](tracker/README.md): frame isolation and browser interaction.

Return to the [project contents](../README.md).
