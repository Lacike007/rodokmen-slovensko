# Prepínač jazyka SK / CZ na rodinnom webe

Šablóna webu hlavného skillu je po česky. Tento doplnok pridá tlačidlo **SK/CZ** do hlavičky: preloží texty rozhrania
(menu, nadpisy, popisky) do slovenčiny, údaje rodokmeňa nechá tak. Voľba sa pamätá v prehliadači.

1. Skopíruj `web/preklad_sk.js` do `<projekt>/web/src/lib/preklad_sk.js`.
2. V `web/src/layouts/Base.astro` za tlačidlo `menu-btn` pridaj
   `<button class="jazyk-btn" type="button" title="Jazyk rozhrania / Jazyk rozhraní" data-no-preklad>SK</button>`
   a pred `<main …>` vlož skript nižšie.
3. Na koniec `web/src/styles/global.css` pridaj CSS nižšie.
4. Predvolený jazyk: v `data/web.json` `"jazyk": "sk"` (bez neho je predvolená čeština).
5. Nový text šablóny, ktorý ostal po česky: pridaj ho do `PRESNE` v `preklad_sk.js` (presná zhoda celého textu),
   texty s číslami do `VZORY`. Kontrola: prejdi stránky v SK a hľadaj ě, ř, ů.

Pri aktualizácii hlavného skillu (`novy_projekt.py`) sa úpravy Base.astro a global.css zlúčia ako vlastné úpravy webu.

## Skript do Base.astro
```astro
    <script is:inline define:vars={{ predvoleny: config.jazyk || 'cs' }}>
      window.__jazykPredvoleny = predvoleny;
    </script>
    <script>
      import { prelozText } from '../lib/preklad_sk.js';
      const KLUC = 'rodokmen-jazyk';
      let jazyk = window.__jazykPredvoleny;
      try { jazyk = localStorage.getItem(KLUC) || jazyk; } catch {}
      const ATR = ['placeholder', 'title', 'aria-label', 'alt'];
      const povodne = new WeakMap();   // text uzla pred prekladom – návrat na CZ bez obnovenia stránky
      const vynechat = (el) => el?.closest?.('script,style,[data-no-preklad]');
      function prelozUzol(n) {
        if (n.nodeType === 3) {
          if (vynechat(n.parentElement)) return;
          if (!povodne.has(n)) povodne.set(n, n.nodeValue);
          const p = povodne.get(n);
          const novy = jazyk === 'sk' ? prelozText(p) : p;
          if (n.nodeValue !== novy) n.nodeValue = novy;
        } else if (n.nodeType === 1 && !vynechat(n)) {
          for (const a of ATR) {
            if (!n.hasAttribute(a)) continue;
            const k = 'data-cz-' + a;
            if (!n.hasAttribute(k)) n.setAttribute(k, n.getAttribute(a));
            const p = n.getAttribute(k);
            n.setAttribute(a, jazyk === 'sk' ? prelozText(p) : p);
          }
          for (const c of n.childNodes) prelozUzol(c);
        }
      }
      const titulCz = document.title;
      function prelozVsetko() {
        document.documentElement.lang = jazyk === 'sk' ? 'sk' : 'cs';
        document.title = jazyk === 'sk' ? titulCz.split(' · ').map(prelozText).join(' · ') : titulCz;
        prelozUzol(document.body);
        const b = document.querySelector('.jazyk-btn');
        if (b) { b.textContent = jazyk === 'sk' ? 'CZ' : 'SK'; b.title = jazyk === 'sk' ? 'Přepnout do češtiny' : 'Prepnúť do slovenčiny'; }
      }
      prelozVsetko();
      // dynamický obsah (vejár, mapa, hľadanie)
      new MutationObserver((zmeny) => {
        if (jazyk !== 'sk') return;
        for (const z of zmeny) for (const n of z.addedNodes) prelozUzol(n);
      }).observe(document.body, { childList: true, subtree: true });
      document.querySelector('.jazyk-btn')?.addEventListener('click', () => {
        jazyk = jazyk === 'sk' ? 'cs' : 'sk';
        try { localStorage.setItem(KLUC, jazyk); } catch {}
        prelozVsetko();
      });
    </script>
```

## CSS
```css
/* prepínač jazyka SK/CZ (lib/preklad_sk.js) */
.jazyk-btn { order: 10; margin-left: 0.6rem; font: inherit; font-size: 0.8rem; font-weight: 600; letter-spacing: 0.05em; color: #fbf3e6; background: transparent; border: 1px solid #8a7660; border-radius: 6px; padding: 0.15rem 0.5rem; cursor: pointer; }
.jazyk-btn:hover { background: #54443a; }
@media (max-width: 760px) { .jazyk-btn { order: 0; margin-left: 0.4rem; } }
```
