"""Runtime checks of generated HTML; diagram fixtures do not use the network."""

import json

from tests.scripts.test_site import HOSTILE, site_workspace, flow_rule_workspace
from tests.tracker.browser import BrowserTestCase


MERMAID_URL = "https://cdn.jsdelivr.net/npm/mermaid@12.1.0/dist/mermaid.esm.min.mjs"
ELK_URL = "https://cdn.jsdelivr.net/npm/@mermaid-js/layout-elk@1.0.1/dist/mermaid-layout-elk.esm.min.mjs"


class SiteBrowser(BrowserTestCase):
    def build(self, diagram=None):
        ws = site_workspace()
        self.addCleanup(ws.close)
        if diagram is not None:
            ws.write("docs/software-knowledges/system/context.md", "# Context\n\n```mermaid\n" + diagram + "\n```\n")
        run = ws.run("site.py")
        self.assertEqual(run.returncode, 0, run.stderr)
        return (ws.root / "build/site.html").read_text(encoding="utf-8")

    def open_site(self, html):
        self.page.route(self.url + "/fixture.html", lambda route: route.fulfill(body=html, content_type="text/html"))
        self.page.goto(self.url + "/fixture.html")
        self.page.locator("#goal-options input").first.wait_for(state="attached")

    def analyze(self):
        self.page.locator("#drop summary").click()
        self.page.locator('#goal-options input[value="*"]').check()
        self.page.locator("#run").click()
        self.page.locator("#results").wait_for(state="visible")

    def diagram_library(self, svg):
        # Exercise our rendering boundary with deterministic upstream output. Real Mermaid/ELK
        # rendering is a separate browser acceptance check, not a claim made by this fake.
        module = """window.diagramCalls=[];
          export default {registerLayoutLoaders(){}, initialize(config){window.diagramConfig=config;},
          async render(id, code){window.diagramCalls.push(code);return {svg:%s.replaceAll('fixture',id)};}};
        """ % json.dumps(svg)
        self.page.route(MERMAID_URL, lambda route: route.fulfill(body=module, content_type="text/javascript", headers={"Access-Control-Allow-Origin": "*"}))
        self.page.route(ELK_URL, lambda route: route.fulfill(body="export default [];", content_type="text/javascript", headers={"Access-Control-Allow-Origin": "*"}))

    def assert_no_workspace_requests(self):
        self.assertFalse([url for url in self.requests if "workspace.invalid" in url])

    def test_KN_13_F_VIEW_31_flow_rules_counts_and_safety(self):
        """KN-13, F-VIEW-31, SYS-7: real DOM counts rules apart and keeps text inert."""
        ws = flow_rule_workspace()
        self.addCleanup(ws.close)
        run = ws.run("site.py")
        self.assertEqual(run.returncode, 0, run.stderr)
        self.open_site((ws.root / "build/site.html").read_text())
        self.analyze()
        self.assertEqual(self.page.locator("#metrics .v").nth(3).inner_text(), "4")
        for goal, expected in (("G-SAFE", "4"), ("G-OTHER", "2"), ("G-SAFE", "4")):
            self.page.locator("#drop summary").click()
            self.page.locator('#goal-options input[value="*"]').uncheck()
            for item in self.page.locator('#goal-options input:not([value="*"])').all():
                item.uncheck()
            self.page.locator(f'#goal-options input[value="{goal}"]').check()
            self.page.locator("#run").click()
            self.assertEqual(self.page.locator("#slice-metrics .v").nth(3).inner_text(), expected)
            self.assertEqual(self.page.locator("#slice-metrics .v").nth(2).inner_text(), "1")
        self.page.locator('[data-lang="vi"]').click()
        self.assertEqual(self.page.locator("img,[onerror],[onload]").count(), 0)
        self.assertNotIn("FR-DESIGN", self.page.locator("#results").text_content())
        self.assertIsNone(self.page.evaluate("window.injected"))
        self.assert_no_workspace_requests()

    def test_SYS_7_F_VIEW_24_text_attributes_and_controls(self):
        """SYS-7, F-VIEW-24: every generated data kind stays text while controls work."""
        self.open_site(self.build())
        self.assertEqual(self.page.locator("h1").inner_text(), HOSTILE + " & \u2028\u2029")
        # The path without a criterion becomes a goal key. Attribute quotes must stay in it.
        keys = self.page.locator("#goal-options input").evaluate_all("els => els.map(e => e.value)")
        self.assertTrue(any('" onfocus="' in key for key in keys))
        self.analyze()
        self.page.locator('#goal-cards [data-goal="G-SAFE"]').click()
        self.assertIn(HOSTILE, self.page.locator("#side-title").inner_text())
        self.assertIn(HOSTILE, self.page.locator("#side-body").inner_text())
        self.page.locator("#side-close").click()
        self.page.locator('[data-lang="vi"]').click()
        self.assertEqual(self.page.locator("h1").inner_text(), HOSTILE + " & \u2028\u2029")
        self.assertEqual(self.page.locator("img,[onfocus],[onerror],[onload]").count(), 0)
        self.page.locator("#coverage-bars details").last.locator("summary").click()
        self.assertIn("WORKSPACE.INVALID/METHOD", self.page.locator("#coverage-bars").inner_text())
        self.assertIsNone(self.page.evaluate("window.injected"))
        self.assert_no_workspace_requests()

    def test_SYS_7_F_VIEW_25_unavailable_diagrams_keep_source(self):
        """SYS-7, F-VIEW-25: blocked diagram libraries leave readable source and controls."""
        self.open_site(self.build())
        self.analyze()
        self.assertIn("flowchart TB", self.page.locator("#guide-system pre").inner_text())
        self.assertEqual(self.page.locator("#guide-system svg").count(), 0)
        self.assertEqual(self.page.locator('[data-layer="system/"]').count(), 0)
        self.page.locator('#goal-cards [data-goal="G-SAFE"]').click()
        self.page.keyboard.press("Escape")
        self.assertTrue(self.page.locator("#side").is_hidden())
        self.assert_no_workspace_requests()

    def test_SYS_7_F_VIEW_24_diagram_directives_and_resources_never_reach_renderer(self):
        """SYS-7, F-VIEW-24: resource/config syntax remains source before rendering."""
        self.diagram_library('<svg xmlns="http://www.w3.org/2000/svg"><text>Safe</text></svg>')
        hostile = [
            '%%{init: {"securityLevel":"loose","themeCSS":"@import url(https://workspace.invalid/css)"}}%%\nflowchart TB\n A[Unsafe]',
            '---\nconfig:\n  securityLevel: loose\n---\nflowchart TB\n A[Unsafe]',
            'flowchart TB\n A["<img src=https://workspace.invalid/image onerror=alert(1)>"]',
            'flowchart TB\n A["&lt;img src=https://workspace.invalid/entity&gt;"]',
            'flowchart TB\n A[Unsafe]\n click A "javascript:alert(1)"',
            'flowchart TB\n A@{ img: "https://workspace.invalid/image" }',
            'flowchart TB\n A[Unsafe]\n style A fill:url(https://workspace.invalid/fill)',
        ]
        for source in hostile:
            with self.subTest(source=source):
                self.open_site(self.build(source))
                self.page.wait_for_function("() => !!window.mermaid")
                self.analyze()
                self.assertEqual(self.page.locator("#guide-system pre").inner_text(), source + "\n")
                self.assertNotIn(source + "\n", self.page.evaluate("window.diagramCalls"))
                self.assertEqual(self.page.locator("#guide-system svg").count(), 0)
                self.assertEqual(self.page.locator("#guide-system pre").inner_text(), source + "\n")
                self.assertEqual(self.page.locator("#guide-system svg").count(), 0)
        self.assert_no_workspace_requests()

    def test_SYS_7_F_VIEW_24_rendered_svg_drops_executable_and_resource_markup(self):
        """SYS-7, F-VIEW-24: SVG output keeps geometry/text, not links or resource sinks."""
        svg = '''<svg xmlns="http://www.w3.org/2000/svg" id="fixture" viewBox="0 0 100 40">
          <style>@import url(https://workspace.invalid/css); #fixture .node{fill:red;stroke:url(https://workspace.invalid/stroke)} body{display:none}</style>
          <script>window.injected=4</script><image href="https://workspace.invalid/svg-image"/>
          <foreignObject><img xmlns="http://www.w3.org/1999/xhtml" src="https://workspace.invalid/html-image"/></foreignObject>
          <a href="javascript:alert(1)"><text>Unsafe link</text></a>
          <g class="node" onclick="window.injected=5"><rect width="100" height="40" fill="url(https://workspace.invalid/fill)"/><text x="4" y="20">Safe flow</text></g>
        </svg>'''
        self.diagram_library(svg)
        self.open_site(self.build())
        self.page.wait_for_function("() => !!window.mermaid")
        self.analyze()
        self.page.locator("#guide-system svg").wait_for()
        self.assertEqual(self.page.locator("#guide-system script,#guide-system image,#guide-system a,#guide-system foreignObject,#guide-system [onclick]").count(), 0)
        self.assertEqual(self.page.locator("#guide-system text").text_content(), "Safe flow")
        self.assertNotIn("workspace.invalid", self.page.locator("#guide-system svg").evaluate("svg => svg.outerHTML"))
        self.assertIn(HOSTILE, self.page.locator("#guide-system > p").first.text_content())
        self.assertNotIn("body", self.page.locator("#guide-system style").text_content())
        self.assertTrue(self.page.evaluate("window.diagramConfig.securityLevel==='strict' && window.diagramConfig.htmlLabels===false"))
        self.page.locator("#guide-system svg").wait_for()
        self.assertEqual(self.page.locator("#guide-system script,#guide-system image,#guide-system a,#guide-system foreignObject,#guide-system [onclick]").count(), 0)
        self.assertNotIn("workspace.invalid", self.page.locator("#guide-system svg").evaluate("svg => svg.outerHTML"))
        self.page.locator('[data-layer="goals/"] .to-flow').click()
        self.assertTrue(self.page.locator('[data-layer="flows/"]').is_visible())
        self.assert_no_workspace_requests()

    def test_SYS_7_F_VIEW_25_narrow_diagrams_keep_natural_size(self):
        """SYS-7, F-VIEW-25: safe SVG copying keeps narrow class/state drawings readable."""
        self.diagram_library('''<svg xmlns="http://www.w3.org/2000/svg" width="100%"
          style="max-width:118.1px" viewBox="0 0 118.1 245">
          <rect x="1" y="1" width="116" height="243"/><text x="4" y="20">Reader</text></svg>''')
        self.open_site(self.build())
        self.page.wait_for_function("() => !!window.mermaid")
        self.analyze()
        drawing = self.page.locator("#guide-system svg")
        drawing.wait_for()
        box = drawing.bounding_box()
        self.assertGreater(box["width"], 100)
        self.assertLessEqual(box["width"], 119)
        self.assertLessEqual(box["height"], 246)
        self.page.set_viewport_size({"width": 360, "height": 640})
        box = drawing.bounding_box()
        self.assertLessEqual(box["width"], 119)
        self.assertLessEqual(box["height"], 246)
        self.assert_no_workspace_requests()
