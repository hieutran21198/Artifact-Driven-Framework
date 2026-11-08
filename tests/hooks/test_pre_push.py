"""GEN-704, GEN-705: real Git checks for the repository-only push workflow."""

import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
ZERO = "0" * 40


class PrePushTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.repo = self.home / "repo"
        self.repo.mkdir()
        self.remote = self.home / "remote.git"
        self.env = dict(os.environ, GIT_CONFIG_NOSYSTEM="1",
                        GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
        for key in list(self.env):
            if key.startswith("GIT_CONFIG_") and key not in ("GIT_CONFIG_NOSYSTEM", "GIT_CONFIG_GLOBAL"):
                del self.env[key]
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.name", "Hook Test")
        self.git("config", "user.email", "hook@example.invalid")
        self.git("init", "--bare", "-q", str(self.remote))
        self.git("remote", "add", "origin", str(self.remote))
        shutil.copytree(ROOT / ".githooks", self.repo / ".githooks")
        self.write("scripts/check_structure.py", "print('structure fixture passed')\n")
        self.write("scripts/check_docs.py", "print('docs fixture passed')\n")
        self.write("scripts/check_tests.py", "print('test IDs fixture passed')\n")
        self.write("tests/__init__.py", "")
        self.write("tests/test_fixture.py", "import unittest\nclass Fixture(unittest.TestCase):\n    def test_ok(self):\n        self.assertTrue(True)\n")
        self.write(".gitignore", "__pycache__/\n*.pyc\n")
        self.write("content.txt", "existing trailing  \nunchanged\n")
        self.commit()
        self.git("push", "-q", "origin", "main")
        self.base = self.head()
        shutil.copy2(self.repo / ".githooks/pre-push", self.repo / ".git/hooks/pre-push")

    def run_command(self, args, **kwargs):
        return subprocess.run(args, cwd=self.repo, env=kwargs.pop("env", self.env),
                              capture_output=True, text=True, **kwargs)

    def git(self, *args):
        result = self.run_command(["git", *args])
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return result.stdout.strip()

    def write(self, name, value):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

    def head(self):
        return self.git("rev-parse", "HEAD")

    def push(self, *refs):
        return self.run_command(["git", "push", "origin", *(refs or ("main",))])

    def hook(self, lines, env=None):
        return self.run_command([str(self.repo / ".git/hooks/pre-push"), "origin", str(self.remote)],
                                input=lines, env=env or self.env)

    def line(self, oid=None, base=None, name="main"):
        return f"refs/heads/{name} {oid or self.head()} refs/heads/{name} {base or self.base}\n"

    def assert_blocked(self, result, message):
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stderr + result.stdout)

    def test_clean_push_and_checks(self):
        self.write("new.txt", "clean\n")
        self.commit()
        result = self.push()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("docs fixture passed", result.stdout)
        self.assertEqual(self.git("ls-remote", "origin", "refs/heads/main").split()[0], self.head())

    def test_fix_blocks_preserves_index_head_remote_and_retry_succeeds(self):
        self.write("content.txt", "existing trailing  \nunchanged\nnew trailing  \n")
        self.commit()
        head = self.head()
        index = (self.repo / ".git/index").read_bytes()
        result = self.push()
        self.assert_blocked(result, "Review, stage and commit")
        self.assertNotIn("fixture passed", result.stdout)
        self.assertEqual(self.head(), head)
        self.assertEqual((self.repo / ".git/index").read_bytes(), index)
        self.assertEqual(self.git("write-tree"), self.git("rev-parse", "HEAD^{tree}"))
        self.assertEqual(self.git("ls-remote", "origin", "refs/heads/main").split()[0], self.base)
        self.assertEqual((self.repo / "content.txt").read_text(),
                         "existing trailing  \nunchanged\nnew trailing\n")
        self.commit()
        self.assertEqual(self.push().returncode, 0)

    def test_color_configuration_does_not_break_repair(self):
        self.git("config", "color.ui", "always")
        self.git("config", "diff.noprefix", "true")
        self.git("config", "diff.mnemonicPrefix", "true")
        self.write("new.txt", "bad  \n")
        self.commit()
        self.assert_blocked(self.push(), "Review, stage and commit")
        self.assertEqual((self.repo / "new.txt").read_text(), "bad\n")
        self.commit()
        self.assertEqual(self.push().returncode, 0)

    def test_unusual_filename_repair(self):
        name = "tab\tand\nnewline.txt"
        self.write(name, "bad  \n")
        self.commit()
        self.assert_blocked(self.push(), "Review, stage and commit")
        self.assertEqual((self.repo / name).read_text(), "bad\n")
        self.commit()
        self.assertEqual(self.push().returncode, 0)

    def test_extra_eof_blank_lines_unchanged(self):
        self.write("new.txt", "allowed\n\n\n")
        self.commit()
        self.assertEqual(self.push().returncode, 0)
        self.assertEqual((self.repo / "new.txt").read_text(), "allowed\n\n\n")
        self.assertEqual(self.git("status", "--porcelain"), "")

    def test_conflict_markers_rejected(self):
        self.write("new.txt", "<<<<<<< ours\na\n=======\nb\n>>>>>>> theirs\n")
        self.commit()
        self.assert_blocked(self.push(), "leftover conflict marker")

    def test_dirty_staged_untracked_untouched(self):
        self.write("new.txt", "bad  \n")
        self.commit()
        for kind in ("dirty", "staged", "untracked"):
            with self.subTest(kind=kind):
                self.write("content.txt" if kind != "untracked" else "loose.txt", "local\n")
                if kind == "staged":
                    self.git("add", "content.txt")
                before = self.git("diff", "HEAD")
                self.assert_blocked(self.push(), "must be clean")
                self.assertEqual(self.git("diff", "HEAD"), before)
                self.assertEqual((self.repo / "new.txt").read_text(), "bad  \n")
                self.git("reset", "--hard", "HEAD")
                if kind == "untracked":
                    self.assertEqual((self.repo / "loose.txt").read_text(), "local\n")
                    (self.repo / "loose.txt").unlink()

    def test_new_branch_uses_main_merge_base(self):
        self.git("checkout", "-qb", "feature")
        self.write("new.txt", "clean\n")
        self.commit()
        self.assertEqual(self.push("feature").returncode, 0)
        self.assertIn("existing trailing  ", (self.repo / "content.txt").read_text())

    def test_unknown_base_and_missing_main(self):
        self.assert_blocked(self.hook(self.line(base="a" * 40)), "fetch it")
        self.git("update-ref", "-d", "refs/remotes/origin/main")
        self.assert_blocked(self.hook(self.line(base=ZERO)), "fetch main")

    def test_non_head_multiple_refs_and_malformed_input(self):
        self.write("new.txt", "clean\n")
        self.commit()
        self.assert_blocked(self.hook(self.line(oid=self.base)), "checked-out HEAD")
        self.assert_blocked(self.hook(self.line() + self.line(name="other")), "multiple updated refs")
        self.assert_blocked(self.hook(self.line(oid="--help")), "invalid object ID")
        self.assert_blocked(self.hook("bad input\n"), "invalid pre-push input")

    def test_delete_only_passes_even_when_dirty(self):
        self.write("loose.txt", "local\n")
        self.assertEqual(self.hook(self.line(oid=ZERO)).returncode, 0)

    def test_missing_python_git_and_check_failure(self):
        bin_dir = self.home / "bin"
        bin_dir.mkdir()
        env = dict(self.env, PATH=str(bin_dir))
        self.assert_blocked(self.hook(self.line(), env), "Git is required")
        (bin_dir / "git").symlink_to(shutil.which("git"))
        self.assert_blocked(self.hook(self.line(), env), "Python 3 is required")
        self.write("scripts/check_docs.py", "raise SystemExit(2)\n")
        self.commit()
        self.assert_blocked(self.push(), "check failed")
        (self.repo / "scripts/check_docs.py").unlink()
        self.commit()
        self.assert_blocked(self.push(), "check failed")

    def test_binary_mode_and_symlink_not_changed(self):
        (self.repo / "binary").write_bytes(b"\x00bad  \n")
        self.write("executable", "#!/bin/sh\nexit 0\n")
        (self.repo / "executable").chmod(0o755)
        (self.repo / "link").symlink_to("content.txt")
        self.commit()
        self.assertEqual(self.push().returncode, 0)
        self.assertEqual((self.repo / "binary").read_bytes(), b"\x00bad  \n")
        self.assertTrue((self.repo / "executable").stat().st_mode & 0o111)
        (self.repo / "link").unlink()
        (self.repo / "link").symlink_to("target  ")
        self.commit()
        self.assert_blocked(self.push(), "nonregular file")
        self.assertEqual(os.readlink(self.repo / "link"), "target  ")
        self.assertEqual(self.git("diff", "HEAD"), "")

    def test_workspace_installer_excludes_hook_docs_and_tests(self):
        destination = self.home / "workspace"
        result = subprocess.run(["sh", str(ROOT / "install.sh"), str(destination)],
                                env=dict(self.env, AD_SOURCE=str(ROOT)), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse((destination / ".githooks").exists())
        self.assertFalse((destination / "tests").exists())
        self.assertNotIn(".githooks", (destination / "README.md").read_text())
