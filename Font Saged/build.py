"""Rebuild Saged 1.402 with Diana's І, Ї and updated Д artwork."""
from pathlib import Path
from xml.etree import ElementTree as ET
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.svgLib.path import parse_path

HERE = Path(__file__).resolve().parent
font = TTFont(HERE / 'Sources/Latest letters/base-v1.399.ttf')
cmap = font.getBestCmap()
for char, filename, bottom in [('І', 'І - Ukrainian I.svg', 110), ('Ї', 'Ї - Yi.svg', 132), ('Д', 'Д - De.svg', 110)]:
    root = ET.parse(HERE / 'Sources/Latest letters' / filename).getroot()
    scale = 735 / 110  # Same 110-unit letter body in both supplied frames.
    pen = TTGlyphPen(None)
    transformed = TransformPen(Cu2QuPen(pen, max_err=0.7, reverse_direction=True),
                               (scale, 0, 0, -scale, 64, bottom * scale))
    for path in root.findall('{http://www.w3.org/2000/svg}path'):
        parse_path(path.attrib['d'], transformed)
    glyph = pen.glyph()
    glyph.recalcBounds(font['glyf'])
    width = float(root.attrib['viewBox'].split()[2])
    for name in {cmap[ord(char)], cmap[ord(char.lower())]}:
        font['glyf'][name] = glyph
        font['hmtx'][name] = (round(width * scale + 128), glyph.xMin)

for record in font['name'].names:
    value = record.toUnicode().replace('1.399', '1.402').replace('1399', '1402')
    record.string = value.encode(record.getEncoding())
font['head'].fontRevision = 1.402
font.recalcTimestamp = False
font.save(HERE / 'Font files/saged-v1.402.ttf')
font.flavor = 'woff'
font.save(HERE / 'Font files/saged-display-cyrillic-v1.402.woff')
print('Built Saged 1.402 TTF and WOFF')
