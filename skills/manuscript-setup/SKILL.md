# Manuscript Setup

Scaffold a new or augment an existing Quarto-based manuscript project for journal submission.

## When to Use

Use this skill when:
- Starting a new manuscript project from scratch
- Adding quartopress build pipeline to an existing project
- Converting an existing draft into a structured Quarto project
- Setting up table/figure generation in a project that already has .qmd files

## New vs. Existing Projects

**New project:** `quartopress-init ./my-manuscript --title "My Study"`
Creates the full directory structure, all section templates, build scripts, and bibliography files.

**Existing project:** `quartopress-init . `
Detects what's already present (.qmd sections, .bib files, build scripts, table builder) and adds only what's missing. Never overwrites existing files unless `--force` is used.

**Force mode:** `quartopress-init . --force`
Overwrites all files with fresh templates. Use when you want to reset to defaults.

## Project Structure

The scaffold creates:

```
manuscript-project/
├── manuscript/
│   ├── manuscript.qmd              # Master Quarto file (includes all sections)
│   ├── _sections/
│   │   ├── _title_page.qmd         # Title, authors, affiliations
│   │   ├── _abstract.qmd           # Structured abstract
│   │   ├── _introduction.qmd       # Background, gap, objectives
│   │   ├── _methods.qmd            # Study design, measures, analysis
│   │   ├── _results.qmd            # Primary and secondary outcomes
│   │   └── _discussion.qmd         # Interpretation, limitations, conclusions
│   ├── _templates/
│   │   └── journal-reference.docx  # Journal Word template (controls formatting)
│   ├── references.bib              # BibTeX bibliography
│   └── citation-style.csl          # Citation style (AMA, Vancouver, etc.)
├── data/
│   ├── tables/                     # CSV source files for tables
│   └── figures/                    # Data files for figure generation
├── scripts/
│   ├── prs_table_builder.py        # Reusable table generation module
│   ├── build_tables.py             # Declarative table definitions
│   └── build_upload.py             # Master build script
├── output/                         # Generated submission files
│   ├── Manuscript.docx
│   ├── Table 1.docx
│   ├── Figure 1.tiff
│   └── ...
└── review/                         # Reviewer feedback and responses
    ├── reviewer_comments.md
    ├── response_to_reviewers.md
    └── compliance_checklist.md
```

## Setup Steps

### 1. Create the project directory
```bash
mkdir -p manuscript-project/{manuscript/_sections,manuscript/_templates,data/tables,data/figures,scripts,output,review}
```

### 2. Copy core modules
Copy `prs_table_builder.py` from the plugin's `scripts/` directory into `scripts/`.

### 3. Create the master Quarto file
Use the template from `${CLAUDE_PLUGIN_ROOT}/templates/manuscript_unified.qmd`. Configure:
- `reference-doc` pointing to your journal's Word template
- `bibliography` pointing to your `.bib` file
- `csl` pointing to your citation style

### 4. Create section files
Each section is a separate `.qmd` file. Start with the templates from `${CLAUDE_PLUGIN_ROOT}/templates/_sections/`.

### 5. Set up the build pipeline
Copy `build_tables.py` and `build_upload.py` templates from the plugin. Customize:
- Table definitions (from your CSV data)
- Figure copy paths
- Cross-reference map (table/figure label to number)
- Figure legends and SDC legends

### 6. Configure for your journal
Update word limits, abstract structure, figure requirements, and reference format based on your target journal's author guidelines.

## Journal Configurations

| Journal | Word Limit | Abstract | Figures | Tables | Reference Style |
|---------|-----------|----------|---------|--------|-----------------|
| PRS | 3,000 (+500 ext) | 250, structured | 300 DPI TIFF | Separate .docx | AMA |
| JPRAS | 4,000 | 250, structured | 300 DPI TIFF/EPS | Separate .docx | Vancouver |
| Ann Plast Surg | 3,000 | 200, unstructured | 300 DPI TIFF | Embedded | AMA |

## Key Principles

1. **Sections as separate files** — enables parallel editing and targeted AI review
2. **Tables from data** — CSV is the source of truth; `.docx` is generated output
3. **Figures from code** — data-driven, reproducible, never hardcoded
4. **One build command** — `uv run python scripts/build_upload.py` generates everything
5. **Cross-references resolved at build time** — Quarto handles citations; build script handles table/figure numbering
