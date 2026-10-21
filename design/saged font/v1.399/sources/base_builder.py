#!/usr/bin/env python3
"""Build Saged Display Cyrillic from original modular vector construction."""

from math import cos, pi, sin
from pathlib import Path
from fontTools.fontBuilder import FontBuilder
from fontTools.feaLib.builder import addOpenTypeFeaturesFromString
from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.reverseContourPen import reversedContour
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.svgLib.path import parse_path
from fontTools.ttLib import TTFont
from xml.etree import ElementTree as ET

UPM = 1000
BASE = 40
CAP = 735
STROKE = 118
SIDE = 45
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parents[1] / "outputs" / "fonts" / "saged-display-cyrillic"
FULL_SET_DIR = ROOT / "src" / "glyph-sources" / "batch-v1.381-originals"
COSTA_SOURCE = ROOT.parents[1] / "brand-system" / "design-system" / "public" / "fonts" / "costa-light.otf"
GE_SOURCE = ROOT / "src" / "glyph-sources" / "ge-user.svg"
BE_SOURCE = ROOT / "src" / "glyph-sources" / "be-user-v4.svg"
DE_SOURCE = ROOT / "src" / "glyph-sources" / "de-user-v3.svg"
ZHE_SOURCE = ROOT / "src" / "glyph-sources" / "zhe-user-v2.svg"
EURO_SOURCE = ROOT / "src" / "glyph-sources" / "euro-user-v4.svg"
SHORT_I_SOURCE = ROOT / "src" / "glyph-sources" / "short-i-user-v2.svg"
UKRAINIAN_I_SOURCE = ROOT / "src" / "glyph-sources" / "ukrainian-i-user-v1.svg"
EL_SOURCE = ROOT / "src" / "glyph-sources" / "el-user.svg"
EM_SOURCE = ROOT / "src" / "glyph-sources" / "em-user-v2.svg"
PE_SOURCE = ROOT / "src" / "glyph-sources" / "pe-user-v2.svg"
U_SOURCE = ROOT / "src" / "glyph-sources" / "u-user-v1.svg"
EF_SOURCE = ROOT / "src" / "glyph-sources" / "ef-user-vector-v11.svg"
SHA_SOURCE = ROOT / "src" / "glyph-sources" / "sha-user-v2.svg"
SHCHA_SOURCE = ROOT / "src" / "glyph-sources" / "shcha-user-v2.svg"
HARD_SIGN_SOURCE = ROOT / "src" / "glyph-sources" / "hard-sign-user-v3.svg"
TSE_SOURCE = ROOT / "src" / "glyph-sources" / "tse-user-v2.svg"
E_REVERSED_SOURCE = ROOT / "src" / "glyph-sources" / "e-reversed-user.svg"
YERY_SOURCE = ROOT / "src" / "glyph-sources" / "yery-user-v2.svg"
SOFT_SIGN_SOURCE = ROOT / "src" / "glyph-sources" / "soft-sign-user-v2.svg"
YU_SOURCE = ROOT / "src" / "glyph-sources" / "yu-user.svg"
SUPPLIED_RUSSIAN_SOURCES = {
    "А": "letter-0410-А.svg", "Б": "letter-0411-Б-open.svg", "В": "letter-0412-В.svg",
    "Г": "Vector-4.svg", "Д": "Vector-14.svg", "Е": "letter-0415-Е.svg",
    "Ё": "letter-0401-Ё.svg", "Ж": "Vector-15.svg", "З": "letter-0417-З.svg",
    "И": "letter-0418-И.svg", "Й": "Vector.svg", "К": "Vector-1.svg",
    "Л": "Vector-8.svg", "М": "M-final.svg", "Н": "letter-041d-Н.svg",
    "О": "letter-041e-О.svg", "П": "Vector-3.svg", "Р": "letter-0420-Р.svg",
    "С": "letter-0421-С.svg", "Т": "letter-0422-Т.svg", "У": "letter-0423-У.svg",
    "Ф": "Vector-13.svg", "Х": "letter-0425-Х.svg", "Ц": "Vector-12.svg",
    "Ч": "letter-0427-Ч.svg", "Ш": "Vector-10.svg", "Щ": "Vector-11.svg",
    "Ъ": "Vector-6.svg", "Ы": "letter-042b-Ы.svg", "Ь": "letter-042c-Ь.svg",
    "Э": "Vector-5.svg", "Ю": "Vector-2.svg", "Я": "letter-042f-Я.svg",
}
COSTA_VISUAL_EQUIVALENTS = {
    "А": "A", "В": "B", "Е": "E", "З": "three", "К": "K", "М": "M", "Н": "H",
    "О": "O", "Р": "P", "С": "C", "Т": "T", "У": "Y", "Х": "X", "Ч": "four",
}
COSTA_PUNCTUATION = {
    "period": "period",
    "comma": "comma",
    "colon": "colon",
    "exclam": "exclam",
    "question": "question",
    "quotedbl": "quotedbl",
    "quotesingle": "quotesingle",
    "ampersand": "ampersand",
}


