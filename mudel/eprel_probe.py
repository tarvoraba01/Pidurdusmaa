# -*- coding: utf-8 -*-
"""EPREL-i PROOVIPARING -- uks leht, et naha paris valjanimesid.

MIKS SEE ON OLEMAS
------------------
Esimene import andis tuhja tulemuse, sest ma PAKKUSIN valjanimesid
("registrationNumber", "supplierOrTrademark" jne) ja kui pakkumine ei
klapi, visati rida ara. Rohkem ma ei paku. See skript tombab UHE lehe
ja salvestab vastuse TOORELT, ilma midagi valja viskamata -- siis on
nimed mustvalgel kirjas ja ulejaanu saab kirjutada oigesti.

Fail on vaike (uks leht, ~25 rehvi) ja kiire.

VOTMEGA SAMA REEGEL: loetakse failist, ei trukita, kaib ainult paises
X-API-KEY, valjundfaili ta ei joua.

KASUTAMINE
----------
    python3 eprel_probe.py eprel-key.txt

Kirjutab eprel_probe.json -- saada see mulle.
"""
import json
import re
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://eprel.ec.europa.eu/api/products/tyres"
SIZE = "195/65 R15"          # Eesti levinuim modu, sinu Passati oma


def read_key(path):
    """Loeb votme failist. EI TRUKI teda kunagi."""
    if path.lower().endswith(".pdf"):
        raw = subprocess.run(["pdftotext", "-layout", path, "-"],
                             capture_output=True, check=True).stdout
        text = raw.decode("utf-8", "replace")
    else:
        text = open(path, encoding="utf-8", errors="replace").read()
    bad = re.compile(r"^(https?|eprel|europa|european|commission|registry|"
                     r"energy|labelling|public|apikey|api|key)$", re.I)
    cands = [t.strip("-_") for t in
             re.findall(r"[A-Za-z0-9][A-Za-z0-9_\-]{15,}", text)]
    cands = [t for t in cands if len(t) >= 16 and not bad.match(t)
             and not t.isalpha()]
    if not cands:
        sys.exit("Votit ei leidnud sellest failist.")
    cands.sort(key=len, reverse=True)
    return cands[0]


def main(argv):
    if len(argv) < 2:
        sys.exit(__doc__)
    key = read_key(argv[1])

    url = (BASE + "?tyreSize=" + urllib.parse.quote(SIZE)
           + "&page=0&size=25")
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "X-API-KEY": key,            # ainult paises
    })
    try:
        with urllib.request.urlopen(req, timeout=60,
                                    context=ssl.create_default_context()) as r:
            data = json.loads(r.read().decode("utf-8"))
            status = r.status
    except urllib.error.HTTPError as e:
        sys.exit(f"HTTP {e.code}")
    except Exception as e:                      # noqa: BLE001
        sys.exit(f"{type(e).__name__}")

    with open("eprel_probe.json", "w", encoding="utf-8") as f:
        json.dump({"staatus": status, "moot": SIZE, "toorvastus": data},
                  f, ensure_ascii=False, indent=1)

    print(f"staatus {status}")
    if isinstance(data, dict):
        print("umbriku valjad:", sorted(data.keys()))
        for k, v in data.items():
            if not isinstance(v, (list, dict)):
                print(f"   {k} = {v}")
        rows = data.get("hits") or []
        if rows:
            print(f"ridu sellel lehel: {len(rows)}")
            print("esimese rea valjad:", sorted(rows[0].keys()))
    print("\nKirjutatud eprel_probe.json -- votit seal EI OLE, "
          "voib edasi saata.")


if __name__ == "__main__":
    main(sys.argv)
