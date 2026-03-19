"""Master build script for journal upload package.

Generates all submission files from Quarto sources and data files.

Usage:
    uv run python scripts/build_upload.py
"""

import re
import shutil
import subprocess
from pathlib import Path

# Paths — adjust these for your project
PROJECT_DIR = Path(__file__).resolve().parent.parent
MANUSCRIPT_DIR = PROJECT_DIR / "manuscript"
OUTPUT_DIR = PROJECT_DIR / "output"
FIGURES_DIR = PROJECT_DIR / "data" / "figures"

# Cross-reference map: Quarto label -> plain text
# Update this to match your table/figure numbering
CROSS_REF_MAP = {
    "@tbl-demographics": "Table 1",
    "@tbl-results": "Table 2",
    "@fig-workflow": "Figure 1",
    "@fig-outcomes": "Figure 2",
}

# Manuscript sections to include (in order)
SECTIONS = [
    "_title_page.qmd",
    "_abstract.qmd",
    "_introduction.qmd",
    "_methods.qmd",
    "_results.qmd",
    "_discussion.qmd",
]

# Figure file map: source filename -> submission filename
FIGURE_MAP = {
    "workflow.tiff": "Figure 1.tiff",
    "outcomes.tiff": "Figure 2.tiff",
}

# Figure legends (appended after References)
FIGURE_LEGENDS = """

# FIGURE LEGENDS

**Figure 1.** [Description of Figure 1.]

**Figure 2.** [Description of Figure 2.]

# SUPPLEMENTAL DIGITAL CONTENT LEGENDS

**Supplementary Table S1.** [Description of SDC item.]
"""


def setup_output_dir():
    OUTPUT_DIR.mkdir(exist_ok=True)


def build_manuscript():
    """Assemble sections, replace cross-refs, render with Quarto."""
    sections_dir = MANUSCRIPT_DIR / "_sections"
    revised_qmd = MANUSCRIPT_DIR / "manuscript_revised.qmd"

    # Assemble sections
    parts = []
    for fname in SECTIONS:
        section_path = sections_dir / fname
        if section_path.exists():
            parts.append(section_path.read_text())
            parts.append("\n\n{{< pagebreak >}}\n\n")

    body = "\n".join(parts)

    # Replace Quarto cross-refs with plain text
    for ref, plain in CROSS_REF_MAP.items():
        body = body.replace(ref, plain)

    # Remove content-visible blocks (table/figure placeholders for docx)
    body = re.sub(
        r'::: \{\.content-visible when-format="docx"\}\n.*?\n:::', "", body, flags=re.DOTALL
    )

    # Remove HTML comments
    body = re.sub(r'<!--.*?-->', '', body)

    # Build full .qmd
    frontmatter = """\
---
format:
  docx:
    reference-doc: _templates/journal-reference.docx
    number-sections: false
    toc: false
bibliography: references.bib
csl: citation-style.csl
---
"""

    refs_and_legends = "\n\n# References\n\n::: {#refs}\n:::\n\n" + FIGURE_LEGENDS

    revised_qmd.write_text(frontmatter + body + refs_and_legends)

    # Render
    print("Rendering manuscript...")
    result = subprocess.run(
        ["quarto", "render", str(revised_qmd), "--to", "docx"],
        cwd=str(MANUSCRIPT_DIR),
        capture_output=True, text=True, timeout=300,
    )

    if result.returncode != 0:
        print(f"Quarto render failed:\n{result.stderr[:500]}")
        return False

    rendered = MANUSCRIPT_DIR / "manuscript_revised.docx"
    if rendered.exists():
        shutil.copy2(rendered, OUTPUT_DIR / "Manuscript.docx")
        print("  Manuscript.docx")
        return True
    return False


def build_all_tables():
    """Build tables using the project's build_tables.py."""
    import os
    scripts_dir = PROJECT_DIR / "scripts"
    result = subprocess.run(
        ["python", str(scripts_dir / "build_tables.py")],
        cwd=str(scripts_dir),
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print(result.stdout)
    else:
        print(f"Table build failed:\n{result.stderr}")


def copy_figures():
    """Copy figure TIFFs to output with submission naming."""
    for src_name, dst_name in FIGURE_MAP.items():
        src = FIGURES_DIR / src_name
        if src.exists():
            shutil.copy2(src, OUTPUT_DIR / dst_name)
            print(f"  {dst_name}")
        else:
            print(f"  WARNING: {src_name} not found")


def main():
    print("=" * 60)
    print("Building Upload Package")
    print("=" * 60)

    setup_output_dir()

    print("\n--- Manuscript ---")
    build_manuscript()

    print("\n--- Tables ---")
    build_all_tables()

    print("\n--- Figures ---")
    copy_figures()

    print("\n" + "=" * 60)
    print("Upload package:")
    print("=" * 60)
    for f in sorted(OUTPUT_DIR.iterdir()):
        if f.name.startswith("~$"):
            continue
        size = f.stat().st_size
        size_str = f"{size / 1024:.0f} KB" if size > 1024 else f"{size} B"
        print(f"  {f.name:40s} {size_str:>10s}")


if __name__ == "__main__":
    main()
