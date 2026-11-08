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
    ws.write(base + "artifacts/thing/web.md", "# Web\n\n## `getThing`\n\n- " + HOSTILE + "\n")
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
        self.assertEqual(data["clientNames"]["web"], HOSTILE)
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


if __name__ == "__main__":
    unittest.main()
