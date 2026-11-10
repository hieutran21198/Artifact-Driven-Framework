# Tests of scripts

Each test makes a small workspace in a temporary folder and runs a script of
[scripts](../../scripts/README.md) in it, as a person runs it.

[test_site.py](test_site.py) checks the actual generated HTML with hostile
configuration, knowledge text, paths and route data. It verifies the embedded
JSON and script hashes with the Python standard library. Flow-rule fixtures
check separate kinds, shared-rule deduplication, dependencies, aggregate
counts and design-link exclusion (KN-13, F-VIEW-31). When `node` is
installed, it also runs the side panel's Markdown renderer from the generated
page on a goal page and on raw HTML and unsafe links (F-VIEW-32, SYS-7):

```sh
python3 -m unittest tests.scripts.test_site -v
```

[test_site_browser.py](test_site_browser.py) runs that output in Chromium. It
checks Flow-rule details, repeated goal selection, both languages,
text and attribute sinks, controls, offline source fallback, unsafe
diagram syntax and the SVG output boundary. These tests use deterministic
Mermaid module responses and block other external requests. They do not
replace the acceptance check with the actual pinned Mermaid and ELK modules.
The [test setup](../README.md) lists the development-only browser dependencies
and the full unittest command. The scripts and generated site need no added
runtime package.

Return to [tests](../README.md).
