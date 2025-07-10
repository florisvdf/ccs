from typing import Dict, List
from pathlib import Path
from loguru import logger

from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


def create_table(data: Dict[str, str]) -> Table:
    table_data = [["Key", "Value"]] + [[k, v] for k, v in data.items()]
    table = Table(table_data)
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]
    )
    table.setStyle(style)
    return table


def write_tables(data: List[dict], output_path: Path):
    file_path = str(output_path / "comprehension_report.pdf")
    content = [create_table(data) for data in data]
    pdf = SimpleDocTemplate(file_path, pagesize=LETTER)
    pdf.build(content)
    logger.info(f"Wrote PDF to: {file_path}")
