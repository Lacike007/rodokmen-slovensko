#!/usr/bin/env python3
"""Rodinný strom potomkov z data/rodina.py.

Použitie:  python3 -I tools/rodinny_strom.py [--predpoklady]
Vytvorí:   web/src/generated/rodinny_strom.html   (fragment pre stránku webu /strom/)
           dokumenty/pre_rodinu/rodinny_strom.html (samostatná stránka na tlač / do PDF, A3 na šírku)
--predpoklady: strom z data/predpoklady.py (pravdepodobné a nepotvrdené vetvy) → predpokladany_strom.html
           (web /predpoklady/); osoby s ist="doc"/"prob"/"hyp" a väzby s ist="hyp" majú vlastné označenie.
"""
import ast
import html
import os
import sys

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRED = "--predpoklady" in sys.argv
MENO = "predpokladany_strom" if PRED else "rodinny_strom"


def nacitaj_data(cesta):
    """Načíta rodina.py / predpoklady.py BEZ spúšťania kódu: len priradenia textov, čísel, zoznamov,
    n-tic, slovníkov a dict(...). Čokoľvek iné (import, volanie funkcie…) je chyba – zdieľaný súbor nič nespustí."""
    def hodnota(n):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "dict" and not n.args:
            return {k.arg: hodnota(k.value) for k in n.keywords if k.arg}
        if isinstance(n, ast.List):
            return [hodnota(x) for x in n.elts]
        if isinstance(n, ast.Tuple):
            return tuple(hodnota(x) for x in n.elts)
        if isinstance(n, ast.Dict):
            return {hodnota(k): hodnota(v) for k, v in zip(n.keys, n.values)}
        if isinstance(n, ast.Constant):
            return n.value
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):  # "text " "pokračovanie" na viac riadkov
            return hodnota(n.left) + hodnota(n.right)
        raise ValueError(f"{cesta}, riadok {getattr(n, 'lineno', '?')}: nepovolený zápis (len texty, čísla, zoznamy a dict(...))")
    ns = {}
    for st in ast.parse(open(cesta, encoding="utf-8").read(), cesta).body:
        if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
            ns[st.targets[0].id] = hodnota(st.value)
        elif isinstance(st, ast.Expr) and isinstance(st.value, ast.Constant):
            continue  # docstring
        else:
            raise ValueError(f"{cesta}, riadok {st.lineno}: nepovolený príkaz (len PREMENNA = hodnota)")
    return ns


try:
    ns = nacitaj_data(os.path.join(ROOT, "data", "predpoklady.py" if PRED else "rodina.py"))
except ValueError as e:
    sys.exit(str(e))
OSOBY, ZVAZKY, KORENE = ns["OSOBY"], ns["ZVAZKY"], ns["KORENE"]
PODPIS = ns.get("PODPIS", "")  # napr. "Opravy a doplnky prosím Janovi."
_MES = ["januáru", "februáru", "marcu", "aprílu", "máju", "júnu", "júlu", "augustu", "septembru", "októbru", "novembru", "decembru"]
import datetime
_d = datetime.date.today()
STAV = f"{_MES[_d.month - 1]} {_d.year}"

chyby = []
for z in ZVAZKY:
    for k in [z["a"], z.get("b")] + z.get("deti", []):
        if k and k not in OSOBY:
            chyby.append(k)
if chyby:
    sys.exit("Neznáme id v ZVAZKY: " + ", ".join(sorted(set(chyby))))