def reference_glyph(latin):
    """Convert a supplied Latin reference glyph to quadratic outlines."""
    source = TTFont(COSTA_SOURCE)
    glyph_set = source.getGlyphSet()
    pen = TTGlyphPen(None)
    glyph_set[latin].draw(Cu2QuPen(pen, max_err=1.0, reverse_direction=True))
    advance, _ = source["hmtx"].metrics[latin]
    return pen.glyph(), advance


def reference_glyph_with_metrics(latin):
    """Copy a Costa glyph together with its original advance and sidebearing."""
    source = TTFont(COSTA_SOURCE)
    glyph_set = source.getGlyphSet()
    pen = TTGlyphPen(None)
    glyph_set[latin].draw(Cu2QuPen(pen, max_err=1.0, reverse_direction=True))
    advance, lsb = source["hmtx"].metrics[latin]
    return pen.glyph(), advance, lsb


def user_svg_glyph(path, source_height, source_width, side_padding=0, target_height=CAP,
                   advance_adjust=0):
    """Convert supplied SVG paths into a font glyph at cap height."""
    pen = TTGlyphPen(None)
    scale = target_height / source_height
    quadratic = Cu2QuPen(pen, max_err=1.0, reverse_direction=True)
    transformed = TransformPen(quadratic, (scale, 0, 0, -scale, side_padding, target_height))
    root = ET.parse(path).getroot()
    for element in root.findall("{http://www.w3.org/2000/svg}path"):
        parse_path(element.attrib["d"], transformed)
    return pen.glyph(), round(source_width * scale + side_padding * 2 + advance_adjust)


def user_svg_glyph_reversing(path, source_height, source_width, reverse_contours,
                             side_padding=0, target_height=CAP, advance_adjust=0):
    """Convert SVG artwork while correcting explicitly named contour windings."""
    recording = RecordingPen()
    root = ET.parse(path).getroot()
    for element in root.findall("{http://www.w3.org/2000/svg}path"):
        parse_path(element.attrib["d"], recording)

    contours, current = [], []
    for command in recording.value:
        if command[0] == "moveTo" and current:
            contours.append(current)
            current = []
        current.append(command)
        if command[0] in ("closePath", "endPath"):
            contours.append(current)
            current = []
    if current:
        contours.append(current)

    pen = TTGlyphPen(None)
    scale = target_height / source_height
    quadratic = Cu2QuPen(pen, max_err=1.0, reverse_direction=True)
    transformed = TransformPen(quadratic, (scale, 0, 0, -scale, side_padding, target_height))
    for index, contour_commands in enumerate(contours):
        commands = list(reversedContour(list(contour_commands))) if index in reverse_contours else contour_commands
        for operator, operands in commands:
            getattr(transformed, operator)(*operands)
    return pen.glyph(), round(source_width * scale + side_padding * 2 + advance_adjust)


def supplied_svg_glyph(path, body_top=0, body_bottom=110, side_padding=64,
                       tiny_area=1.0):
    """Import a supplied grid-based SVG, dropping accidental zero-area scraps."""
    root = ET.parse(path).getroot()
    viewbox = [float(value) for value in root.attrib["viewBox"].split()]
    source_width = viewbox[2]
    contours = []
    for element in root.findall("{http://www.w3.org/2000/svg}path"):
        recording = RecordingPen()
        parse_path(element.attrib["d"], recording)
        current = []
        for command in recording.value:
            if command[0] == "moveTo" and current:
                contours.append(current); current = []
            current.append(command)
            if command[0] in ("closePath", "endPath"):
                contours.append(current); current = []
        if current:
            contours.append(current)

    def control_area(commands):
        points = []
        for operator, operands in commands:
            if operator in ("moveTo", "lineTo"):
                points.extend(operands)
            elif operator in ("curveTo", "qCurveTo"):
                points.extend(point for point in operands if point is not None)
        if len(points) < 3:
            return 0
        closed = points + [points[0]]
        return abs(sum(a[0] * b[1] - b[0] * a[1]
                       for a, b in zip(closed, closed[1:]))) / 2

    pen = TTGlyphPen(None)
    scale = CAP / (body_bottom - body_top)
    quadratic = Cu2QuPen(pen, max_err=1.0, reverse_direction=True)
    transformed = TransformPen(
        quadratic, (scale, 0, 0, -scale, side_padding, body_bottom * scale)
    )
    for commands in contours:
        if control_area(commands) < tiny_area:
            continue
        for operator, operands in commands:
            getattr(transformed, operator)(*operands)
    return pen.glyph(), round(source_width * scale + side_padding * 2)


