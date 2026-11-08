# Framework pre-push hook

This opt-in hook is for contributors to this framework repository only.
The [workspace installer](../install.sh) does not copy it, its documentation,
or its [tests](../tests/hooks/README.md). It needs Git and Python 3 only.

## Enable in your clone

First review [pre-push](pre-push) and [pre_push.py](pre_push.py). From the
repository root, run these commands in a subshell:

```sh
(
  set -eu
  if git config --get core.hooksPath >/dev/null; then
    echo 'core.hooksPath is configured; stop and review your existing hooks.' >&2
    exit 1
  fi
  hooks=$(git rev-parse --git-path hooks)
  mkdir -p "$hooks"
  if [ -e "$hooks/pre-push" ] || [ -L "$hooks/pre-push" ]; then
    echo 'A pre-push hook already exists; stop and review it.' >&2
    exit 1
  fi
  # noclobber also refuses a hook created after the preceding check.
  (set -C; cat .githooks/pre-push > "$hooks/pre-push")
  chmod +x "$hooks/pre-push"
)
```

This copies a small wrapper into this clone's existing hooks directory. It
changes no Git configuration. The wrapper runs the checked-out helper, so
review hook changes before pushing. In linked worktrees, the hooks directory
can be shared. Do not use this setup if it would affect another worktree
without your agreement. To disable, remove only the wrapper you installed,
after checking that nobody has replaced or extended it.

## What a push does

The hook accepts one updated ref whose supplied object ID is the checked-out
HEAD commit. Other commits, tags that do not name that commit directly, and
multiple updated refs fail with instructions. Delete-only pushes pass.

For an existing remote ref, it compares the supplied remote commit with HEAD.
For a new branch, it uses the merge base of HEAD and the local
`refs/remotes/<remote>/main`. Missing commits or main history stop the push:
fetch the required history yourself and retry. The hook does not fetch or use
the network. Use a named remote for new branches.

The worktree and index must be entirely clean, including non-ignored untracked
files. Then the hook uses Git's whitespace repair on added or changed lines
in the pushed range. It uses a temporary index, applies only the resulting
repair to the worktree, and leaves the real index and commits unchanged.
If it repairs anything, it stops the push immediately: review the diff, stage
and commit the fixes, and push again. Do not edit files concurrently with a
push. Whitespace repair can change meaningful text, so always review it.

With no repairs, it runs native `git diff --check` on the same range, then
`python3 scripts/check_structure.py`, `python3 scripts/check_docs.py`,
`python3 scripts/check_tests.py`, and
`python3 -m unittest discover -s tests -t .`. A failed command blocks the push.
Conflict markers fail the Git check. Repairs to symlink targets or other
nonregular files stop for manual resolution without changing the worktree. Git commands use
`-c core.whitespace=-blank-at-eof`, as the repository's
[whitespace policy](../docs/governances/artifact-driven/runbooks/check.md)
requires: extra blank lines at EOF are allowed and unchanged.

This is not a semantic formatter or an OpenAPI linter. The repository has no
configured language formatter or linter. Contract changes still need the
checks in [Contributing](../CONTRIBUTING.md). The hook is a local convenience,
not a replacement for CI or review.

Return to the [project contents](../README.md).
