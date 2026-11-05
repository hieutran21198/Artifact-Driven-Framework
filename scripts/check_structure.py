"""Check that each repository content directory has a README.md."""

from pathlib import Path
import subprocess
import sys

from project import ROOT


def main():
    root = ROOT
    try:
        result = subprocess.run(
            [
                "git", "-C", str(root), "ls-files", "--cached", "--others",
                "--exclude-standard", "-z",
            ],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError):
        print("Cannot read the repository file list with Git.", file=sys.stderr)
        return 2

    directories = {Path(".")}
    for name in result.stdout.split(b"\0"):
        if name:
            relative = Path(name.decode(sys.getfilesystemencoding(), "surrogateescape"))
            directories.update(relative.parents)

    missing = sorted(
        str(directory / "README.md")
        for directory in directories
        if not (root / directory / "README.md").is_file()
    )
    if missing:
        for path in missing:
            print(f"Missing: {path}", file=sys.stderr)
        return 1

    print(f"README coverage passed: {len(directories)} directories.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