CSS = """
.ft-wrap{overflow-x:auto;padding:8px 0 24px}
.ft{width:max-content;margin:0 auto}
.ft-title{font-size:1.15rem;margin:18px 0 6px}
.ft ul{position:relative;display:flex;justify-content:center;padding:18px 0 0;margin:0;list-style:none}
.ft li{position:relative;display:flex;flex-direction:column;align-items:center;padding:18px 6px 0}
.ft li::before,.ft li::after{content:"";position:absolute;top:0;width:50%;height:18px;border-top:1.5px solid #9b8d80}
.ft li::before{right:50%}
.ft li::after{left:50%;border-left:1.5px solid #9b8d80}
.ft li:only-child::before,.ft li:only-child::after{display:none}
.ft li:only-child{padding-top:0}
.ft li:first-child::before,.ft li:last-child::after{border:0 none}
.ft li:last-child::before{border-right:1.5px solid #9b8d80;border-radius:0 6px 0 0}
.ft li:first-child::after{border-radius:6px 0 0 0}
.ft ul ul::before{content:"";position:absolute;top:0;left:50%;height:18px;border-left:1.5px solid #9b8d80}
.ft>ul{padding-top:0}
.ft>ul>li{padding-top:0}
.ft>ul>li::before,.ft>ul>li::after{display:none}
.ft-couple{display:flex;align-items:stretch;gap:0;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.12)}
.ft-p{background:#fff;border:1.5px solid #c9bcae;padding:5px 8px;min-width:118px;max-width:170px;font:12px/1.3 Arial,Helvetica,sans-serif;color:#2b2420;text-align:left}
.ft-p b{display:block;font-size:12.5px}
.ft-p span{display:block;color:#6b5e54;font-size:11px}
.ft-p i{display:block;color:#8a7a6a;font-size:10.5px;font-style:italic}
.ft-couple .ft-p:first-child{border-radius:8px 0 0 8px}
.ft-couple .ft-p:last-child{border-radius:0 8px 8px 0}
.ft-couple .ft-p:only-child{border-radius:8px}
.ft-link{display:flex;align-items:center;justify-content:center;background:#f3ede6;border-top:1.5px solid #c9bcae;border-bottom:1.5px solid #c9bcae;padding:0 4px;font:11px Arial,sans-serif;color:#6b5e54;white-space:nowrap}
.ft-p.ft-blood{border-color:#2f7f86;background:#f2f8f8}
.ft-p.ft-empty{border-style:dashed;color:#aaa;background:#fbfaf8}
.ft-p.ft-ref{border-style:dotted}
.ft-rod{font-style:italic}
.ft-legend{font:12px Arial,sans-serif;color:#6b5e54;margin:4px 0 12px}
.ft-legend em{display:inline-block;width:12px;height:12px;vertical-align:-2px;margin:0 4px 0 10px;border:1.5px solid #2f7f86;background:#f2f8f8;border-radius:3px}
.ft-p.ft-prob{border-color:#c9a227;background:#fdf8e6}
.ft-p.ft-hyp{border:2px dashed #d9822b;background:#fff4e8}
.ft-p small{display:block;color:#a0602a;font-size:10px;margin-top:2px}
.ft-link.ft-link-hyp{color:#d9822b;font-weight:bold;border-color:#d9822b;border-style:dashed}
.ft-legend em.lg-prob{border-color:#c9a227;background:#fdf8e6}
.ft-legend em.lg-hyp{border:2px dashed #d9822b;background:#fff4e8}
"""


def box(pid, blood=True, ref=False):
    if not pid:
        return '<div class="ft-p ft-empty"><b>?</b><span>partner/ka – doplniť</span></div>'
    o = OSOBY[pid]
    roky = []
    if o.get("nar"):
        roky.append("* " + o["nar"].strip())
    if o.get("zom"):
        roky.append("† " + o["zom"].strip())
    ist = o.get("ist", "")
    cls = ("ft-p" + (" ft-blood" if blood and ist not in ("prob", "hyp") else "") + (" ft-ref" if ref else "")
           + (" ft-prob" if ist == "prob" else "") + (" ft-hyp" if ist == "hyp" else ""))
    s = f'<div class="{cls}"><b>{html.escape(o["n"])}</b>'
    if o.get("rod"):
        s += f'<span class="ft-rod">rod. {html.escape(o["rod"])}</span>'
    for r in roky:
        s += f"<span>{html.escape(r)}</span>"
    if not roky and not ref:
        s += "<span>dátumy – doplniť</span>"
    if o.get("pozn"):
        s += f"<i>{html.escape(o['pozn'])}</i>"
    if o.get("preco"):
        stitok = {"hyp": "predpoklad: ", "prob": "pravdepodobné: ", "doc": "doklad: "}.get(ist, "")
        s += f"<small>{html.escape(stitok + o['preco'])}</small>"
    if ref:
        s += "<i>(pozri v strome vyššie)</i>"
    return s + "</div>"


def zvazky_osoby(pid):
    return [z for z in ZVAZKY if z["a"] == pid or z.get("b") == pid]


def node(pid, seen):
    """Jedna osoba so svojimi zväzkami a deťmi."""
    if pid in seen:
        return f"<li>{box(pid, True, ref=True)}</li>"
    seen.add(pid)
    zv = zvazky_osoby(pid)
    if not zv:
        return f"<li>{box(pid)}</li>"
    out = []
    for z in zv:
        partner = z["b"] if z["a"] == pid else z["a"]
        if z.get("sobas") is None:
            spoj = "partneri"
        elif z.get("sobas"):
            spoj = "× " + z["sobas"]
        else:
            spoj = "×"
        lcls = "ft-link"
        if z.get("ist") == "hyp":
            spoj += " · predpoklad"
            lcls += " ft-link-hyp"
        couple = f'<div class="ft-couple">{box(pid)}<div class="{lcls}">{html.escape(spoj)}</div>{box(partner, blood=False)}</div>'
        deti = z.get("deti", [])
        if z.get("strom") and z is not KOREN_ZVAZOK:
            # potomkovia sa kreslia v samostatnom strome (KORENE s dvojicou), tu len odkaz
            stub = f'<li><div class="ft-p ft-empty"><b>deti</b><span>pozri strom „{html.escape(z["strom"])}“</span></div></li>'
            out.append(f"<li>{couple}<ul>{stub}</ul></li>")
            continue
        if z.get("bez_deti"):
            out.append(f"<li>{couple}</li>")
            continue
        if deti:
            inner = "".join(node(d, seen) for d in deti)
        else:
            inner = '<li><div class="ft-p ft-empty"><b>deti?</b><span>doplniť</span></div></li>'
        out.append(f"<li>{couple}<ul>{inner}</ul></li>")
    # viac zväzkov jednej osoby (napr. Anna) – vedľa seba
    if len(out) == 1:
        return out[0]
    return "<li><ul>" + "".join(out) + "</ul></li>"


