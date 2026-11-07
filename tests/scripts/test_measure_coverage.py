"""Scenarios of the flow Measure coverage."""

import unittest

from tests.scripts.workspace import Workspace


class MeasureCoverage(unittest.TestCase):
    def test_F_COVER_10_folder_of_several_parts_keeps_each_glob(self):
        """F-COVER-10, CFG-8, CFG-4: measureCoverage with tests reads tests/a
        and tests/b, each with its part's glob."""
        ws = Workspace({"services": {
            "a": {"tests": {"folder": "tests/a", "glob": "**/check_*.py"}},
            "b": {"tests": {"folder": "tests/b", "glob": "**/*.spec.js"}},
        }})
        self.addCleanup(ws.close)
        ws.write("docs/software-knowledges/artifacts/thing/specification.md",
                 "# Thing\n\n| ID | Rule | Error |\n| --- | --- | --- |\n"
                 "| TH-1 | One. | — |\n| TH-2 | Two. | — |\n")
        # Only the parts' globs match these files; the default **/*_test.* does not.
        ws.write("tests/a/check_one.py", "# TH-1\n")
        ws.write("tests/b/two.spec.js", "// TH-2\n")
        run = ws.run("impact.py", "--coverage", "tests")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("rules 2/2", run.stdout)

    def test_F_COVER_6_folder_of_no_part_takes_the_default_glob(self):
        """F-COVER-6, CFG-8: a folder that holds no part's tests folder is read
        with the default glob."""
        ws = Workspace({})
        self.addCleanup(ws.close)
        ws.write("docs/software-knowledges/artifacts/thing/specification.md",
                 "# Thing\n\n| ID | Rule | Error |\n| --- | --- | --- |\n| TH-1 | One. | — |\n")
        ws.write("other/one_test.py", "# TH-1\n")
        ws.write("other/check_one.py", "# TH-1 is here too, but not in a test file\n")
        run = ws.run("impact.py", "--coverage", "other")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("rules 1/1", run.stdout)

    def test_F_COVER_11_system_requirements_have_a_line_of_their_own(self):
        """F-COVER-11, TST-4: three requirements, one named by a test, give a
        system line of 1/3 with the two others."""
        ws = Workspace({})
        self.addCleanup(ws.close)
        ws.write("docs/software-knowledges/system/requirements.md",
                 "# Requirements\n\n| ID | Requirement |\n| --- | --- |\n"
                 "| SYS-1 | One. |\n| SYS-2 | Two. |\n| SYS-3 | Three. |\n")
        ws.write("checks/one_test.py", "# SYS-2\n")
        run = ws.run("impact.py", "--coverage", "checks")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("system       requirements 1/3", run.stdout)
        self.assertIn("untested: SYS-1, SYS-3", run.stdout)


if __name__ == "__main__":
    unittest.main()
