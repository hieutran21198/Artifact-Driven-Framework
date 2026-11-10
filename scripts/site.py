"""Build a one-file HTML view of the software knowledge, with its metrics.

Usage:
    python3 scripts/site.py [output] [--routes DIR]...

output defaults to site.output in artifact-driven.json. The API coverage reads
the routes of each service from its code, as the service's routes setting
says. Each --routes DIR, relative to the repository root, replaces every
service's folders with one set read by the first service's pattern. With no
routes setting, the page leaves API coverage out.
"""

from datetime import datetime, timezone
from pathlib import Path
import argparse
import os
import base64
import hashlib
import json
import re
import subprocess
import sys

import impact
from project import KNOWLEDGE, ROOT, SERVICES, SITE, contracts

TEMPLATE = Path(__file__).with_name("site.html")
ROW = re.compile(r"^\| (" + impact.ID.pattern + r") \|(.*)\|\s*$")
TITLE = re.compile(r"^# (?:Goal|Flow): (.+)$", re.MULTILINE)
MERMAID = re.compile(r"^```mermaid\n(.*?)^```", re.MULTILINE | re.DOTALL)
COLUMN = {"Requirements": 0, "Goal criteria": 0, "Flow scenarios": 1, "Flow rules": 5, "Artifact rules": 2, "Operations": 3}


def html_data(data):
    """Keep JSON inside its script element, including HTML parser sentinels."""
    text = json.dumps(data, ensure_ascii=False)
    for char in "<>&\u2028\u2029":
        text = text.replace(char, f"\\u{ord(char):04x}")
    return text


def site_html(data):
    """Authorize only the template scripts and its fixed diagram/font sources."""
    html = TEMPLATE.read_text(encoding="utf-8").replace("/*DATA*/null", html_data(data))
    hashes = ["'sha256-" + base64.b64encode(hashlib.sha256(script.encode("utf-8")).digest()).decode("ascii") + "'"
              for script in re.findall(r"<script(?:\s[^>]*)?>(.*?)</script>", html, re.DOTALL)]
    policy = "; ".join([
        "default-src 'none'",
        "script-src " + " ".join(hashes) + " https://cdn.jsdelivr.net/npm/mermaid@12.1.0/dist/ https://cdn.jsdelivr.net/npm/@mermaid-js/layout-elk@1.0.1/dist/",
        "style-src 'unsafe-inline' https://fonts.googleapis.com/css2",
        "font-src https://fonts.gstatic.com/s/sourceserif4/ https://fonts.gstatic.com/s/ibmplexsans/ https://fonts.gstatic.com/s/ibmplexmono/",
        "connect-src 'none'", "img-src 'none'", "object-src 'none'",
        "base-uri 'none'", "form-action 'none'",
    ])
    return html.replace('<meta http-equiv="Content-Security-Policy" content="/*CSP*/">',
                        f'<meta http-equiv="Content-Security-Policy" content="{policy}">', 1)


def cells(rest):
    return [c.strip() for c in rest.split(" | ")]