KOREN_ZVAZOK = None


def strom():
    global KOREN_ZVAZOK
    seen = set()
    parts = []
    for nadpis, koren in KORENE:
        if isinstance(koren, tuple):
            # koreň = zväzok (a, b) so strom="…" – jeho potomkovia ako samostatný strom
            KOREN_ZVAZOK = next(z for z in ZVAZKY if (z["a"], z.get("b")) == koren)
            seen.discard(koren[0])
            koren = koren[0]
            zv_backup = ZVAZKY[:]
            ZVAZKY[:] = [z for z in ZVAZKY if not (koren in (z["a"], z.get("b")) and z is not KOREN_ZVAZOK)]
            parts.append(f'<section style="break-inside:avoid"><h2 class="ft-title">{html.escape(nadpis)}</h2>'
                         f'<div class="ft-wrap"><div class="ft"><ul>{node(koren, seen)}</ul></div></div></section>')
            ZVAZKY[:] = zv_backup
            KOREN_ZVAZOK = None
            continue
        parts.append(f'<section style="break-inside:avoid"><h2 class="ft-title">{html.escape(nadpis)}</h2>'
                     f'<div class="ft-wrap"><div class="ft"><ul>{node(koren, seen)}</ul></div></div></section>')
    leg = ('<p class="ft-legend"><em></em>pokrvní príbuzní &nbsp;·&nbsp; biele rámčeky = manželia a partneri'
           ' &nbsp;·&nbsp; prerušované = treba doplniť &nbsp;·&nbsp; „×“ = sobáš, „partneri“ = nezosobášení</p>')
    if PRED:
        leg = ('<p class="ft-legend"><em></em>doložené zápisom <em class="lg-prob"></em>pravdepodobné'
               ' <em class="lg-hyp"></em>predpoklad – nedoložené &nbsp;·&nbsp; oranžová väzba = predpoklad,'
               ' kto je čie dieťa. <b>Nie je to overený rodokmeň</b> – po potvrdení zápisom sa osoba presunie'
               ' do hlavného stromu.</p>')
    return leg + "".join(parts)


body = strom()
frag = f"<style>{CSS}</style>{body}"

gen = os.path.join(ROOT, "web", "src", "generated")
os.makedirs(gen, exist_ok=True)
open(os.path.join(gen, MENO + ".html"), "w", encoding="utf-8").write(frag)

out_dir = os.path.join(ROOT, "dokumenty", "pre_rodinu")
os.makedirs(out_dir, exist_ok=True)
page = f"""<!doctype html><html lang="sk"><head><meta charset="utf-8"><title>{"Strom predpokladov" if PRED else "Rodinný strom"}</title>
<style>@page{{size:A3 landscape;margin:12mm}} body{{font-family:Georgia,serif;color:#2b2420;margin:16px}}
h1{{font-weight:normal;margin:0 0 4px}} .sub{{color:#6b5e54;font-style:italic;margin:0 0 8px}}
@media print{{.ft-wrap{{overflow:visible}}}} {CSS}</style></head><body>
<h1>{"Strom predpokladov – nepotvrdené" if PRED else "Rodinný strom"}</h1><p class="sub">Súkromné – pre najbližšiu rodinu. Stav k {STAV}.{(" " + html.escape(PODPIS)) if PODPIS else ""}</p>
{body}
<script>
// na tlač: každý strom zmenšiť tak, aby sa zmestil na šírku strany
function fit(){{document.querySelectorAll('.ft').forEach(function(t){{t.style.zoom=1;var w=t.parentElement.clientWidth,s=t.scrollWidth;if(s>w)t.style.zoom=(w/s).toFixed(3);}});}}
fit(); window.addEventListener('beforeprint',fit); window.addEventListener('resize',fit);
</script></body></html>"""
open(os.path.join(out_dir, MENO + ".html"), "w", encoding="utf-8").write(page)
print("OK:", len(OSOBY), "osôb,", len(ZVAZKY), "zväzkov ->",
      f"web/src/generated/{MENO}.html, dokumenty/pre_rodinu/{MENO}.html")
