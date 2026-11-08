# Framework hook tests

Run `python3 -m unittest tests.hooks.test_pre_push` from the repository root.
The tests use temporary real Git repositories and a local bare remote. Their
small check scripts and test suite do no work outside those fixtures; they do
not recursively run the framework tests through the hook. No hook is installed
in the contributor's clone. The tests cover the repository-only developer
workflow, not a downstream knowledge requirement.

Return to [tests](../README.md).
