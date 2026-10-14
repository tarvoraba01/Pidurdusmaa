# -*- coding: utf-8 -*-
"""Testimata naastrehvid, mida Eesti poed müüvad (presets_hinnang.py).

MIKS. Naastrehvil ei ole EL-i märgist ja EPREL-is teda pole. Kui rehv pole
olnud üheski ajakirjatestis, ei ole meil tema kohta ühtegi mõõtmist. Poes on
ta siiski müügil (IceContact 8, Sailun Ice Blazer Spike, Barum Polaris Ice 6 …)
ja ostja tahab teada, mida temalt oodata. Seepärast anname HINNANGU, mitte
mõõtmise, ja leht ütleb seda selgelt („testimata, hinnang“).

KUIDAS (iga rehv eraldi, pind kaupa: jää, lumi, märg, kuiv):
  1. Kaksik. Kui sama rehvi müüakse teise nime all (Westlake Z506 =
     Goodride IceMaster Spike Z-506, sama tehas ja muster) või on see sama
     mustri teine versioon (Kumho WI31+ ja SUV WS31 = WI31), võetakse
     kaksiku haardetegurid.
  2. Muidu tootja enda naastrehvid. Meie testitud ja ajakirjatestidest
     tuletatud naastrehvid (2016 ja hiljem) annavad iga tootja keskmise.
     Seda tõmmatakse tootja hinnaklassi keskmise poole (kaal K_KLASS), et
     ühe vana mudeliga tootja ei saaks liiga kindlat numbrit.
  3. Tootja, kelle naastrehvi meil pole, saab oma hinnaklassi keskmise.
Hinnaklass (premium / kesk / soodne) on ainult viiteväärtuse valik, mitte
hinnang rehvi kvaliteedile — kõik number tuleb ikka mõõdetud rehvidest.

Veapiir: gSource "hinnang" -> mootor lisab sigma_hinnang (jääl naastrehvide
hajuvus on ~15 %). Vt model.py.

Käivita: cd <pk> && python3 -m pidurdus.naastud_hinnang -> mudel/presets_hinnang.py
"""
from __future__ import annotations

import json
import os
import statistics

from .model import TyreCategory as C
from .presets import TYRES as _TYRES
from .rehvinimi import kanooniline, voti

try:
    from .presets_tuletatud import TYRES_TULETATUD, TULETUS
except ImportError:  # pragma: no cover
    TYRES_TULETATUD, TULETUS = {}, {}

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "presets_hinnang.py")
K_KLASS = 1.5          # mitu „virtuaalset rehvi“ klassi keskmist tootja keskmisele lisandub
AASTA_MIN = 2016       # vanemad tuletatud mudelid on teise põlvkonna tehnika

KLASS = {
    "premium": {"continental", "nokian", "michelin", "goodyear", "bridgestone", "pirelli"},
    "kesk": {"hankook", "kumho", "dunlop", "yokohama", "toyo", "gislaved", "nexen", "falken",
             "maxxis", "matador", "sava", "firestone", "bfgoodrich", "general", "barum",
             "laufenn", "kormoran", "tigar", "gtradial", "fulda", "semperit", "uniroyal", "vredestein"},
}


def klass(mark):
    for k, s in KLASS.items():
        if mark in s:
            return k
    return "soodne"


# (nimi nagu poes, kaksiku nimi või None, märkus lehe jaoks)
# Nimi on valitud nii, et poe nimi sobitub (sobitus.js); mõõt on viide.
REHVID = [
    ("Continental IceContact 8", None, "205/55 R16"),
    ("Sailun Ice Blazer Spike", None, "205/55 R16"),
    ("Sailun Ice Blazer WST2", None, "215/65 R16"),
    ("Barum Polaris Ice 6", None, "205/55 R16"),
    ("Fortune Polaro Ice", None, "205/55 R16"),
    ("GT Radial IcePro 3 EVO", None, "205/55 R16"),
    ("GT Radial IcePro SUV 3", None, "215/65 R16"),
    ("GT Radial IcePro SUV 3 EVO", None, "215/65 R16"),
    ("Dynamo Nordic Ice", None, "205/55 R16"),
    ("Dynamo Snow-H MWH02", None, "205/55 R16"),
    ("Dynamo Snow-H MWH03", None, "205/55 R16"),
    ("Dynamo Snow-H MWS01", None, "215/65 R16"),
    ("Maxxis Premitra Ice Nord NP5", "Maxxis Premitra Ice Nord 5 SUV", "205/55 R16"),
    ("Kumho WinterCraft Ice WI31+", "Kumho WinterCraft Ice WI31", "205/55 R16"),
    ("Kumho WinterCraft SUV Ice WS31", "Kumho WinterCraft Ice WI31", "215/65 R16"),
    ("Goodride SW606", None, "205/55 R16"),
    ("Westlake SW606", "Goodride SW606", "205/55 R16"),
    ("Westlake Z506", "Goodride IceMaster Spike Z-506", "235/60 R18"),
    ("Zeta Antarctica Sport", None, "205/55 R16"),
    ("Tigar SiguraStud", None, "205/55 R16"),
    ("Rotalla Setula W-Race S500", None, "205/55 R16"),
    ("Tracmax Ice-Plus SR1", None, "205/55 R16"),
    ("Nankang SW-9", None, "205/55 R16"),
    ("Nankang SW-8", None, "205/55 R16"),
    ("Laufenn I Fit Ice LW71", None, "205/55 R16"),
    ("Leao Winter Defender Grip", None, "205/55 R16"),
    # kaubiku (C) naastrehvid
    ("Continental VanContact Ice", None, "215/65 R16 C"),
    ("Sailun Commercio Ice", None, "215/65 R16 C"),
    ("Barum SnoVanis Ice", None, "215/65 R16 C"),
    ("Gislaved Nord Frost Van 2", None, "215/65 R16 C"),
    ("Hankook Winter i*Pike LV RW15", None, "215/65 R16 C"),
    ("Nokian Hakkapeliitta C4", None, "215/65 R16 C"),
    ("Nokian Hakkapeliitta LT3", None, "245/75 R16 C"),
    ("Michelin Agilis X-Ice North", None, "215/65 R16 C"),
]

