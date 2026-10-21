# Saged 1.399

Updates €, Ы/ы, Ю/ю from supplied SVGs; Й/й traced from Group 441.png.
Based on editable Saged 1.398 source. Only these four outlines changed; vertical metrics and remaining glyphs preserved. Lowercase retains existing unicase mapping.

Rebuild: `python3 build.py` (fontTools and Pillow required).
Editable artwork and construction source are in sources/. TTF is for desktop use; WOFF is for websites. proof.png shows updated glyphs and full language samples.

Validation: all 48 requested uppercase/language/numeral/currency characters pass audit without errors. Existing digit metric/duplicate-point warnings remain; traced Й has 496 points, above the audit advisory threshold. Both formats reopened successfully; cmap and vertical metrics checked. Visual proof inspected. Browser/OTS/FontBakery checks not performed. No system installation or live website replacement made.

The original font contains supplied Costa-derived outlines; existing licensing conditions remain unchanged.
