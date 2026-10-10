from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "CAPGEMINI_INTERVIEW_QUESTION_BANK.md"
OUTPUT = ROOT / "CAPGEMINI_INTERVIEW_QUESTION_BANK.pdf"


def inline(markdown: str) -> str:
    """Convert the small Markdown subset used by the guide to ReportLab markup."""
    text = html.escape(markdown.strip())
    text = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        r'<link href="\2" color="#1857a4">\1</link>',
        text,
    )
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", r'<font face="Courier">\1</font>', text)
    return text


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#d1d5db"))
    canvas.line(doc.leftMargin, 1.25 * cm, A4[0] - doc.rightMargin, 1.25 * cm)
    canvas.setFillColor(colors.HexColor("#475569"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(doc.leftMargin, 0.85 * cm, "Capgemini Interview Preparation — Visvatharsan Saravanan")
    canvas.drawRightString(A4[0] - doc.rightMargin, 0.85 * cm, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf() -> None:
    styles = getSampleStyleSheet()
    normal = ParagraphStyle(
        "GuideBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.1,
        leading=12.3,
        spaceAfter=4,
        textColor=colors.HexColor("#172033"),
    )
    bullet = ParagraphStyle(
        "GuideBullet",
        parent=normal,
        leftIndent=14,
        firstLineIndent=-9,
        spaceAfter=2.5,
    )
    quote = ParagraphStyle(
        "GuideQuote",
        parent=normal,
        leftIndent=13,
        rightIndent=8,
        borderColor=colors.HexColor("#93c5fd"),
        borderWidth=1,
        borderPadding=6,
        backColor=colors.HexColor("#eff6ff"),
        spaceBefore=2,
        spaceAfter=7,
    )
    title = ParagraphStyle(
        "GuideTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=27,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#1e3a8a"),
        spaceAfter=10,
    )
    subtitle = ParagraphStyle(
        "GuideSubtitle",
        parent=normal,
        alignment=TA_CENTER,
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=12,
    )
    h1 = ParagraphStyle(
        "GuideH1",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=13,
        spaceAfter=7,
        keepWithNext=True,
    )
    h2 = ParagraphStyle(
        "GuideH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12.4,
        leading=16,
        textColor=colors.HexColor("#1e40af"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True,
    )
    h3 = ParagraphStyle(
        "GuideH3",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True,
    )
    code = ParagraphStyle(
        "GuideCode",
        fontName="Courier",
        fontSize=7.2,
        leading=9.2,
        leftIndent=5,
        rightIndent=5,
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=3,
        spaceAfter=7,
    )
    table_cell = ParagraphStyle(
        "GuideTableCell",
        parent=normal,
        fontSize=7.3,
        leading=9.2,
        spaceAfter=0,
    )
    table_header = ParagraphStyle(
        "GuideTableHeader",
        parent=table_cell,
        fontName="Helvetica-Bold",
        textColor=colors.white,
    )

    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=1.35 * cm,
        leftMargin=1.35 * cm,
        topMargin=1.35 * cm,
        bottomMargin=1.65 * cm,
        title="Capgemini Interview Question Bank",
        author="Visvatharsan Saravanan",
    )

    story = [
        Spacer(1, 3.2 * cm),
        Paragraph("Capgemini Interview Question Bank", title),
        Paragraph("CV-tailored preparation for Visvatharsan Saravanan", subtitle),
        HRFlowable(width="62%", thickness=1.2, color=colors.HexColor("#2563eb"), hAlign="CENTER"),
        Spacer(1, 0.7 * cm),
        Paragraph(
            "Projects • Java & MySQL • JDBC & OOP • GCP & Gemini API • Docker • SQL • HR practice",
            subtitle,
        ),
        Spacer(1, 1.5 * cm),
        Paragraph(
            "Use this guide to rehearse answers aloud. Replace every [personal detail] with your real implementation before the interview.",
            quote,
        ),
        PageBreak(),
    ]

    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    in_code = False
    code_lines: list[str] = []
    table_lines: list[str] = []

    def flush_table() -> None:
        nonlocal table_lines
        if not table_lines:
            return
        rows: list[list[Paragraph]] = []
        for raw in table_lines:
            cells = [cell.strip() for cell in raw.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
                continue
            style = table_header if not rows else table_cell
            rows.append([Paragraph(inline(cell), style) for cell in cells])
        if rows:
            width = A4[0] - doc.leftMargin - doc.rightMargin
            columns = max(len(row) for row in rows)
            col_widths = [width / columns] * columns
            table = Table(rows, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e40af")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ]))
            story.extend([table, Spacer(1, 7)])
        table_lines = []

    for raw in lines:
        stripped = raw.strip()

        if stripped.startswith("```"):
            flush_table()
            if in_code:
                story.append(Preformatted("\n".join(code_lines), code))
                code_lines = []
            in_code = not in_code
            continue
        if in_code:
            code_lines.append(raw)
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines.append(raw)
            continue
        flush_table()
        if not stripped:
            story.append(Spacer(1, 3))
        elif stripped == "---":
            story.extend([Spacer(1, 5), HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#cbd5e1")), Spacer(1, 5)])
        elif stripped.startswith("# "):
            story.append(Paragraph(inline(stripped[2:]), h1))
        elif stripped.startswith("## "):
            story.append(Paragraph(inline(stripped[3:]), h2))
        elif stripped.startswith("### "):
            story.append(Paragraph(inline(stripped[4:]), h3))
        elif stripped.startswith("> "):
            story.append(Paragraph(inline(stripped[2:]), quote))
        elif re.match(r"^[-*] \[[ xX]\] ", stripped):
            story.append(Paragraph("☐ " + inline(stripped[6:]), bullet))
        elif re.match(r"^[-*] ", stripped):
            story.append(Paragraph("• " + inline(stripped[2:]), bullet))
        elif re.match(r"^\d+\. ", stripped):
            story.append(Paragraph(inline(stripped), bullet))
        else:
            story.append(Paragraph(inline(stripped), normal))

    flush_table()
    if code_lines:
        story.append(Preformatted("\n".join(code_lines), code))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
