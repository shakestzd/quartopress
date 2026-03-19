---
name: fix-ai-tells
description: Scan and fix AI writing tells in manuscript .qmd files. Runs the ai-tell-fixer agent in parallel on all section files.
arguments:
  - name: files
    description: "Specific files to scan (default: all .qmd files in the project)"
    required: false
---

Scan and fix AI writing tells in this manuscript project.

1. If specific files were provided as arguments, use those. Otherwise, find all `.qmd` files in the project that contain manuscript prose (look for files with sections like Introduction, Methods, Results, Discussion, Abstract, or any `.qmd` in a `_sections/` directory).

2. Launch a `quartopress:ai-tell-fixer` agent on each file **in parallel** (one agent per file). If the `quartopress:ai-tell-fixer` agent is not available, use `general-purpose` agents with the following instructions for each file:

   - Scan for overused AI words: delve, intricate, meticulous, commendable, showcase, pivotal, realm, tapestry, underscore, noteworthy, invaluable, versatile, holistic, landscape, crucial, cutting-edge, novel (when meaning "new"), innovative, unprecedented, robust, comprehensive, streamline, facilitate, harness, leverage, elevate, utilize
   - Scan for generic AI transitions: Furthermore, Moreover, Additionally, Notably, Importantly, Interestingly, It is important to note, It is worth noting
   - Scan for em-dashes (--- or —) used as parenthetical separators — replace with commas, semicolons, colons, or parentheses depending on context
   - Flag structural patterns: 3+ consecutive "This..." sentences, uniform paragraph lengths, excessive hedging
   - Replace each tell with a natural alternative, preserving meaning exactly
   - Skip YAML frontmatter, code blocks, HTML comments
   - Report changes made in a structured table

3. After all agents complete, present a combined summary showing total tells found and fixed across all files.
