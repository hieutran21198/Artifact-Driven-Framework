"""Safety of the actual HTML produced by the knowledge-site command."""

import base64
import hashlib
from html.parser import HTMLParser
import json
import unittest

from tests.scripts.workspace import Workspace


HOSTILE = '</ScRiPt><img src="https://workspace.invalid/leak" onerror="window.injected=1">'


def site_workspace():
    """Seed configuration, knowledge, paths and diagrams that cross HTML sinks."""
    ws = Workspace({
        "site": {"title": HOSTILE + " & \u2028\u2029", "output": "build/site.html"},
        "clients": {"web": HOSTILE},
        "services": {HOSTILE: {"routes": {
            "folders": ["routes"], "glob": "*.txt",
            "pattern": r"(?P<method>[^|]+)\|(?P<path>[^\n]+)",
        }}},
    })
    base = "docs/software-knowledges/"
    ws.write(base + "system/requirements.md", "# Requirements\n\n| SYS-1 | " + HOSTILE + " |\n")
    ws.write(base + "system/context.md", "# Context " + HOSTILE + "\n\n```mermaid\nflowchart TB\n A[Reader] --> B[Workspace]\n```\n")
    ws.write(base + "goals/safe.md", "# Goal: " + HOSTILE + "\n\n| G-SAFE-1 | " + HOSTILE + " | F-SAFE-1 |\n\n[Flow](../flows/safe.md)\n\n```mermaid\nflowchart TB\n A[Safe flow] --> B[Done]\n```\n")
    ws.write(base + 'goals/odd" onfocus="window.injected=2.md', "# Goal: Odd key\n")
    ws.write(base + "flows/safe.md", "# Flow: Safe flow\n\n| F-SAFE-1 | " + HOSTILE + " | `getThing` | " + HOSTILE + " | TH-1, SYS-1 |\n\n[Thing](../artifacts/thing/specification.md)\n\n```mermaid\nsequenceDiagram\n Reader->>Workspace: Read\n Workspace-->>Reader: Knowledge\n```\n")
    ws.write(base + "artifacts/thing/specification.md", "# Thing\n\n| TH-1 | " + HOSTILE + " | — |\n")
    ws.write(base + "artifacts/thing/openapi.yaml", "openapi: 3.0.3\npaths:\n  /thing:\n    get:\n      operationId: getThing\n      summary: " + HOSTILE + "\n")
    ws.write("routes/routes.txt", '<img src="https://workspace.invalid/method">|/unsafe"<svg onload="window.injected=3">\nGET|/thing\n')
    return ws


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=False)
        self.tags = []
        self.scripts = []
        self.active_script = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))
        if tag == "script":
            self.scripts.append("")
            self.active_script = len(self.scripts) - 1

    def handle_endtag(self, tag):
        if tag == "script":
            self.active_script = None

    def handle_data(self, data):
        if self.active_script is not None:
            self.scripts[self.active_script] += data


class Site(unittest.TestCase):
    def build(self, title=None):
        ws = site_workspace()
        self.addCleanup(ws.close)
        if title is not None:
            config = json.loads((ws.root / "artifact-driven.json").read_text())
            config["site"]["title"] = title
            ws.write("artifact-driven.json", json.dumps(config))
        run = ws.run("site.py")
        self.assertEqual(run.returncode, 0, run.stderr)
        return (ws.root / "build/site.html").read_text(encoding="utf-8")

    def test_SYS_7_F_VIEW_24_script_closing_content_stays_json_data(self):
        """SYS-7, F-VIEW-24: generated JSON preserves data without ending script."""
        page = Page(self.build())
        self.assertEqual(len(page.scripts), 3)
        self.assertFalse([tag for tag, _ in page.tags if tag == "img"])
        source = next(script for script in page.scripts if script.startswith("const DATA="))
        data = json.loads(source.removeprefix("const DATA=").removesuffix(";"))
        self.assertEqual(data["title"], HOSTILE + " & \u2028\u2029")
        self.assertEqual(data["requirements"][0]["text"], HOSTILE)
        self.assertNotIn("clientNames", data)
        self.assertNotIn("clients", data)
        self.assertIn('" onfocus="', data["goals"][0]["key"])
        for unsafe in ("<", ">", "&", "\u2028", "\u2029"):
            self.assertNotIn(unsafe, source)

    def test_SYS_7_standalone_policy_authorizes_only_trusted_scripts(self):
        """SYS-7: standalone HTML denies workspace resource destinations."""
        page = Page(self.build())
        policies = [attrs["content"] for tag, attrs in page.tags
                    if tag == "meta" and attrs.get("http-equiv") == "Content-Security-Policy"]
        self.assertEqual(len(policies), 1)
        policy = policies[0]
        directives = dict(part.strip().split(" ", 1) for part in policy.split(";") if part.strip())
        for name in ("default-src", "connect-src", "img-src", "object-src", "base-uri", "form-action"):
            self.assertEqual(directives[name], "'none'")
        self.assertNotIn("'unsafe-inline'", directives["script-src"])
        self.assertNotIn("https://cdn.jsdelivr.net ", directives["script-src"] + " ")
        for source in page.scripts:
            digest = base64.b64encode(hashlib.sha256(source.encode()).digest()).decode()
            self.assertIn("'sha256-" + digest + "'", directives["script-src"])

    def test_SYS_7_template_markers_in_workspace_data_stay_literal(self):
        """SYS-7: workspace text cannot replace template markers or invalidate script hashes."""
        title = "Literal /*CSP*/ and /*DATA*/null"
        page = Page(self.build(title))
        source = next(script for script in page.scripts if script.startswith("const DATA="))
        data = json.loads(source.removeprefix("const DATA=").removesuffix(";"))
        self.assertEqual(data["title"], title)
        policy = next(attrs["content"] for tag, attrs in page.tags
                      if tag == "meta" and attrs.get("http-equiv") == "Content-Security-Policy")
        for source in page.scripts:
            digest = base64.b64encode(hashlib.sha256(source.encode()).digest()).decode()
            self.assertIn("'sha256-" + digest + "'", policy)


