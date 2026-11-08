"""Static behavior checks for the canonical guide and its old entrypoints."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[2]
TOPICS = ["overview", "knowledge", "change", "checks", "install"]
PAGES = ["index.html", "how-we-work.html", "agents.html", "framework.html"]
SOURCE = "https://github.com/hieutran21198/Artifact-Driven-Framework/blob/main/"
GOVERNANCE = "docs/governances/artifact-driven/"


class Element:
    def __init__(self, tag, attrs=()):
        self.tag = tag
        self.attrs = dict(attrs)
        self.content = []

    @property
    def raw_text(self):
        return "".join(item.raw_text if isinstance(item, Element) else item
                       for item in self.content)

    @property
    def text(self):
        return " ".join(self.raw_text.split())

    def find_all(self, tag=None, **attrs):
        found = []
        for child in self.content:
            if not isinstance(child, Element):
                continue
            if (tag is None or child.tag == tag) and all(
                    child.attrs.get(key) == value for key, value in attrs.items()):
                found.append(child)
            found.extend(child.find_all(tag, **attrs))
        return found

    @property
    def links(self):
        return [link.attrs["href"] for link in self.find_all("a") if "href" in link.attrs]


class Page(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.ids = []
        self.sections = []
        self.links = []
        self.external_scripts = []
        self.root = Element("document")
        self.stack = [self.root]
        self.feed((ROOT / filename).read_text())

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        element = Element(tag, attrs)
        self.stack[-1].content.append(element)
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input",
                       "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append(element)
        if "id" in values:
            self.ids.append(values["id"])
        if tag == "section" and "id" in values:
            self.sections.append(values["id"])
        if tag == "a" and "href" in values:
            self.links.append(values["href"])
        if tag == "script" and values.get("src"):
            self.external_scripts.append(values["src"])

    def handle_endtag(self, tag):
        if self.stack[-1].tag == tag:
            self.stack.pop()

    def handle_data(self, data):
        self.stack[-1].content.append(data)

    def by_id(self, identifier):
        matches = self.root.find_all(id=identifier)
        if len(matches) != 1:
            raise AssertionError(f"Expected one #{identifier}, found {len(matches)}")
        return matches[0]


class ContentAssertions(unittest.TestCase):
    def assertExplains(self, element, *patterns):
        """Check local propositions, not a page-wide bag of keywords."""
        for pattern in patterns:
            self.assertRegex(element.text, re.compile(pattern, re.I))

    def assertSources(self, element, *paths):
        for path in paths:
            self.assertIn(SOURCE + path, element.links)


class ReadingPages(unittest.TestCase):
    def test_SYS_8_F_LEARN_29_canonical_topics_and_tracker(self):
        """SYS-8, F-LEARN-29: one guide exposes all topics and the separate tracker."""
        page = Page("index.html")
        self.assertEqual(page.sections, TOPICS)
        for topic in TOPICS:
            self.assertIn("#" + topic, page.links)
        self.assertIn("tracker/", page.links)
        self.assertFalse(page.external_scripts)

    def test_SYS_8_F_LEARN_30_old_entrypoints_have_valid_fallbacks(self):
        """SYS-8, F-LEARN-30: old page URLs remain useful with scripts disabled."""
        expected = {
            "how-we-work.html": {"knowledge", "terms"},
            "agents.html": {"change", "limits", "install", "files", "tools"},
            "framework.html": {"files"},
        }
        for filename, topics in expected.items():
            with self.subTest(filename=filename):
                page = Page(filename)
                for topic in topics:
                    self.assertIn("index.html#" + topic, page.links)
                self.assertIn("tracker/", page.links)
                self.assertFalse(page.external_scripts)

    def test_SYS_8_all_local_links_resolve_and_ids_are_unique(self):
        """SYS-8: published reading-page links resolve to real files and anchors."""
        for filename in PAGES:
            with self.subTest(filename=filename):
                page = Page(filename)
                duplicates = [key for key, count in Counter(page.ids).items() if count > 1]
                self.assertEqual(duplicates, [])
                for href in page.links:
                    address = urlsplit(href)
                    if address.scheme or address.netloc:
                        continue
                    target = ROOT / unquote(address.path or filename)
                    if target.is_dir():
                        target /= "index.html"
                    self.assertTrue(target.is_file(), (filename, href))
                    if address.fragment:
                        self.assertIn(unquote(address.fragment), Page(target.relative_to(ROOT)).ids, (filename, href))

    def test_INTRO_2_GUIDE_2_reference_links_name_existing_repo_files(self):
        """INTRO-2, GUIDE-2: sample and reference links name real repository sources."""
        for href in Page("index.html").links:
            if href.startswith(SOURCE):
                path = unquote(urlsplit(href[len(SOURCE):]).path)
                self.assertTrue((ROOT / path).is_file(), href)


class ReadingContent(ContentAssertions):
    def setUp(self):
        self.page = Page("index.html")

    def test_INTRO_10_MTH_1_layers_keep_rules_and_dependencies_in_their_places(self):
        """INTRO-10, MTH-1: the diagram and linked example preserve layer relationships."""
        overview = self.page.by_id("overview")
        diagram = overview.find_all("figure")[0]
        path = diagram.find_all("div", **{"class": "map-path"})[0]
        self.assertEqual([node.text for node in path.find_all("strong")],
                         ["Goal", "Flow", "Artifact"])
        self.assertExplains(diagram, r"System.*shared", r"Each layer.*cite System")
        self.assertNotIn("System", path.text)
        artifact = path.find_all("div", **{"class": "map-node map-artifact"})[0]
        self.assertExplains(artifact, r"rules belong inside the artifact")
        self.assertExplains(diagram.find_all("figcaption")[0], r"arrows.*cites", r"Goal.*Flow.*Artifact")
        attachments = diagram.find_all("div", **{"class": "map-attachments"})[0]
        self.assertExplains(attachments, r"contracts and client needs.*dependencies", r"tests.*IDs")
        knowledge = self.page.by_id("knowledge")
        example = knowledge.find_all("dl")[0]
        self.assertEqual(len(example.find_all("dt")), 3)
        self.assertSources(example, *["template/docs/software-knowledges/" + path for path in
                           ["goals/borrow-a-book.md", "flows/borrow-book.md",
                            "artifacts/book/specification.md", "artifacts/member/specification.md"]])
        self.assertExplains(knowledge, r"contracts, client needs and tests.*not extra layers")

    def test_INTRO_3_F_LEARN_4_checks_distinguish_id_presence_from_runtime_evidence(self):
        """INTRO-3, F-LEARN-4: Checks states both limits of the textual scan."""
        checks = self.page.by_id("checks")
        self.assertExplains(checks, r"static checks do not run.*or prove", r"IDs appear in test files",
                            r"Neither command proves that a test passes")
        self.assertIn("python3 scripts/impact.py --coverage",
                      [code.text for code in checks.find_all("code")])
        self.assertExplains(self.page.by_id("terms"),
                            r"IDs found in test files, not.*correctness.*passing tests")

    def test_MTH_7_F_LEARN_20_tests_and_diagrams_match_their_layers(self):
        """MTH-7, F-LEARN-20: test and diagram mappings link their governing definitions."""
        checks, files = self.page.by_id("checks"), self.page.by_id("files")
        self.assertExplains(checks, r"Domain tests prove artifact rules", r"command tests prove flow scenarios",
                            r"end-to-end tests prove goal criteria")
        self.assertExplains(files, r"context diagram for System", r"flowchart for a goal",
                            r"sequence diagram.*for a flow", r"model or lifecycle diagrams for an artifact")
        self.assertSources(files, GOVERNANCE + "knowledge.md#diagrams")
        self.assertSources(checks, GOVERNANCE + "runbooks/check.md")

    def test_MTH_4_terms_explain_comparisons_without_adding_module_boundaries(self):
        """MTH-4: familiar terms map to knowledge without replacing its definitions."""
        terms = self.page.by_id("terms")
        self.assertExplains(terms, r"user story.*goal's need", r"acceptance criteria.*success criteria",
                            r"use case.*flow", r"bounded context.*domain.*artifact",
                            r"without requiring a module boundary")
        self.assertSources(terms, GOVERNANCE + "knowledge.md")

    def test_MTH_11_human_roles_keep_their_work_and_approvals(self):
        """MTH-11: work can be delegated, but approval stays with the owners."""
        change = self.page.by_id("change")
        self.assertExplains(change, r"solution architect or knowledge-writer agent changes.*BK-4",
                            r"product owner approves goal changes",
                            r"each affected service or client owner approves their share",
                            r"developers or implementer agents change.*default.*help text")
        self.assertSources(change, GOVERNANCE + "README.md#approval-of-knowledge")

    def test_AGT_11_roles_report_to_coordinator_and_preserve_review_limits(self):
        """AGT-11: handoffs, independent review, escalation and publication keep their limits."""
        limits, change = self.page.by_id("limits"), self.page.by_id("change")
        self.assertExplains(limits, r"handoff.*coordinator", r"knowledge gap.*back to the knowledge writer",
                            r"coordinator commits, pushes, opens pull requests.*only when.*owner asks",
                            r"Owners merge knowledge branches")
        self.assertExplains(change, r"reviewer who did not write the change")
        self.assertSources(limits, GOVERNANCE + "team.md#limits")

    def test_AGT_12_worked_steps_name_work_human_checks_and_applicable_guidance(self):
        """AGT-12: each worked step identifies its role, human check and source."""
        steps = self.page.by_id("change").find_all("ol")[0].find_all("li")
        expected = [
            (r"coordinator.*clarifies.*runs", r"requester confirms", "runbooks/shape.md"),
            (r"knowledge-writer.*changes", r"Owners check", "runbooks/artifact-rule.md"),
            (r"reviewer.*checks.*reports", r"Owners check", "runbooks/check.md"),
            (r"implementer agents change", r"Owners check.*test results", "workflow.md#steps"),
            (r"reviewer.*checks.*tests", r"Owners check.*evidence", "runbooks/check.md"),
        ]
        self.assertEqual(len(steps), len(expected))
        for step, (role, human, source) in zip(steps, expected):
            with self.subTest(step=step.find_all("h3")[0].text):
                self.assertExplains(step, role, human)
                self.assertSources(step, GOVERNANCE + source)
        self.assertExplains(steps[1], r"if its promises still hold, no contract edit is needed")

    def test_MTH_9_F_LEARN_26_clarification_precedes_knowledge_and_links_runbooks(self):
        """MTH-9, F-LEARN-26: current rule and unresolved choices precede edits."""
        change = self.page.by_id("change")
        steps = change.find_all("ol")[0].find_all("li")
        self.assertExplains(change, r"BK-4.*defaults to 14", r"new loans only")
        self.assertExplains(steps[0], r"clarifies the need", r"choice is still open.*rules.*before writing knowledge",
                            r"ask.*owner.*(option|choice)|ask.*(option|choice).*owner")
        self.assertSources(steps[0], GOVERNANCE + "runbooks/shape.md", GOVERNANCE + "runbooks/artifact-rule.md")
        self.assertSources(steps[1], GOVERNANCE + "runbooks/artifact-rule.md",
                           GOVERNANCE + "runbooks/contract.md", GOVERNANCE + "runbooks/client.md")

    def test_INTRO_19_tasks_link_the_resources_that_handle_them(self):
        """INTRO-19: shaping, checking and starting lead to their task resources."""
        self.assertSources(self.page.by_id("knowledge"), GOVERNANCE + "runbooks/shape.md",
                           GOVERNANCE + "runbooks/goal.md", GOVERNANCE + "runbooks/flow.md")
        self.assertSources(self.page.by_id("checks"), GOVERNANCE + "runbooks/check.md", "scripts/README.md")
        self.assertSources(self.page.by_id("install"), "install.sh", "README.md#create-a-workspace",
                           "template/README.md#start-a-new-project")

    def test_AGT_9_tool_reference_separates_workspace_instructions_and_tool_docs(self):
        """AGT-9: each tool has its own instruction entrypoint and delegation guidance."""
        tools = self.page.by_id("tools")
        entries = {item.find_all("dt")[0].text: item for item in tools.find_all("dl")[0].find_all("div")}
        self.assertEqual(set(entries), {"Claude Code", "Codex"})
        self.assertExplains(entries["Claude Code"], r"CLAUDE.md imports AGENTS.md", r"\.claude.*roles and skills",
                            r"Ask for.*agent by name")
        self.assertExplains(entries["Codex"], r"AGENTS.md.*project instructions", r"\.agents/skills.*skills",
                            r"delegating.*role file.*write limits")
        for name, host in [("Claude Code", "code.claude.com"), ("Codex", "developers.openai.com")]:
            self.assertEqual({urlsplit(link).netloc for link in entries[name].links}, {host})
            self.assertEqual({link.text for link in entries[name].find_all("a")},
                             {"project instructions", "subagents", "skills"})
        self.assertSources(tools, ".agents/agents/README.md", GOVERNANCE + "team.md")

    def test_AGT_13_F_LEARN_28_prompt_and_checklist_preserve_approval_and_evidence(self):
        """AGT-13, F-LEARN-28: supplied task and checklist keep scope and approval boundaries."""
        install = self.page.by_id("install")
        prompt = install.find_all("blockquote")[0]
        self.assertExplains(prompt, r"loan_days.*14 to 21.*new loans only", r"Confirm.*before editing",
                            r"trace BK-4.*update.*knowledge.*report.*checks.*gaps",
                            r"Do not.*commit, push or open pull requests")
        checklist = install.find_all("ul", **{"class": "review-checklist"})[0]
        self.assertSources(checklist, GOVERNANCE + "workflow.md#questions",
                           GOVERNANCE + "README.md#approval-of-knowledge", "scripts/README.md#impact",
                           GOVERNANCE + "runbooks/check.md", GOVERNANCE + "team.md#limits")
        self.assertExplains(checklist, r"knowledge comes first.*implementation waits for.*approval",
                            r"actual.*impact output.*check results.*failures.*skipped checks",
                            r"merges within.*approval limits")


if __name__ == "__main__":
    unittest.main()
