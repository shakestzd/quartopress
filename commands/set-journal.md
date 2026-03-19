---
name: set-journal
description: Configure a manuscript .qmd file to use a specific journal template (PRS, JPRAS, or Annals).
arguments:
  - name: journal
    description: "Journal name: prs, jpras, or annals"
    required: true
  - name: file
    description: "Target .qmd file (default: finds manuscript .qmd in current project)"
    required: false
---

Configure a manuscript for a specific journal's formatting template.

## Available Journals

| Journal | Template | Reference Style | Abstract | Word Limit |
|---------|----------|----------------|----------|------------|
| `prs` | prs-reference.docx | AMA | 250, structured | 3,000 (+500 ext) |
| `jpras` | jpras-reference.docx | Vancouver | 250, unstructured | No strict limit |
| `annals` | annals-reference.docx | AMA | 200, unstructured | 3,000 |

## Steps

1. **Identify the target .qmd file.** If a file argument was provided, use it. Otherwise, search the project for the main manuscript `.qmd` file (look for files containing `{{< include` or a Quarto `format:` block).

2. **Copy the journal template** from the quartopress plugin's `templates/_templates/` directory into the project's manuscript `_templates/` directory. The plugin templates are at `${CLAUDE_PLUGIN_ROOT}/templates/_templates/`. If the project doesn't have a `_templates/` directory, create one next to the .qmd file.

3. **Update the .qmd YAML frontmatter** to point to the correct template:
   - For `prs`: set `reference-doc: _templates/prs-reference.docx`
   - For `jpras`: set `reference-doc: _templates/jpras-reference.docx`
   - For `annals`: set `reference-doc: _templates/annals-reference.docx`

4. **Update the citation style** if the project has a `.csl` file reference in the YAML:
   - For `prs` and `annals`: use AMA style (`american-medical-association.csl`)
   - For `jpras`: use Vancouver style. If a Vancouver `.csl` isn't present, copy one from the plugin or advise the user to download it.

5. **Report the changes** made to the file and remind the user of the journal's key requirements (word limit, abstract format, figure specs).
