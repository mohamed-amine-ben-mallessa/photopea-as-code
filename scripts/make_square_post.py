#!/usr/bin/env python3
"""
make_square_post.py — generate a 1080x1080 Instagram post with Photopea.

    python make_square_post.py "EYEBROW" "Big headline" "Accent line" "subtitle" "CTA" "@handle" out.png

Every arg optional. No Photoshop, no API key — just Node + the Photopea MCP.
"""
import sys
from photopea import Photopea, gradient_bg, text, rect, export

NAVY, NAVY2, GOLD, WHITE, MUTE = "#16182e", "#283276", "#f5d76e", "#ffffff", "#c9cde0"


def arg(i, default):
    return sys.argv[i] if len(sys.argv) > i else default


def main() -> int:
    eyebrow  = arg(1, "DESIGN, AS CODE")
    line1    = arg(2, "Make your posts")
    accent   = arg(3, "while you sleep.")
    subtitle = arg(4, "Programmatic, free, no Photoshop.")
    cta      = arg(5, "Get started")
    handle   = arg(6, "@photopea.as.code")
    out      = arg(7, "post.png")

    with Photopea() as pp:
        gradient_bg(pp, 1080, 1080, NAVY, NAVY2, angle=120, name="IG Post")
        rect(pp, 90, 150, 120, 12, GOLD)                       # accent bar
        text(pp, eyebrow, 90, 205, 30, GOLD, bold=True, letterSpacing=4)
        text(pp, line1, 88, 320, 84, WHITE, bold=True)
        text(pp, accent, 88, 430, 84, GOLD, bold=True)
        text(pp, subtitle, 92, 580, 36, MUTE)
        rect(pp, 90, 740, 380, 92, GOLD)                       # CTA button
        text(pp, cta, 120, 770, 38, NAVY, bold=True)
        text(pp, handle, 90, 1005, 32, "#8b90b0", bold=True)
        export(pp, out, "png")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
