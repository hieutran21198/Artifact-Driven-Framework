# Tests of tracker

The browser checks use a local static server and seeded workspaces. Chromium
executes the tracker and the generated site. Repository responses are fixtures;
the tests do not need GitHub accounts or tokens.

The 18 `ScanSnapshotTests` use fixed analyzer results and block external
requests. The three `CoverageParityTests` run the real analyzer with
Pyodide 0.26.4. They compare browser coverage with the CLI, verify HTTP hashing
and initialization recovery, and check that workspace modules stay data.
These three tests require Chromium to reach
`https://cdn.jsdelivr.net/pyodide/v0.26.4/full/` for the pinned runtime files.
Other external requests remain blocked.

[Browser setup](../README.md) installs test-only dependencies. Run this part:

```sh
python3 -m unittest discover -s tests/tracker -t . -v
```

- [browser.py](browser.py): Chromium and the local static-server fixture.
- [test_frame_isolation.py](test_frame_isolation.py): frame origin, parent
  access and sizing-message validation (TRK-14, F-VIEW-25).
- [test_scan_snapshots.py](test_scan_snapshots.py): captured inputs, stale
  responses, cache identity, read outcomes, local reloads, coverage parity and
  trusted Python imports (TRK-15, TRK-16, TRK-17, SYS-6).

Run the scan fixtures and actual runtime checks separately when diagnosing an
environment problem:

```sh
python3 -m unittest tests.tracker.test_scan_snapshots.ScanSnapshotTests -v
python3 -m unittest tests.tracker.test_scan_snapshots.CoverageParityTests -v
```

The process must be able to launch Chromium and open loopback sockets. Missing
dependencies, denied sockets or unavailable runtime downloads fail the checks;
they do not silently skip them. Report those limits separately from assertions
about tracker behavior. Passing the fixture class does not prove the real
runtime checks.

Return to [tests](../README.md).
