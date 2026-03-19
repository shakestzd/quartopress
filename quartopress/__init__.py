"""quartopress — Quarto-based academic manuscript pipeline.

Build publication-ready tables, detect AI writing tells,
and generate journal upload packages.
"""

from quartopress.table_builder import (
    TableSpec,
    build_prs_table,
    build_prs_document,
)

__version__ = "0.3.0"

__all__ = [
    "TableSpec",
    "build_prs_table",
    "build_prs_document",
]
