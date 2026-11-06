# End-to-end tests

The end-to-end tests of the goals, owned by the quality owner named in
[Contributing](../CONTRIBUTING.md#owners). They start at a trigger (a client
request, a webhook or a worker run) against deployed services, and each test
names the goal criterion it proves (`G-<GOAL>-n`, D3 of
[Done](../docs/governances/artifact-driven/done.md)) and the scenarios it
passes through.

Keep them in their own repository, cloned here and ignored by this workspace:

```sh
git clone <repository URL> e2e/suite
```

The `e2e` setting of [artifact-driven.json](../artifact-driven.json) points
the test check and the test coverage at them; set its `glob` to the suite's
test files, such as `**/*.spec.*`.

Return to the [project contents](../README.md).
