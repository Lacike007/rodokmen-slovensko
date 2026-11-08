# Rodokmeň – slovenský doplnok pre Claude Code

Doplnok k skillu **[rodokmen](https://github.com/sarsonj/rodokmen-skill)** (Jindřich Šaršon), ktorý vedie
začiatočníkov od rodinných spomienok cez matriky až k rodinnému webu. Hlavný skill je stavaný na české archívy;
tento doplnok pridáva to, čo treba pre **predkov zo Slovenska a bývalého Uhorska**:

- **FamilySearch** – kde sú slovenské matriky, vyhľadávanie v indexe z prihláseného okna, vlastné okno prehliadača
  (`scripts/fs_okno.py`), keď rozšírenie Claude in Chrome nefunguje
- **maďarské a latinské zápisy** – slovník stavov, povolaní, uhorských názvov obcí
- **žiadosti na matričné úrady** (zákon 154/1994 Z. z.) ako Word – a **skúsenosti**, čo úrady a archívy
  naozaj odpovedajú, poplatky, na čo si dať pozor (`reference/ziadosti_skusenosti.md`)
- **rodinné doklady** (rodné, sobášne, úmrtné, domovské listy) – čo z ktorého vyťažiť
- **strom potomkov a strom predpokladov** pre rodinu – web, PDF na tlač, veľký obrázok na tablet
- **sčítanie ľudu 1930** zo Slovakiany – index hárkov obce podľa ulice a čísla domu (`tools/slovakiana.py`)
- **web po slovensky** – prepínač SK/CZ v hlavičke rodinného webu, strom s rozbaľovaním vetiev

## Inštalácia
Najprv nainštaluj hlavný skill podľa [jeho návodu](https://github.com/sarsonj/rodokmen-skill). Potom v Claude Code:

```
/plugin marketplace add Lacike007/rodokmen-slovensko
/plugin install rodokmen-slovensko@rodokmen-slovensko
```

a reštartuj Claude Code. Skill sa použije sám, keď ide o slovenských predkov; prípadne napíš „použi skill rodokmen-slovensko“.

## Prispievanie
Vítané sú skúsenosti (ako odpovedal ktorý úrad či archív, nové zdroje, opravy slovníka) aj opravy nástrojov –
cez **Issues** alebo **pull request**. Každú zmenu pred zaradením prečíta a schváli správca.
Pozri [CONTRIBUTING.md](CONTRIBUTING.md) – hlavne: **žiadne osobné údaje** (mená žijúcich ľudí, adresy, skeny dokladov).

## Poďakovanie
Časti sú prevzaté (MIT) z forkov hlavného skillu: sčítanie 1930 zo Slovakiany (jozefizso), postupy pre FamilySearch (xsigik),
nápad rozbaľovania stromu (jozefizso, mplisek).

## Licencia
MIT – pozri [LICENSE](LICENSE).
