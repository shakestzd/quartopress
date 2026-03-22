# CLAUDE.md — quartopress

## Project Overview

quartopress is a dual-purpose project: a **Python package** (PyPI) and a **Claude Code plugin** for building Quarto-based academic manuscripts for journal submission.

**Repo:** https://github.com/shakestzd/quartopress
**PyPI:** https://pypi.org/project/quartopress/

## Architecture

```
quartopress/
├── .claude-plugin/
│   ├── plugin.json              # Claude plugin manifest
│   └── marketplace.json         # GitHub marketplace registration
├── quartopress/                 # Python package
│   ├── __init__.py              # Exports: TableSpec, build_prs_table, build_prs_document
│   ├── table_builder.py         # Core module — three-line table generation for Word
│   └── scaffold.py              # Project scaffolding (quartopress-init CLI)
├── agents/
│   ├── ai-tell-fixer.md         # Detects/fixes AI writing markers in .qmd files
│   ├── manuscript-reviewer.md   # Reviews sections against journal/reviewer requirements
│   └── table-builder.md         # Builds Word tables from CSV/data using prs_table_builder
├── skills/
│   ├── manuscript-setup/SKILL.md    # Scaffold new or augment existing projects
│   ├── build-upload/SKILL.md        # Generate complete journal upload packages
│   └── journal-compliance/SKILL.md  # Validate against journal requirements (PRS, JPRAS, Annals)
├── commands/
│   ├── build-manuscript.md      # /build-manuscript — run full build pipeline
│   ├── fix-manuscript.md        # /fix-manuscript — detect/fix 8 common rendering issues
│   ├── fix-ai-tells.md          # /fix-ai-tells — scan/fix AI writing markers in parallel
│   └── set-journal.md           # /set-journal <prs|jpras|annals> — configure journal template
├── templates/
│   ├── manuscript_unified.qmd   # Master Quarto template with section includes
│   ├── _sections/*.qmd          # Starter section templates (title, abstract, intro, etc.)
│   ├── _templates/
│   │   ├── prs-reference.docx   # PRS journal Word template
│   │   ├── jpras-reference.docx # JPRAS journal Word template
│   │   └── annals-reference.docx # Annals of Plastic Surgery Word template
│   ├── build_tables.py          # Template for declarative table definitions
│   ├── build_upload.py          # Template for master build script
│   ├── references.bib           # Empty starter bibliography
│   └── american-medical-association.csl
├── scripts/
│   └── bump_version.py          # Version bump across all 4 version files + publish
├── pyproject.toml               # Python package config (hatch build system)
└── .env                         # PYPI_API_KEY (gitignored)
```

## Development Rules

### Version Management
**All four files must stay in sync:**
- `pyproject.toml` → `version = "X.Y.Z"`
- `quartopress/__init__.py` → `__version__ = "X.Y.Z"`
- `.claude-plugin/plugin.json` → `"version": "X.Y.Z"`
- `.claude-plugin/marketplace.json` → `"version": "X.Y.Z"` (appears twice)

**Use the bump script:**
```bash
# Bump, commit, push, build, publish to PyPI
python scripts/bump_version.py 0.6.0 --publish

# Bump without publishing
python scripts/bump_version.py 0.6.0
```

### Agent Development
- Agents are single `.md` files in `agents/` with YAML frontmatter
- Validate with: `bash /Users/shakes/.claude/plugins/cache/claude-plugins-official/plugin-dev/bd041495bd2a/skills/agent-development/scripts/validate-agent.sh agents/<name>.md`
- Valid colors: blue, cyan, green, yellow, magenta, red
- System prompt max: 10,000 characters
- Description must start with "Use this agent when"

### Template Development
- Word reference templates (`.docx`) are generated via python-docx, not manually edited
- All styles must use: Times New Roman, black (`RGBColor(0,0,0)`), no colored accents
- Title, Heading 1-4, Subtitle, Normal all must be explicitly styled
- Test templates by rendering a `.qmd` with `reference-doc:` pointing to the template

### Key Design Decisions
- **Tables use three-line format** (top thick, header underline, bottom thick, no internal borders) — standard for medical journals
- **Title page uses bold text, not `#` heading** — prevents double title when Quarto YAML `title:` is also set
- **Scaffold never overwrites existing files** (unless `--force`) — safe for existing projects
- **Cross-references resolved at build time** by the build script's `CROSS_REF_MAP`, not by Quarto (since tables/figures are separate files)

## Testing

No test suite yet (known gap). Key areas to test:
- `quartopress-init` on new vs existing projects
- `--force` flag overwrites all files
- `--title` substitution works in both new and existing projects
- `TableSpec.from_csv()` → `.docx` output
- Template styles render correctly in Word
- Agent validation passes for all agents

## Common Tasks

### Add a new journal template
1. Create the `.docx` in `templates/_templates/` using python-docx (see existing templates for pattern)
2. Add journal specs to `skills/journal-compliance/SKILL.md`
3. Update `/set-journal` command to include the new journal name
4. Bump version and publish

### Add a new slash command
1. Create `.md` file in `commands/` with YAML frontmatter (name, description, arguments)
2. Body contains instructions for Claude to execute
3. Bump version and publish

### Add a new agent
1. Create `.md` file in `agents/` with YAML frontmatter
2. Validate with the validation script
3. Bump version and publish

## Origin

This plugin was built during a PRS manuscript revision session for "From Months to Minutes: Evaluating an AI-Assisted Approach to Systematic Reviews in Plastic Surgery." The production-tested infrastructure (table builder, build pipeline, AI-tell detection) was extracted and generalized into this reusable package.
