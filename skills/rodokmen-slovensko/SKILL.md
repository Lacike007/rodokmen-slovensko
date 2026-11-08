---
name: rodokmen-slovensko
description: Slovenský doplnok k skillu rodokmen – matriky na Slovensku a v bývalom Uhorsku (FamilySearch, maďarské a latinské zápisy), žiadosti na matričné úrady vo Worde, rodinné dokumenty (PDF skeny), domovské právo, hroby. Použi spolu so skillom rodokmen vždy, keď ide o slovenské/uhorské predky, žiadosť na matriku alebo triedenie rodinných dokumentov.
---

# Rodokmeň – slovenský doplnok

Dopĺňa skill **rodokmen** (ten je pre české archívy). Všetko z neho platí; tu sú len veci navyše pre Slovensko.
Komunikuj **po slovensky**.

## 1. Kde sú slovenské matriky
- **FamilySearch** – zbierka „Slovakia, Church and Synagogue Books, 1592–1935“ (cc=1554443). Väčšina kníh
  je online **len do ~1895–1905**, index (vyhľadávanie mien) je neúplný a končí zväčša okolo 1895.
  Používateľ sa prihlasuje sám (heslo nikdy nezadávaj).
- Mladšie záznamy: **štátne matriky od 1. 10. 1895** sú na matričných úradoch. Knihy idú do štátneho archívu
  až **100 rokov od posledného zápisu** (zákon 154/1994 § 5 ods. 3).
- Hľadaj vo farnosti, nie v obci: obec býva filiálka susednej farnosti. Farnosť zistíš z FS katalógu
  alebo zo schematizmu diecézy. Gréckokatolíci a rímskokatolíci majú oddelené knihy.
- Druhopisy (duplikáty) majú na FS často celé roky po sebe: krsty → sobáše → úmrtia, rok ≈ 6–8 snímok,
  sobáše bývajú 1 strana na rok.

## 2. Vyhľadávanie v indexe FamilySearch bez klikania
V otvorenej (prihlásenej) karte FamilySearch spusti cez `javascript_tool` kód z `reference/fs_index.js`.
Vráti riadky „meno | udalosti | rodičia | id“. Výstup nástroja sa reže (~2,5 kB) – výsledok ulož do
`window.out` a filtruj (napr. podľa farnosti). Detail záznamu cez API vracia 401 – otvor stránku
`https://www.familysearch.org/ark:/61903/1:1:<id>` a prečítaj ju (`get_page_text`).

## 3. Prehliadač snímok FamilySearch (praktické)
- Keď Claude in Chrome nefunguje (skúsenosť: vo Vivaldi karty vypadávali zo skupiny aj po reštarte), použi vlastné okno `scripts/fs_okno.py` (v priečinku tohto skillu) (Playwright Chromium, profil `~/.local/share/rodokmen-fs-profil`, náhodný lokálny port; **po práci vždy `stop`** – kým okno beží, mohol by sa k nemu pripojiť iný program na počítači): `PY=~/.local/share/rodokmen-pdf/bin/python; $PY <SKILL_DIR>/scripts/fs_okno.py start` → používateľ sa prihlási sám (Apple passkey cez QR/iPhone), potom `text <url>`, `js @subor.js`, `snimok <ark> out.jpg`, `obrazok out.png`. Index API: `fetch('/service/search/hr/v2/personas?…', {credentials:'include', headers:{accept:'application/json'}})`.
- Číslo snímky zadaj do poľa „Obrázok“ (triple-click, napíš číslo, Enter). V URL je `i` = číslo − 1.
- Približovanie: koliesko myši nad miestom (scroll up = zoom in). Pred `zoom` výrezom **odsuň kurzor** – inak zakryje text.
- Občas zamrzne snímanie obrazovky (CDP timeout) – počkaj 3 s a skús znova.
- Ak sa „stratí“ skupina kariet hneď po otvorení FS, zavolaj `tabs_context_mcp` s `createIfEmpty` a skús znova;
  pri opakovaní reštart `claude --chrome --continue`.

