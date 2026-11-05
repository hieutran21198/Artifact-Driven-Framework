"""Show what in the software knowledge depends on an ID, an operation or a field.

Usage:
    python3 scripts/impact.py <ID | operationId | field>          # what is affected
    python3 scripts/impact.py --down <ID | operationId | page>    # what it relies on
    python3 scripts/impact.py --stats [goal | ID | operationId]   # size and blast radius
    python3 scripts/impact.py --fragile [tests folder]            # the 20 most fragile nodes
    python3 scripts/impact.py --coverage [tests folder]           # IDs each goal relies on that tests name
    python3 scripts/impact.py --questions                         # open questions that hold each goal
"""

from collections import defaultdict
import re
import sys

from project import CLIENTS, KNOWLEDGE, ROOT, TESTS

ID = re.compile(r"\b[A-Z]{1,6}(?:-[A-Z]{1,8})?-\d+\b")
ID_ROW = re.compile(r"^\| (" + ID.pattern + r") \|")
TICKED = re.compile(r"`([A-Za-z_][A-Za-z0-9_]*)`")
LINK = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)\s]*)?\)")
REF = re.compile(r"\$ref: '([^'#]*)#/components/([A-Za-z]+)/([A-Za-z0-9_]+)'")
OPERATION_ID = re.compile(r"^\s+operationId: (\w+)")
LAYER = {"goals": 1, "flows": 2, "artifacts": 3}
CLIENT_PAGES = tuple(f"/{name}.md" for name in CLIENTS)


class Graph:
    def __init__(self):
        self.text = defaultdict(list)    # unit -> lines
        self.file = {}                   # unit -> file
        self.fields = defaultdict(set)   # unit -> schema property names
        self.links = defaultdict(set)    # file -> files it links downward
        self.edges = defaultdict(set)    # unit -> units it cites

    def add(self, unit, path, line):
        self.file.setdefault(unit, path)
        self.text[unit].append(line)


def rel(path):
    return path.relative_to(KNOWLEDGE).as_posix()


def layer(path):
    return LAYER.get(rel(path).split("/")[0], 0)


def read_markdown(graph, path):
    page = rel(path)
    section = page
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = re.match(r"^### `?([\w-]+)`?$", line)
        if line.startswith("#"):
            section = f"{page}#{heading.group(1)}" if heading else page
        row = ID_ROW.match(line)
        graph.add(row.group(1) if row else section, page, line)
        for target in LINK.findall(line):
            linked = (path.parent / target).resolve()
            if KNOWLEDGE in linked.parents and 0 < layer(path) < layer(linked):
                graph.links[page].add(rel(linked))


def read_contract(graph, path):
    page = rel(path)
    unit, kind = page, None
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"^  /", line):
            unit = page
        if line.startswith("components:"):
            unit, kind = page, None
        if re.match(r"^\S", line):
            unit, kind = page, None
        if line.startswith("paths:"):
            kind = "paths"
        if line.startswith("x-triggers:"):
            kind = "x-triggers"
        component = re.match(r"^  (\w+):$", line)
        if component and kind == "x-triggers":
            unit = component.group(1)
        elif component and kind != "paths":
            kind = component.group(1)
        named = re.match(r"^    ([A-Za-z0-9_]+):$", line)
        if named and kind not in (None, "paths", "x-triggers"):
            unit = f"{page}#{kind}/{named.group(1)}"
        operation = OPERATION_ID.match(line)
        if operation:
            unit = operation.group(1)
        prop = re.match(r"^\s{8,}([a-z][a-z0-9_]*):", line)
        if prop and kind == "schemas":
            graph.fields[unit].add(prop.group(1))
        graph.add(unit, page, line)


