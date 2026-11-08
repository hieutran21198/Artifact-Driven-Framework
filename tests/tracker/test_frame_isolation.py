"""Seeded checks of the opaque knowledge-site frame and its small message API."""

from html.parser import HTMLParser
import unittest

from tests.tracker.browser import BrowserTestCase, ROOT


PROBE = """<!doctype html><html><body style="margin:0"><div style="height:800px">Frame</div>
<script>
window.messages=[];
addEventListener('message', event => {
  messages.push(event.data);
  if(event.data.type==='adf:site-init') {
    window.render=event.data.render;
    parent.postMessage({type:'adf:site-size',render,height:800},'*');
  }
});
</script></body></html>"""


class FrameIsolation(BrowserTestCase):
    def setUp(self):
        super().setUp()
        self.open_tracker()

    def test_TRK_14_frame_cannot_access_tracker_state_or_navigate_parent(self):
        """TRK-14, F-VIEW-25: running frame code cannot reach tracker state or navigation."""
        frame = self.embed(PROBE)
        blocked = frame.evaluate("""() => {
          const result={};
          for (const [name, read] of Object.entries({
            document:()=>parent.document.body,
            settings:()=>parent.config,
            tokens:()=>parent.sessionStorage.getItem('viewer-tokens'),
            parentStorage:()=>parent.localStorage.getItem('viewer-config'),
            localStorage:()=>localStorage.getItem('viewer-config'),
            sessionStorage:()=>sessionStorage.getItem('viewer-tokens'),
            navigation:()=>{parent.location.href='https://attacker.invalid/escape';}
          })) {try{read();result[name]=false;}catch{result[name]=true;}}
          return result;
        }""")
        self.assertTrue(all(blocked.values()), blocked)
        self.assertEqual(self.page.url, self.url + "/tracker/")
        self.assertEqual(self.page.locator("#view").get_attribute("sandbox"), "allow-scripts")
        self.assertIsNone(self.page.evaluate("document.getElementById('view').contentDocument"))

    def test_TRK_14_sizing_rejects_unrelated_stale_and_invalid_messages(self):
        """TRK-14, F-VIEW-25: only the active document can supply bounded frame dimensions."""
        frame = self.embed(PROBE)
        frame.wait_for_function("() => typeof render === 'string'")
        self.page.wait_for_function("() => document.getElementById('view').style.height === '802px'")
        render = frame.evaluate("render")
        # Real child messages with an invalid type, render, shape or number must do nothing.
        frame.evaluate("""() => {
          const base={type:'adf:site-size',render,height:923};
          for(const data of [null,[],{}, {...base,type:'unknown'}, {...base,render:'old'},
            {...base,height:-1}, {...base,height:Infinity}, {...base,height:NaN},
            {...base,height:'923'}, {...base,height:10000001}]) parent.postMessage(data,'*');
        }""")
        self.page.evaluate("""render => {
          const data={type:'adf:site-size',render,height:923};
          dispatchEvent(new MessageEvent('message',{data,source:window,origin:'null'}));
          dispatchEvent(new MessageEvent('message',{data,source:document.getElementById('view').contentWindow,origin:location.origin}));
        }""", render)
        self.page.evaluate("() => new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)))")
        self.assertEqual(self.page.locator("#view").evaluate("e=>e.style.height"), "802px")
        frame.evaluate("parent.postMessage({type:'adf:site-size',render,height:925.5},'*')")
        self.page.wait_for_function("() => document.getElementById('view').style.height === '928px'")
        self.page.evaluate("window.oldFrame=document.getElementById('view').contentWindow")
        fresh = self.embed(PROBE)
        fresh.wait_for_function("() => typeof render === 'string'")
        fresh_id = fresh.evaluate("render")
        self.assertNotEqual(render, fresh_id)
        self.page.evaluate("""ids => {
          const current=document.getElementById('view').contentWindow;
          dispatchEvent(new MessageEvent('message',{source:oldFrame,origin:'null',data:{type:'adf:site-size',render:ids[1],height:999}}));
          dispatchEvent(new MessageEvent('message',{source:current,origin:'null',data:{type:'adf:site-size',render:ids[0],height:999}}));
        }""", [render, fresh_id])
        self.assertEqual(self.page.locator("#view").evaluate("e=>e.style.height"), "802px")
        messages = fresh.evaluate("messages")
        self.assertNotIn("test-only-marker", str(messages))
        for message in messages:
            self.assertIn(message["type"], ("adf:site-init", "adf:site-viewport"))


class FramePolicy(unittest.TestCase):
    def test_TRK_14_frame_declares_only_script_sandbox_permission(self):
        """TRK-14: the site frame has an opaque origin and cannot navigate its parent."""
        class Frames(HTMLParser):
            def __init__(self):
                super().__init__()
                self.frame = None

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if tag == "iframe" and attrs.get("id") == "view":
                    self.frame = attrs

        parser = Frames()
        parser.feed((ROOT / "tracker/index.html").read_text(encoding="utf-8"))
        self.assertIsNotNone(parser.frame)
        self.assertEqual(parser.frame.get("sandbox"), "allow-scripts")


