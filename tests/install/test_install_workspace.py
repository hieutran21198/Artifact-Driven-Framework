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


if __name__ == "__main__":
    unittest.main()
