"""Scenarios of the flow Check a change."""

import unittest

from tests.scripts.workspace import Workspace

INVALID = '{\n  "knowledge": "docs/software-knowledges",\n  "skip": [,]\n}\n'


class CheckChange(unittest.TestCase):
    def test_F_CHECK_21_invalid_configuration_stops_each_check_with_one_line(self):
        """F-CHECK-21, CFG-7, SYS-3: each check exits with 2 and one line that
        names artifact-driven.json, its line and its column."""
        ws = Workspace(raw=INVALID)
        self.addCleanup(ws.close)
        ws.git()
        for script in ("check_structure.py", "check_docs.py", "check_tests.py"):
            with self.subTest(script=script):
                run = ws.run(script)
                self.assertEqual(run.returncode, 2)
                lines = run.stderr.strip().splitlines()
                self.assertEqual(len(lines), 1)
                self.assertIn("artifact-driven.json:3:", lines[0])
                self.assertNotIn("Traceback", run.stderr)

    def test_F_CHECK_21_configuration_that_is_not_an_object(self):
        """F-CHECK-21, CFG-7: a JSON list is not a configuration."""
        ws = Workspace(raw="[]\n")
        self.addCleanup(ws.close)
        run = ws.run("check_docs.py")
        self.assertEqual(run.returncode, 2)
        self.assertIn("not a JSON object", run.stderr)

    def test_F_CHECK_22_repeated_headings_take_numbered_anchors(self):
        """F-CHECK-22, REPO-3: the second Rules heading is #rules-1, and there
        is no #rules-2."""
        ws = Workspace({})
        self.addCleanup(ws.close)
        ws.write("page.md", "# Page\n\n## Rules\n\n## Rules\n\n"
                            "[a](#rules) [b](#rules-1) [c](#rules-2)\n")
        run = ws.run("check_docs.py")
        self.assertEqual(run.returncode, 1)
        self.assertEqual(run.stderr.strip().splitlines(), ["page.md: missing anchor #rules-2"])

    def test_F_CHECK_17_missing_folder_cannot_run(self):
        """F-CHECK-17, SYS-3: checkTests with a folder that does not exist
        exits with 2."""
        ws = Workspace({})
        self.addCleanup(ws.close)
        run = ws.run("check_tests.py", "no-such-folder")
        self.assertEqual(run.returncode, 2)
        self.assertIn("Not a folder", run.stderr)

    def test_F_CHECK_16_parts_with_tests_and_no_folder_cannot_run(self):
        """F-CHECK-16, TST-6, SYS-3: parts have a tests setting and none of
        their folders exists, so checkTests exits with 2 and names them."""
        ws = Workspace({"services": {"lending": {"tests": {"folder": "services/lending"}}}})
        self.addCleanup(ws.close)
        run = ws.run("check_tests.py")
        self.assertEqual(run.returncode, 2)
        self.assertIn("lending (services/lending)", run.stderr)

    def test_F_CHECK_23_no_part_with_tests_has_nothing_to_check(self):
        """F-CHECK-23, TST-6: with no tests setting, checkTests passes."""
        ws = Workspace({"clients": {"web": "Web"}})
        self.addCleanup(ws.close)
        run = ws.run("check_tests.py")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("No tests to check", run.stdout)

    def test_F_CHECK_24_listed_standards_are_not_ids(self):
        """F-CHECK-24, KN-1, CFG-9: EN-301549 fails as an ID until EN is listed
        under standards."""
        for standards, status in ((None, 1), (["EN"], 0)):
            with self.subTest(standards=standards):
                ws = Workspace({"standards": standards} if standards else {})
                self.addCleanup(ws.close)
                ws.write("docs/software-knowledges/system/requirements.md",
                         "# Requirements\n\nPages read as EN-301549 asks.\n")
                run = ws.run("check_docs.py")
                self.assertEqual(run.returncode, status, run.stderr)
                if status:
                    self.assertIn("EN-301549 is cited but not defined", run.stderr)

    def test_CFG_9_standards_must_be_a_list(self):
        """CFG-9, CFG-7: standards that is not a list of prefixes stops the
        check with status 2."""
        ws = Workspace({"standards": "EN"})
        self.addCleanup(ws.close)
        run = ws.run("check_docs.py")
        self.assertEqual(run.returncode, 2)
        self.assertIn("standards must be a list", run.stderr)


if __name__ == "__main__":
    unittest.main()