def short_i_svg_glyph(path, side_padding=64):
    """Import Diana's Й while keeping its body at cap height and breve unclipped."""
    root = ET.parse(path).getroot()
    paths = root.findall("{http://www.w3.org/2000/svg}path")
    if len(paths) != 2:
        raise ValueError(f"Expected body and breve paths in {path}")

    pen = TTGlyphPen(None)
    body_top = 35.527825
    body_bottom = 141.3495542668947
    body_scale = CAP / (body_bottom - body_top)
    body = Cu2QuPen(pen, max_err=1.0, reverse_direction=True)
    parse_path(paths[0].attrib["d"], TransformPen(
        body, (body_scale, 0, 0, -body_scale, side_padding, body_bottom * body_scale + 2)
    ))

    # The supplied breve is taller than the previous font metrics permit.
    # Preserve its horizontal drawing while fitting it optically into 755–919.
    mark_scale_y = (919 - 755) / 25
    mark = Cu2QuPen(pen, max_err=1.0, reverse_direction=True)
    parse_path(paths[1].attrib["d"], TransformPen(
        mark, (body_scale, 0, 0, -mark_scale_y, side_padding, 919)
    ))
    return pen.glyph(), round(104.78 * body_scale + side_padding * 2)


def derived_ukrainian_letter(ch):
    """Extend the supplied Russian system to Ukrainian-specific capitals."""
    if ch == "І":
        return user_svg_glyph(UKRAINIAN_I_SOURCE, 110, 31, side_padding=64)
    if ch == "Ї":
        body, advance = user_svg_glyph(UKRAINIAN_I_SOURCE, 110, 31, side_padding=64)
        pen = TTGlyphPen(None)
        body.draw(pen, None)
        center = advance / 2
        oval(pen, center - 100, 810, center - 40, 870)
        oval(pen, center + 40, 810, center + 100, 870)
        return pen.glyph(), advance
    if ch == "Є":
        source, advance = supplied_svg_glyph(FULL_SET_DIR / "Vector-5.svg")
        pen = TTGlyphPen(None)
        source.draw(TransformPen(pen, (-1, 0, 0, 1, advance, 0)), None)
        return pen.glyph(), advance
    if ch == "Ґ":
        source, advance = supplied_svg_glyph(FULL_SET_DIR / "Vector-4.svg")
        coordinates, _, _ = source.getCoordinates(None)
        x_max = max(point[0] for point in coordinates)
        pen = TTGlyphPen(None)
        source.draw(pen, None)
        stroke(pen, x_max - 59, CAP - 59, x_max - 59, 810, w=118)
        return pen.glyph(), advance
    raise ValueError(ch)


def reference_e_dieresis():
    """Build Cyrillic Ё from the supplied rounded Latin E plus original dots."""
    source = TTFont(COSTA_SOURCE)
    glyph_set = source.getGlyphSet()
    pen = TTGlyphPen(None)
    glyph_set["E"].draw(Cu2QuPen(pen, max_err=1.0, reverse_direction=True))
    advance, _ = source["hmtx"].metrics["E"]
    dot = 92
    center = advance / 2
    oval(pen, center - 122 - dot / 2, 790, center - 122 + dot / 2, 790 + dot)
    oval(pen, center + 122 - dot / 2, 790, center + 122 + dot / 2, 790 + dot)
    return pen.glyph(), advance


def reference_flipped_n(with_breve=False):
    """Build Cyrillic И/Й by horizontally mirroring the supplied Latin N."""
    source = TTFont(COSTA_SOURCE)
    glyph_set = source.getGlyphSet()
    advance, _ = source["hmtx"].metrics["N"]
    pen = TTGlyphPen(None)
    quadratic = Cu2QuPen(pen, max_err=1.0, reverse_direction=True)
    glyph_set["N"].draw(TransformPen(quadratic, (-1, 0, 0, 1, advance, 0)))
    if with_breve:
        arc(pen, advance / 2, 835, 120, 68, pi, 2 * pi, w=58, steps=14)
    return pen.glyph(), advance


def reference_upside_down_m():
    """Build Cyrillic Ш by vertically mirroring the supplied Latin M."""
    source = TTFont(COSTA_SOURCE)
    glyph_set = source.getGlyphSet()
    advance, _ = source["hmtx"].metrics["M"]
    pen = TTGlyphPen(None)
    quadratic = Cu2QuPen(pen, max_err=1.0, reverse_direction=True)
    glyph_set["M"].draw(TransformPen(quadratic, (1, 0, 0, -1, 0, CAP)))
    return pen.glyph(), advance


def reference_flipped_r():
    """Build Cyrillic Я by horizontally mirroring the supplied Latin R."""
    source = TTFont(COSTA_SOURCE)
    glyph_set = source.getGlyphSet()
    advance, _ = source["hmtx"].metrics["R"]
    pen = TTGlyphPen(None)
    quadratic = Cu2QuPen(pen, max_err=1.0, reverse_direction=True)
    glyph_set["R"].draw(TransformPen(quadratic, (-1, 0, 0, 1, advance, 0)))
    return pen.glyph(), advance


