---
name: build-manuscript
description: Build the complete journal upload package (manuscript, tables, figures) from source files.
---

Build the journal upload package for this manuscript project.

1. Find the project's `build_upload.py` script (in `scripts/` or project root)
2. Run it with `uv run python` to generate all output files
3. Report the contents of the output directory with file sizes
4. Run a quick word count on the manuscript sections to verify the title page count

If `build_upload.py` doesn't exist, guide the user through setting up the build pipeline using the `build-upload` skill.