## 4. Maďarské a latinské výrazy v zápisoch
Pozri `reference/slovnik.md` (stav, náboženstvo, povolania, legitimita, uhorské názvy obcí).

## 5. Žiadosti na matričné úrady (zákon 154/1994 Z. z.)
- **§ 18 ods. 2**: výpis dostane osoba a **člen rodiny** – manžel, rodičia, deti, vnuci, pravnuci,
  prapravnuci, **súrodenci a ich deti**. Príbuzenstvo dolož rodnými listami (vnuk: svoj + rodiča).
- **§ 18 ods. 5**: **doslovný výpis sa vydáva len úradom** – nežiadaj ho. Žiadaj rodný / sobášny / úmrtný list
  a popros o ďalšie údaje zo zápisu, prípadne **nahliadnutie do matriky** (osobne, v prítomnosti matrikára).
- Výpis z elektronickej matriky vydá ktorýkoľvek matričný úrad; staré zápisy však bývajú len na úrade podľa miesta udalosti.
- Písomná žiadosť: matrika môže chcieť úradne overený podpis alebo podanie cez slovensko.sk. Odporuč najprv zavolať.
- **Údaje žiadateľa** sú v `data/ziadatel.md` – doplň ich automaticky. Žiadosť vytvor ako .docx:
  `python3 -I .claude/skills/rodokmen-slovensko/scripts/ziadost_docx.py <spec.json> dokumenty/ziadosti/<názov>.docx`
  (formát spec.json je v hlavičke skriptu; treba `python-docx`, napr. vo venv v scratchpade).
- Každá žiadosť má vlastný priečinok `dokumenty/ziadosti/<n>_<úrad>_<čo>/`: žiadosť, kópie príloh (`priloha_1_…pdf`) a `CO_POSLAT.txt` (komu, čo sa spýtať telefonicky, zaškrtávací zoznam).
- **Praktické skúsenosti** (čo matriky a archívy skutočne odpovedali, poplatky, lehoty): `reference/ziadosti_skusenosti.md`.
- **Hotový .docx, ktorý už používateľ otvoril alebo upravil, nikdy neprepisuj** – vytvor nový súbor
  alebo navrhni zmenu textom. Pred presunom súboru over `lsof`, či nie je otvorený vo Worde.

## 6. Rodinné dokumenty (skeny)
- Ukladaj do `dokumenty/<typ>/RRRR_typ_meno.pdf`: `rodne_listy/`, `sobasne_listy/`, `umrtne_listy/`,
  `domovske_listy/`, `ziadosti/`, `hroby/`, prípadne `fotky/`, `ine/`. Celé `dokumenty/` je v `.gitignore`.
- PDF skeny: obrázky vytiahni `scripts/pdf_nastroje.py obrazky <pdf> <prefix>` (netreba ghostscript),
  otoč `magick x.jpg -rotate -90 y.jpg`, čítaj výrezy. Viac skenov jedného dokumentu spoj
  `scripts/pdf_nastroje.py spoj vystup.pdf a.pdf b.pdf`.
- Čo z ktorého dokumentu vyťažiť:
  - **rodný list 20. storočia**: rodičia, ich vek → rok narodenia; od ~1950 aj **rodičia rodičov** (cenné!).
  - **sobášny list**: rodičia oboch snúbencov vrátane rodného priezviska matky, bydliská, svedkovia.
  - **úmrtný list**: dátum a miesto narodenia zomrelého. Rodičia v slovenských úmrtných listoch z 2. pol. 20. stor.
    často **nie sú** (skúsenosť: listy z r. 1969, 1986 a 2002 – ani jeden) – na rodičov radšej rodný alebo sobášny list.
  - **domovský list**: obec domovskej príslušnosti. Dieťa bez uvedeného otca malo **domovskú obec matky**
    → silná stopa, odkiaľ matka pochádzala. Domovské právo sa dedilo po otcovi, u žien po manželovi.
