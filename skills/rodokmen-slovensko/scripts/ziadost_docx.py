"""Žiadosť na matričný úrad ako Word (.docx), Calibri 11, A4. Treba: pip install python-docx

  python3 -I ziadost_docx.py <spec.json> <vystup.docx> [data/ziadatel.md]

Údaje žiadateľa sa načítajú z data/ziadatel.md (riadky „- Meno: …“, „- Narodený: …“, „- Adresa: ulica, PSČ obec“,
„- Telefón: …“, „- E-mail: …“, „- Miesto podpisu: …“).

spec.json:
{
  "urad": ["Mesto Príkladov", "Mestský úrad – matričný úrad", "Hlavná 1", "000 00 Príkladov"],
  "datum": "3. 11. 2026",
  "vec": "Žiadosť o vydanie rodného listu",
  "uvod": "ako syn (člen rodiny podľa § 18 ods. 2 zákona č. 154/1994 Z. z. o matrikách) Vás žiadam o vydanie rodného listu môjho otca:",
  "udaje": [["meno a priezvisko:", "Ján Novák"], ["dátum narodenia:", "1. 1. 1930"]],
  "odseky": ["Postačí mi sken … ", "Správny poplatok uhradím podľa Vašich pokynov."],
  "prilohy": ["kópia rodného listu žiadateľa"]
}
Text v hranatých zátvorkách [takto] sa zvýrazní žltou (miesto na doplnenie).
"""
import json
import re
import sys

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_COLOR_INDEX
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

FONT = "Calibri"


def nacitaj_ziadatela(path):
    d = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"-\s*([^:]+):\s*(.+)", line.strip())
        if m:
            d[m.group(1).strip().lower()] = m.group(2).strip()
    adresa = [a.strip() for a in d.get("adresa", "[ulica a číslo], [PSČ a obec]").split(",", 1)]
    return dict(meno=d.get("meno", "[meno]"), narodeny=d.get("narodený", ""), adresa=adresa,
                tel=d.get("telefón", "[telefón]"), email=d.get("e-mail", "[e-mail]"),
                miesto=d.get("miesto podpisu", "[miesto]"))


def main(spec_path, out, ziadatel_path="data/ziadatel.md"):
    s = json.load(open(spec_path, encoding="utf-8"))
    z = nacitaj_ziadatela(ziadatel_path)
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    sec.left_margin = sec.right_margin = sec.top_margin = sec.bottom_margin = Cm(2.5)
    st = doc.styles["Normal"]
    st.font.name, st.font.size = FONT, Pt(11)
    rf = st.element.get_or_add_rPr().find(qn("w:rFonts"))
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(a), FONT)
    st.paragraph_format.space_after = Pt(0)
    st.paragraph_format.line_spacing = 1.15
    J = WD_ALIGN_PARAGRAPH.JUSTIFY

    def para(text="", bold=False, after=0, align=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(after)
        if align is not None:
            p.alignment = align
        for part in re.split(r"(\[[^\]]+\])", text):
            if part:
                r = p.add_run(part)
                r.bold = bold
                if part.startswith("["):
                    r.font.highlight_color = WD_COLOR_INDEX.YELLOW
        return p

    para(z["meno"], bold=True)
    for a in z["adresa"]:
        para(a)
    para(f"tel.: {z['tel']}    e-mail: {z['email']}", after=24)
    for i, r in enumerate(s["urad"]):
        para(r, after=24 if i == len(s["urad"]) - 1 else 0)
    para(f"{z['miesto']}, {s.get('datum', '[dátum]')}", align=WD_ALIGN_PARAGRAPH.RIGHT, after=18)
    para("Vec: " + s["vec"].removeprefix("Vec: "), bold=True, after=18)
    para("Dobrý deň,", after=10)
    para(s["uvod"], align=J, after=8)
    if s.get("udaje"):
        t = doc.add_table(rows=len(s["udaje"]), cols=2)
        t.autofit = False
        ind = OxmlElement("w:tblInd")
        ind.set(qn("w:w"), "567")
        ind.set(qn("w:type"), "dxa")
        t._tbl.tblPr.append(ind)
        for i, (k, v) in enumerate(s["udaje"]):
            c0, c1 = t.rows[i].cells
            c0.width, c1.width = Cm(4), Cm(11.5)
            c0.paragraphs[0].add_run(k)
            c1.paragraphs[0].add_run(v).bold = True
        para()
    for t in s.get("odseky", []):
        para(t, align=J, after=10)
    para("Ďakujem a s pozdravom", after=40)
    para("........................................")
    para(z["meno"])
    if z["narodeny"]:
        para("narodený " + z["narodeny"], after=30)
    if s.get("prilohy"):
        para("Príloha:" if len(s["prilohy"]) == 1 else "Prílohy:", bold=True)
        for t in s["prilohy"]:
            doc.add_paragraph(t, style="List Bullet")
    doc.core_properties.author = z["meno"]
    doc.core_properties.title = s["vec"]
    doc.save(out)
    print(out)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
    else:
        main(*sys.argv[1:4])
