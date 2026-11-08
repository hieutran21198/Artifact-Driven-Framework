# Tests of tracker

The browser checks use a local static server and seeded workspaces. Chromium
executes the tracker and the generated site. External requests are blocked
unless a test supplies a fixed response.

[Browser setup](../README.md) installs test-only dependencies. Run this part:

```sh
python3 -m unittest discover -s tests/tracker -t . -v
```

- [browser.py](browser.py): Chromium and the local static-server fixture.
- [test_frame_isolation.py](test_frame_isolation.py): frame origin, parent
  access and sizing-message validation (TRK-14, F-VIEW-25).

Return to [tests](../README.md).
