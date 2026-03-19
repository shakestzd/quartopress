"""Declarative table definitions for manuscript submission.

Define each table as a TableSpec (pure data). The build functions
generate PRS-formatted .docx files using prs_table_builder.

Usage:
    uv run python scripts/build_tables.py
"""

from pathlib import Path
from prs_table_builder import TableSpec, build_prs_document

TABLES_DIR = Path("data/tables")
OUTPUT_DIR = Path("output")


# =============================================================================
# Table 1: Example — from CSV
# =============================================================================

def build_table_1():
    spec = TableSpec.from_csv(
        csv_path=TABLES_DIR / "table1_data.csv",
        label="Table 1. [Table Title]",
        col1_bold=True,
    )
    build_prs_document(
        title_bold="Table 1. ",
        title_text="[Description of the table]",
        tables=[spec],
        output_path=OUTPUT_DIR / "Table 1.docx",
    )


# =============================================================================
# Table 2: Example — from explicit rows
# =============================================================================

TABLE_2 = TableSpec(
    label="Table 2. [Table Title]",
    headers=["Parameter", "Group A", "Group B"],
    col_widths=(2.0, 2.25, 2.25),
    col1_bold=True,
    rows=[
        ("Age (years)", "45.2 +/- 12.3", "43.8 +/- 11.7"),
        ("BMI (kg/m2)", "24.1 +/- 3.2", "25.3 +/- 4.1"),
        # Add more rows...
    ],
)


def build_table_2():
    build_prs_document(
        title_bold="Table 2. ",
        title_text="[Description of the table]",
        tables=[TABLE_2],
        output_path=OUTPUT_DIR / "Table 2.docx",
    )


# =============================================================================
# Table 3: Example — landscape with section headers
# =============================================================================

TABLE_3 = TableSpec(
    label="Table 3. [Table Title]",
    headers=["Category", "Group A", "Group B", "Group C"],
    col_widths=(1.5, 2.5, 2.5, 2.5),
    col1_bold=True,
    section_headers={
        0: "PRIMARY OUTCOMES",
        3: "SECONDARY OUTCOMES",
    },
    rows=[
        # PRIMARY OUTCOMES (indices 0-2)
        ("Outcome 1", "Value A", "Value B", "Value C"),
        ("Outcome 2", "Value A", "Value B", "Value C"),
        ("Outcome 3", "Value A", "Value B", "Value C"),
        # SECONDARY OUTCOMES (indices 3+)
        ("Outcome 4", "Value A", "Value B", "Value C"),
        ("Outcome 5", "Value A", "Value B", "Value C"),
    ],
)


def build_table_3():
    build_prs_document(
        title_bold="Table 3. ",
        title_text="[Description of the table]",
        tables=[TABLE_3],
        output_path=OUTPUT_DIR / "Table 3.docx",
        landscape=True,
    )


# =============================================================================
# Build All
# =============================================================================

if __name__ == "__main__":
    OUTPUT_DIR.mkdir(exist_ok=True)
    build_table_1()
    build_table_2()
    build_table_3()
