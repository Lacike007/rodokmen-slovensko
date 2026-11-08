#!/usr/bin/env python3
"""Vlastné okno prehliadača (Playwright Chromium) pre FamilySearch a iné stránky s prihlásením – nezávislé od Vivaldi.

Okno beží samostatne s vlastným profilom (~/.local/share/rodokmen-fs-profil); používateľ sa v ňom raz prihlási sám,
prihlásenie ostane. Claude sa k oknu pripája cez lokálny ladiaci port (len 127.0.0.1) a číta stránky / volá JS.
Bezpečnosť: port je náhodný a zapísaný len v súbore čitateľnom pre používateľa (0600), profil má práva 0700.
Kým okno beží, iný program na tom istom počítači by sa k nemu mohol pripojiť – po práci ho zatvor (`stop`).

Použitie (venv s playwright, napr. python3 -m venv ~/.local/share/rodokmen-pdf && …/pip install playwright && …/python -m playwright install chromium):  PY=~/.local/share/rodokmen-pdf/bin/python
  $PY scripts/fs_okno.py start [url] [--skryte]  otvorí okno (ak ešte nebeží); predvolene familysearch.org;
                                              --skryte = bez viditeľného okna (na pozadí, neruší používateľa)
  $PY scripts/fs_okno.py stav                 beží? adresa a názov aktuálnej stránky
  $PY scripts/fs_okno.py otvor <url>          prejde na adresu, vypíše názov
  $PY scripts/fs_okno.py text [url]           text stránky (voliteľne najprv otvorí url)
  $PY scripts/fs_okno.py js <kód|@súbor.js> [url]   vyhodnotí JS v stránke (výraz alebo "async () => {...}"), výsledok ako JSON
  $PY scripts/fs_okno.py obrazok <out.png>    snímka obrazovky stránky
  $PY scripts/fs_okno.py snimok <ark 3:1:…> <out.jpg>   stiahne snímku FamilySearch v plnom rozlíšení ($dist) cez prihlásené okno
  $PY scripts/fs_okno.py stop                 zatvorí okno
Heslá nikdy nezadáva Claude – prihlásenie robí používateľ v okne.
"""
import base64, json, os, pathlib, re, signal, socket, subprocess, sys, time, urllib.request

from playwright.sync_api import sync_playwright

PROFIL = pathlib.Path.home() / ".local/share/rodokmen-fs-profil"
STAV = PROFIL.parent / "rodokmen-fs-okno.json"  # port a PID bežiaceho okna (práva 0600)


def nacitaj():
    try:
        return json.loads(STAV.read_text())
    except Exception:
        return None


def cdp():
    s = nacitaj()
    return f"http://127.0.0.1:{s['port']}" if s else None


def bezi():
    if not cdp():
        return False
    try:
        urllib.request.urlopen(cdp() + "/json/version", timeout=2)
        return True
    except Exception:
        return False


def volny_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def start(url, skryte=False):
    if bezi():
        print("Okno už beží.")
        return
    with sync_playwright() as p:
        exe = p.chromium.executable_path
    PROFIL.mkdir(parents=True, exist_ok=True)
    os.chmod(PROFIL, 0o700)
    port = volny_port()
    proc = subprocess.Popen([exe, f"--user-data-dir={PROFIL}", f"--remote-debugging-port={port}",
                      "--remote-debugging-address=127.0.0.1", "--no-first-run", "--no-default-browser-check",
                      "--window-size=1400,950", "--force-device-scale-factor=2",
                      *(["--headless=new"] if skryte else []), url],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)
    fd = os.open(STAV, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump({"port": port, "pid": proc.pid}, f)
    for _ in range(30):
        if bezi():
            print("Okno otvorené:", url)
            return
        time.sleep(0.5)
    sys.exit("Okno sa nepodarilo otvoriť.")


def stranka(p):
    if not bezi():
        sys.exit("Okno nebeží – najprv: fs_okno.py start")
    br = p.chromium.connect_over_cdp(cdp())
    ctx = br.contexts[0]
    pages = [pg for pg in ctx.pages if not pg.url.startswith("devtools://")]
    return br, (pages[-1] if pages else ctx.new_page())


def chod(pg, url):
    pg.goto(url, wait_until="domcontentloaded", timeout=60000)
    try:
        pg.wait_for_load_state("networkidle", timeout=15000)
    except Exception:
        pass


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    cmd = a[0]
    if cmd == "start":
        b = [x for x in a[1:] if x != "--skryte"]
        return start(b[0] if b else "https://www.familysearch.org/", "--skryte" in a)
    if cmd == "stop":   # bez pripojenia – ukončí proces podľa PID (funguje aj keď sa k oknu nedá pripojiť)
        s = nacitaj()
        try:
            os.kill(s["pid"], signal.SIGTERM)
        except Exception:
            pass
        STAV.unlink(missing_ok=True)
        return print("Okno zatvorené.")
    with sync_playwright() as p:
        br, pg = stranka(p)
        if cmd == "stav":
            print(pg.url, "|", pg.title())
        elif cmd == "otvor":
            chod(pg, a[1]); print(pg.url, "|", pg.title())
        elif cmd == "text":
            if len(a) > 1:
                chod(pg, a[1])
            print(pg.inner_text("body"))
        elif cmd == "js":
            kod = a[1]
            if kod.startswith("@"):
                kod = pathlib.Path(kod[1:]).read_text(encoding="utf-8")
            if len(a) > 2:
                chod(pg, a[2])
            print(json.dumps(pg.evaluate(kod), ensure_ascii=False, indent=1))
        elif cmd == "obrazok":
            pg.screenshot(path=a[1]); print("uložené", a[1])
        elif cmd == "snimok":
            ark, out = a[1], a[2]
            if not re.fullmatch(r"3:1:[A-Z0-9-]{4,30}", ark):
                sys.exit("Neplatné ark – očakávam tvar 3:1:XXXX-XXXX-XXX")
            res = pg.evaluate("""async (ark) => {
              const r = await fetch(`https://www.familysearch.org/service/records/storage/deepzoomcloud/dz/v1/${ark}/$dist`, {credentials: 'include'});
              if (!r.ok) return {err: r.status};
              const b = new Uint8Array(await r.arrayBuffer()); let s = '';
              for (let i = 0; i < b.length; i += 32768) s += String.fromCharCode(...b.subarray(i, i + 32768));
              return {data: btoa(s)};
            }""", ark)
            if "err" in res:
                sys.exit(f"HTTP {res['err']} – snímka nejde stiahnuť (prihlásenie? obmedzená snímka?)")
            pathlib.Path(out).write_bytes(base64.b64decode(res["data"])); print("uložené", out)
        elif cmd == "stop":
            br.close()
            try:
                os.kill(nacitaj()["pid"], signal.SIGTERM)
            except Exception:
                pass
            STAV.unlink(missing_ok=True)
            print("Okno zatvorené.")
        else:
            sys.exit(__doc__)


if __name__ == "__main__":
    main()