def build():
    graph = Graph()
    for path in sorted(KNOWLEDGE.rglob("*")):
        if path.suffix == ".md":
            read_markdown(graph, path)
        elif path.suffix == ".yaml":
            read_contract(graph, path)
    operations = {u for u in graph.file if "#" not in u and "/" not in u and not ID.fullmatch(u)}
    schemas = {u.rsplit("/", 1)[1]: u for u in graph.file if "#schemas/" in u}
    for unit, lines in graph.text.items():
        body = "\n".join(lines)
        cited = set(ID.findall(body))
        if graph.file[unit].endswith(".md"):
            cited |= set(TICKED.findall(body)) & operations
        if unit.endswith(tuple(f"#{op}" for op in operations)):
            cited.add(unit.rsplit("#", 1)[1])
        heading = unit.rsplit("#", 1)[1] if "#" in unit and graph.file[unit].endswith(".md") else None
        if heading in schemas:
            cited.add(schemas[heading])
        if heading and ID.fullmatch(heading):
            cited.add(heading)
        for target, kind, name in REF.findall(body):
            base = graph.file[unit] if not target else rel((KNOWLEDGE / graph.file[unit]).parent.joinpath(target).resolve())
            cited.add(f"{base}#{kind}/{name}")
        graph.edges[unit] = {c for c in cited if c != unit and c in graph.file}
    return graph


def walk(edges, start):
    seen, todo = set(start), list(start)
    while todo:
        for nxt in edges.get(todo.pop(), ()):
            if nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    return seen


def starts(graph, term):
    if term in graph.file:
        return {term}
    prefixed = {u for u in graph.file if u.startswith(term + "-") and ID.fullmatch(u)}
    if prefixed:
        return prefixed
    by_page = {u for u, f in graph.file.items() if f == term}
    if by_page:
        return by_page
    tick = f"`{term}`"
    return {u for u, lines in graph.text.items() if term in graph.fields[u] or any(tick in l for l in lines)}


def kind(unit):
    if unit.startswith("SYS-"):
        return "Requirements"
    if unit.startswith("G-"):
        return "Goal criteria"
    if unit.startswith("F-"):
        return "Flow scenarios"
    if ID.fullmatch(unit):
        return "Artifact rules"
    if "#schemas/" in unit or "#responses/" in unit:
        return "Contract schemas"
    if "#" not in unit and not unit.endswith((".md", ".yaml")):
        return "Operations"
    if "#" in unit and unit.split("#")[0].endswith(CLIENT_PAGES):
        return "Client needs"
    return None


def report(graph, units, pages):
    groups = defaultdict(set)
    for unit in units:
        if kind(unit):
            groups[kind(unit)].add(unit.split("#")[0] + "#" + unit.split("#")[1].split("/")[-1] if "#" in unit else unit)
    order = ["Requirements", "Goal criteria", "Flow scenarios", "Artifact rules", "Operations", "Contract schemas", "Client needs"]
    for name in order:
        if groups[name]:
            print(f"{name}: {', '.join(sorted(groups[name]))}")
    print(f"Pages: {', '.join(sorted(pages))}")


def relies_on(graph, start):
    start = start | {u for u, cited in graph.edges.items() if u.startswith("F-") and cited & start}
    units = walk(graph.edges, start)
    return units, walk(graph.links, {graph.file[u] for u in units})


def affected(graph, start):
    reverse = defaultdict(set)
    for unit, cited in graph.edges.items():
        for c in cited:
            reverse[c].add(unit)
    units = walk(reverse, start)
    units |= {g for u in units if u.startswith("F-") for g in graph.edges[u] if g.startswith("G-")}
    back = defaultdict(set)
    for page, linked in graph.links.items():
        for l in linked:
            back[l].add(page)
    return units, walk(back, {graph.file[u] for u in units})


def with_client_needs(graph, units):
    """Add the client needs on any operation the units reach."""
    return units | {u for u in graph.file if kind(u) == "Client needs" and graph.edges[u] & units}


def counts(graph, units, pages):
    flows = {graph.file[u] for u in units if u.startswith("F-")}
    artifacts = {p.split("/")[1] for p in pages if p.startswith("artifacts/")}
    clients = {u.split("#")[0] for u in units if kind(u) == "Client needs"}
    by_kind = defaultdict(int)
    for u in units:
        by_kind[kind(u)] += 1
    return {
        "criteria": by_kind["Goal criteria"], "flows": len(flows),
        "scenarios": by_kind["Flow scenarios"], "rules": by_kind["Artifact rules"],
        "operations": by_kind["Operations"], "artifacts": len(artifacts),
        "client pages": len(clients),
    }


