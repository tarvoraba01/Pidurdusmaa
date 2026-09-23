# -*- coding: utf-8 -*-
"""EPREL-i import: rehvid modu kaupa -> JSON, mille saab data.js-i kupsetada.

SEE SKRIPT ON MOELDUD JOOKSUTAMISEKS SINU ENDA MASINAS.
Anthropicu pilvekonteinerist ei paase europa.eu hostidele ligi (puhverserver
vastab CONNECT-ile 403-ga), seega ma ei saa seda siit ise ara teha.

VOTMEGA UMBERKAIMINE
--------------------
Voti loetakse failist, mille tee antakse argumendina. Teda EI TRUKITA
kunagi ja teda EI PANDA kunagi URL-i sisse -- ainult paisesse X-API-KEY,
sest URL-id jouavad logidesse ja puhvritesse, paised mitte.
Valjundfaili voti ei joua.

KASUTAMINE
----------
    python3 eprel_import.py <votme-fail.pdf|txt> [valjund.json]

Votme fail voib olla see PDF, mille EPREL saatis, voi tavaline tekstifail,
kus on ainult voti. Muud ei ole vaja -- ainult python3.

MIDA TA TEEB
------------
Kaib labi nimekirja modusid (SIZES allpool), kusib EPREL-ist iga modu
rehvid ja kirjutab valja JSON-i: tootja, mudeli nimi, modu, marghaarde
klass, kutuseklass, mura, 3PMSF, jaamargis.

MIDA TA EI TEE
--------------
Ei kusi kuiva ega lume/jaa numbreid -- neid EL-i margis ei kata ja
EPREL-is neid ei ole. Need tulevad mudelis kategooria keskmisest.

AUS HOIATUS: otsingu otspunkti parameetrite nimed ja vastuse umbrik ei ole
paris vastuse vastu kontrollitud (otsing noudis votit, mida mul ei olnud).
Seeparast proovib skript mitut kuju ja UTLEB VALJA, mis tootas. Kui
midagi ei toota, trukib ta diagnostika, milles votit EI OLE -- selle voib
mulle rahulikult tagasi saata.
"""
import json
import re
import ssl
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://eprel.ec.europa.eu/api/products/tyres"

# Eesti sagedasemad modud -- need katavad enamiku kalkulaatori autodest.
SIZES = [
    "195/65 R15", "205/55 R16", "205/60 R16", "215/65 R16", "185/65 R15",
    "235/60 R18", "225/65 R17", "215/60 R16", "185/60 R15", "225/55 R17",
    "215/55 R16", "225/60 R17", "235/65 R17", "225/50 R17", "215/55 R17",
    "225/45 R17", "225/40 R18", "195/65 R16", "205/65 R15", "175/70 R13",
]


# --------------------------------------------------------------------------
# voti
# --------------------------------------------------------------------------
def read_key(path):
    """Loeb votme failist. EI TRUKI teda kunagi."""
    if path.lower().endswith(".pdf"):
        try:
            raw = subprocess.run(["pdftotext", "-layout", path, "-"],
                                 capture_output=True, check=True).stdout
            text = raw.decode("utf-8", "replace")
        except (OSError, subprocess.CalledProcessError):
            sys.exit("Ei saanud PDF-i lugeda. Paigalda poppler-utils "
                     "(pdftotext) voi kopeeri voti tavalisse tekstifaili.")
    else:
        text = open(path, encoding="utf-8", errors="replace").read()

    bad = re.compile(r"^(https?|eprel|europa|european|commission|registry|"
                     r"energy|labelling|public|apikey|api|key|terms|"
                     r"conditions|application|programming|interface)$", re.I)
    cands = []
    for tok in re.findall(r"[A-Za-z0-9][A-Za-z0-9_\-]{15,}", text):
        tok = tok.strip("-_")
        if len(tok) < 16 or bad.match(tok) or (tok.isalpha()):
            continue
        if tok not in cands:
            cands.append(tok)
    if not cands:
        sys.exit("Votit ei leidnud sellest failist.")
    cands.sort(key=len, reverse=True)
    return cands[0]


# --------------------------------------------------------------------------
# HTTP
# --------------------------------------------------------------------------
def get_json(url, key):
    """GET + X-API-KEY paises. Tagastab (staatus, andmed-voi-None)."""
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "X-API-KEY": key,                 # AINULT siin, mitte kunagi URL-is
    })
    try:
        with urllib.request.urlopen(req, timeout=60,
                                    context=ssl.create_default_context()) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:                      # noqa: BLE001
        return type(e).__name__, None