def draw_soft_sign(pen, x_offset=0):
    """Draw Ь with a left stem and a lower bowl opening to the right."""
    source = TTFont(COSTA_SOURCE)
    glyph_set = source.getGlyphSet()
    advance, _ = source["hmtx"].metrics["P"]
    quadratic = Cu2QuPen(pen, max_err=1.0, reverse_direction=True)
    glyph_set["P"].draw(
        TransformPen(quadratic, (1, 0, 0, -1, x_offset, CAP))
    )
    return advance


def reference_soft_sign():
    """Build Cyrillic Ь by vertically flipping the supplied Latin P."""
    pen = TTGlyphPen(None)
    advance = draw_soft_sign(pen)
    return pen.glyph(), advance


def reference_soft_sign_i():
    """Build Cyrillic Ы as a compact Ь + supplied Latin I combination."""
    source = TTFont(COSTA_SOURCE)
    glyph_set = source.getGlyphSet()
    i_advance, _ = source["hmtx"].metrics["I"]
    pen = TTGlyphPen(None)
    # Ь component: the same left-stem form used by standalone Ь.
    soft_advance = draw_soft_sign(pen)
    # Tuck the Latin I against the soft-sign bowl.
    i_offset = soft_advance - 55
    quadratic = Cu2QuPen(pen, max_err=1.0, reverse_direction=True)
    glyph_set["I"].draw(TransformPen(quadratic, (1, 0, 0, 1, i_offset, 0)))
    return pen.glyph(), i_offset + i_advance


def contour(pen, pts):
    pen.moveTo(pts[0])
    for p in pts[1:]:
        pen.lineTo(p)
    pen.closePath()


def oval(pen, x0, y0, x1, y1, reverse=False):
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rx, ry = (x1 - x0) / 2, (y1 - y0) / 2
    angles = [2 * pi * i / 32 for i in range(32)]
    if reverse:
        angles.reverse()
    contour(pen, [(cx + rx * cos(a), cy + ry * sin(a)) for a in angles])


def stroke(pen, x1, y1, x2, y2, w=STROKE, rounded=True):
    dx, dy = x2 - x1, y2 - y1
    length = max((dx * dx + dy * dy) ** 0.5, 1)
    angle = __import__("math").atan2(dy, dx)
    radius = w / 2
    if not rounded:
        nx, ny = -dy / length * radius, dx / length * radius
        contour(pen, [(x1 + nx, y1 + ny), (x2 + nx, y2 + ny),
                      (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)])
        return
    # A single capsule contour prevents pinholes where caps meet the stem.
    points = []
    for i in range(9):
        a = angle + pi / 2 - pi * i / 8
        points.append((x2 + radius * cos(a), y2 + radius * sin(a)))
    for i in range(9):
        a = angle - pi / 2 - pi * i / 8
        points.append((x1 + radius * cos(a), y1 + radius * sin(a)))
    contour(pen, points)


def arc(pen, cx, cy, rx, ry, a0, a1, w=STROKE, steps=18):
    outer, inner = [], []
    for i in range(steps + 1):
        a = a0 + (a1 - a0) * i / steps
        outer.append((cx + (rx + w / 2) * cos(a), cy + (ry + w / 2) * sin(a)))
        inner.append((cx + (rx - w / 2) * cos(a), cy + (ry - w / 2) * sin(a)))
    # Round the two open ends as part of the same contour.
    end_angle = a1
    start_angle = a0
    end_cap = []
    start_cap = []
    ex, ey = cx + rx * cos(end_angle), cy + ry * sin(end_angle)
    sx, sy = cx + rx * cos(start_angle), cy + ry * sin(start_angle)
    for i in range(1, 8):
        a = end_angle + pi * i / 8
        end_cap.append((ex + w / 2 * cos(a), ey + w / 2 * sin(a)))
    for i in range(1, 8):
        a = start_angle + pi + pi * i / 8
        start_cap.append((sx + w / 2 * cos(a), sy + w / 2 * sin(a)))
    contour(pen, outer + end_cap + list(reversed(inner)) + start_cap)


def ring(pen, x0, y0, x1, y1, w=STROKE):
    oval(pen, x0, y0, x1, y1)
    oval(pen, x0 + w, y0 + w, x1 - w, y1 - w, reverse=True)


def glyph(draw, width=620):
    pen = TTGlyphPen(None)
    draw(pen, width)
    return pen.glyph(), width