- Rozpory medzi rodinou a dokumentom zapíš do `udaje_od_rodiny.md`; dokument má prednosť, ale používateľ rozhoduje.

## 6b. Výstupy pre rodinu: strom potomkov, strom predpokladov, PDF, obrázok
Vejár predkov nestačí – rodina chce vidieť aj **potomkov** (kto s kým, deti, vnúčatá, nezosobášení partneri,
viac manželstiev). Nástroje sú v `tools/` tohto skillu, web stránky vo `web/`, ukážkové dáta v `priklady/`.
- **Inštalácia do projektu:** skopíruj `tools/*.py` do `<projekt>/tools/`, `web/*.astro` do `<projekt>/web/src/pages/`
  (a do menu v `web/src/layouts/Base.astro` pridaj `['/strom/', 'Strom']`, `['/predpoklady/', 'Predpoklady']`),
  `priklady/rodina.py` a `priklady/predpoklady.py` do `<projekt>/data/` a prepíš na skutočnú rodinu.
  Do `web/package.json` k skriptu `data` pridaj `&& python3 -I ../tools/rodinny_strom.py && python3 -I ../tools/rodinny_strom.py --predpoklady`.
- **Strom potomkov:** `data/rodina.py` → `python3 -I tools/rodinny_strom.py` → `web/src/generated/rodinny_strom.html`
  (stránka /strom/ s posúvaním a zväčšovaním) a `dokumenty/pre_rodinu/rodinny_strom.html` (na tlač, A3 na šírku).
  Široká vetva (napr. druhé manželstvo) sa dá vyčleniť do samostatného stromu: zväzok `strom="Nadpis"` + koreň `("a", "b")`.
- **Strom predpokladov:** `data/predpoklady.py` → `--predpoklady` → /predpoklady/ – pravdepodobné a nepotvrdené
  vetvy oddelene od overeného rodokmeňa (farebne: doložené / pravdepodobné / predpoklad).
- **PDF:** `~/.local/share/rodokmen-pdf/bin/python tools/pdf.py <in.html> <out.pdf> [A4|A3] [--na-sirku]`
  (Playwright; inštalácia v hlavičke `pdf.py`). Nepoužívať Brave; Vivaldi headless na macOS zamŕza.
- **Obrázok na tablet:** `… tools/strom_obrazok.py dokumenty/pre_rodinu/rodinny_strom.html out.jpg` – stromy v plnej
  veľkosti (PDF ich zmenšuje na šírku strany). Cez WhatsApp poslať ako dokument.
- Po každej zmene `rodina.py` pregeneruj **všetko**: web (`npm run data && npm run build`), PDF aj obrázok –
  rodina pozerá to, čo dostala.

## 7. Iné slovenské zdroje
- **Hroby**: virtuálne cintoríny miest (Prešov – Technické služby mesta Prešov, cintorin@tsmp.sk) – dátumy, číslo hrobu.
- **Noviny** (parte, nehody): Štátna vedecká knižnica (Prešov, Košice, B. Bystrica), digitálna knižnica Slovakiana.
- **Ulice** sa premenovávali (napr. Hlinkova → Stalinova → …) – adresu v dokumente porovnaj s dobou.
- **Vojnové obete 2. sv. v.**: Vojenský historický archív Bratislava, VÚA Praha (kartotéka), miestne pamätníky.
- **Sčítania**: Sáros 1869 (FS katalóg), uhorské súpisy.

## 8. Súkromie
Žiadosti, kontakty, skeny dokladov a snímky hrobov nikdy do gitu ani na web. Nemanželský pôvod, choroby,
príčiny smrti a žijúci ľudia – na web len so súhlasom (`kontrola.py` hlási CITLIVÉ).
