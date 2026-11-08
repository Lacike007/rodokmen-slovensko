# Rodina – strom potomkov (kto je s kým a kto je čie dieťa), pre najbližšiu rodinu.
# Skopíruj do data/rodina.py; obrázok stromu vyrobí:  python3 -I tools/rodinny_strom.py
#
# OSOBY:  "id": dict(n="Meno Priezvisko", nar="1. 1. 1950 Príkladov", zom="", pozn="krátka poznámka")
#         n = meno, ktoré osoba nosila/nosí (u vydatých žien po sobáši); rod="Kováčová" = rodné priezvisko
#         (zobrazí sa „rod. …“; vynechať, ak sa nemenilo); neznáme nechať prázdne ""; neistý údaj s (?)
# ZVAZKY: dict(a="id", b="id", sobas="1. 5. 1975 Príkladov", deti=["id", ...])
#         sobas=None  -> neboli zosobášení (partneri);  sobas="" -> zosobášení, dátum nepoznáme
#         deti v poradí od najstaršieho; bez_deti=True -> nemajú deti (nezobrazí sa „deti? doplniť“)
#         strom="Nadpis" -> potomkovia tohto zväzku sa kreslia ako samostatný strom (pozri KORENE)
#         viac zväzkov jednej osoby (2. manželstvo) – v poradí, v akom ich chceš vidieť
# KORENE: od koho sa kreslia stromy (každý koreň = jeden strom); koreň ("a", "b") = zväzok so strom="nadpis"
# PODPIS: voliteľný text do hlavičky (napr. komu posielať opravy)
#
# Súkromné – len pre rodinu, nikam nezverejňovať.  (Toto je vymyslená ukážka.)

PODPIS = "Opravy a doplnky prosím Janovi."

OSOBY = {
    "jozef": dict(n="Jozef Novák", nar="3. 3. 1901 Bardejov", zom="1975", pozn="stolár"),
    "maria": dict(n="Mária Nováková", rod="Kováčová", nar="1905", zom="1980", pozn=""),
    "peter": dict(n="Peter Horák", nar="", zom="1940", pozn="1. manžel Márie (?)"),
    "anna": dict(n="Anna Horáková", nar="1925", zom="", pozn=""),
    "jan": dict(n="Ján Novák", nar="12. 5. 1930", zom="2010", pozn=""),
    "eva": dict(n="Eva Nováková", rod="Malá", nar="1932", zom="", pozn=""),
    "jan_ml": dict(n="Ján Novák", nar="1958", zom="", pozn="ten, kto robí rodokmeň"),
    "zuzana": dict(n="Zuzana Bieliková", rod="Nováková", nar="1961", zom="", pozn=""),
    "milan": dict(n="Milan Bielik", nar="1960", zom="", pozn=""),
}

ZVAZKY = [
    dict(a="maria", b="peter", sobas="", deti=["anna"]),
    dict(a="maria", b="jozef", sobas="1929 Bardejov", deti=["jan"], strom="Novákovci"),
    dict(a="jan", b="eva", sobas="", deti=["jan_ml", "zuzana"]),
    dict(a="zuzana", b="milan", sobas=None, deti=[]),
    dict(a="jan_ml", b="", sobas=None, bez_deti=True),
]

KORENE = [
    ("Mária Kováčová a jej deti", "maria"),
    ("Novákovci", ("maria", "jozef")),
]