def normalize_letter_spacing(glyph_outline, advance, target=64):
    """Give display letters balanced sidebearings without changing outlines."""
    if glyph_outline.numberOfContours <= 0:
        return glyph_outline, advance, 0
    coordinates, _, _ = glyph_outline.getCoordinates(None)
    x_min = min(point[0] for point in coordinates)
    x_max = max(point[0] for point in coordinates)
    left = x_min
    right = advance - x_max

    # І deliberately has wider, already-balanced breathing room. Preserve any
    # similarly balanced pair instead of narrowing it mechanically.
    if left >= 80 and right >= 80 and abs(left - right) <= 4:
        return glyph_outline, advance, round(left)

    shift = target - x_min
    coordinates.translate((shift, 0))
    glyph_outline.coordinates = coordinates
    ink_width = x_max - x_min
    return glyph_outline, round(ink_width + target * 2), target


def normalize_cap_height(glyph_outline, target_bottom=0, target_top=CAP):
    """Align a base-letter silhouette to the shared baseline and cap line."""
    if glyph_outline.numberOfContours <= 0:
        return glyph_outline
    coordinates, _, _ = glyph_outline.getCoordinates(None)
    y_min = min(point[1] for point in coordinates)
    y_max = max(point[1] for point in coordinates)
    source_height = y_max - y_min
    if source_height <= 0:
        return glyph_outline
    scale = (target_top - target_bottom) / source_height
    for index, (x, y) in enumerate(coordinates):
        coordinates[index] = (x, round(target_bottom + (y - y_min) * scale))
    glyph_outline.coordinates = coordinates
    return glyph_outline


def bars(p, xs, y0=BASE, y1=CAP):
    for x in xs:
        stroke(p, x, y0, x, y1)


