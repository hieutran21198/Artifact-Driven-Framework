"""Scenarios of the flow Install a workspace."""

from pathlib import Path
import json
import os
import re
import sys
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

    def test_F_START_5_project_decisions_come_from_the_sample(self):
        """F-START-5, WS-11: the architecture decisions of a new workspace are the
        sample's, not the framework project's."""
        source = self.tmp / "source"
        shutil.copytree(FRAMEWORK, source, ignore=shutil.ignore_patterns(".git", "build"))
        (source / "docs/architecture/decisions.md").write_text("# Decisions\n\n## A framework project choice\n")
        run = install(source, self.out / "ws")
        self.assertEqual(run.returncode, 0, run.stderr)
        ws = self.out / "ws"
        self.assertEqual((ws / "docs/architecture/decisions.md").read_bytes(),
                         (FRAMEWORK / "template/docs/architecture/decisions.md").read_bytes())
        self.assertEqual((ws / "docs/governances/artifact-driven/decisions.md").read_bytes(),
                         (FRAMEWORK / "docs/governances/artifact-driven/decisions.md").read_bytes())

    @unittest.skipUnless(shutil.which("git"), "needs git")
    def test_F_START_6_flow_rule_sample_runs_with_installed_tools(self):
        """F-START-6, WS-3, WS-11, KN-13: installed tools read the sample rule."""
        ws = self.out / "ws"
        run = install(FRAMEWORK, ws)
        self.assertEqual(run.returncode, 0, run.stderr)
        subprocess.run(["git", "init", "-q"], cwd=ws, check=True)
        for name in ("scripts/flow_rules.py",
                     "docs/coding-standards/landing-pages/README.md",
                     ".agents/skills/landing-page/SKILL.md"):
            self.assertEqual((ws / name).read_bytes(), (FRAMEWORK / name).read_bytes())

        def command(script, *args, status=0):
            result = subprocess.run([sys.executable, "scripts/" + script, *args],
                                    cwd=ws, capture_output=True, text=True)
            self.assertEqual(result.returncode, status, result.stdout + result.stderr)
            return result.stdout + result.stderr

        command("check_structure.py")
        command("check_docs.py")
        down = command("impact.py", "--down", "FR-RETURN-1")
        self.assertIn("Flow rules: FR-RETURN-1", down)
        self.assertIn("Artifact rules: BK-6, NTC-1", down)
        self.assertIn("SYS-8", down)
        up = command("impact.py", "FR-RETURN-1")
        for name in ("G-BORROW-5", "G-BORROW-7", "F-RETURN-3", "F-RETURN-8",
                     "F-RETURN-9", "F-RETURN-10"):
            self.assertIn(name, up)

        checks = ws / "checks"
        checks.mkdir()
        test = checks / "rule_test.py"
        test.write_text("# FR-RETURN-1\n")
        command("check_tests.py", "checks")
        coverage = command("impact.py", "--coverage", "checks")
        self.assertRegex(coverage, r"all +criteria 0/\d+ +scenarios 0/\d+ +rules 1/\d+")
        self.assertNotIn("FR-RETURN-1", coverage)
        test.write_text("# FR-RETURN-99\n")
        self.assertIn("FR-RETURN-99", command("check_tests.py", "checks", status=1))
        test.write_text("# FR-UNKNOWN-1\n")
        command("check_tests.py", "checks")

        command("site.py")
        html = (ws / "build/site/index.html").read_text()
        data = json.loads(re.search(r"<script>const DATA=(.*?);</script>", html).group(1))
        self.assertEqual(len(data["flowRules"]), 1)
        rule = data["flowRules"][0]
        self.assertEqual(rule["id"], "FR-RETURN-1")
        edges = data["graph"]["edges"]
        self.assertLessEqual({"BK-6", "NTC-1", "SYS-8"}, {b for a, b in edges if a == "FR-RETURN-1"})
        scenarios = [scenario for flow in data["flows"] for scenario in flow["scenarios"]]
        self.assertNotIn("FR-RETURN-1", [scenario["id"] for scenario in scenarios])
        self.assertEqual({scenario["id"] for scenario in scenarios
                          if "FR-RETURN-1" in scenario["covers"]},
                         {"F-RETURN-3", "F-RETURN-8", "F-RETURN-9", "F-RETURN-10"})

    def test_KN_16_F_VIEW_32_story_of_the_sample_goal(self):
        """KN-16, F-VIEW-32: the story of G-BORROW holds its flows, rules and artifacts."""
        ws = self.out / "ws"
        run = install(FRAMEWORK, ws)
        self.assertEqual(run.returncode, 0, run.stderr)

        def command(script, *args):
            result = subprocess.run([sys.executable, "scripts/" + script, *args],
                                    cwd=ws, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return result.stdout

        command("site.py")
        html = (ws / "build/site/index.html").read_text()
        story = json.loads(re.search(r"<script>const DATA=(.*?);</script>", html).group(1))["stories"]["G-BORROW"]
        self.assertEqual([f["page"] for f in story["flows"]], ["flows/borrow-book.md", "flows/return-book.md"])
        down = command("impact.py", "--down", "G-BORROW")
        expected = {i for line in down.splitlines() if line.startswith(("Artifact rules: ", "Flow rules: "))
                    for i in line.split(": ", 1)[1].split(", ")}
        listed = [i for f in story["flows"] for i in f["rules"]]
        self.assertEqual(len(listed), len(set(listed)))
        self.assertEqual(set(listed), expected)
        self.assertEqual(set(story["artifacts"]), {"book", "member", "notice"})
        held = {i for rules in story["artifacts"].values() for i in rules}
        self.assertEqual(held, {i for i in expected if not i.startswith("FR-")})

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