class GeneratedFrame(BrowserTestCase):
    def build_site(self, extra_goals=0):
        from tests.scripts.test_site import site_workspace
        ws = site_workspace()
        self.addCleanup(ws.close)
        for index in range(extra_goals):
            ws.write(f"docs/software-knowledges/goals/extra-{index}.md", f"# Goal: Extra {index}\n")
        run = ws.run("site.py")
        self.assertEqual(run.returncode, 0, run.stderr)
        return (ws.root / "build/site.html").read_text(encoding="utf-8")

    def analyze(self, frame):
        frame.locator("#drop > summary").click()
        frame.locator('#goal-options input[value="*"]').check()
        frame.locator("#run").click()
        frame.locator("#goal-cards [data-goal]").first.wait_for()

    def test_F_VIEW_24_generated_hostile_content_remains_data_embedded(self):
        """F-VIEW-24, SYS-7, TRK-14: the real generated page stays inert and usable embedded."""
        from tests.scripts.test_site import HOSTILE
        html = self.build_site()
        self.open_tracker()
        frame = self.embed(html)
        self.assertEqual(frame.locator("h1").text_content(), HOSTILE + " & \u2028\u2029")
        self.analyze(frame)
        self.assertEqual(frame.locator("#goal-cards [data-goal]").count(), 2)
        self.assertIsNone(frame.evaluate("window.injected"))
        self.assertEqual(frame.locator("img,[onerror],[onfocus]").count(), 0)
        self.assertFalse(any("workspace.invalid" in request for request in self.requests), self.requests)
        # The malformed goal key is still a selectable value, not an attribute.
        self.assertTrue(any('" onfocus="' in key for key in frame.locator("#goal-options input").evaluate_all("items=>items.map(i=>i.value)")))
        frame.locator('[data-goal="G-SAFE"]').click()
        self.assertIn(HOSTILE, frame.locator("#side-body").text_content())
        frame.locator("#side-close").click()
        self.assertTrue(frame.locator("#side").is_hidden())

    def test_F_VIEW_25_fitting_expanded_controls_details_and_offline_diagrams(self):
        """F-VIEW-25, TRK-14: controls fit one page; details track its viewport and source stays readable."""
        html = self.build_site(extra_goals=12)
        self.open_tracker()
        frame = self.embed(html)
        frame.wait_for_function("() => document.documentElement.style.overflow === 'hidden'")
        frame.locator("#drop > summary").click()
        frame.wait_for_function("() => document.querySelector('.drop-list').getBoundingClientRect().bottom + 16 <= innerHeight + 1")
        frame.locator('#goal-options input[value="*"]').check()
        frame.locator("#run").click()
        frame.wait_for_function("() => document.body.scrollHeight <= innerHeight + 1")
        self.assertGreater(frame.locator(".diagram pre").count(), 0)
        self.assertIn("flowchart TB", frame.locator(".diagram pre").first.text_content())
        # Repeated pager actions and language changes preserve the layout.
        frame.locator('#goal-pager [data-page="1"]').click()
        frame.locator('#goal-pager [data-page="-1"]').click()
        frame.locator('[data-lang="vi"]').click()
        frame.locator('[data-lang="en"]').click()
        frame.locator("#goal-cards [data-goal]").first.click()
        render = self.page.evaluate("siteFrame.render")
        unchanged = frame.evaluate("""render => {
          const side=document.getElementById('side');
          const before=[side.style.top,side.style.height];
          const base={type:'adf:site-viewport',render,top:90,height:321};
          for(const data of [null,{}, {...base,type:'unknown'}, {...base,render:'old'},
            {...base,top:Infinity}, {...base,top:-1}, {...base,height:NaN},
            {...base,height:-1}, {...base,height:'321'}, {...base,height:10000001}]) {
            dispatchEvent(new MessageEvent('message',{source:parent,data}));
          }
          dispatchEvent(new MessageEvent('message',{source:window,data:base}));
          return {before,after:[side.style.top,side.style.height]};
        }""", render)
        self.assertEqual(unchanged["before"], unchanged["after"])
        self.page.evaluate("scrollBy(0, 120)")
        self.page.wait_for_function("() => scrollY > 0")
        frame.wait_for_function("() => parseFloat(document.getElementById('side').style.height) > 0")
        side = frame.locator("#side").bounding_box()
        self.assertGreaterEqual(side["y"], -2)
        self.assertLessEqual(side["y"] + side["height"], 802)
        self.assertLessEqual(side["height"], 800)
        self.page.set_viewport_size({"width": 360, "height": 640})
        frame.wait_for_function("() => parseFloat(document.getElementById('side').style.height) <= 640")
        self.assertLessEqual(frame.locator("#side").bounding_box()["width"], 360)
        self.assertEqual(self.page.locator("#view").get_attribute("scrolling"), "no")
        self.assertEqual(frame.evaluate("getComputedStyle(document.documentElement).overflow"), "hidden")
        frame.locator("#side-close").click()
        frame.locator("#drop > summary").click()
        frame.wait_for_function("() => document.querySelector('.drop-list').getBoundingClientRect().bottom + 16 <= innerHeight + 1")