def draw_letter(ch):
    if ch == "Й":
        return short_i_svg_glyph(SHORT_I_SOURCE)
    if ch == "Б":
        return user_svg_glyph(BE_SOURCE, 110, 89, side_padding=64)
    if ch == "Ё":
        # The supplied SVG includes diaeresis above a 110-unit-tall base body.
        return supplied_svg_glyph(FULL_SET_DIR / SUPPLIED_RUSSIAN_SOURCES[ch],
                                  body_top=27.5, body_bottom=137.5)
    if ch == "Й":
        # Keep the breve above the cap line while the И body sits on baseline.
        return supplied_svg_glyph(FULL_SET_DIR / SUPPLIED_RUSSIAN_SOURCES[ch],
                                  body_top=23, body_bottom=133)
    if ch == "У":
        return user_svg_glyph(U_SOURCE, 110, 98, side_padding=64)
    if ch == "Ф":
        return user_svg_glyph(EF_SOURCE, 110, 160, side_padding=64)
    if ch in SUPPLIED_RUSSIAN_SOURCES:
        return supplied_svg_glyph(FULL_SET_DIR / SUPPLIED_RUSSIAN_SOURCES[ch])
    if ch in "ІЇЄҐ":
        return derived_ukrainian_letter(ch)
    if ch == "Д":
        return user_svg_glyph(DE_SOURCE, 110, 125, side_padding=64)
    if ch == "Ж":
        return user_svg_glyph(ZHE_SOURCE, 107, 149)
    if ch == "Г":
        return user_svg_glyph(GE_SOURCE, 111, 77)
    if ch == "Л":
        return user_svg_glyph(EL_SOURCE, 106, 106, side_padding=71,
                              target_height=700, advance_adjust=-7)
    if ch == "М":
        return user_svg_glyph(EM_SOURCE, 106, 175, side_padding=64)
    if ch == "П":
        # Keep П at the shared cap height and give the wide doorway shape
        # equal breathing room on both sides.
        return user_svg_glyph(PE_SOURCE, 114, 106, side_padding=64, target_height=700)
    if ch == "Ф":
        return user_svg_glyph(EF_SOURCE, 110, 160, side_padding=64)
    if ch == "Ш":
        return user_svg_glyph(SHA_SOURCE, 114, 183, side_padding=64)
    if ch == "Щ":
        # The source's first 114 units form the cap-height letter; the final
        # 15 units intentionally descend below the baseline as Щ's tail.
        return user_svg_glyph(SHCHA_SOURCE, 114, 211, side_padding=64)
    if ch == "Ъ":
        return user_svg_glyph(HARD_SIGN_SOURCE, 110, 121, side_padding=64)
    if ch == "Ц":
        # Vector (8).svg uses a 114-unit cap body with a 16-unit descending tail.
        return user_svg_glyph(TSE_SOURCE, 114, 134, side_padding=64)
    if ch == "Э":
        return user_svg_glyph(E_REVERSED_SOURCE, 112, 86)
    if ch == "Ы":
        return user_svg_glyph(YERY_SOURCE, 111, 112, side_padding=64)
    if ch == "Ь":
        return user_svg_glyph(SOFT_SIGN_SOURCE, 110, 81, side_padding=64)
    if ch == "Ю":
        return user_svg_glyph(YU_SOURCE, 112, 143, side_padding=64)
    if ch == "Ё":
        return reference_e_dieresis()
    if ch == "И":
        return reference_flipped_n()
    if ch == "Й":
        return reference_flipped_n(with_breve=True)
    if ch == "Ш":
        return reference_upside_down_m()
    if ch == "Я":
        return reference_flipped_r()
    if ch == "Ы":
        return reference_soft_sign_i()
    if ch in COSTA_VISUAL_EQUIVALENTS:
        return reference_glyph(COSTA_VISUAL_EQUIVALENTS[ch])
    widths = {"Ж": 820, "М": 760, "Ш": 760, "Щ": 800, "Ф": 700, "Ю": 790,
              "Ы": 760, "Д": 700, "Л": 680, "Т": 610, "Г": 560, "І": 330,
              "Ї": 330, "Й": 640}
    w = widths.get(ch, 620)
    l, r, m = SIDE + 30, w - SIDE - 30, w / 2
    top, bot, mid = CAP - 20, BASE + 20, 385

    def d(p, _):
        if ch == "А":
            stroke(p, l, bot, m, top); stroke(p, m, top, r, bot); stroke(p, l+80, mid, r-80, mid)
        elif ch == "Б":
            stroke(p, l, bot, l, top); stroke(p, l, top, r-25, top); stroke(p, l, mid, r-110, mid)
            arc(p, r-150, (mid+bot)/2, 155, (mid-bot)/2, pi/2, -pi/2)
        elif ch == "В":
            stroke(p, l, bot, l, top)
            arc(p, l+145, 560, 150, 175, pi/2, -pi/2)
            arc(p, l+155, 210, 170, 175, pi/2, -pi/2)
        elif ch == "Г":
            stroke(p, l, bot, l, top); stroke(p, l, top, r, top)
        elif ch == "Д":
            stroke(p, l+70, bot+15, l+145, top); stroke(p, l+145, top, r-65, top); stroke(p, r-65, top, r-5, bot+15)
            stroke(p, l, bot, r+30, bot); stroke(p, l+15, bot, l-5, -75); stroke(p, r+15, bot, r+35, -75)
        elif ch == "Е" or ch == "Ё":
            stroke(p, l, bot, l, top); stroke(p, l, top, r, top); stroke(p, l, mid, r-65, mid); stroke(p, l, bot, r, bot)
            if ch == "Ё": oval(p, m-105, 825, m-45, 885); oval(p, m+45, 825, m+105, 885)
        elif ch == "Ж":
            stroke(p, m, bot, m, top); stroke(p, m, mid, l, top); stroke(p, m, mid, l, bot); stroke(p, m, mid, r, top); stroke(p, m, mid, r, bot)
        elif ch == "З":
            arc(p, m-20, 565, 225, 175, pi*0.55, -pi*0.52); arc(p, m-25, 215, 235, 175, pi*0.52, -pi*0.55)
        elif ch in ("И", "Й"):
            bars(p, [l, r]); stroke(p, l, bot, r, top)
            if ch == "Й": arc(p, m, 840, 115, 65, pi, 2*pi, w=48, steps=10)
        elif ch == "К":
            stroke(p, l, bot, l, top); stroke(p, l, mid, r, top); stroke(p, l, mid, r, bot)
        elif ch == "Л":
            stroke(p, l, bot, m-65, top); stroke(p, m-65, top, r, top); stroke(p, r, top, r, bot)
        elif ch == "М":
            bars(p, [l, r]); stroke(p, l, top, m, mid+10); stroke(p, m, mid+10, r, top)
        elif ch == "Н":
            bars(p, [l, r]); stroke(p, l, mid, r, mid)
        elif ch == "О": ring(p, l, bot, r, top)
        elif ch == "П": bars(p, [l, r]); stroke(p, l, top, r, top)
        elif ch == "Р":
            stroke(p, l, bot, l, top); arc(p, l+150, 555, 160, 180, pi/2, -pi/2)
        elif ch == "С": arc(p, m, 390, (r-l)/2, 350, pi*0.30, pi*1.70, steps=24)
        elif ch == "Т": stroke(p, l, top, r, top); stroke(p, m, top, m, bot)
        elif ch == "У":
            stroke(p, l, top, m, mid-25); stroke(p, r, top, m-55, bot)
        elif ch == "Ф":
            stroke(p, m, -15, m, 790); ring(p, l, 225, r, 625)
        elif ch == "Х": stroke(p, l, top, r, bot); stroke(p, r, top, l, bot)
        elif ch == "Ц":
            bars(p, [l, r]); stroke(p, l, bot, r, bot); stroke(p, r, bot, r+10, -75)
        elif ch == "Ч":
            stroke(p, l, top, l, mid); stroke(p, l, mid, r, mid+55); stroke(p, r, top, r, bot)
        elif ch in ("Ш", "Щ"):
            bars(p, [l, m, r]); stroke(p, l, bot, r, bot)
            if ch == "Щ": stroke(p, r, bot, r+10, -75)
        elif ch == "Ъ":
            stroke(p, l-40, top, l+120, top); stroke(p, l+75, top, l+75, bot); stroke(p, l+75, mid, r-100, mid)
            arc(p, r-140, 210, 150, 175, pi/2, -pi/2)
        elif ch == "Ы":
            stroke(p, l, top, l, bot); stroke(p, l, mid, m-80, mid); arc(p, m-110, 210, 145, 175, pi/2, -pi/2); stroke(p, r, top, r, bot)
        elif ch == "Ь":
            stroke(p, l, top, l, bot); stroke(p, l, mid, r-105, mid); arc(p, r-145, 210, 150, 175, pi/2, -pi/2)
        elif ch == "Э":
            arc(p, m, 390, (r-l)/2, 350, pi*0.70, -pi*0.70, steps=24); stroke(p, m-30, mid, r-15, mid)
        elif ch == "Ю":
            stroke(p, l, top, l, bot); stroke(p, l, mid, m-20, mid); ring(p, m-20, bot, r, top)
        elif ch == "Я":
            stroke(p, r, bot, r, top); arc(p, r-150, 555, 160, 180, pi/2, pi*1.5); stroke(p, r-150, mid, l, bot)
        elif ch == "І": stroke(p, m, bot, m, top)
        elif ch == "Ї":
            stroke(p, m, bot, m, top); oval(p, m-100, 825, m-40, 885); oval(p, m+40, 825, m+100, 885)
        elif ch == "Є":
            arc(p, m, 390, (r-l)/2, 350, pi*0.30, pi*1.70, steps=24); stroke(p, l+20, mid, m+65, mid)
        elif ch == "Ґ":
            stroke(p, l, bot, l, top); stroke(p, l, top, r, top); stroke(p, r, top, r, top+90)
        else: raise ValueError(ch)
    return glyph(d, w)


