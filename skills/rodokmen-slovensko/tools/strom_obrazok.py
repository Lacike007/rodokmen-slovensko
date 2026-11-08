"""Rodinný strom ako jeden veľký obrázok (JPG) – na prezeranie a zväčšovanie na tablete/mobile.

  ~/.local/share/rodokmen-pdf/bin/python tools/strom_obrazok.py dokumenty/pre_rodinu/rodinny_strom.html out.jpg

Na rozdiel od PDF sa stromy nezmenšujú na šírku strany – každý je v plnej veľkosti (1,5× hustota).
Cez WhatsApp posielať ako dokument, nie ako fotku (inak sa zmenší).
"""
import sys, pathlib
from playwright.sync_api import sync_playwright
src, out = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1600, "height": 1000}, device_scale_factor=1.5)
    pg.goto(pathlib.Path(src).resolve().as_uri())
    # bez zmenšovania: každý strom v plnej veľkosti, stránka taká široká ako najširší strom
    w = pg.evaluate("""()=>{window.removeEventListener('resize',fit);document.querySelectorAll('.ft').forEach(t=>t.style.zoom=1);
      document.querySelectorAll('.ft-wrap').forEach(x=>x.style.overflow='visible');
      return Math.max(...[...document.querySelectorAll('.ft')].map(t=>t.scrollWidth))+80}""")
    pg.set_viewport_size({"width": int(w), "height": 1000})
    pg.evaluate("document.querySelectorAll('.ft').forEach(t=>t.style.zoom=1)")
    pg.screenshot(path=out, full_page=True, type="jpeg", quality=88)
    b.close()
