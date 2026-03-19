"""Scaffold a new Quarto manuscript project.

Creates the directory structure and copies templates from the plugin.

Usage:
    python scaffold_project.py /path/to/new-project --title "My Manuscript" --journal prs
"""

import argparse
import shutil
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PLUGIN_ROOT / "templates"
SCRIPTS_DIR = PLUGIN_ROOT / "scripts"


def scaffold(project_dir: Path, title: str = "Manuscript Title", journal: str = "prs"):
    """Create a new manuscript project from templates."""
    project_dir = Path(project_dir)

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
    sections_src = TEMPLATES_DIR / "_sections"
    sections_dst = project_dir / "manuscript" / "_sections"
    for f in sections_src.glob("*.qmd"):
        shutil.copy2(f, sections_dst / f.name)

    # Copy master Quarto file
    shutil.copy2(TEMPLATES_DIR / "manuscript_unified.qmd", project_dir / "manuscript" / "manuscript.qmd")

    # Copy bibliography and citation style
    shutil.copy2(TEMPLATES_DIR / "references.bib", project_dir / "manuscript" / "references.bib")
    csl_src = TEMPLATES_DIR / "american-medical-association.csl"
    if csl_src.exists():
        shutil.copy2(csl_src, project_dir / "manuscript" / "citation-style.csl")

    # Copy build scripts
    shutil.copy2(SCRIPTS_DIR / "prs_table_builder.py", project_dir / "scripts" / "prs_table_builder.py")
    shutil.copy2(TEMPLATES_DIR / "build_tables.py", project_dir / "scripts" / "build_tables.py")
    shutil.copy2(TEMPLATES_DIR / "build_upload.py", project_dir / "scripts" / "build_upload.py")

    # Copy journal Word template if available
    template_src = TEMPLATES_DIR / "_templates"
    template_dst = project_dir / "manuscript" / "_templates"
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
    print(f"\nNext steps:")
    print(f"  1. Edit manuscript/_sections/*.qmd to write your manuscript")
    print(f"  2. Add CSV data to data/tables/")
    print(f"  3. Update scripts/build_tables.py with your table definitions")
    print(f"  4. Run: cd {project_dir} && uv run python scripts/build_upload.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a manuscript project")
    parser.add_argument("project_dir", help="Path for the new project")
    parser.add_argument("--title", default="Manuscript Title", help="Manuscript title")
    parser.add_argument("--journal", default="prs", help="Target journal (prs, jpras, etc.)")
    args = parser.parse_args()
    scaffold(Path(args.project_dir), args.title, args.journal)
