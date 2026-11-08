"""Check one pushed HEAD, with reviewable native Git whitespace repairs."""

import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


class HookError(Exception):
    """A push cannot be checked safely."""


def git(*args, data=None, env=None, allowed=(0,)):
    result = subprocess.run(
        ["git", "-c", "core.whitespace=-blank-at-eof", *args],
        input=data, capture_output=True,
        env=dict(os.environ if env is None else env, GIT_OPTIONAL_LOCKS="0"),
    )
    if result.returncode not in allowed:
        detail = (result.stderr + result.stdout).decode(errors="replace").strip()
        raise HookError(f"git {args[0]} failed: {detail}")
    return result.stdout


def commit(oid):
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", oid):
        raise HookError("invalid object ID in pre-push input")
    try:
        return git("rev-parse", "--verify", oid + "^{commit}").decode().strip()
    except HookError as error:
        raise HookError("pushed commit or remote base is unavailable; fetch it and retry") from error


def clean(head=None):
    if head and git("rev-parse", "--verify", "HEAD^{commit}").decode().strip() != head:
        raise HookError("HEAD changed during checks; retry the push")
    if git("status", "--porcelain=v1", "--untracked-files=all", "--ignore-submodules=none"):
        raise HookError("worktree and index must be clean, including untracked files; review, commit or stash work before retrying")


def base_for_push(remote, head):
    updates = []
    for line in sys.stdin:
        fields = line.split()
        if len(fields) != 4:
            raise HookError("invalid pre-push input")
        local_ref, local_oid, remote_ref, remote_oid = fields
        for oid in (local_oid, remote_oid):
            if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", oid):
                raise HookError("invalid object ID in pre-push input")
        git("check-ref-format", remote_ref)
        if set(local_oid) == {"0"}:
            continue
        # Git also accepts HEAD and revision expressions as local sources.
        # Use only the supplied, validated object ID, never that expression.
        if local_oid != head or commit(local_oid) != head:
            raise HookError("only the checked-out HEAD can be pushed; push one HEAD ref at a time")
        updates.append(remote_oid)
    if not updates:
        return None
    if len(updates) != 1:
        raise HookError("multiple updated refs are unsupported; push one HEAD ref at a time")
    remote_oid = updates[0]
    if set(remote_oid) != {"0"}:
        return commit(remote_oid)
    reference = f"refs/remotes/{remote}/main"
    git("check-ref-format", reference)
    try:
        upstream = git("rev-parse", "--verify", reference + "^{commit}").decode().strip()
        return git("merge-base", head, upstream).decode().strip()
    except HookError as error:
        raise HookError(f"new branch needs a local merge base with {reference}; fetch main and retry") from error


def repair(base, head):
    patch = git("diff", "--no-color", "--binary", "--full-index", "--src-prefix=a/", "--dst-prefix=b/", "--no-ext-diff", "--no-textconv",
                "--no-renames", base, head, "--")
    if not patch:
        return False
    with tempfile.TemporaryDirectory(prefix="framework-pre-push-") as folder:
        env = dict(os.environ, GIT_INDEX_FILE=str(Path(folder) / "index"))
        git("read-tree", base, env=env)
        git("apply", "--cached", "--whitespace=fix", "-", data=patch, env=env)
        entries = git("diff", "--no-color", "--cached", "--raw", "-z", "--no-renames", head, "--", env=env)
        for entry in entries.split(b"\0")[::2]:
            if entry and entry.split()[0:2] not in (
                [b":100644", b"100644"], [b":100755", b"100755"],
            ):
                raise HookError("whitespace repair affects a nonregular file; resolve it manually")
        fix = git("diff", "--no-color", "--cached", "--binary", "--full-index", "--src-prefix=a/", "--dst-prefix=b/", "--no-ext-diff",
                  "--no-textconv", "--no-renames", head, "--", env=env)
    if not fix:
        return False
    # Recheck before writing. The real index is never used for applying a patch.
    clean(head)
    git("apply", "--check", "--whitespace=nowarn", "-", data=fix)
    git("apply", "--whitespace=nowarn", "-", data=fix)
    return True


def main():
    try:
        if len(sys.argv) != 3:
            raise HookError("expected remote name and URL from Git pre-push")
        os.chdir(git("rev-parse", "--show-toplevel").decode().strip())
        head = git("rev-parse", "--verify", "HEAD^{commit}").decode().strip()
        base = base_for_push(sys.argv[1], head)
        if base is None:
            return 0
        clean(head)
        if repair(base, head):
            raise HookError("whitespace fixed in the worktree; push stopped. Review, stage and commit the fixes, then push again")
        git("diff", "--no-color", "--check", base, head, "--")
        for command in (
            [sys.executable, "scripts/check_structure.py"],
            [sys.executable, "scripts/check_docs.py"],
            [sys.executable, "scripts/check_tests.py"],
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-t", "."],
        ):
            print("pre-push: " + " ".join(command), flush=True)
            if subprocess.run(command).returncode:
                raise HookError("check failed: " + " ".join(command))
        clean(head)
        return 0
    except (HookError, OSError) as error:
        print(f"pre-push: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
