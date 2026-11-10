"""How impact finds the operations of a rule: through the scenarios that cover it."""
import unittest
from tests.scripts.workspace import Workspace

K = 'docs/software-knowledges/'


class ImpactViaScenarios(unittest.TestCase):
    def setUp(self):
        self.ws = Workspace()
        self.addCleanup(self.ws.close)
        self.ws.write(K + 'goals/lend.md', '# Goal: Lend\n\n| ID | Criterion | Proven by |\n| --- | --- | --- |\n'
                      '| G-LEND-1 | A book is lent. | F-LEND-1 |\n\n[Lend](../flows/lend.md)\n')
        self.ws.write(K + 'flows/lend.md', '# Flow: Lend\n\n| ID | Given | When | Then | Covers |\n| --- | --- | --- | --- | --- |\n'
                      '| F-LEND-1 | A book | The member calls `lendBook` | It is lent | BK-1 |\n'
                      '| F-LEND-2 | A book | The member calls `readBook` | It is shown | BK-2 |\n\n'
                      '[Book](../artifacts/book/specification.md)\n')
        self.ws.write(K + 'artifacts/book/specification.md', '# Book\n\n| ID | Rule | Error |\n| --- | --- | --- |\n'
                      '| BK-1 | A book on the shelf can be lent. | — |\n| BK-2 | A book can be read. | — |\n')
        # The contract cites no knowledge ID.
        self.ws.write(K + 'artifacts/book/openapi.yaml', '\n'.join([
            'openapi: 3.0.3', 'info:', '  title: Book', '  version: 1.0.0', 'paths:',
            '  /books/{id}/lend:', '    post:', '      operationId: lendBook', '      summary: Lend a book.',
            '      responses:', "        '200':", '          description: The book.', '          content:',
            '            application/json:', '              schema:', "                $ref: '#/components/schemas/Book'",
            '  /books/{id}:', '    get:', '      operationId: readBook', '      summary: Read a book.',
            '      responses:', "        '200':", '          description: The book.',
            'components:', '  schemas:', '    Book:', '      type: object', '      properties:',
            '        title:', '          type: string', '']))

    def run_impact(self, *args):
        run = self.ws.run('impact.py', *args)
        self.assertEqual(run.returncode, 0, run.stderr)
        return run.stdout

    def test_F_TRACE_13_rule_reaches_operation_through_scenario(self):
        """F-TRACE-13, KN-17, KN-8: no contract cites the rule, yet its operation is found."""
        out = self.run_impact('BK-1')
        self.assertIn('Flow scenarios: F-LEND-1\n', out)
        self.assertIn('Operations: lendBook\n', out)
        self.assertIn('Contract schemas: artifacts/book/openapi.yaml#Book\n', out)
        self.assertIn('Goal criteria: G-LEND-1', out)
        self.assertNotIn('readBook', out)
        op = self.run_impact('lendBook')
        self.assertIn('Flow scenarios: F-LEND-1', op)
        self.assertNotIn('Artifact rules', op)
        down = self.run_impact('--down', 'G-LEND-1')
        self.assertIn('Artifact rules: BK-1\n', down)
        self.assertIn('Operations: lendBook\n', down)

    def test_KN_17_ids_in_a_contract_add_no_edge(self):
        """KN-17: a rule ID in a contract summary does not tie the operation to it."""
        path = self.ws.root / (K + 'artifacts/book/openapi.yaml')
        path.write_text(path.read_text().replace('Read a book.', 'Read a book (BK-1).'))
        self.assertNotIn('readBook', self.run_impact('BK-1'))


if __name__ == '__main__':
    unittest.main()
