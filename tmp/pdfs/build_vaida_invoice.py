from pathlib import Path

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


ROOT = Path("/Users/diana/Documents/saged.club")
OUTPUT = ROOT / "finances/invoices/SAGED-2026-001-Vaida-Alijeva.pdf"
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

W, H = A4
PAPER = HexColor("#FAF7F2")
SAND = HexColor("#F1E9DA")
INK = HexColor("#2A2520")
MUTED = HexColor("#6B5F54")
ORANGE = HexColor("#FF7A23")
LINE = HexColor("#E1D6C5")
WHITE = HexColor("#FFFFFF")

def text(c, x, y, value, size=9, color=INK, font="Helvetica", align="left"):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == "right":
        c.drawRightString(x, y, value)
    else:
        c.drawString(x, y, value)


def label(c, x, y, value):
    text(c, x, y, value.upper(), 6.7, MUTED, "Helvetica-Bold")


c = canvas.Canvas(str(OUTPUT), pagesize=A4)
c.setTitle("Invoice SAGED-2026-001 - Vaida Alijeva")
c.setAuthor("Saged.club")
c.setFillColor(PAPER)
c.rect(0, 0, W, H, fill=1, stroke=0)

# Brand gesture: a cropped orange ring in the upper-right corner.
c.setStrokeColor(ORANGE)
c.setLineWidth(52)
c.circle(W + 30, H + 8, 122, fill=0, stroke=1)

margin = 52

# Header
text(c, margin, H - 60, "S A G E D", 11, ORANGE, "Helvetica-Bold")
text(c, margin, H - 75, "C L U B", 11, ORANGE, "Helvetica-Bold")
text(c, margin, H - 127, "INVOICE", 38, ORANGE, "Helvetica-Bold")
text(c, margin, H - 145, "SAGED-2026-001", 7, MUTED, "Helvetica-Bold")

issuer_x = W - margin
text(c, issuer_x, H - 58, "Diana Voroneca", 8.5, INK, "Helvetica-Bold", "right")
text(c, issuer_x, H - 72, "NIE Z1981847B", 8, MUTED, "Helvetica", "right")
text(c, issuer_x, H - 86, "C/ de les Cuines, 8", 8, MUTED, "Helvetica", "right")
text(c, issuer_x, H - 100, "Ciutat Vella, 46001 Valencia", 8, MUTED, "Helvetica", "right")
text(c, issuer_x, H - 114, "Spain", 8, MUTED, "Helvetica", "right")

# Client and dates card
card_x, card_y, card_w, card_h = margin, H - 300, W - 2 * margin, 104
c.setFillColor(SAND)
c.roundRect(card_x, card_y, card_w, card_h, 13, fill=1, stroke=0)

label(c, card_x + 20, card_y + 78, "Billed to")
text(c, card_x + 20, card_y + 52, "Vaida Alijeva", 18, INK, "Helvetica-Bold")
text(c, card_x + 20, card_y + 35, "Autonoma - NIE Y9308589C", 8.5, INK)
text(c, card_x + 20, card_y + 21, "Calle 233/35, La Canyada, Valencia, Spain", 8.5, MUTED)

facts_x = card_x + 290
label(c, facts_x, card_y + 78, "Invoice date")
text(c, facts_x, card_y + 61, "24 September 2026", 8.5, INK, "Helvetica-Bold")
label(c, facts_x, card_y + 36, "Currency")
text(c, facts_x, card_y + 19, "EUR", 8.5, INK, "Helvetica-Bold")

facts2_x = card_x + 400
label(c, facts2_x, card_y + 78, "Due date")
text(c, facts2_x, card_y + 61, "9 October 2026", 8.5, INK, "Helvetica-Bold")
label(c, facts2_x, card_y + 36, "Status")
text(c, facts2_x, card_y + 19, "Payment due", 8.5, INK, "Helvetica-Bold")

# Line items
table_top = card_y - 49
cols = [margin, margin + 350, margin + 420, W - margin]
label(c, cols[0], table_top, "Description")
label(c, cols[1], table_top, "Qty")
text(c, cols[2], table_top, "RATE", 6.7, MUTED, "Helvetica-Bold", "right")
text(c, cols[3], table_top, "AMOUNT", 6.7, MUTED, "Helvetica-Bold", "right")
c.setStrokeColor(INK)
c.setLineWidth(0.7)
c.line(margin, table_top - 11, W - margin, table_top - 11)

row_y = table_top - 36
text(c, cols[0], row_y, "Event management services", 9.5, INK, "Helvetica-Bold")
text(c, cols[0], row_y - 16, "Professional services provided by Saged.club", 7.8, MUTED)
text(c, cols[1], row_y, "1", 9, INK)
text(c, cols[2], row_y, "EUR 350.00", 9, INK, "Helvetica", "right")
text(c, cols[3], row_y, "EUR 350.00", 9, INK, "Helvetica", "right")
c.setStrokeColor(LINE)
c.line(margin, row_y - 30, W - margin, row_y - 30)

# Totals
totals_x = W - margin - 220
totals_right = W - margin
total_y = row_y - 78
text(c, totals_x, total_y, "Subtotal", 9, MUTED)
text(c, totals_right, total_y, "EUR 350.00", 9, INK, "Helvetica-Bold", "right")
text(c, totals_x, total_y - 23, "IVA (21%)", 9, MUTED)
text(c, totals_right, total_y - 23, "+ EUR 73.50", 9, INK, "Helvetica-Bold", "right")
text(c, totals_x, total_y - 46, "IRPF withholding (15%)", 9, MUTED)
text(c, totals_right, total_y - 46, "- EUR 52.50", 9, INK, "Helvetica-Bold", "right")

grand_y = total_y - 97
c.setFillColor(ORANGE)
c.roundRect(totals_x - 12, grand_y, totals_right - totals_x + 12, 43, 11, fill=1, stroke=0)
text(c, totals_x, grand_y + 15, "Total due", 14, WHITE, "Helvetica-Bold")
text(c, totals_right - 12, grand_y + 15, "EUR 371.00", 15, WHITE, "Helvetica-Bold", "right")

# Payment details
payment_y = 175
c.setStrokeColor(LINE)
c.setLineWidth(0.8)
c.line(margin, payment_y + 58, W - margin, payment_y + 58)
label(c, margin, payment_y + 35, "Payment details")
text(c, margin, payment_y + 16, "Bank", 8, INK, "Helvetica-Bold")
text(c, margin + 42, payment_y + 16, "Banco Santander", 8, INK)
text(c, margin, payment_y + 1, "IBAN", 8, INK, "Helvetica-Bold")
text(c, margin + 42, payment_y + 1, "ES51 0049 3328 8221 1409 0997", 8, INK)
text(c, margin, payment_y - 14, "BIC", 8, INK, "Helvetica-Bold")
text(c, margin + 42, payment_y - 14, "BSCHESMMXXX", 8, INK)

contact_x = margin + 285
label(c, contact_x, payment_y + 35, "Contact")
text(c, contact_x, payment_y + 16, "hello@saged.club", 8, INK)
text(c, contact_x, payment_y + 1, "+34 605 54 33 00", 8, INK)
text(c, contact_x, payment_y - 14, "saged.club", 8, INK)

# Footer
text(c, margin, 62, "THANK YOU", 17, INK, "Helvetica-Bold")
text(c, margin, 46, "Please include SAGED-2026-001 with the payment.", 7.5, MUTED)
text(c, W - margin, 46, "Valencia  |  saged.club", 7.5, MUTED, "Helvetica", "right")

c.showPage()
c.save()
print(OUTPUT)
