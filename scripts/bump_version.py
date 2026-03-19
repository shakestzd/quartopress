"""Bump version across all quartopress files and optionally publish.

Usage:
    python scripts/bump_version.py 0.3.1
    python scripts/bump_version.py 0.3.1 --publish
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

VERSION_FILES = [
    ("pyproject.toml", r'version = "[^"]+"', 'version = "{version}"'),
    ("quartopress/__init__.py", r'__version__ = "[^"]+"', '__version__ = "{version}"'),
    (".claude-plugin/plugin.json", r'"version": "[^"]+"', '"version": "{version}"'),
    (".claude-plugin/marketplace.json", r'"version": "[^"]+"', '"version": "{version}"'),
]


def bump(version: str, publish: bool = False):
    print(f"Bumping to v{version}\n")

    for rel_path, pattern, replacement in VERSION_FILES:
        fpath = PROJECT_ROOT / rel_path
        if not fpath.exists():
            print(f"  SKIP {rel_path} (not found)")
            continue

        content = fpath.read_text()
        new_content = re.sub(pattern, replacement.format(version=version), content)

        if content == new_content:
            print(f"  SKIP {rel_path} (already {version})")
        else:
            fpath.write_text(new_content)
            count = len(re.findall(pattern, content))
            print(f"  DONE {rel_path} ({count} occurrence{'s' if count > 1 else ''})")

    print(f"\nAll files updated to v{version}")

    # Git commit + push
    subprocess.run(["git", "add", "-A"], cwd=PROJECT_ROOT)
    subprocess.run(
        ["git", "commit", "-m", f"Bump version to {version}"],
        cwd=PROJECT_ROOT,
    )
    subprocess.run(["git", "push"], cwd=PROJECT_ROOT)
    print("Pushed to GitHub")

    if publish:
        # Build + publish to PyPI
        dist = PROJECT_ROOT / "dist"
        if dist.exists():
            import shutil
            shutil.rmtree(dist)

        subprocess.run(["uv", "build"], cwd=PROJECT_ROOT)

        # Load token from .env
        env_file = PROJECT_ROOT / ".env"
        token = None
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("PYPI_API_KEY="):
                    token = line.split("=", 1)[1].strip().strip('"').strip("'")

        if token:
            subprocess.run(
                ["uv", "publish", "--token", token],
                cwd=PROJECT_ROOT,
            )
            print(f"Published v{version} to PyPI")
        else:
            print("No PYPI_API_KEY in .env — skipping PyPI publish")


def main():
    parser = argparse.ArgumentParser(description="Bump quartopress version")
    parser.add_argument("version", help="New version (e.g., 0.3.1)")
    parser.add_argument("--publish", action="store_true", help="Also publish to PyPI")
    args = parser.parse_args()
    bump(args.version, args.publish)


if __name__ == "__main__":
    main()