def unwrap(d):
    """EPREL-i vastuse umbrik ei ole dokumenteeritud ja kliendid on eri
    meelt: uks loeb 'hits', teine 'content' + 'totalElements'. Proovime
    molemat ja utleme valja, kumb tootas."""
    if isinstance(d, list):
        return d, "list"
    if not isinstance(d, dict):
        return [], "?"
    for k in ("hits", "content", "items", "results", "products"):
        if isinstance(d.get(k), list):
            return d[k], k
    return [], "tundmatu:" + ",".join(sorted(d)[:8])


def fetch_size(size, key, page_size=100, max_pages=20):
    """Uhe modu koik rehvid. Tagastab (read, kasutatud-parameeter, umbrik)."""
    # modu kirjutusviisid, mida EPREL voib oodata
    variants = [size, size.replace(" ", ""), size.replace(" R", "R")]
    for param in ("tyreSize", "size", "modelIdentifier", "search"):
        for v in variants:
            rows, page, env = [], 0, "?"
            while page < max_pages:
                q = urllib.parse.urlencode(
                    {param: v, "page": page, "size": page_size})
                st, d = get_json(f"{BASE}?{q}", key)
                if st != 200 or d is None:
                    break
                batch, env = unwrap(d)
                if not batch:
                    break
                rows.extend(batch)
                if len(batch) < page_size:
                    break
                page += 1
                time.sleep(0.3)
            if rows:
                return rows, param, env
    return [], None, None


# --------------------------------------------------------------------------
# valjund
# --------------------------------------------------------------------------
def pick(row):
    """Vota valja ainult see, mida mudel kasutab. Tundmatud valjad jaavad
    valja -- parem tuhi koht kui vale vali."""
    def g(*names):
        for n in names:
            if isinstance(row, dict) and row.get(n) not in (None, ""):
                return row[n]
        return None
    return {
        "reg": g("registrationNumber", "registrationNo", "id"),
        "tootja": g("supplierOrTrademark", "trademark", "supplier"),
        "mudel": g("modelIdentifier", "modelIdentifierLong", "model"),
        "moot": g("tyreSize", "size", "sizeDesignation"),
        "margkl": g("wetGripClass", "wetGripAdhesionClass", "wetGrip"),
        "kutusekl": g("fuelEfficiencyClass", "energyClass"),
        "mura_db": g("externalRollingNoiseValue", "noiseValue", "noise"),
        "mura_kl": g("noiseClass", "externalRollingNoiseClass"),
        "lumi": g("snowGrip", "threePeakMountainSnowFlake", "snowTyre"),
        "jaa": g("iceGrip", "iceTyre"),
        "kl": g("tyreClass", "vehicleClass"),
    }


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    key = read_key(argv[1])
    out_path = argv[2] if len(argv) > 2 else "eprel_tyres.json"

    # 1) kiire tervisekontroll: kas host on ulepse kattesaadav
    st, _ = get_json(BASE + "?page=0&size=1", key)
    print(f"uhendustest: {st}")
    if st == 403:
        sys.exit("403 -- voti ei kolba selle otspunkti jaoks voi ei ole "
                 "veel aktiveeritud. Kontrolli EPREL-i kirjast.")
    if st != 200:
        sys.exit(f"Ei saanud uhendust ({st}). Vork voi host.")

    all_rows, report = {}, []
    for size in SIZES:
        rows, param, env = fetch_size(size, key)
        report.append((size, len(rows), param, env))
        print(f"  {size:<14} {len(rows):>5} rehvi   "
              f"param={param}  umbrik={env}")
        for r in rows:
            p = pick(r)
            if p["reg"]:
                all_rows[p["reg"]] = p

    data = {"allikas": "EPREL (Euroopa Komisjon)",
            "imporditud": time.strftime("%Y-%m-%d"),
            "modud": [{"moot": s, "leitud": n, "param": p, "umbrik": e}
                      for s, n, p, e in report],
            "rehvid": list(all_rows.values())}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print(f"\nKirjutatud {out_path}: {len(all_rows)} rehvi. "
          f"Votit selles failis EI OLE -- voib rahulikult edasi saata.")


if __name__ == "__main__":
    main(sys.argv)
