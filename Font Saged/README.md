# Saged font

Current version: **1.403**.

- **Font files** — current desktop TTF and website WOFF.
- **Preview** — current alphabet and Ukrainian word samples.
- **Sources / Latest letters** — current І / Ї / Д SVGs and required base font. Artwork filenames use the character and letter name; variation numbers distinguish drawings, not release chronology.
- **Sources / Original construction** — full editable alphabet, Costa dependency and original construction script. These are still required source materials, not an older release to install.
- **Sources / Letter variations** — unique alternative letter drawings.
- **Sources / Additional letter variations** — identified alternative letter drawings.
- **Documentation** — original brief, artwork inventory and cleanup records.
- **build.py** — rebuild current font: `python3 build.py` (fontTools required).

Superseded releases, duplicate files, ZIPs with already-extracted artwork, and unused Summer font references were moved to macOS Trash on 2026-11-09. Originals used by websites, videos or installed fonts were left in place. The required 1.399 base is retained inside Sources because the current build depends on it. Previous collection manifests describe the collection before this cleanup; consult the cleanup record for moved folders.

Д updated from supplied PNG on 2026-11-09, traced into editable Д - De.svg. Audit: zero errors; raster trace has an outline-complexity warning. Only Д/д changed; coverage and vertical metrics retained. Not installed or published.

Latest update: v1.402 replaces Д/д from the new 144×110 Frame 104.png. Source PNG and traced SVG are in Sources/Latest letters. Previous Д artwork preserved under Letter variations. Russian and Ukrainian share this Cyrillic Д. Only Д/д outline and width changed; coverage and vertical metrics preserved. Audit zero errors, traced-outline complexity warning (428 points). 2.0 draft and website unchanged.

Version 1.403 imports the original Frame 134 SVG for Д/д (140×110). A zero-area source fragment is ignored. Two real contours and one counter verified; no errors or warnings for updated letters. Other outlines/coverage/vertical metrics unchanged. Previous Д preserved as v1.402 variations.
