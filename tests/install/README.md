# Tests of install

Each test runs [install.sh](../../install.sh) with `AD_SOURCE` into a
temporary folder. The installed-sample regression runs structure and docs
checks, Flow-rule test references, bidirectional impact, aggregate rule
coverage and site generation. It also checks that the parser, landing-page
guide and skill are copied. Unknown test-reference scopes retain the existing
filtering behavior; a passing check does not establish that their IDs exist.

Run this part from the repository root:

```sh
python3 -m unittest discover -s tests/install -t .
```

Return to [tests](../README.md).
