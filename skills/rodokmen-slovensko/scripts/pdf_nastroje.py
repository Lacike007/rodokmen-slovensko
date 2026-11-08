"""Nástroje na PDF skeny rodinných dokumentov (bez ghostscriptu). Treba: pip install pypdf

  python3 -I pdf_nastroje.py obrazky <vstup.pdf> <prefix>     -> vytiahne naskenované obrázky (prefix_p1_0.jpg …)
  python3 -I pdf_nastroje.py spoj <vystup.pdf> <a.pdf> <b.pdf> …  -> spojí PDF do jedného (poradie podľa argumentov)
"""
import os
import sys

import pypdf


def obrazky(src, prefix):
    for pi, page in enumerate(pypdf.PdfReader(src).pages):
        for ii, im in enumerate(page.images):
            fn = f"{prefix}_p{pi + 1}_{ii}{os.path.splitext(im.name)[1] or '.png'}"
            with open(fn, "wb") as f:
                f.write(im.data)
            print(fn, im.image.size if hasattr(im, "image") and im.image else "")


def spoj(out, files):
    w = pypdf.PdfWriter()
    for f in files:
        w.append(f)
    w.write(out)
    print(out, len(pypdf.PdfReader(out).pages), "strán")


if __name__ == "__main__":
    if len(sys.argv) >= 4 and sys.argv[1] == "obrazky":
        obrazky(sys.argv[2], sys.argv[3])
    elif len(sys.argv) >= 4 and sys.argv[1] == "spoj":
        spoj(sys.argv[2], sys.argv[3:])
    else:
        print(__doc__)