def plain(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    return text.replace("`", "")


def pages(folder):
    for path in sorted((KNOWLEDGE / folder).rglob("*.md")):
        if path.name != "README.md":
            yield path, path.read_text(encoding="utf-8")


def section(text, name):
    """The text under a ## heading, up to the next one."""
    part = re.split(r"^## " + re.escape(name) + r"\s*$", text, maxsplit=1, flags=re.MULTILINE)
    return re.split(r"^#{1,2} ", part[1], maxsplit=1, flags=re.MULTILINE)[0] if len(part) > 1 else ""


def blocks(text):
    """The paragraphs and list items of a Markdown passage, as plain text."""
    found, current = [], []
    for line in text.splitlines() + [""]:
        if line.startswith(("- ", "```")) or not line.strip() or re.match(r"^\d+\. ", line):
            if current:
                found.append(plain(" ".join(current)))
            current = [line[2:]] if line.startswith("- ") else []
        else:
            current.append(line.strip())
    return [b for b in found if b]


def head_item(text, label):
    """The text of a "- Label: value" item before the first ## heading."""
    head = re.split(r"^## ", text, maxsplit=1, flags=re.MULTILINE)[0]
    for item in blocks(head):
        if item.startswith(label + ": "):
            return item[len(label) + 2:]
    return ""


def read_rows(text):
    for line in text.splitlines():
        row = ROW.match(line)
        if row:
            yield row.group(1), cells(row.group(2))


def knowledge(graph):
    requirements = [{"id": i, "text": plain(c[0])} for i, c in read_rows((KNOWLEDGE / "system" / "requirements.md").read_text(encoding="utf-8"))]
    goals, flows, rules = [], [], []
    for path, text in pages("goals"):
        page = impact.rel(path)
        criteria = [{"id": i, "text": plain(c[0]), "proven": impact.ID.findall(c[1]) if len(c) > 1 else []}
                    for i, c in read_rows(text)]
        goals.append({
            "key": criteria[0]["id"].rsplit("-", 1)[0] if criteria else page,
            "title": (TITLE.search(text) or [None, page])[1],
            "page": page,
            "criteria": criteria,
            "flows": sorted(graph.links.get(page, ())),
            "need": blocks(section(text, "Need")),
        })
    for path, text in pages("flows"):
        page = impact.rel(path)
        scenarios = []
        for i, c in read_rows(text):
            if i not in graph.flow_rules and len(c) >= 4:
                scenarios.append({"id": i, "given": plain(c[0]), "when": plain(c[1]), "then": plain(c[2]),
                                  "covers": impact.ID.findall(c[3])})
        head = re.split(r"^## ", text, maxsplit=1, flags=re.MULTILINE)[0]
        crosses = next((line for line in re.split(r"\n(?=- )", head) if line.startswith("- Crosses:")), "")
        flows.append({"page": page, "title": (TITLE.search(text) or [None, page])[1], "scenarios": scenarios,
                      "trigger": head_item(text, "Trigger"), "outcome": head_item(text, "Outcome"),
                      "crosses": list(dict.fromkeys(re.findall(r"\(\.\./artifacts/([^/)]+)/", crosses)))})
    for path, text in pages("artifacts"):
        if path.name == "specification.md":
            artifact = path.parent.name
            for i, c in read_rows(text):
                rules.append({"id": i, "artifact": artifact, "text": plain(c[0])})
    operations = []
    for path in contracts():
        route = method = None
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^  (/\S*):$", line)
            if m:
                route = m.group(1)
            m = re.match(r"^    (get|post|put|patch|delete):$", line)
            if m:
                method = m.group(1).upper()
            m = impact.OPERATION_ID.match(line)
            if m and route:
                operations.append({"id": m.group(1), "method": method, "path": route, "contract": impact.rel(path)})
            m = re.match(r"^\s+summary: (.+)$", line)
            if m and operations and operations[-1]["contract"] == impact.rel(path) and "summary" not in operations[-1]:
                operations[-1]["summary"] = m.group(1)
    return requirements, goals, flows, rules, operations


def diagrams():
    found = []
    for path in sorted(KNOWLEDGE.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        title = re.search(r"^# (.+)$", text, re.MULTILINE)
        for block in MERMAID.finditer(text):
            section = re.findall(r"^## (.+)$", text[:block.start()], re.MULTILINE)
            found.append({"page": impact.rel(path), "title": title[1] if title else impact.rel(path),
                          "section": section[-1] if section else "", "code": block[1]})
    return found


def service_routes(operations, services):
    """List the routes each service's routes setting finds in its code, or None
    when no service has a routes setting whose folders exist yet. With more
    than one service, a route's space starts with its service name."""
    present = {name: r for name, r in services.items()
               if r and any((ROOT / folder).is_dir() for folder in r.get("folders", []))}
    if not present:
        return None
    known = {(o["method"], re.sub(r"\{[^}]*\}", "{}", o["path"])): o["id"] for o in operations}
    routes = []
    for name, setting in present.items():
        pattern = re.compile(setting["pattern"])
        files = sorted({p for folder in setting.get("folders", []) if (ROOT / folder).is_dir()
                        for p in (ROOT / folder).glob(setting.get("glob", "**/*")) if p.is_file()})
        for path in files:
            for found in pattern.finditer(path.read_text(encoding="utf-8", errors="replace")):
                method, route = found.group("method").upper(), found.group("path")
                key = (method, re.sub(r"\{[^}]*\}", "{}", route))
                space = "/" + route.strip("/").split("/")[0]
                if len(services) > 1:
                    space = f"{name} {space}"
                routes.append({"method": method, "path": route, "space": space, "service": name,
                               "covered": known.get(key)})
    return routes


def display_graph(graph):
    def show(unit):
        return unit if impact.kind(unit, graph) in COLUMN else None

    nodes, edges = {}, set()
    for unit in graph.file:
        name = show(unit)
        if not name:
            continue
        nodes[name] = COLUMN[impact.kind(unit, graph)]
        seen, todo = set(), list(graph.edges[unit])
        while todo:
            other = todo.pop()
            if other in seen:
                continue
            seen.add(other)
            target = show(other)
            if target and target != name:
                edges.add((name, target))
            elif not target:
                todo.extend(graph.edges[other])
    return {"nodes": sorted(nodes.items(), key=lambda n: (n[1], n[0])), "edges": sorted(edges)}


def metrics(graph):
    goals = sorted({u.rsplit("-", 1)[0] for u in graph.file if u.startswith("G-") and impact.ID.fullmatch(u)})
    size = {}
    for goal in goals:
        start = {u for u in graph.file if u.startswith(goal + "-") and impact.ID.fullmatch(u)}
        units, pages = impact.relies_on(graph, start)
        size[goal] = impact.counts(graph, units, pages)
    return size


def natural(unit):
    return [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", unit)]


def stories(graph, goals, flows):
    """For each goal: its flows, each with the rules it reaches, and the
    artifacts that hold those rules or that the flows cross. A rule is listed
    once, under the first flow that reaches it."""
    crosses = {f["page"]: f["crosses"] for f in flows}
    found = {}
    for goal in goals:
        start = {c["id"] for c in goal["criteria"]}
        units, _ = impact.relies_on(graph, start)
        rules = {u for u in units if impact.kind(u, graph) in ("Artifact rules", "Flow rules")}
        text = (KNOWLEDGE / goal["page"]).read_text(encoding="utf-8")
        pages = sorted((p for p in goal["flows"] if p.startswith("flows/")),
                       key=lambda p: (text.find(p.split("/")[-1]), p))
        story, placed, artifacts = [], set(), {}
        for page in pages:
            mine = {u for u in units if graph.file.get(u) == page and u.startswith("F-")}
            reached = impact.relies_on(graph, mine)[0] & rules - placed
            placed |= reached
            story.append({"page": page, "rules": sorted(reached, key=natural)})
            for name in crosses.get(page, []):
                artifacts.setdefault(name, [])
        if rules - placed:
            story.append({"page": None, "rules": sorted(rules - placed, key=natural)})
        for rule in sorted(rules, key=natural):
            home = graph.file[rule].split("/")
            if home[0] == "artifacts":
                artifacts.setdefault(home[1], []).append(rule)
        found[goal["key"]] = {"flows": story, "artifacts": artifacts}
    return found


def commit():
    try:
        return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], check=True,
                              capture_output=True, text=True).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def main(argv):
    parser = argparse.ArgumentParser(description="Build the knowledge site.")
    parser.add_argument("output", nargs="?", type=Path, default=ROOT / SITE["output"])
    parser.add_argument("--routes", action="append", metavar="DIR",
                        help="folder to read routes from, relative to the repository root; repeatable")
    args = parser.parse_args(argv)
    output = args.output
    services = {name: s["routes"] for name, s in SERVICES.items()}
    if args.routes:
        for folder in args.routes:
            if not (ROOT / folder).is_dir():
                print(f"Skipped {folder}: not a folder", file=sys.stderr)
        first = next((r for r in services.values() if r), None)
        if not first:
            print("--routes needs a service with a routes setting in artifact-driven.json", file=sys.stderr)
            return 2
        services = {"routes": {**first, "folders": args.routes}}
    graph = impact.build()
    requirements, goals, flows, rules, operations = knowledge(graph)
    size = metrics(graph)
    data = {
        "title": SITE["title"],
        "commit": commit(),
        "built": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "requirements": requirements, "goals": goals, "flows": flows, "rules": rules,
        "flowRules": [{"id": i, "owner": r["owner"], "text": plain(r["rule"])} for i, r in sorted(graph.flow_rules.items())],
        "stories": stories(graph, goals, flows),
        # The Markdown of every knowledge page, which the side panel renders as text.
        "pages": {impact.rel(path): path.read_text(encoding="utf-8") for path in sorted(KNOWLEDGE.rglob("*.md"))},
        # Story links open the source pages, relative to the written page.
        "source": Path(os.path.relpath(KNOWLEDGE, output.resolve().parent)).as_posix() + "/",
        "operations": operations, "routes": service_routes(operations, services),
        "graph": display_graph(graph), "diagrams": diagrams(), "size": size,
    }
    html = site_html(data)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html, encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT) if output.is_relative_to(ROOT) else output}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
