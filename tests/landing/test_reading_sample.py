"""Verify the guide's concrete examples against a locally installed workspace."""

import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote, urlsplit

from tests.landing.test_reading_pages import ContentAssertions, GOVERNANCE, Page, ROOT, SOURCE


class ReadingSample(ContentAssertions):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.workspace = Path(cls.tmp.name) / "sample"
        subprocess.run(["sh", str(ROOT / "install.sh"), str(cls.workspace)], check=True,
                       env={**os.environ, "AD_SOURCE": str(ROOT)}, capture_output=True, text=True)
        subprocess.run(["git", "init", "-q"], cwd=cls.workspace, check=True, capture_output=True)
        cls.page = Page("index.html")

    def impact(self, *args):
        result = subprocess.run([sys.executable, "scripts/impact.py", *args], cwd=self.workspace,
                                capture_output=True, text=True, check=True)
        return {name: set(values.split(", ")) for name, values in
                (line.split(": ", 1) for line in result.stdout.splitlines() if ": " in line)}

    def test_INTRO_2_F_LEARN_5_sample_sources_and_citations_exist_after_install(self):
        """INTRO-2, F-LEARN-5: linked sample files, named IDs and citation edges survive install."""
        sample_prefix = SOURCE + "template/"
        sources = [unquote(urlsplit(link[len(sample_prefix):]).path)
                   for link in self.page.links if link.startswith(sample_prefix)]
        self.assertTrue(sources)
        for path in sources:
            with self.subTest(path=path):
                self.assertEqual((self.workspace / path).read_text(), (ROOT / "template" / path).read_text())
        sample = self.workspace / "docs/software-knowledges"
        rows = {}
        for path in sample.rglob("*.md"):
            for line in path.read_text().splitlines():
                match = re.match(r"\| ((?:G-BORROW|F-BORROW|BK|MBR)-\d+) \|", line)
                if match:
                    rows[match.group(1)] = line
        named = set(re.findall(r"\b(?:G-BORROW|BK|MBR)-\d+\b", self.page.root.find_all("main")[0].text))
        self.assertTrue(named)
        self.assertLessEqual(named, rows.keys())
        self.assertIn("F-BORROW-1", rows["G-BORROW-1"])
        self.assertIn("BK-3", rows["F-BORROW-1"])
        flow = (sample / "flows/borrow-book.md").read_text()
        self.assertIn("borrowBook", flow)
        self.assertIn("MBR-2, MBR-3 and MBR-4", flow)
        self.assertIn("artifacts/book/README.md", flow)
        self.assertIn("artifacts/member/README.md", flow)

    def test_AGT_1_GUIDE_5_F_LEARN_22_file_tree_and_agent_roles_match_the_installed_workspace(self):
        """AGT-1, GUIDE-5, F-LEARN-22: advertised paths and Claude links exist in the installer output."""
        files = self.page.by_id("files")
        tree = files.find_all("pre")[0].raw_text
        parents, advertised = [], set()
        for line in tree.splitlines():
            match = re.match(r"(.*?)[├└]── (\S+)", line)
            if not match:
                continue
            depth, name = len(match.group(1)) // 4, match.group(2).rstrip("/")
            parents[depth:] = [name]
            relative = Path(*parents)
            advertised.add(relative.as_posix())
            self.assertTrue((self.workspace / relative).exists(), relative)
        self.assertLessEqual({"AGENTS.md", "CLAUDE.md", ".agents/agents", ".agents/skills", ".claude",
                              "docs/governances", "scripts", "services", "apps", "e2e"}, advertised)
        self.assertEqual((self.workspace / "CLAUDE.md").read_text().strip(), "@AGENTS.md")
        for name in ["agents", "skills"]:
            link = self.workspace / ".claude" / name
            self.assertTrue(link.is_symlink())
            self.assertEqual(link.resolve(), self.workspace / ".agents" / name)
        tools = self.page.by_id("tools")
        for role in (self.workspace / ".agents/agents").glob("*.md"):
            if role.name != "README.md":
                self.assertIn(role.stem.replace("-", " "), tools.text)
        self.assertSources(files, GOVERNANCE + "README.md", GOVERNANCE + "runbooks/README.md",
                           GOVERNANCE + "knowledge.md#artifact-files", ".agents/skills/README.md")

    def test_INTRO_4_F_LEARN_15_F_LEARN_24_worked_change_agrees_with_real_sample_impact(self):
        """INTRO-4, F-LEARN-15, F-LEARN-24: the displayed impact command reaches its cited dependencies."""
        change = self.page.by_id("change")
        self.assertIn("python3 scripts/impact.py BK-4", [node.text for node in change.find_all("code")])
        self.assertExplains(change, r"14 to 21 days.*new loans only", r"keeps existing due times")
        sample = self.workspace / "docs/software-knowledges"
        rule = next(line for line in (sample / "artifacts/book/specification.md").read_text().splitlines()
                    if line.startswith("| BK-4 |"))
        self.assertRegex(rule, r"loan_days.*default 14.*new loans only")
        impact = self.impact("BK-4")
        self.assertIn("F-BORROW-1", impact["Flow scenarios"])
        self.assertIn("borrowBook", impact["Operations"])
        self.assertIn("artifacts/book/openapi.yaml#Book", impact["Contract schemas"])
        clients = {"artifacts/book/mobile.md", "artifacts/book/web.md"}
        self.assertLessEqual(clients, impact["Pages"])
        self.assertIn("artifacts/book/mobile.md#BK-4", impact["Client needs"])
        self.assertIn("artifacts/book/web.md#getBook", impact["Client needs"])
        self.assertSources(change, *["template/docs/software-knowledges/" + path for path in clients])
        self.assertExplains(change, r"mobile app's help text.*default loan period.*update",
                            r"web client.*returned due_at", r"rather than assuming.*web needs no work")
        self.assertRegex(" ".join((sample / "artifacts/book/mobile.md").read_text().split()),
                         r"help text states the loan period.*default of `loan_days`")
        self.assertIn("`due_at` is present", (sample / "artifacts/book/web.md").read_text())
