# quartopress

Publication-ready tables and manuscript pipeline for Quarto-based academic projects.

## Install

```bash
# As a Python package
uv add quartopress

# As a Claude Code plugin
/plugin install github:shakestzd/quartopress
```

## Quick Start

### Scaffold a new manuscript project

```bash
quartopress-init ./my-manuscript --title "My Study" --journal prs
```

### Build tables from data

```python
from quartopress import TableSpec, build_prs_document

# From CSV
spec = TableSpec.from_csv("data.csv", label="Table 1. Demographics")

# From explicit rows
spec = TableSpec(
    label="Table 2. Results",
    headers=["Metric", "Value"],
    rows=[("Sensitivity", "99.3%"), ("Specificity", "84.4%")],
)

# Generate Word document with three-line table formatting
build_prs_document(
    title_bold="Table 1. ",
    title_text="Patient Demographics",
    tables=[spec],
    output_path="Table 1.docx",
)
```

### Build the upload package

```bash
cd my-manuscript
uv run python scripts/build_upload.py
```

## Claude Code Plugin

When installed as a plugin, quartopress provides:

| Component | Description |
|-----------|-------------|
| **ai-tell-fixer** agent | Detects and fixes AI writing markers (em-dashes, "Furthermore", "delve", etc.) |
| **manuscript-reviewer** agent | Reviews sections against journal requirements and reviewer comments |
| **table-builder** agent | Generates publication-ready Word tables from CSV data |
| **manuscript-setup** skill | Scaffolds a new Quarto manuscript project |
| **build-upload** skill | Generates complete journal upload packages |
| **journal-compliance** skill | Validates manuscript against journal requirements |
| `/build-manuscript` command | Runs the full build pipeline |

## Table Formatting

Tables use the standard three-line academic format:
- Thick top border
- Thin rule under header row
- Thick bottom border
- No internal gridlines, no shading

Supports landscape orientation, section headers within tables, and multi-table documents.
