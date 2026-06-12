#!/usr/bin/env python3
"""
make_banner.py — generate a 1200x630 banner (OG image / blog header) with Photopea.

    python make_banner.py "Your Title" "Your subtitle" out.png

Pure orchestration over the Photopea MCP via photopea.py. No Photoshop, no API key.
"""
import sys
from photopea import Photopea, gradient_bg, text, rect, export

NAVY, NAVY2, GOLD, WHITE = "#16182e", "#283276", "#f5d76e", "#ffffff"


def main() -> int:
    title = sys.argv[1] if len(sys.argv) > 1 else "Photopea as Code"
    subtitle = sys.argv[2] if len(sys.argv) > 2 else "Design, programmatically. Free."
    out = sys.argv[3] if len(sys.argv) > 3 else "banner.png"

    with Photopea() as pp:
        gradient_bg(pp, 1200, 630, NAVY, NAVY2, angle=45, name="Banner")
        rect(pp, 120, 150, 120, 12, GOLD)                      # accent bar
        text(pp, title, 116, 250, 110, WHITE, bold=True)
        text(pp, subtitle, 122, 400, 42, GOLD)
        export(pp, out, "png")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
