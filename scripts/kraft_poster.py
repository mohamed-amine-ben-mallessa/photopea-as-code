#!/usr/bin/env python3
"""
kraft_poster.py — a textured poster: your custom font, printed onto a paper texture.

Demonstrates two techniques the docs gloss over (see docs/SCRIPTING.md):
  1. CUSTOM FONT — load a local OTF/TTF via a data: URI (file:// is sandbox-blocked).
  2. INK ON TEXTURE — set each text layer to MULTIPLY so the ink soaks into the paper.

    python kraft_poster.py texture.png MyFont.otf "PHOTOPEA" "AS CODE" out.png

⚠️ Multiply darkens — use DARK ink colors (near-black, deep red, forest green).
Light colors vanish under multiply on a dark texture.

Free, no Photoshop, no API key. Node + the Photopea MCP only.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from photopea import (Photopea, load_font_file, text_on_texture, export, rect,  # noqa: E402
                      multiply_active_layer)

INK = "#191210"   # near-black ink
RED = "#a8392c"   # brick red accent (dark enough to survive multiply)


def arg(i, default):
    return sys.argv[i] if len(sys.argv) > i else default


def main() -> int:
    texture = arg(1, "texture.png")
    font_file = arg(2, "")            # optional; falls back to a default font if empty
    line1 = arg(3, "PHOTOPEA")
    line2 = arg(4, "AS CODE")
    out = arg(5, "poster.png")

    with Photopea() as pp:
        # background = the paper texture (square-ish works best for posts)
        pp.call("photopea_open_file", {"source": os.path.abspath(texture)})

        font_name = ""
        if font_file and os.path.exists(font_file):
            load_font_file(pp, font_file)
            # discover the registered PostScript name
            import json
            try:
                names = json.loads(pp.call("photopea_list_fonts", {}) or "[]")
                stem = os.path.splitext(os.path.basename(font_file))[0]
                hit = [n for n in names if stem.split("-")[0].lower() in str(n).lower()]
                font_name = hit[0] if hit else ""
            except Exception:  # noqa: BLE001
                font_name = ""

        # red accent bar (multiplied so it tints the paper)
        rect(pp, 92, 330, 140, 16, RED)
        multiply_active_layer(pp)

        # type ramp — all dark, all multiplied
        text_on_texture(pp, "OPEN SOURCE TOOLKIT", 96, 290, 30, INK, font=font_name)
        text_on_texture(pp, line1, 90, 400, 134, INK, font=font_name)
        text_on_texture(pp, line2, 92, 545, 134, RED, font=font_name)
        text_on_texture(pp, "Design images programmatically.", 96, 740, 44, INK,
                        font=font_name, bold=False)
        text_on_texture(pp, "Free. No Photoshop.", 96, 800, 44, RED,
                        font=font_name, bold=False)

        export(pp, out, "png")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