def draw_digit(ch):
    w = 560; l, r, m = 85, 475, 280; top, bot, mid = 715, 55, 385
    def d(p, _):
        if ch == "0": ring(p, l, bot, r, top)
        elif ch == "1": stroke(p, m, bot, m, top); stroke(p, m, top, m-105, top-115); stroke(p, m-115, bot, m+115, bot)
        elif ch == "2": arc(p, m, 555, 195, 165, pi, 0, steps=12); stroke(p, r, 555, l, bot); stroke(p, l, bot, r, bot)
        elif ch == "3": arc(p, m-20, 555, 195, 165, pi*0.55, -pi*0.52); arc(p, m-20, 220, 205, 165, pi*0.52, -pi*0.55)
        elif ch == "4": stroke(p, r-65, bot, r-65, top); stroke(p, r-65, top, l, mid); stroke(p, l, mid, r, mid)
        elif ch == "5": stroke(p, r, top, l, top); stroke(p, l, top, l, mid); stroke(p, l, mid, r-120, mid); arc(p, r-145, 215, 155, 170, pi/2, -pi/2)
        elif ch == "6": arc(p, m, 240, 195, 190, 0, 2*pi, steps=24); stroke(p, l+35, 300, r-55, top)
        elif ch == "7": stroke(p, l, top, r, top); stroke(p, r, top, m-45, bot)
        elif ch == "8": ring(p, l+35, mid, r-35, top); ring(p, l, bot, r, mid+20)
        elif ch == "9": arc(p, m, 540, 195, 190, 0, 2*pi, steps=24); stroke(p, r-35, 480, l+55, bot)
    return glyph(d, w)