def line(name, numbers):
    return f"{name:28} " + "  ".join(f"{k} {v}" for k, v in numbers.items())


def stats(graph, term):
    if term:
        start = starts(graph, term)
        if not start:
            print(f"Nothing in the knowledge cites {term}.", file=sys.stderr)
            return 1
        units, pages = relies_on(graph, start)
        print(line("relies on", counts(graph, with_client_needs(graph, units), pages)))
        units, pages = affected(graph, start)
        print(line("affected by a change", counts(graph, with_client_needs(graph, units), pages)))
        return 0
    goals = sorted({u.rsplit("-", 1)[0] for u in graph.file if u.startswith("G-") and ID.fullmatch(u)})
    print("Size of each goal (what it relies on):")
    for goal in goals:
        start = {u for u in graph.file if u.startswith(goal + "-") and ID.fullmatch(u)}
        units, pages = relies_on(graph, start)
        print("  " + line(goal, counts(graph, with_client_needs(graph, units), pages)))
    print("Blast radius of each rule and operation (what a change affects):")
    nodes = [u for u in graph.file if kind(u) in ("Requirements", "Artifact rules", "Operations")]
    rows = []
    for node in nodes:
        units, pages = affected(graph, {node})
        units = with_client_needs(graph, units)
        rows.append((node, counts(graph, units, pages)))
    rows.sort(key=lambda r: (-r[1]["scenarios"], -r[1]["operations"], r[0]))
    for node, numbers in rows:
        numbers.pop("criteria"), numbers.pop("rules")
        print("  " + line(node, numbers))
    return 0


def test_files(folder):
    """The test files under a folder, as the tests setting names them."""
    return sorted(p for p in folder.glob(TESTS["glob"]) if p.is_file())


def tested_ids(folder):
    """How many test files name each knowledge ID."""
    found = defaultdict(int)
    for path in test_files(folder):
        for name in set(ID.findall(path.read_text(encoding="utf-8", errors="ignore"))):
            found[name] += 1
    return found


def fragile(graph, folder, limit=20):
    """Rank requirements, rules, operations and schemas by how much a change
    would break and how weakly it is proved."""
    tests = tested_ids(folder) if folder else {}
    if folder and not folder.is_dir():
        print(f"Not a folder: {folder}", file=sys.stderr)
        return 1
    open_questions = set()
    for path in KNOWLEDGE.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        if "## Open questions" in text:
            section = text.split("## Open questions", 1)[1]
            open_questions |= set(ID.findall(section)) | set(TICKED.findall(section))
    rows = []
    for node in graph.file:
        if kind(node) not in ("Requirements", "Artifact rules", "Operations", "Contract schemas"):
            continue
        units, pages = affected(graph, {node})
        numbers = counts(graph, with_client_needs(graph, units), pages)
        reach = numbers["scenarios"] + numbers["criteria"] + 2 * numbers["operations"] + 3 * numbers["client pages"]
        is_id = bool(ID.fullmatch(node))
        direct = sum(1 for unit, cited in graph.edges.items() if unit.startswith("F-") and node in cited)
        weak = (is_id and direct == 0) + (is_id and bool(folder) and tests.get(node, 0) == 0)
        score = reach * (1 + weak) + (8 if node in open_questions else 0)
        rows.append((score, node, numbers, direct, tests.get(node, 0) if is_id and folder else "-", node in open_questions))
    rows.sort(key=lambda r: (-r[0], r[1]))
    print("The most fragile nodes: reach times weakness. Reach counts scenarios and criteria,")
    print("operations twice and client pages three times; weakness adds 1 for a rule with no")
    print("scenario citing it and 1 for a rule no test names.")
    for i, (score, node, numbers, direct, named, question) in enumerate(rows[:limit], 1):
        print(f"{i:3}  {score:4}  {node.split('#')[-1]:28} scenarios {numbers['scenarios']}  operations {numbers['operations']}"
              f"  client pages {numbers['client pages']}  cited by {direct}  tests {named}" + ("  open question" if question else ""))
    return 0


def goal_keys(graph):
    return sorted({u.rsplit("-", 1)[0] for u in graph.file if u.startswith("G-") and ID.fullmatch(u)})


