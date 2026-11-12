"""Flow-rule trace and coverage contracts."""
import unittest
from tests.scripts.workspace import Workspace
from tests.scripts.test_flow_rules import K, HEADER, fixture


class FlowImpact(unittest.TestCase):
    def setUp(self):
        self.ws = Workspace()
        self.addCleanup(self.ws.close)
        fixture(self.ws)

    def run_impact(self, *args):
        run = self.ws.run('impact.py', *args)
        self.assertEqual(run.returncode, 0, run.stderr)
        return run.stdout

    def test_F_TRACE_12_up_down_counts_and_design_boundary(self):
        """F-TRACE-12, KN-17, KN-15, KN-13: rule kinds and dependency edges."""
        self.ws.write('apps/client/design.md', '# Design\n')
        path = self.ws.root / (K + 'flows/run.md')
        path.write_text(path.read_text() + '\n[Design](../../../apps/client/design.md)\n[Artifact](../artifacts/book/specification.md)\n')
        down = self.run_impact('--down', 'G-RUN-1')
        self.assertIn('Flow rules: FR-RUN-1, FR-SHARED-1', down)
        self.assertIn('Artifact rules: BK-1', down)
        self.assertNotIn('design.md', down)
        up = self.run_impact('FR-SHARED-1')
        self.assertIn('Goal criteria: G-RUN-1', up)
        self.assertIn('Flow scenarios: F-RUN-1', up)
        stats = self.run_impact('--stats', 'G-RUN-1')
        self.assertIn('scenarios 1  rules 3  operations 1  artifacts 1', stats)

    def test_F_TRACE_12_legacy_rules_and_absent_group(self):
        """F-TRACE-12, SYS-5: legacy artifact IDs remain artifact rules."""
        self.ws.write(K + 'artifacts/legacy/specification.md', HEADER + '| FR-1 | Legacy. | None |\n| FR-RETRY-1 | Legacy. | None |\n')
        for name in ['FR-1', 'FR-RETRY-1']:
            out = self.run_impact('--down', name)
            self.assertIn('Artifact rules: ' + name, out)
            self.assertNotIn('Flow rules:', out)

    def test_KN_7_links_and_shared_rule_deduplication(self):
        """KN-17, KN-15, KN-13: ordinary downward links and shared dedup remain."""
        self.ws.write(K + 'flows/other.md', '| F-OTHER-1 | `run` | FR-SHARED-1 |\n')
        self.ws.write(K + 'goals/run.md', '| G-RUN-1 | F-RUN-1, F-OTHER-1 |\n'
                      + '[Other](../flows/other.md)\n')
        out = self.run_impact('--stats', 'G-RUN-1')
        self.assertIn('flows 2  scenarios 2  rules 3', out)
        # A page link adds the destination page without inventing unit edges.
        self.ws.write(K + 'artifacts/empty/specification.md', '# Empty\n')
        path = self.ws.root / (K + 'flows/run.md')
        path.write_text(path.read_text() + '[Empty](../artifacts/empty/specification.md)\n')
        self.assertIn('artifacts/empty/specification.md', self.run_impact('--down', 'G-RUN-1'))

    def test_F_COVER_12_rules_aggregate(self):
        """F-COVER-12, TST-4: one tested Flow rule is 20%, not a scenario."""
        self.ws.write('checks/rule_test.py', '# FR-RUN-1\n')
        out = self.run_impact('--coverage', 'checks')
        self.assertIn('20%  criteria 0/1  scenarios 0/1  rules 1/3', out)
        self.assertIn('all          criteria 0/1  scenarios 0/1  rules 1/3', out)
        self.assertNotIn('FR-OLD-1', out)
        self.assertIn('FR-RUN-1', self.run_impact('--fragile', 'checks'))
        self.assertIn('FR-SHARED-1', self.run_impact('--stats'))

    def test_KN_3_stale_rows_block_impact_and_coverage(self):
        """KN-3, TST-4: stale rows fail rather than silently reducing counts."""
        self.ws.write(K + 'flows/old.md', HEADER + '| FR-OLD-1 | Withdrawn. | None |\n')
        self.ws.write('checks/rule_test.py', '# FR-RUN-1\n')
        for args in [('FR-RUN-1',), ('--coverage', 'checks'), ('--stats',), ('--fragile', 'checks')]:
            with self.subTest(args=args):
                run = self.ws.run('impact.py', *args)
                self.assertEqual(run.returncode, 1)
                self.assertIn('FR-OLD-1 is withdrawn', run.stderr)
                self.assertEqual(run.stdout, '')
