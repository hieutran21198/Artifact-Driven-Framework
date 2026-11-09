"""Read explicitly authored Flow rules without reclassifying legacy IDs (KN-13)."""

import re

from project import ID

FLOW_ID = re.compile(r"FR-([A-Z]{1,8})-\d+")



def table_cells(line):
    """Read pipe-delimited Markdown cells, retaining escaped pipes as content."""
    cells = re.split(r'(?<!\\)\|', line.strip())
    if cells and not cells[0]:
        cells.pop(0)
    if cells and not cells[-1]:
        cells.pop()
    return [cell.strip() for cell in cells] or ['']


def read_flow_rules(path, text):
    """Return ID metadata and definition problems for a knowledge-relative path.

    Only the exact Coordination rules section in an approved Markdown home
    opts in. Other definitions retain the existing text-based interpretation.
    Recognizable declarations remain classified even when invalid; callers
    must use the returned problems to validate them before adoption.
    """
    parts = path.parts
    home = (len(parts) == 2 and parts[0] == 'flows' or
            len(parts) == 3 and parts[:2] == ('flows', 'contracts'))
    if not home or path.suffix != '.md':
        return {}, []
    rules, problems = {}, []
    active, columns = False, None
    for number, line in enumerate(text.splitlines(), 1):
        if re.match(r'^#{1,2} ', line):
            active = line == '## Coordination rules'
            columns = None
            continue
        if not active or not line.startswith('|'):
            if line.strip():
                columns = None
            continue
        cells = table_cells(line)
        if all(re.fullmatch(r':?-+:?', cell) for cell in cells):
            continue
        if cells[0] == 'ID':
            columns = cells
            if not all(column in cells for column in ('ID', 'Rule', 'Dependencies')):
                problems.append(f'{path}:{number}: Flow rule table needs ID, Rule and Dependencies columns')
            continue
        where = f'{path}:{number}: {cells[0] or "Flow rule"}'
        match = FLOW_ID.fullmatch(cells[0])
        if not match:
            problems.append(f'{where}: invalid Flow-rule ID (expected FR-<SCOPE>-<n>)')
        if columns is None or not all(column in columns for column in ('ID', 'Rule', 'Dependencies')):
            problems.append(f'{where}: Flow rule needs ID, Rule and Dependencies columns')
            continue
        row = dict(zip(columns, cells))
        statement, dependencies = row.get('Rule', ''), row.get('Dependencies', '')
        if not statement or not dependencies:
            problems.append(f'{where}: Flow rule needs a nonempty Rule and Dependencies')
        names = ID.findall(dependencies)
        remainder = ID.sub('', dependencies)
        if dependencies != 'None' and (not names or remainder.strip(' ,')):
            problems.append(f'{where}: Dependencies must contain IDs or None')
        if not re.match(r'Withdrawn\b', statement):
            missing = set(ID.findall(line)) - {cells[0]} - set(names)
            if missing:
                problems.append(f'{where}: row citations missing from Dependencies: {", ".join(sorted(missing))}')
        if match:
            rules[cells[0]] = {'scope': match.group(1), 'owner': path.as_posix(),
                              'rule': statement, 'dependencies': names}
    return rules, problems
