"""Scaffold a new Quarto manuscript project.

Creates the directory structure and copies templates from the package.

Usage:
    quartopress-init ./my-manuscript --title "My Study" --journal prs
"""

from __future__ import annotations

import argparse
import importlib.resources
import shutil
from pathlib import Path


def _package_root() -> Path:
    """Resolve the installed package root (parent of quartopress/)."""
    return Path(__file__).resolve().parent.parent


def scaffold(project_dir: str | Path, title: str = "Manuscript Title", journal: str = "prs"):
    """Create a new manuscript project from templates.

    Args:
        project_dir: Path for the new project directory.
        title: Manuscript title (inserted into title page template).
        journal: Target journal identifier (prs, jpras, etc.).
    """
    project_dir = Path(project_dir)
    pkg_root = _package_root()
    templates_dir = pkg_root / "templates"

    # Create directory structure
    dirs = [
        "manuscript/_sections",
        "manuscript/_templates",
        "data/tables",
        "data/figures",
        "scripts",
        "output",
        "review",
    ]
    for d in dirs:
        (project_dir / d).mkdir(parents=True, exist_ok=True)

    # Copy section templates
    sections_src = templates_dir / "_sections"
    sections_dst = project_dir / "manuscript" / "_sections"
    if sections_src.exists():
        for f in sections_src.glob("*.qmd"):
            shutil.copy2(f, sections_dst / f.name)

    # Copy master Quarto file
    qmd_src = templates_dir / "manuscript_unified.qmd"
    if qmd_src.exists():
        shutil.copy2(qmd_src, project_dir / "manuscript" / "manuscript.qmd")

    # Copy bibliography and citation style
    bib_src = templates_dir / "references.bib"
    if bib_src.exists():
        shutil.copy2(bib_src, project_dir / "manuscript" / "references.bib")
    csl_src = templates_dir / "american-medical-association.csl"
    if csl_src.exists():
        shutil.copy2(csl_src, project_dir / "manuscript" / "citation-style.csl")

    # Copy build script templates
    for name in ["build_tables.py", "build_upload.py"]:
        src = templates_dir / name
        if src.exists():
            shutil.copy2(src, project_dir / "scripts" / name)

    # Copy journal Word template if available
    template_src = templates_dir / "_templates"
    template_dst = project_dir / "manuscript" / "_templates"
    if template_src.exists():
        for f in template_src.glob("*"):
            shutil.copy2(f, template_dst / f.name)

    # Update title in title page
    title_page = sections_dst / "_title_page.qmd"
    if title_page.exists():
        content = title_page.read_text()
        content = content.replace("[Manuscript Title: Include Study Design and Population]", title)
        title_page.write_text(content)

    print(f"Scaffolded manuscript project at: {project_dir}")
    print(f"  Journal: {journal.upper()}")
    print(f"  Title: {title}")
    print()
    print("Next steps:")
    print(f"  1. Edit manuscript/_sections/*.qmd to write your manuscript")
    print(f"  2. Add CSV data to data/tables/")
    print(f"  3. Update scripts/build_tables.py with your table definitions")
    print(f"  4. Run: cd {project_dir} && uv run python scripts/build_upload.py")


def main():
    """CLI entry point for quartopress-init."""
    parser = argparse.ArgumentParser(
        prog="quartopress-init",
        description="Scaffold a new Quarto manuscript project for journal submission.",
    )
    parser.add_argument("project_dir", help="Path for the new project")
    parser.add_argument("--title", default="Manuscript Title", help="Manuscript title")
    parser.add_argument("--journal", default="prs", help="Target journal (prs, jpras, etc.)")
    args = parser.parse_args()
    scaffold(args.project_dir, args.title, args.journal)


if __name__ == "__main__":
    main()
