# Reading guide tests

[test_reading_pages.py](test_reading_pages.py) checks the canonical topics,
local links, compatibility entrypoints and source references without a browser.
Its focused content assertions protect layer relationships, scan limits, test
and diagram mappings, role and approval boundaries, task resources, tool
instructions, and the prompt's review checklist. They check statements in the
relevant section, not whether a reader understands them.

[test_reading_sample.py](test_reading_sample.py) installs the local checkout
into a temporary workspace with `AD_SOURCE`, then checks the advertised file
tree, Claude Code links, agent roles, sample citations and the real impact of
the worked rule. It needs Python 3, Git and POSIX `sh`, but no network access.

```sh
python3 -m unittest tests.landing.test_reading_pages tests.landing.test_reading_sample -v
```

[test_reading_pages_browser.py](test_reading_pages_browser.py) checks the actual
guide and old URLs in Chromium: viewport arrival after topic and legacy-link
navigation, details, keyboard focus, Back and Forward, exact clipboard content
and failure feedback, no-script fallback, blocked external resources and narrow
screens. It checks the tracker links in the top and foot navigation.
It uses the existing [browser dependencies](../README.md#setup) and does not
replace visual review of the page.

```sh
python3 -m unittest tests.landing.test_reading_pages_browser -v
```

## Evidence limits

A test's IDs identify the contract slice it exercises. A green content or
local browser check is not evidence of comprehension, a successful agent run
or the deployed site. Keep these review checks explicit on the pull request:

- Read the complete guide and opened references for misleading costs, timing,
  status, promotional language, invented results or unsupported promises
  (F-LEARN-6). Text-pattern tests do not establish the absence of such claims.
- Compare the explanations with the governing sources, including the plain
  meaning of diagrams, term comparisons, suggested versus required practices,
  and current vendor documentation. The tests check links and selected
  statements, not every assertion the pages or vendors make.
- Ask a new reader to explain the layers, traceability limits, responsibilities
  and approval boundaries. Goal-level understanding needs human evidence;
  string and DOM checks are not an end-to-end comprehension test.
- Check the published old URLs and source links. The browser harness blocks
  other hosts, and a source file existing locally does not prove GitHub Pages
  or the linked main-branch file has been published (F-LEARN-13).
- Run the copied network install command from the published guide when that
  environment is available (F-LEARN-8). The local installer check deliberately
  uses this checkout rather than downloading main.
- Give the sample-change prompt to an agent in a new workspace and review its
  actual decisions, output and limits (F-LEARN-28). Checking the supplied prompt
  and checklist does not execute or predict that agent's work.

Record browser launch or socket failures as blocked checks, not skips or passes.
Inspect desktop and mobile rendering as well as the automated overflow checks.

Return to [tests](../README.md).