def simple_glyph(ch):
    widths = {"space": 260, "period": 230, "comma": 250, "colon": 250, "hyphen": 360,
              "exclam": 260, "question": 500, "quotedbl": 350, "quotesingle": 210,
              "parenleft": 300, "parenright": 300, "ampersand": 600,
              "middot": 230, "euro": 560}
    w = widths[ch]
    def d(p, _):
        if ch == "space": return
        if ch == "period": oval(p, 80, 35, 155, 110)
        elif ch == "comma": oval(p, 85, 45, 160, 120); stroke(p, 125, 65, 85, -45, 38)
        elif ch == "colon": oval(p, 90, 185, 160, 255); oval(p, 90, 535, 160, 605)
        elif ch == "hyphen": stroke(p, 70, 360, 290, 360, 55)
        elif ch == "exclam": stroke(p, 130, 230, 130, 715); oval(p, 92, 40, 168, 116)
        elif ch == "question": arc(p, 245, 555, 180, 165, pi, 0, steps=12); stroke(p, 425, 555, 250, 330); oval(p, 210, 40, 286, 116)
        elif ch in ("quotedbl", "quotesingle"):
            stroke(p, 105, 705, 85, 560, 48)
            if ch == "quotedbl": stroke(p, 245, 705, 225, 560, 48)
        elif ch == "parenleft": arc(p, 285, 385, 175, 355, pi/2, pi*1.5, steps=20)
        elif ch == "parenright": arc(p, 15, 385, 175, 355, -pi/2, pi/2, steps=20)
        elif ch == "ampersand":
            arc(p, 280, 555, 150, 165, 0, 2*pi, steps=18); arc(p, 280, 220, 210, 190, 0, 2*pi, steps=20); stroke(p, 150, 430, 500, 70)
        elif ch == "middot": oval(p, 80, 335, 155, 410)
        elif ch == "euro":
            arc(p, 305, 385, 205, 320, pi*0.28, pi*1.72, steps=24)
            stroke(p, 80, 465, 390, 465, 48); stroke(p, 70, 315, 365, 315, 48)
    return glyph(d, w)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    upper = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯІЇЄҐ"
    lower = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяіїєґ"
    glyphs = {".notdef": TTGlyphPen(None).glyph()}
    metrics = {".notdef": (600, 0)}
    cmap = {}
    order = [".notdef"]

    for ch in upper:
        name = f"uni{ord(ch):04X}"
        g, aw = draw_letter(ch)
        # Base letters share one exact 0–735 body height. Accented letters keep
        # their marks above the cap line, while Ц and Щ retain required tails.
        if ch not in "ЁЙЇЦЩҐ":
            g = normalize_cap_height(g)
        g, aw, lsb = normalize_letter_spacing(g, aw)
        glyphs[name] = g; metrics[name] = (aw, lsb); order.append(name); cmap[ord(ch)] = name
    for lo, up in zip(lower, upper): cmap[ord(lo)] = f"uni{ord(up):04X}"
    digit_names = {"0":"zero","1":"one","2":"two","3":"three","4":"four","5":"five","6":"six","7":"seven","8":"eight","9":"nine"}
    for ch in "0123456789":
        name = f"digit{ch}"; g, aw = reference_glyph(digit_names[ch]); glyphs[name] = g; metrics[name] = (aw, 0); order.append(name); cmap[ord(ch)] = name
    punctuation = {" ": "space", ".": "period", ",": "comma", ":": "colon", "-": "hyphen",
                   "!": "exclam", "?": "question", '"': "quotedbl", "'": "quotesingle",
                   "(": "parenleft", ")": "parenright", "&": "ampersand",
                   "·": "middot", "€": "euro"}
    for char, name in punctuation.items():
        if name == "euro":
            g, aw = user_svg_glyph(EURO_SOURCE, 110, 102)
            g, aw, lsb = normalize_letter_spacing(g, aw)
        elif name in COSTA_PUNCTUATION:
            g, aw, lsb = reference_glyph_with_metrics(COSTA_PUNCTUATION[name])
        else:
            g, aw = simple_glyph(name)
            lsb = 0
        glyphs[name] = g; metrics[name] = (aw, lsb); order.append(name); cmap[ord(char)] = name
    cmap[0x00A0] = "space"; cmap[0x2013] = "hyphen"; cmap[0x2014] = "hyphen"
    cmap[0x2018] = "quotesingle"; cmap[0x2019] = "quotesingle"; cmap[0x201C] = "quotedbl"; cmap[0x201D] = "quotedbl"

    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(order)
    fb.setupCharacterMap(cmap)
    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=900, descent=-180)
    fb.setupNameTable({"familyName": "Saged Display Cyrillic 1399", "styleName": "Regular",
                       "uniqueFontIdentifier": "SagedDisplayCyrillic1399-Regular-1.399",
                       "fullName": "Saged Display Cyrillic 1399 Regular",
                       "psName": "SagedDisplayCyrillic1399-Regular",
                       "version": "Version 1.399",
                       "copyright": "Copyright 2026 Diana Sage. Original custom artwork."})
    fb.setupOS2(sTypoAscender=900, sTypoDescender=-180, sTypoLineGap=0,
                usWinAscent=920, usWinDescent=200, sxHeight=CAP, sCapHeight=CAP,
                usWeightClass=400, fsType=0, fsSelection=0x00C0)
    fb.font["OS/2"].version = 4
    fb.setupPost(italicAngle=0, underlinePosition=-100, underlineThickness=45)
    fb.setupMaxp()
    fb.font["head"].fontRevision = 1.399
    addOpenTypeFeaturesFromString(fb.font, """
        languagesystem DFLT dflt;
        languagesystem cyrl dflt;
        feature kern {
            pos uni0410 [uni0422 uni0423] -24;
            pos [uni0413 uni0422 uni0423] [uni0410 uni041E uni0421] -22;
            pos [uni041B uni042F] [uni0410 uni041E] -16;
            pos uni0420 [uni0410 uni041E] -12;
        } kern;
    """)
    ttf = OUT / "saged-v1.399.ttf"
    fb.save(ttf)
    web = TTFont(ttf); web.flavor = "woff"; web.save(OUT / "saged-display-cyrillic-v1.399.woff")
    print(ttf)


if __name__ == "__main__": main()
