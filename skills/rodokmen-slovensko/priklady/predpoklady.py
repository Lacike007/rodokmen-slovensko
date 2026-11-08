# Strom predpokladov – PRAVDEPODOBNÉ a NEPOTVRDENÉ vetvy, oddelene od overeného rodokmeňa.
# Skopíruj do data/predpoklady.py; kreslí ho:  python3 -I tools/rodinny_strom.py --predpoklady
#
# Formát ako rodina.py, navyše:
#   ist="doc" doložené zápisom · ist="prob" pravdepodobné (žltý) · ist="hyp" predpoklad (oranžový prerušovaný)
#   preco="…"  prečo si to myslíme / čo to rozhodne
#   v ZVAZKY: ist="hyp" pri väzbe, ktorá je len predpokladom (napr. kto je čia mama)
# Keď sa predpoklad potvrdí zápisom, osoba sa presunie do rodina.py a odtiaľto sa zmaže.
# (Toto je vymyslená ukážka.)

OSOBY = {
    "stefan": dict(n="Štefan Kováč", nar="asi 1870", zom="1920", pozn="", ist="doc", preco="úmrtie čítané v matrike"),
    "zuzana": dict(n="Zuzana Kováčová", nar="1880", zom="", pozn="", ist="prob", preco="jediná Zuzana v obci v tom veku"),
    "maria": dict(n="Mária Kováčová", nar="1905", zom="1980", pozn="", ist="doc"),
}

ZVAZKY = [
    dict(a="stefan", b="zuzana", sobas="", deti=["maria"], ist="hyp"),
]

KORENE = [("Kováčovci – predpoklad", "stefan")]
