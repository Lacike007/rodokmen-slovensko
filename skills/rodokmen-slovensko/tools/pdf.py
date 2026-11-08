#!/usr/bin/env python3
"""HTML -> PDF cez Playwright (headless Chromium), bez Chrome/Brave/Vivaldi.

Použitie:  ~/.local/share/rodokmen-pdf/bin/python tools/pdf.py <vstup.html> <vystup.pdf> [A4|A3] [--na-sirku]
Ak strana nemá @page, použije sa zadaný formát (predvolené A4 na výšku).

Inštalácia (jednorazovo; na Linuxe rovnako):
  python3 -m venv ~/.local/share/rodokmen-pdf
  ~/.local/share/rodokmen-pdf/bin/pip install playwright pypdf
  ~/.local/share/rodokmen-pdf/bin/python -m playwright install chromium
  (Linux navyše: ~/.local/share/rodokmen-pdf/bin/python -m playwright install-deps chromium)
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if len(args) < 2:
    sys.exit(__doc__)
src, out = pathlib.Path(args[0]).resolve(), pathlib.Path(args[1]).resolve()
fmt = args[2] if len(args) > 2 else "A4"
landscape = "--na-sirku" in sys.argv

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page()
    page.goto(src.as_uri(), wait_until="networkidle")
    # A3 na šírku pri 12 mm okrajoch ~ 1540 px šírky; nastav okno, aby skript na strane vedel zmenšiť široké stromy
    w = {"A4": 1000 if landscape else 690, "A3": 1430 if landscape else 1000}.get(fmt, 1050)
    page.set_viewport_size({"width": w, "height": 1000})
    page.evaluate("typeof fit==='function' && fit()")
    page.pdf(path=str(out), format=fmt, landscape=landscape, print_background=True,
             prefer_css_page_size=True, margin={"top": "12mm", "bottom": "12mm", "left": "12mm", "right": "12mm"})
    b.close()
print("PDF:", out)