def flow_rule_workspace():
    """Local/shared rule definitions plus an FR-shaped artifact and design data."""
    ws = site_workspace()
    base = "docs/software-knowledges/"
    ws.write(base + "flows/safe.md", "# Flow: Safe flow\n\n## Coordination rules\n\n"
             "| ID | Rule | Dependencies |\n| --- | --- | --- |\n"
             "| FR-LOCAL-1 | " + HOSTILE + " | TH-1, SYS-1 |\n\n"
             "## Scenarios\n\n| ID | Given | When | Then | Rules |\n| --- | --- | --- | --- | --- |\n"
             "| F-SAFE-1 | Files | `getThing` | Read | FR-LOCAL-1, FR-SHARED-1, FR-LEGACY-1 |\n\n"
             "[Thing](../artifacts/thing/specification.md)\n"
             "[Design](../../../apps/web/design/FR-DESIGN-1.md)\n"
             '[Hostile design](https://workspace.invalid/FR-DESIGN-2?x="<img>)\n')
    ws.write(base + "flows/contracts/shared.md", "# Shared interaction\n\n## Coordination rules\n\n"
             "| ID | Rule | Dependencies |\n| --- | --- | --- |\n"
             "| FR-SHARED-1 | Share safely. | TH-1 |\n")
    ws.write(base + "artifacts/thing/specification.md", "# Thing\n\n"
             "| TH-1 | An artifact rule. | — |\n| FR-LEGACY-1 | A legacy artifact rule. | — |\n")
    ws.write(base + "goals/other.md", "# Goal: Other\n\n| G-OTHER-1 | Share | F-OTHER-1 |\n")
    ws.write(base + "flows/other.md", "# Flow: Other\n\n"
             "| F-OTHER-1 | Files | `getThing` | Read | FR-SHARED-1 |\n")
    ws.write("apps/web/design/FR-DESIGN-1.md", "# Design\n\n| FR-DESIGN-1 | Navigation only. |\n")
    return ws


class FlowRuleSite(unittest.TestCase):
    def test_KN_13_F_VIEW_31_generated_data_distinguishes_rules(self):
        """KN-13, F-VIEW-31, SYS-7: classified definitions, dependencies and safe data."""
        ws = flow_rule_workspace()
        self.addCleanup(ws.close)
        run = ws.run("site.py")
        self.assertEqual(run.returncode, 0, run.stderr)
        page = Page((ws.root / "build/site.html").read_text())
        source = next(s for s in page.scripts if s.startswith("const DATA="))
        data = json.loads(source.removeprefix("const DATA=").removesuffix(";"))
        self.assertEqual({r["id"] for r in data["flowRules"]}, {"FR-LOCAL-1", "FR-SHARED-1"})
        self.assertEqual({r["id"] for r in data["rules"]}, {"TH-1", "FR-LEGACY-1"})
        self.assertEqual({s["id"] for f in data["flows"] for s in f["scenarios"]}, {"F-SAFE-1", "F-OTHER-1"})
        nodes = dict(data["graph"]["nodes"])
        self.assertNotEqual(nodes["FR-LOCAL-1"], nodes["FR-LEGACY-1"])
        self.assertNotEqual(nodes["FR-LOCAL-1"], nodes["F-SAFE-1"])
        self.assertNotIn("FR-DESIGN-1", nodes)
        self.assertNotIn("FR-DESIGN-2", nodes)
        self.assertIn(["FR-LOCAL-1", "TH-1"], data["graph"]["edges"])
        self.assertEqual(data["size"]["G-SAFE"]["rules"], 4)
        self.assertEqual(data["size"]["G-SAFE"]["scenarios"], 1)
        self.assertFalse([tag for tag, _ in page.tags if tag == "img"])


if __name__ == "__main__":
    unittest.main()
