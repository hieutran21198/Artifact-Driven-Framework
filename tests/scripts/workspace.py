"""A throwaway workspace to run the scripts in."""

from pathlib import Path
import json
import subprocess
import sys
import tempfile

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"


class Workspace:
    def __init__(self, config=None, raw=None):
        self._dir = tempfile.TemporaryDirectory()
        self.root = Path(self._dir.name)
        text = raw if raw is not None else json.dumps(config or {}, indent=2)
        self.write("artifact-driven.json", text)
        self.write("README.md", "# Workspace\n")

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def git(self):
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "add", "-A"], cwd=self.root, check=True)

    def run(self, script, *args):
        return subprocess.run([sys.executable, str(SCRIPTS / script), *args], cwd=self.root,
                              capture_output=True, text=True)

    def close(self):
        self._dir.cleanup()
