"""Scenarios of the flow Install a workspace."""

from pathlib import Path
import os
import shutil
import subprocess
import tempfile
import unittest

FRAMEWORK = Path(__file__).resolve().parents[2]


def install(source, dest):
    env = {**os.environ, "AD_SOURCE": str(source)}
    return subprocess.run(["sh", str(FRAMEWORK / "install.sh"), str(dest)], env=env,
                          capture_output=True, text=True)


class InstallWorkspace(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        self.out = self.tmp / "out"
        self.out.mkdir()

    def test_F_START_10_source_that_is_no_folder_leaves_nothing(self):
        """F-START-10, WS-9: AD_SOURCE that names no folder fails, and no folder
        is left in out."""
        run = install(self.tmp / "no-such-copy", self.out / "ws")
        self.assertNotEqual(run.returncode, 0)
        self.assertEqual(list(self.out.iterdir()), [])

    def test_F_START_10_copy_that_stops_half_way_leaves_nothing(self):
        """F-START-10, WS-9: a local copy with no template folder stops the copy
        half way, and no folder is left in out."""
        source = self.tmp / "copy"
        shutil.copytree(FRAMEWORK, source, ignore=shutil.ignore_patterns(".git", "build", "template"))
        run = install(source, self.out / "ws")
        self.assertNotEqual(run.returncode, 0)
        self.assertEqual(list(self.out.iterdir()), [])

    @unittest.skipUnless(shutil.which("git"), "needs git")
    def test_F_START_11_git_copy_gives_no_ignored_file(self):
        """F-START-11, WS-10: a local copy that is a Git working tree gives the
        files it tracks and not the ones Git ignores."""
        source = self.tmp / "copy"
        shutil.copytree(FRAMEWORK, source, ignore=shutil.ignore_patterns(".git", "build", "__pycache__"))
        subprocess.run(["git", "init", "-q"], cwd=source, check=True)
        (source / "scripts" / "__pycache__").mkdir()
        (source / "scripts" / "__pycache__" / "check.pyc").write_text("x")
        (source / "docs" / "notes.swp").write_text("x")
        run = install(source, self.out / "ws")
        self.assertEqual(run.returncode, 0, run.stderr)
        ws = self.out / "ws"
        self.assertTrue((ws / "scripts" / "check_docs.py").is_file())
        self.assertFalse((ws / "scripts" / "__pycache__").exists())
        self.assertFalse((ws / "docs" / "notes.swp").exists())


if __name__ == "__main__":
    unittest.main()