PINNAD = ("ice", "snow", "wet", "dry")


def _pinnad(t):
    return {"ice": t.mu_ice_override, "snow": t.mu_snow_override,
            "wet": t.wet_grip_index, "dry": t.mu_dry_override}


def teadaolevad():
    """Kõik naastrehvid, mille haare on mõõdetud või ajakirjatestidest tuletatud."""
    out = {}
    for key, t in list(_TYRES.items()) + list(TYRES_TULETATUD.items()):
        if t.category != C.WINTER_STUDDED:
            continue
        aasta = TULETUS.get(key, {}).get("viimane") or 2025
        if key in TYRES_TULETATUD and aasta < AASTA_MIN:
            continue
        b = kanooniline(t.name)[0]
        out[voti(t.name)] = {"nimi": t.name, "mark": b, "p": _pinnad(t)}
    return out


def main():
    tea = teadaolevad()
    nimi_voti = {voti(v["nimi"]): v for v in tea.values()}
    # tootja ja klassi keskmised pinna kaupa
    by_mark, by_klass = {}, {}
    for v in tea.values():
        for p, mu in v["p"].items():
            if mu is None:
                continue
            by_mark.setdefault(v["mark"], {}).setdefault(p, []).append(mu)
            by_klass.setdefault(klass(v["mark"]), {}).setdefault(p, []).append(mu)
    kl_mean = {k: {p: statistics.mean(x) for p, x in d.items()} for k, d in by_klass.items()}

    tulem, meta = {}, {}
    for nimi, kaksik, size in REHVID:
        b = kanooniline(nimi)[0]
        key = "h_" + "_".join(nimi.lower().replace("*", "").replace("+", " plus").replace("-", " ").split())
        if kaksik:
            kk = nimi_voti.get(voti(kaksik))
            if kk is None:
                # kaksik võib olla ka selles samas nimekirjas (Westlake SW606 -> Goodride SW606)
                kk2 = next((tulem[k2] for k2 in tulem if meta[k2]["nimi"] == kaksik), None)
                if kk2 is None:
                    raise SystemExit(f"kaksikut ei leitud: {kaksik}")
                p = dict(kk2)
            else:
                p = dict(kk["p"])
            alus = {"viis": "kaksik", "kaksik": kaksik}
        else:
            kl = klass(b)
            p, n_mark = {}, {}
            for pind in PINNAD:
                oma = by_mark.get(b, {}).get(pind, [])
                kv = kl_mean[kl].get(pind)
                if kv is None:
                    p[pind] = statistics.mean(oma) if oma else None
                else:
                    p[pind] = (sum(oma) + K_KLASS * kv) / (len(oma) + K_KLASS)
                n_mark[pind] = len(oma)
            alus = {"viis": "tootja" if any(n_mark.values()) else "klass", "klass": kl,
                    "n": n_mark}
        p = {k: (round(v, 4) if v is not None else None) for k, v in p.items()}
        tulem[key] = p
        meta[key] = {"nimi": nimi, "size": size, **alus}

    rida = []
    for key, p in tulem.items():
        m = meta[key]
        lisa = "".join(f", mu_{n}_override={p[k]}" for k, n in (("dry", "dry"), ("snow", "snow"), ("ice", "ice")) if p[k] is not None)
        rida.append(f"    {key!r}: Tyre({m['nimi']!r}, C.WINTER_STUDDED, {p['wet']}{lisa}, studded=True, size={m['size']!r}, g_source=\"hinnang\"),")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write('# -*- coding: utf-8 -*-\n"""GENEREERITUD — mudel/naastud_hinnang.py. ÄRA MUUDA KÄSITSI.\n\n'
                'Testimata naastrehvid: haare on HINNANG (kaksik, tootja naastrehvide keskmine\n'
                'või hinnaklassi keskmine), mitte mõõtmine. Vt naastud_hinnang.py.\n"""\n'
                "from .model import Tyre, TyreCategory as C\n\nTYRES_HINNANG = {\n")
        f.write("\n".join(rida) + "\n}\n\nHINNANG = ")
        f.write(json.dumps(meta, ensure_ascii=False, indent=1) + "\n")
    for key, p in tulem.items():
        m = meta[key]
        print(f"{m['nimi']:34s} {m['viis']:7s} jää {p['ice']}  lumi {p['snow']}  märg {p['wet']}  kuiv {p['dry']}")
    print("klassid:", {k: {p: round(v, 3) for p, v in d.items()} for k, d in kl_mean.items()})


if __name__ == "__main__":
    main()
