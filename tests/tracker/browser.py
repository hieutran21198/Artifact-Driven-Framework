"""A local static server and an isolated Chromium page for each browser check."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import os
import shutil
import threading
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


class BrowserTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as error:
            raise RuntimeError("Install tests/requirements-browser.txt and Chromium; see tests/README.md") from error
        cls.playwright = sync_playwright().start()
        cls.addClassCleanup(cls.playwright.stop)
        executable = os.environ.get("ADF_CHROMIUM_PATH") or shutil.which("chromium")
        cls.browser = cls.playwright.chromium.launch(executable_path=executable, headless=True)
        cls.addClassCleanup(cls.browser.close)
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
        cls.addClassCleanup(cls.server.server_close)
        cls.addClassCleanup(cls.server.shutdown)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.url = f"http://127.0.0.1:{cls.server.server_port}"

    def setUp(self):
        super().setUp()
        self.context = self.browser.new_context(viewport={"width": 1080, "height": 800}, reduced_motion="reduce")
        self.addCleanup(self.context.close)
        self.requests = []
        self.context.route("**/*", self.route_request)
        self.page = self.context.new_page()
        self.page.set_default_timeout(5000)

    def route_request(self, route):
        self.requests.append(route.request.url)
        if urlsplit(route.request.url).netloc == urlsplit(self.url).netloc:
            route.continue_()
        else:
            route.abort()

    def open_tracker(self):
        # A local folder avoids startup GitHub/Pyodide work in frame-only checks.
        config = {"version": 2, "workspaces": [{"type": "local", "name": "fixture"}], "selected": "local:fixture"}
        self.page.add_init_script("""(() => {
          if (window !== window.top) return;
          localStorage.setItem('viewer-config', %s);
          sessionStorage.setItem('viewer-tokens', JSON.stringify({fixture:'test-only-marker'}));
        })();""" % json.dumps(json.dumps(config)))
        self.page.goto(self.url + "/tracker/")
        self.page.wait_for_function("() => typeof drawSite === 'function'")

    def embed(self, html):
        self.page.evaluate("html => drawSite(html)", html)
        # Wait for real srcdoc content, not the new frame's initial about:blank.
        self.page.frame_locator("#view").locator("body > *").first.wait_for(state="attached")
        frame = self.page.locator("#view").element_handle().content_frame()
        frame.wait_for_function("() => location.href === 'about:srcdoc' && document.readyState === 'complete'")
        return frame