def goal_units(graph, goal):
    start = {u for u in graph.file if u.startswith(goal + "-") and ID.fullmatch(u)}
    units, _ = relies_on(graph, start)
    return start | units


def withdrawn(graph, unit):
    return any(re.match(r"^\| \S+ \| *Withdrawn\b", line) for line in graph.text.get(unit, ()))


def natural(unit):
    return [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", unit)]


def coverage(graph, folder):
    """For each goal, the scenarios and rules it relies on that a test names."""
    if not folder or not folder.is_dir():
        print(f"Not a folder: {folder}", file=sys.stderr)
        return 1
    tests = tested_ids(folder)
    kinds = ("Flow scenarios", "Artifact rules")
    print("Test coverage by ID: the scenarios and rules each goal relies on that a test names.")
    total = defaultdict(lambda: [0, 0])
    for goal in goal_keys(graph):
        ids = {u for u in goal_units(graph, goal) if kind(u) in kinds and not withdrawn(graph, u)}
        parts, missing = [], []
        for k in kinds:
            mine = sorted((u for u in ids if kind(u) == k), key=natural)
            done = [u for u in mine if tests.get(u)]
            parts.append(f"{k.split()[1]} {len(done)}/{len(mine)}")
            missing += [u for u in mine if not tests.get(u)]
        tested = sum(1 for u in ids if tests.get(u))
        percent = round(100 * tested / len(ids)) if ids else 0
        print(f"  {goal:12} {percent:3}%  " + "  ".join(parts))
        if missing:
            print(f"               untested: {', '.join(missing)}")
    every = {u for u in graph.file if kind(u) in kinds and not withdrawn(graph, u)}
    for u in every:
        total[kind(u)][0] += 1 if tests.get(u) else 0
        total[kind(u)][1] += 1
    print("  all          " + "  ".join(f"{k.split()[1]} {total[k][0]}/{total[k][1]}" for k in kinds))
    return 0


def open_questions():
    """Each open question: the page it is on, its text and the IDs and names it cites."""
    found = []
    for path in sorted(KNOWLEDGE.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if "## Open questions" not in text:
            continue
        section = text.split("## Open questions", 1)[1].split("\n## ", 1)[0].split("\nReturn to ", 1)[0]
        for item in re.split(r"\n(?=- )", section.strip()):
            if item.startswith("- "):
                body = " ".join(item[2:].split())
                found.append((rel(path), body, set(ID.findall(body)) | set(TICKED.findall(body))))
    return found


def questions(graph):
    """For each goal, the open questions that touch what it relies on."""
    found = open_questions()
    print("Open questions that hold each goal: a question counts when it cites an ID or")
    print("operation the goal relies on.")
    for goal in goal_keys(graph):
        units = goal_units(graph, goal)
        mine = [(page, body) for page, body, cites in found if cites & units]
        print(f"  {goal:12} {len(mine)}")
        for page, body in mine:
            print(f"               {page}: {body[:90]}{'…' if len(body) > 90 else ''}")
    loose = [(page, body) for page, body, cites in found if not cites & set(graph.file)]
    if loose:
        print("  Questions that cite nothing in the knowledge:")
        for page, body in loose:
            print(f"               {page}: {body[:90]}")
    return 0


def main(argv):
    folder = (argv[1] if len(argv) > 1 else None) or TESTS["folder"]
    if argv[:1] == ["--coverage"]:
        return coverage(build(), (ROOT / folder) if folder else None)
    if argv[:1] == ["--questions"]:
        return questions(build())
    if argv[:1] == ["--fragile"]:
        return fragile(build(), (ROOT / folder) if folder else None)
    if argv[:1] == ["--stats"]:
        return stats(build(), argv[1] if len(argv) > 1 else None)
    down = "--down" in argv
    terms = [a for a in argv if a != "--down"]
    if len(terms) != 1:
        print(__doc__, file=sys.stderr)
        return 2
    graph = build()
    start = starts(graph, terms[0])
    if not start:
        print(f"Nothing in the knowledge cites {terms[0]}.", file=sys.stderr)
        return 1
    units, pages = (relies_on if down else affected)(graph, start)
    report(graph, units, pages)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
