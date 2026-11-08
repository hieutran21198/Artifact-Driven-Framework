"""Real-browser checks of the reading guide; external resources are blocked."""

from tests.tracker.browser import BrowserTestCase


class ReadingPagesBrowser(BrowserTestCase):
    def assert_destination_in_view(self, identifier):
        target = self.page.locator("#" + identifier)
        anchor = target.locator("summary").first if target.evaluate("el => el.tagName === 'DETAILS'") else target
        self.page.wait_for_function("""el => {
            const box = el.getBoundingClientRect();
            return box.top >= 0 && box.top < innerHeight && box.bottom > 0;
        }""", arg=anchor.element_handle())

    def test_F_LEARN_29_topics_and_tracker_are_real_navigation(self):
        """F-LEARN-29, SYS-8: each topic is reachable without timed animation."""
        topics = [("Knowledge", "knowledge"), ("A change", "change"),
                  ("Checks", "checks"), ("Start", "install"), ("What it is", "overview")]
        for motion in ["reduce", "no-preference"]:
            self.page.emulate_media(reduced_motion=motion)
            for name, topic in topics:
                with self.subTest(motion=motion, topic=topic):
                    self.page.goto(self.url + "/index.html#" + topic)
                    self.assert_destination_in_view(topic)
                    self.page.get_by_role("navigation", name="Sections", exact=True).get_by_role("link", name=name, exact=True).click()
                    self.assertEqual(self.page.evaluate("location.hash"), "#" + topic)
                    self.assert_destination_in_view(topic)
        footer = self.page.get_by_role("navigation", name="Reading topics and tracker", exact=True)
        for name, topic in topics:
            footer.get_by_role("link", name=name, exact=True).click()
            self.assert_destination_in_view(topic)
        self.assertGreater(self.page.locator('a[href="tracker/"]').count(), 0)

    def test_F_LEARN_30_legacy_fragments_and_history(self):
        """F-LEARN-30, SYS-8: old URLs keep their topic, including repeated navigation."""
        routes = {
            "how-we-work.html": "knowledge",
            "how-we-work.html#howto-h": "knowledge",
            "how-we-work.html#words-h": "terms",
            "agents.html": "change",
            "agents.html#change-h": "change",
            "agents.html#team-h": "limits",
            "agents.html#try-h": "install",
            "agents.html#gives-h": "files",
            "agents.html#tools-h": "tools",
            "framework.html": "files",
            "framework.html#checks": "checks",
            "agents.html#unknown": "change",
        }
        for old, target in routes.items():
            with self.subTest(old=old):
                self.page.goto(self.url + "/" + old)
                self.page.wait_for_url(self.url + "/index.html#" + target)
                self.assertTrue(self.page.locator("#" + target).is_visible())
                if target in {"terms", "limits", "files", "tools"}:
                    self.assertTrue(self.page.locator("#" + target).evaluate("el => el.open"))
                self.assert_destination_in_view(target)
        self.page.goto(self.url + "/index.html#overview")
        nav = self.page.get_by_role("navigation", name="Sections", exact=True)
        nav.get_by_role("link", name="Knowledge", exact=True).click()
        nav.get_by_role("link", name="Checks", exact=True).click()
        self.page.go_back()
        self.assertTrue(self.page.url.endswith("#knowledge"))
        self.assert_destination_in_view("knowledge")
        self.page.go_forward()
        self.assertTrue(self.page.url.endswith("#checks"))
        self.assert_destination_in_view("checks")

    def test_F_LEARN_12_F_LEARN_13_framework_entry_opens_governing_references(self):
        """F-LEARN-12, F-LEARN-13: the old framework URL exposes the file tree and source links."""
        self.page.goto(self.url + "/framework.html")
        self.page.wait_for_url(self.url + "/index.html#files")
        self.assert_destination_in_view("files")
        files = self.page.locator("#files")
        self.assertTrue(files.locator("pre").is_visible())
        for name, suffix in [("governance", "docs/governances/artifact-driven/README.md"),
                             ("runbooks", "docs/governances/artifact-driven/runbooks/README.md"),
                             ("skills", ".agents/skills/README.md")]:
            link = files.get_by_role("link", name=name, exact=True)
            self.assertTrue(link.is_visible())
            self.assertTrue(link.get_attribute("href").endswith("/" + suffix))

    def test_F_LEARN_16_F_LEARN_17_method_entry_connects_example_roles_and_terms(self):
        """F-LEARN-16, F-LEARN-17: method entry, worked roles and optional terms remain reachable."""
        self.page.goto(self.url + "/how-we-work.html")
        self.page.wait_for_url(self.url + "/index.html#knowledge")
        self.assert_destination_in_view("knowledge")
        self.assertTrue(self.page.locator("#knowledge dl").is_visible())
        self.page.get_by_role("navigation", name="Sections", exact=True).get_by_role("link", name="A change", exact=True).click()
        self.assert_destination_in_view("change")
        self.assertEqual(self.page.locator("#change ol > li").count(), 5)
        self.page.locator("#terms > summary").focus()
        self.page.keyboard.press("Enter")
        self.assertTrue(self.page.locator("#terms").evaluate("el => el.open"))
        self.assertTrue(self.page.locator("#terms > summary").evaluate("el => el === document.activeElement"))
        self.assert_destination_in_view("terms")
        self.page.keyboard.press("Enter")
        self.assertFalse(self.page.locator("#terms").evaluate("el => el.open"))

    def test_F_LEARN_23_agent_entry_exposes_limits_and_tool_guidance(self):
        """F-LEARN-23: old agent entry and its reference fragments open readable details."""
        for fragment, target in [("", "change"), ("#team-h", "limits"), ("#tools-h", "tools")]:
            self.page.goto(self.url + "/agents.html" + fragment)
            self.page.wait_for_url(self.url + "/index.html#" + target)
            self.assert_destination_in_view(target)
            if target != "change":
                self.assertTrue(self.page.locator("#" + target + " .details-body").is_visible())

    def test_F_LEARN_25_SYS_8_narrow_dark_and_keyboard(self):
        """F-LEARN-25, SYS-8: light-only guide fits narrow screens and keyboard navigation."""
        self.page.emulate_media(color_scheme="dark")
        for width in [360, 390, 1080]:
            with self.subTest(width=width):
                self.page.set_viewport_size({"width": width, "height": 800})
                self.page.goto(self.url + "/index.html#files")
                self.page.locator("#files[open]").wait_for()
                for details in self.page.locator("details").all():
                    if not details.evaluate("el => el.open"):
                        details.locator("summary").click()
                self.assertTrue(self.page.evaluate("document.documentElement.scrollWidth <= innerWidth"))
                self.assertEqual(self.page.locator("body").evaluate("el => getComputedStyle(el).backgroundColor"), "rgb(251, 252, 253)")
        self.page.goto(self.url + "/index.html")
        self.page.keyboard.press("Tab")
        self.assertEqual(self.page.locator(":focus").get_attribute("href"), "#overview")
        self.page.keyboard.press("Enter")
        self.assertTrue(self.page.url.endswith("#overview"))
        self.assert_destination_in_view("overview")
        self.open_tracker()
        for navigation in ["Sections", "Reading topics and tracker"]:
            self.page.goto(self.url + "/index.html")
            self.page.get_by_role("navigation", name=navigation, exact=True).get_by_role("link", name="Project tracker", exact=False).click()
            self.page.wait_for_url(self.url + "/tracker/")
            self.page.wait_for_function("typeof drawSite === 'function'")
            self.assertEqual(self.page.locator("#knowledge").count(), 0)

    def test_F_LEARN_10_INTRO_8_reading_and_old_links_without_scripts(self):
        """F-LEARN-10, INTRO-8: explanations and fallback links do not need scripts or other hosts."""
        context = self.browser.new_context(java_script_enabled=False)
        self.addCleanup(context.close)
        context.route("**/*", self.route_request)
        page = context.new_page()
        page.goto(self.url + "/index.html")
        self.assertTrue(page.get_by_role("heading", name="Artifact Driven", exact=True).is_visible())
        for topic in ["overview", "knowledge", "change", "checks", "install"]:
            page.locator('nav[aria-label="Sections"] a[href="#' + topic + '"]').click()
            self.assertTrue(page.locator("#" + topic).is_visible())
        self.assertTrue(page.locator("#copy").is_hidden())
        page.locator("#files > summary").click()
        self.assertTrue(page.locator("#files").get_attribute("open") is not None)
        for old, target in [("how-we-work.html#words-h", "terms"),
                            ("agents.html#tools-h", "tools"), ("framework.html", "files")]:
            page.goto(self.url + "/" + old)
            page.locator('a[href="index.html#' + target + '"]').first.click()
            self.assertTrue(page.url.endswith("/index.html#" + target))

    def test_F_LEARN_8_copy_install_and_clipboard_failure(self):
        """F-LEARN-8: copyInstall returns the installer command and a visible fallback."""
        self.context.grant_permissions(["clipboard-read", "clipboard-write"])
        self.page.goto(self.url + "/index.html#install")
        self.page.locator("#copy").click()
        self.page.wait_for_function("document.getElementById('copy-status').textContent.includes('copied')")
        self.assertEqual(self.page.evaluate("navigator.clipboard.readText()"), self.page.locator("#cmd").text_content())
        self.page.evaluate("Object.defineProperty(navigator, 'clipboard', {configurable: true, value: {writeText: () => Promise.reject(new Error('Denied'))}})")
        self.page.locator("#copy").click()
        self.page.wait_for_function("getSelection().toString().includes('install.sh')")
        self.assertIn("unavailable", self.page.locator("#copy-status").inner_text())

