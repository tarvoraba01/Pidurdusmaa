# -*- coding: utf-8 -*-
"""EPREL-i API votme lugemine -- ILMA seda kuhugi jatmata.

REEGLID, MIS SIIN KEHTIVAD
--------------------------
1. Votit EI TRUKITA kunagi. Mitte logisse, mitte veateatesse, mitte
   silumisvaljundisse. Ainus asi, mida see moodul valja utleb, on kas
   votme leidmine onnestus ja mitu kandidaati oli.
2. Votit EI KIRJUTATA uhtegi faili. Ta loetakse PDF-ist iga kord uuesti
   malusse. data.js-i, HTML-i ega uhtegi repo faili ta ei joua.
3. Voti kaib AINULT paise X-API-KEY sees, mitte kunagi URL-i sees.
   URL-id jouavad puhvritesse ja logidesse, paised mitte.
4. Veateate korral trukitakse ainult HTTP staatuskood ja erindi TUUP --
   mitte vastuse keha ega paiseid, sest need voivad votit peegeldada.

MIKS PDF-i EI LOETA SILMADEGA
-----------------------------
Kui ma avaksin PDF-i tavalise lugemisega, ilmuks voti sellesse vestlusesse
ja jaaks sinna jaadavalt -- tapselt see, mida kasutaja keelas. Seeparast
kaib tuvastamine PIMEDALT: moodul korjab tekstist koik votmetaolised
sonad ja proovib neid ukshaaval paris paringuga. Oige on see, millega
server vastab 200-ga. Nii ei pea keegi votit vaatama, et teada, kas ta on
oige.
"""
import re
import subprocess

# Kandidaadid, mis EI OLE voti: URL-i osad, sonad dokumendist jne.
_BLACKLIST = re.compile(
    r"^(https?|eprel|europa|european|commission|registry|energy|labelling|"
    r"public|apikey|api|key|terms|conditions|application|programming|"
    r"interface|documentation|swagger|rabarvo)$", re.I)


def _pdf_text(path: str) -> str:
    """PDF -> tekst. Tagastatud teksti EI TOHI trukkida."""
    out = subprocess.run(["pdftotext", "-layout", path, "-"],
                         capture_output=True, check=True)
    return out.stdout.decode("utf-8", "replace")


def candidates(path: str) -> list:
    """Votmetaolised sonad, pikimad enne. Ei truki neid."""
    text = _pdf_text(path)
    seen, out = set(), []
    for tok in re.findall(r"[A-Za-z0-9][A-Za-z0-9_\-]{15,}", text):
        tok = tok.strip("-_")
        if len(tok) < 16 or tok in seen or _BLACKLIST.match(tok):
            continue
        # puhas sona ilma ainsagi numbrita on pigem tekst kui voti
        if not re.search(r"\d", tok) and tok.isalpha():
            continue
        seen.add(tok)
        out.append(tok)
    out.sort(key=len, reverse=True)
    return out


def fingerprint(key: str) -> str:
    """Ohutu kirjeldus logi jaoks: pikkus ja tahestik, mitte sisu."""
    kinds = []
    if re.search(r"[a-z]", key):
        kinds.append("vaiketahti")
    if re.search(r"[A-Z]", key):
        kinds.append("suurtahti")
    if re.search(r"\d", key):
        kinds.append("numbreid")
    if re.search(r"[-_]", key):
        kinds.append("sidekriipse")
    return f"{len(key)} margi pikkune, sisaldab {', '.join(kinds)}"
