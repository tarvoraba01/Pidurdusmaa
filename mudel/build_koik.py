# -*- coding: utf-8 -*-
"""Ehitab lehe KAHES kujus.

MIKS KAHES. Artefaktina avaldades mähib ümbris sisu ise korralikku
HTML-dokumenti: lisab doctype'i, <html>, <head>, laiuse meta-sildi ja
väikese lähtestuse. Seepärast on page.html AINULT SISU -- ilma nendeta.

Staatilisel hostil (pagelive.io, Zone, kust iganes) seda ümbrist EI OLE.
Kui sama fail sinna panna, siis:
  * puudub <meta name="viewport"> -> telefonis renderdatakse leht
    töölaua laiusega ja kõik on tibatilluke. See üksi rikuks esmamulje.
  * puudub lang="et" -> ekraanilugejad ja tõlkijad arvavad, et tekst on
    inglise keeles
  * puudub kirjeldus ja jagamissildid -> Messengeris jagades tuleb
    tühi kastike

Seepärast on siin kaks väljundit ja ÜKS sisu. Sisu ei tohi kunagi
kahes kohas eraldi hooldada.
"""
import io
import re
import subprocess
import sys

ROOT = "/home/claude/web/"

# data.js ja engine.js on GENEREERITUD failid (pidurdus/export_web.py).
# Varem luges build.py neid lihtsalt kettalt -- ja siis, kui Pythoni pool
# oli muutunud, ehitas ta lehe VANADE andmetega, ilma ainsatki kaebust.
# Nii jaid ohe korra tipid lehele uuendamata ja number naitas vana asja.
# Nuud genereeritakse nad alati enne ehitamist.
subprocess.run([sys.executable, "-m", "pidurdus.export_web"],
               cwd="/home/claude", check=True,
               stdout=subprocess.DEVNULL)

# WordPressi teema (theme/pidurdusmaa) saab SAMA mootori ja samast
# allikast genereeritud andmed. Teema ei oma ühtegi oma arvutust.
subprocess.run([sys.executable, "-m", "pidurdus.export_wp"],
               cwd="/home/claude", check=True, stdout=subprocess.DEVNULL)
import shutil  # noqa: E402
shutil.copyfile(ROOT + "engine.js",
                "/home/claude/theme/pidurdusmaa/assets/js/engine.js")

body = open(ROOT + "page.html", encoding="utf-8").read()
data = open(ROOT + "data.js", encoding="utf-8").read()
engine = open(ROOT + "engine.js", encoding="utf-8").read()
assert "__DATA__" in body and "__ENGINE__" in body
body = body.replace("__DATA__", data).replace("__ENGINE__", engine)

# --- 1) artefakti kuju: ainult sisu, ümbris lisab ülejäänu ---
io.open(ROOT + "pidurdusmaa.html", "w", encoding="utf-8").write(body)

# --- 2) eraldiseisev kuju: täielik dokument ---
TITLE = "Pidurdusmaa kalkulaator — kui pikk on sinu pidurdusmaa?"
DESC = ("Arvuta oma auto ja rehvidega pidurdusmaa märjal, kuival, lumel, "
        "jääl ja kruusal. Füüsikamudel, kalibreeritud 369 mõõdetud "
        "pidurdusmaa vastu — koos ausa veapiiriga.")
# NB: og:image vajab ABSOLUUTSET URL-i sellel hostil, kus leht seisab.
# Kuni seda ei ole, jätame ta välja -- katkine pildi-URL näeb halvem
# välja kui pildi puudumine.
head = f'''<!doctype html>
<html lang="et">
<head>
<meta charset="utf-8">
<title>{TITLE}</title>
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="description" content="{DESC}">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#090c11">
<meta property="og:type" content="website">
<meta property="og:locale" content="et_EE">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><rect width=%22100%22 height=%22100%22 rx=%2218%22 fill=%22%23090c11%22/><path d=%22M20 70h60M20 70l14-40h32l14 40%22 stroke=%22%23ff8a3d%22 stroke-width=%229%22 fill=%22none%22 stroke-linecap=%22round%22 stroke-linejoin=%22round%22/></svg>">
<style>
  html{{background:#090c11}}
  body{{margin:0}}
  img{{max-width:100%}}
  [hidden]{{display:none !important}}
</style>
</head>
<body>
'''
# Sisus on oma <title> (artefakti ümbris loeb selle sealt). Eraldiseisvas
# dokumendis annaks see KAKS title-silti ja brauser võtaks lühema --
# täpselt selle, mida Messengeris jagades ei taha.
body_pub = re.sub(r"<title>.*?</title>\s*", "", body, count=1, flags=re.S)
io.open(ROOT + "pidurdusmaa-avalik.html", "w", encoding="utf-8").write(
    head + body_pub + "\n</body>\n</html>\n")

import os
for f in ("pidurdusmaa.html", "pidurdusmaa-avalik.html"):
    print(f"{f}: {os.path.getsize(ROOT+f):,} baiti")
