"""Scaffold or augment a Quarto manuscript project.

Works for both new projects and existing ones:
- New project: creates full directory structure + all templates
- Existing project: detects what's present, adds only what's missing, never overwrites

Usage:
    quartopress-init ./my-manuscript --title "My Study" --journal prs
    quartopress-init .  # Add quartopress to current project
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def _package_root() -> Path:
    """Resolve the installed package root (parent of quartopress/)."""
    return Path(__file__).resolve().parent.parent


def _copy_if_missing(src: Path, dst: Path) -> bool:
    """Copy a file only if the destination doesn't already exist.

    Returns True if copied, False if skipped.
    """
    if dst.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def _find_existing_layout(project_dir: Path) -> dict:
    """Detect existing manuscript structure in a project.

    Returns a dict describing what was found.
    """
    found = {
        "qmd_sections": [],
        "quarto_master": None,
        "bib_file": None,
        "csl_file": None,
        "build_scripts": [],
        "table_builder": False,
    }

    # Search for .qmd section files anywhere in the project
    for qmd in project_dir.rglob("*.qmd"):
        name = qmd.name.lower()
        rel = qmd.relative_to(project_dir)
        if any(s in name for s in ["abstract", "introduction", "methods", "results", "discussion", "title"]):
            found["qmd_sections"].append(rel)
        if "unified" in name or (name == "manuscript.qmd"):
            found["quarto_master"] = rel

    # Search for bibliography
    for bib in project_dir.rglob("*.bib"):
        found["bib_file"] = bib.relative_to(project_dir)
        break

    # Search for citation style
    for csl in project_dir.rglob("*.csl"):
        found["csl_file"] = csl.relative_to(project_dir)
        break

    # Search for build scripts
    for py in project_dir.rglob("build_*.py"):
        found["build_scripts"].append(py.relative_to(project_dir))

    # Search for table builder
    for py in project_dir.rglob("*table_builder*"):
        found["table_builder"] = True
        break

    return found


def scaffold(
    project_dir: str | Path,
    title: str = "Manuscript Title",
    journal: str = "prs",
    force: bool = False,
):
    """Create or augment a manuscript project from templates.

    For new projects: creates full structure.
    For existing projects: adds only missing components, never overwrites.

    Args:
        project_dir: Path for the project directory.
        title: Manuscript title (inserted into title page template).
        journal: Target journal identifier (prs, jpras, etc.).
        force: If True, overwrite existing files (default: skip).
    """
    project_dir = Path(project_dir).resolve()
    pkg_root = _package_root()
    templates_dir = pkg_root / "templates"

    is_existing = project_dir.exists() and any(project_dir.iterdir())

    if is_existing:
        print(f"Existing project detected: {project_dir}")
        existing = _find_existing_layout(project_dir)
        if existing["qmd_sections"]:
            print(f"  Found {len(existing['qmd_sections'])} .qmd sections")
        if existing["quarto_master"]:
            print(f"  Found master file: {existing['quarto_master']}")
        if existing["bib_file"]:
            print(f"  Found bibliography: {existing['bib_file']}")
        if existing["table_builder"]:
            print(f"  Found table builder module")
        print()
    else:
        existing = _find_existing_layout(project_dir)  # empty dict

    copy_fn = shutil.copy2 if force else _copy_if_missing
    added = []
    skipped = []

    # --- Create directories (safe — mkdir -p never fails on existing) ---
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

    # --- Section templates (only if no existing sections found) ---
    sections_src = templates_dir / "_sections"
    sections_dst = project_dir / "manuscript" / "_sections"
    if sections_src.exists():
        for f in sections_src.glob("*.qmd"):
            dst = sections_dst / f.name
            if _copy_if_missing(f, dst) if not force else (shutil.copy2(f, dst) or True):
                added.append(f"manuscript/_sections/{f.name}")
            else:
                skipped.append(f"manuscript/_sections/{f.name}")

    # --- Master Quarto file ---
    if not existing["quarto_master"]:
        qmd_src = templates_dir / "manuscript_unified.qmd"
        dst = project_dir / "manuscript" / "manuscript.qmd"
        if qmd_src.exists() and _copy_if_missing(qmd_src, dst):
            added.append("manuscript/manuscript.qmd")
    else:
        skipped.append(f"master .qmd (found {existing['quarto_master']})")

    # --- Bibliography ---
    if not existing["bib_file"]:
        bib_src = templates_dir / "references.bib"
        dst = project_dir / "manuscript" / "references.bib"
        if bib_src.exists() and _copy_if_missing(bib_src, dst):
            added.append("manuscript/references.bib")
    else:
        skipped.append(f".bib (found {existing['bib_file']})")

    # --- Citation style ---
    if not existing["csl_file"]:
        csl_src = templates_dir / "american-medical-association.csl"
        dst = project_dir / "manuscript" / "citation-style.csl"
        if csl_src.exists() and _copy_if_missing(csl_src, dst):
            added.append("manuscript/citation-style.csl")
    else:
        skipped.append(f".csl (found {existing['csl_file']})")

    # --- Build scripts (always add if missing — these are the core value) ---
    for name in ["build_tables.py", "build_upload.py"]:
        src = templates_dir / name
        dst = project_dir / "scripts" / name
        if src.exists() and _copy_if_missing(src, dst):
            added.append(f"scripts/{name}")
        elif dst.exists():
            skipped.append(f"scripts/{name}")

    # --- Table builder module (core — always add if missing) ---
    if not existing["table_builder"]:
        tb_src = pkg_root / "quartopress" / "table_builder.py"
        dst = project_dir / "scripts" / "table_builder.py"
        if tb_src.exists() and _copy_if_missing(tb_src, dst):
            added.append("scripts/table_builder.py")
    else:
        skipped.append("table_builder (already present)")

    # --- Journal Word template ---
    template_src = templates_dir / "_templates"
    template_dst = project_dir / "manuscript" / "_templates"
    if template_src.exists():
        for f in template_src.glob("*"):
            dst = template_dst / f.name
            if _copy_if_missing(f, dst):
                added.append(f"manuscript/_templates/{f.name}")

    # --- Update title in title page (only for new projects) ---
    if not is_existing and title != "Manuscript Title":
        title_page = sections_dst / "_title_page.qmd"
        if title_page.exists():
            content = title_page.read_text()
            content = content.replace("[Manuscript Title: Include Study Design and Population]", title)
            title_page.write_text(content)

    # --- Report ---
    print(f"quartopress setup complete: {project_dir}")
    print(f"  Journal: {journal.upper()}")
    if title != "Manuscript Title":
        print(f"  Title: {title}")
    print()

    if added:
        print(f"Added ({len(added)}):")
        for f in added:
            print(f"  + {f}")

    if skipped:
        print(f"\nSkipped ({len(skipped)}) — already exist:")
        for f in skipped:
            print(f"  . {f}")

    print()
    print("Next steps:")
    if is_existing:
        print("  1. Review scripts/build_tables.py and update table definitions for your data")
        print("  2. Review scripts/build_upload.py and update cross-ref map + figure legends")
        print("  3. Run: uv run python scripts/build_upload.py")
    else:
        print("  1. Edit manuscript/_sections/*.qmd to write your manuscript")
        print("  2. Add CSV data to data/tables/")
        print("  3. Update scripts/build_tables.py with your table definitions")
        print(f"  4. Run: cd {project_dir} && uv run python scripts/build_upload.py")


def main():
    """CLI entry point for quartopress-init."""
    parser = argparse.ArgumentParser(
        prog="quartopress-init",
        description="Scaffold or augment a Quarto manuscript project for journal submission.",
    )
    parser.add_argument(
        "project_dir",
        help="Path for the project (use '.' for current directory)",
    )
    parser.add_argument("--title", default="Manuscript Title", help="Manuscript title")
    parser.add_argument("--journal", default="prs", help="Target journal (prs, jpras, etc.)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()
    scaffold(args.project_dir, args.title, args.journal, args.force)


if __name__ == "__main__":
    main()
