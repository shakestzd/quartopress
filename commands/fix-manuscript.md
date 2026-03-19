---
name: fix-manuscript
description: Detect and fix common manuscript rendering issues before building — double titles, wrong template, stale cross-refs, broken figure/table numbering, and inconsistent terminology.
arguments:
  - name: file
    description: "Target .qmd file (default: finds manuscript .qmd files in current project)"
    required: false
---

Scan a Quarto manuscript project for common rendering issues and fix them.

## Issues to Detect and Fix

### 1. Double Title
The most common rendering issue. Happens when both the YAML `title:` field AND a `#` heading or bold title exist in the body.

**Detection:** Read the master `.qmd` file (or the file that includes sections). Check if:
- YAML frontmatter has a `title:` field
- The title page section (or first section) also has a `#` heading with the same or similar text

**Fix:** Remove the `#` heading from the body and keep only the YAML `title:` field. Or if the title page has formatted author info below it, keep the body version and remove `title:` from YAML. Ask the user which approach they prefer if unclear.

### 2. Wrong or Missing Template
**Detection:** Check the YAML `reference-doc:` path. Verify the file exists at that path relative to the .qmd file.

**Fix:** If the template file doesn't exist, offer to copy the correct one from quartopress using `/set-journal`. If the path is wrong, correct it.

### 3. Outdated Journal Template
**Detection:** Compare the project's reference `.docx` template (from the `reference-doc:` YAML path) against the latest version in the quartopress plugin at `${CLAUDE_PLUGIN_ROOT}/templates/_templates/`. Compare file sizes and modification dates. If the plugin has a newer template, the project copy may be stale.

**Fix:** If the project template is older or differs from the plugin version, offer to update it by copying the latest from the plugin. Show the date difference and ask for confirmation before overwriting.

### 4. Stale Cross-References
**Detection:** Search all .qmd section files for Quarto cross-refs (`@tbl-`, `@fig-`) and verify each label is defined somewhere in the project. Also search for unresolved refs that rendered as `?@tbl-` or `?@fig-` in any .docx output.

**Fix:** List undefined references and suggest either defining the label or replacing with plain text (e.g., "Table 1").

### 5. Figure/Table Numbering Order
**Detection:** Trace the order of first reference to each table and figure through the manuscript sections (Introduction → Methods → Results → Discussion). Compare with the assigned numbers.

**Fix:** If numbering doesn't match first-citation order, report the correct mapping and offer to update the cross-reference map or plain-text references.

### 6. Duplicate Title in Included Sections
**Detection:** When using `{{< include >}}` directives, check if multiple included files have `#` level headings that would create duplicate top-level structure.

**Fix:** Ensure only the main manuscript sections (Introduction, Methods, Results, Discussion) use `#` headings. Title page content should use bold text, not headings.

### 7. Inconsistent Terminology
**Detection:** Scan all section files for mixed usage of terms that should be consistent:
- "gold standard" vs "reference standard"
- "GPT-4" vs "GPT-4.1" vs other model name variants
- Mixed British/American spelling

**Fix:** Report inconsistencies with line numbers and offer to normalize to the dominant usage.

### 8. Word Count Verification
**Detection:** Count words in the body text sections (Introduction through Conclusions), excluding markup, comments, and citations. Compare with the count stated on the title page.

**Fix:** Update the title page word count if it doesn't match. Also check abstract word count.

## Execution Protocol

1. **Find manuscript files.** If a specific file was given, use it. Otherwise, search for `.qmd` files with `format:` in YAML or `{{< include` directives.

2. **Run all 8 checks** on the identified files. Read each section file.

3. **Report findings** in a structured table:
   ```
   ## Manuscript Fix Report

   | # | Issue | File | Line | Status |
   |---|-------|------|------|--------|
   | 1 | Double title | manuscript.qmd + _title_page.qmd | 3, 5 | FIXED |
   | 2 | Missing template | manuscript.qmd | 8 | NEEDS ACTION |
   | 3 | Stale cross-ref @fig-old | _results.qmd | 22 | FIXED |
   ```

4. **Apply automatic fixes** for issues that have a clear correct resolution (double titles, stale refs, word count). For issues requiring a choice (which term to normalize to, which numbering to use), present options and ask.

5. **Suggest next steps:** After fixing, recommend running `/build-manuscript` to regenerate the output, and `/fix-ai-tells` to scan for AI writing markers.
