"""Flow-rule adoption checks, including legacy ID compatibility."""
import json
import subprocess
import sys
import unittest
from tests.scripts.workspace import SCRIPTS, Workspace

K = 'docs/software-knowledges/'
HEADER = '## Coordination rules\n\n| ID | Rule | Dependencies |\n| --- | --- | --- |\n'


def fixture(ws):
    ws.write(K + 'system/requirements.md', '| SYS-1 | Safe. |\n')
    ws.write(K + 'artifacts/book/specification.md', '| BK-1 | Valid. |\n')
    ws.write(K + 'flows/run.yaml', 'x-commands:\n  run:\n    description: Run\n')
    ws.write(K + 'flows/run.md', HEADER + '| FR-RUN-1 | Coordinate. | BK-1, SYS-1 |\n'
             + '\n## Scenarios\n| F-RUN-1 | `run` | FR-RUN-1, FR-SHARED-1 |\n')
    ws.write(K + 'flows/contracts/shared.md', HEADER + '| FR-SHARED-1 | Retry. | None |\n')
    ws.write(K + 'goals/run.md', '| ID | Criterion | Proven by |\n| --- | --- | --- |\n| G-RUN-1 | Works. | F-RUN-1 |\n')


class FlowRules(unittest.TestCase):
    def setUp(self):
        self.ws = Workspace()
        self.addCleanup(self.ws.close)
        fixture(self.ws)

    def check(self, status=0):
        run = self.ws.run('check_docs.py')
        self.assertEqual(run.returncode, status, run.stderr)
        return run.stderr

    def test_F_CHECK_25_local_shared_rules_and_reuse(self):
        """F-CHECK-25, KN-13: definitions need no operation, reuse keeps home."""
        self.ws.write(K + 'flows/other.md', 'Uses FR-RUN-1 and FR-SHARED-1.\n')
        self.check()
        self.ws.write('checks/rule_test.py', '# FR-RUN-1 FR-SHARED-1\n')
        self.assertEqual(self.ws.run('check_tests.py', 'checks').returncode, 0)

    def test_F_CHECK_26_invalid_fields_and_scope_homes(self):
        """F-CHECK-26, KN-13: required fields and scopes are checked."""
        for content in [
            '## Coordination rules\n| ID | Rule |\n| --- | --- |\n| FR-BAD-1 | Bad. |\n',
            HEADER + '| FR-BAD-1 | | None |\n', HEADER + '| FR-BAD-1 | Bad. | |\n',
            HEADER + '| BAD-1 | Bad. | None |\n', HEADER + '| FR-TOOLONGER-1 | Bad. | None |\n',
            HEADER + '| FR-BAD-1 | Bad. | prose |\n', HEADER + '| FR-RUN-2 | Bad. | None |\n',
        ]:
            with self.subTest(content=content):
                self.ws.write(K + 'flows/bad.md', content)
                self.assertIn('flows/bad.md', self.check(1))

    def test_F_CHECK_27_dependencies_are_lower_actual_definitions(self):
        """F-CHECK-27, KN-5: no chains, scenarios, goals or pseudo-artifacts."""
        for dependency in ['FR-SHARED-1', 'F-RUN-1', 'G-RUN-1', 'MISC-1']:
            with self.subTest(dependency=dependency):
                self.ws.write(K + 'flows/other.md', '| MISC-1 | Legacy flow row. |\n')
                self.ws.write(K + 'flows/bad.md', HEADER + f'| FR-BAD-1 | Bad. | {dependency} |\n')
                self.assertIn(dependency, self.check(1))

    def test_F_CHECK_27_artifact_and_goal_cannot_use_rule_as_proof(self):
        """F-CHECK-27, KN-5, KN-6: actual Flow rules are not proof."""
        self.ws.write(K + 'artifacts/book/specification.md', '| BK-1 | FR-RUN-1 |\n')
        self.ws.write(K + 'goals/run.md', '| ID | Criterion | Proven by |\n| --- | --- | --- |\n| G-RUN-1 | Works. | FR-SHARED-1 |\n')
        errors = self.check(1)
        self.assertIn('artifacts/book/specification.md', errors)
        self.assertIn('goals/run.md', errors)

    def test_F_CHECK_27_only_scenarios_prove_operations(self):
        """F-CHECK-27, KN-6: an operation named by a rule is unproved."""
        self.ws.write(K + 'flows/run.md', HEADER + '| FR-RUN-1 | Calls `run`. | BK-1 |\n')
        self.assertIn('run is named by no scenario', self.check(1))

    def test_F_CHECK_28_legacy_forms_keep_classification(self):
        """F-CHECK-28, SYS-5, KN-13: FR spelling alone adopts nothing."""
        self.ws.write(K + 'artifacts/legacy/specification.md', HEADER + '| FR-1 | Legacy. | None |\n| FR-RETRY-1 | Legacy. | None |\n')
        self.ws.write(K + 'flows/legacy.md', '| FR-OLD-1 | Legacy. |\n')
        self.check()
        self.ws.write('checks/legacy_test.py', '# FR-1 FR-RETRY-1 FR-OLD-1\n')
        self.assertEqual(self.ws.run('check_tests.py', 'checks').returncode, 0)

    def test_F_CHECK_7_8_9_unknown_duplicate_withdrawn(self):
        """F-CHECK-7, F-CHECK-8, F-CHECK-9, KN-3: generic checks apply."""
        for content, message in [
            ('Uses FR-UNKNOWN-1.', 'not defined'),
            (HEADER + '| FR-RUN-1 | Again. | None |', 'defined twice'),
            (HEADER + '| FR-OLD-1 | Withdrawn: moved to FR-RUN-1. | None |\nUses FR-OLD-1.', 'withdrawn'),
        ]:
            self.ws.write(K + 'flows/extra.md', content)
            self.assertIn(message, self.check(1))

    def test_KN_13_exact_section_and_home_boundaries(self):
        """KN-13, SYS-5: only explicit sections in the two homes adopt rules."""
        for page, heading in [
            ('flows/nested/legacy.md', '## Coordination rules'),
            ('flows/contracts/nested/legacy.md', '## Coordination rules'),
            ('flows/legacy.md', '### Coordination rules'),
            ('flows/legacy.md', '## Coordination rules extra'),
            ('system/legacy.md', '## Coordination rules'),
        ]:
            with self.subTest(page=page, heading=heading):
                path = self.ws.write(K + page, heading + '\n| FR-LEGACY-1 | Old row. |\n')
                self.check()
                path.unlink()
        self.ws.write(K + 'flows/legacy.md', HEADER + '| FR-LOCAL-1 | New. | None |\n'
                      + '## Other\n| FR-LEGACY-1 | Old row. |\n')
        self.check()

    def test_KN_5_legacy_artifact_id_is_valid_dependency(self):
        """KN-5, KN-13: dependencies use actual homes, not an FR prefix ban."""
        self.ws.write(K + 'artifacts/legacy/specification.md', HEADER + '| FR-RETRY-1 | Legacy. | None |\n')
        self.ws.write(K + 'flows/more.md', HEADER + '| FR-MORE-1 | Coordinate. | FR-RETRY-1 |\n')
        self.check()

    def test_KN_13_statement_citations_are_explicit_dependencies(self):
        """KN-13, KN-14: graph citations must not disappear from dependency metadata."""
        self.ws.write(K + 'flows/more.md', HEADER + '| FR-MORE-1 | Applies BK-1. | None |\n')
        self.assertIn('BK-1', self.check(1))
        self.ws.write(K + 'flows/more.md', HEADER + '| FR-MORE-1 | Applies BK-1. | BK-1 |\n')
        self.check()
        self.ws.write(K + 'flows/more.md', HEADER + '| FR-MORE-1 | Withdrawn: moved to FR-RUN-1. | None |\n')
        self.check()

    def test_KN_13_extra_cells_cannot_hide_dependencies(self):
        """KN-13, KN-5, KN-14: all row citations must be explicit and permitted."""
        header = '## Coordination rules\n| ID | Rule | Dependencies | Notes |\n| --- | --- | --- | --- |\n'
        for reference in ['FR-SHARED-1', 'F-RUN-1', 'BK-1']:
            with self.subTest(reference=reference):
                self.ws.write(K + 'flows/extra.md', header + f'| FR-EXTRA-1 | Coordinate. | None | {reference} |\n')
                self.assertIn(reference, self.check(1))
        for reference in ['FR-SHARED-1', 'F-RUN-1']:
            with self.subTest(explicit=reference):
                self.ws.write(K + 'flows/extra.md', header + f'| FR-EXTRA-1 | Coordinate. | {reference} | {reference} |\n')
                self.assertIn('not an artifact rule or system requirement', self.check(1))
        self.ws.write(K + 'flows/extra.md', header + '| FR-EXTRA-1 | Coordinate. | BK-1 | BK-1 |\n')
        self.check()
        out = self.ws.run('impact.py', '--down', 'FR-EXTRA-1')
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn('Artifact rules: BK-1', out.stdout)
        code = (f"import sys; sys.path.insert(0, {str(SCRIPTS)!r}); "
                "import impact, json; g = impact.build(); "
                "print(json.dumps([g.flow_rules['FR-EXTRA-1']['dependencies'], "
                "sorted(g.edges['FR-EXTRA-1'])]))")
        metadata = subprocess.run([sys.executable, '-c', code], cwd=self.ws.root,
                                  capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(metadata.stdout), [['BK-1'], ['BK-1']])
        self.ws.write(K + 'flows/extra.md', header + '| FR-EXTRA-1 | Withdrawn. | None | Moved to FR-SHARED-1. |\n')
        self.check()

    def test_KN_13_escaped_pipe_keeps_rule_and_dependencies(self):
        """KN-13: Markdown escaped pipes are content, not cell separators."""
        self.ws.write(K + 'flows/more.md', HEADER + '| FR-MORE-1 | Coordinates A \\| B under BK-1. | BK-1 |\n')
        self.check()
        # A pipe in criterion text must not shift Proven by out of validation.
        self.ws.write(K + 'goals/run.md', '| ID | Criterion | Proven by |\n| --- | --- | --- |\n'
                      + '| G-RUN-1 | A \\| B works. | FR-MORE-1 |\n')
        self.assertIn('not scenario proof', self.check(1))

    def test_F_CHECK_13_14_15_complete_prefix_and_withdrawal(self):
        """TST-2, F-CHECK-13, F-CHECK-14, F-CHECK-15: full scope filtering."""
        self.ws.write(K + 'flows/old.md', HEADER + '| FR-OLD-1 | Withdrawn: moved to FR-RUN-1. | None |\n')
        self.check()
        for names, status in [('FR-UNKNOWN-1', 0), ('FR-RUN-99', 1), ('FR-OLD-1', 1)]:
            self.ws.write('checks/rule_test.py', '# ' + names)
            run = self.ws.run('check_tests.py', 'checks')
            self.assertEqual(run.returncode, status, run.stderr)
