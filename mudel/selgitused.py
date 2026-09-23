"""
Infomullikeste sisu — laadimine ja terviklikkuse kontroll.

Sisu ise on `selgitused.json`, et sama fail sobiks nii siia kui hilisemasse
veebiliidesesse ilma teisendamiseta.

Kaks reeglit, mida see moodul jõustab:

  1. IGAL mudeli valikul (pinnas, tekstuur, ABS) peab olema mullike.
     Kui model.py-sse lisatakse uus valik ja siia mitte, siis test punaseks.

  2. Mullike selgitab SISENDIT. Tulemuse veapiir ja usaldus tuleb mootorist
     (Result.sigma_rel / .confidence / .warnings) ja muutub iga arvutusega.
     Neid siin ei dubleerita.

Käivita kontroll:  python3 -m pidurdus.selgitused
"""

from __future__ import annotations

import json
import os
from typing import Optional

from .model import AbsClass, Surface, Texture, TyreCategory

_PATH = os.path.join(os.path.dirname(__file__), "selgitused.json")

with open(_PATH, encoding="utf-8") as _f:
    DATA = json.load(_f)

USALDUS_JARJEKORD = ["korge", "keskmine", "madal", "puudub"]

# Pidurite seisukorra tasemed -> Conditions.brake_condition väärtus.
# Mitte-lineaarne mõju on tahtlik: vt selgitused.json _mittelineaarsus.
PIDURID = {
    "KORRAS": 1.00,
    "NORGENENUD": 0.85,
    "VIGANE": 0.65,
    "KRIITILINE": 0.45,
}

# Mudeli loend -> JSON-i sektsioon
_ENUM_SECTIONS = {
    "pinnas": Surface,
    "tekstuur": Texture,
    "abs": AbsClass,
    "rehvituup": TyreCategory,
}


def bubble(section: str, key: Optional[str] = None) -> dict:
    """Võta ühe välja või ühe valiku mullike.

    >>> bubble("pinnas", "ICE")["usaldus"]
    'madal'
    >>> bubble("muster")["usaldus"]
    'korge'
    """
    node = DATA[section]
    if key is None:
        return node
    return node[key]


def field_help(section: str) -> Optional[str]:
    """Välja üldine abitekst (ilmub välja enda, mitte valiku juures)."""
    return DATA.get(section, {}).get("_valja_abi")


def render(section: str, key: Optional[str] = None) -> str:
    """Mullike lihttekstina — kiireks kontrollimiseks ja CLI jaoks."""
    b = bubble(section, key)
    out = [b.get("pealkiri", section)]
    if b.get("abi"):
        out.append("")
        out.append(b["abi"])
    if b.get("tapsus"):
        out.append("")
        out.append("Kui täpne see on: " + b["tapsus"])
    if b.get("hoiatus"):
        out.append("")
        out.append("! " + b["hoiatus"])
    if b.get("usaldus"):
        out.append("")
        out.append(f"[usaldus: {b['usaldus']}]")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Kontroll
# ---------------------------------------------------------------------------

def check() -> list:
    """Tagastab probleemide loendi. Tühi loend = kõik korras."""
    problems = []

    # 1. iga mudeli valik peab olema kaetud
    for section, enum_cls in _ENUM_SECTIONS.items():
        if section not in DATA:
            problems.append(f"puudub sektsioon '{section}'")
            continue
        for member in enum_cls:
            if member.name not in DATA[section]:
                problems.append(
                    f"{section}: mudelis on {enum_cls.__name__}.{member.name} "
                    f"('{member.value}'), aga mullike puudub")
        # ja vastupidi — mullike ilma mudeli valikuta
        names = {m.name for m in enum_cls}
        for k in DATA[section]:
            if not k.startswith("_") and k not in names:
                problems.append(
                    f"{section}: mullike '{k}' ei vasta ühelegi "
                    f"{enum_cls.__name__} valikule")

    # 2. kohustuslikud väljad
    for section, node in DATA.items():
        if section.startswith("_"):
            continue
        entries = ([(section, node)] if "pealkiri" in node
                   else [(f"{section}.{k}", v) for k, v in node.items()
                         if not k.startswith("_")])
        for name, e in entries:
            if not isinstance(e, dict):
                continue
            for required in ("pealkiri", "abi", "usaldus"):
                if required not in e:
                    problems.append(f"{name}: puudub väli '{required}'")
            u = e.get("usaldus")
            if u and u not in USALDUS_JARJEKORD:
                problems.append(f"{name}: tundmatu usaldustase '{u}'")

    # 3a. iga pidurite tase peab olema nii JSON-is kui PIDURID-is
    for k in PIDURID:
        if k not in DATA.get("pidurite_seisukord", {}):
            problems.append(f"pidurite_seisukord: tase '{k}' puudub JSON-is")
    for k in DATA.get("pidurite_seisukord", {}):
        if not k.startswith("_") and k not in PIDURID:
            problems.append(f"pidurite_seisukord: '{k}' ei ole PIDURID-is")

    # 3. valideerimata asjad ei tohi olla märgitud kõrge usaldusega
    #    (need on kohad, kus mudelil ANKRUD PUUDUVAD -- vt README)
    # Lumi (tallatud), betoon ja rõhk on nüüd ankrutega kaetud ja
    # eemaldatud siit nimekirjast — vt anchors_adac.py ja PRESSURE_RELATIONS.
    ankruteta = [("pinnas", "SNOW_LOOSE"),
                 ("pinnas", "GRAVEL"), ("vanus", None),
                 ("tekstuur", "POLISHED"), ("abs", "NONE"),
                 ("pidurite_seisukord", "NORGENENUD"),
                 ("pidurite_seisukord", "VIGANE"),
                 ("pidurite_seisukord", "KRIITILINE")]
    for section, key in ankruteta:
        b = bubble(section, key)
        if b.get("usaldus") == "korge":
            problems.append(
                f"{section}.{key}: märgitud kõrge usaldusega, aga mudelil "
                f"ei ole selle kohta ühtegi ankrut")

    return problems


def summary() -> None:
    print("Infomullikesed —", DATA["_meta"]["versioon"])
    print("=" * 78)
    rows = []
    for section, node in DATA.items():
        if section.startswith("_"):
            continue
        if "pealkiri" in node:
            rows.append((section, node.get("usaldus", "?")))
        else:
            for k, v in node.items():
                if not k.startswith("_") and isinstance(v, dict):
                    rows.append((f"{section}.{k}", v.get("usaldus", "?")))
    for level in USALDUS_JARJEKORD:
        hits = [n for n, u in rows if u == level]
        if hits:
            print(f"\n  usaldus {level.upper()} ({len(hits)}):")
            for n in hits:
                print(f"      {n}")
    print(f"\n  kokku {len(rows)} mullikest")


if __name__ == "__main__":
    summary()
    print("\n" + "=" * 78)
    probs = check()
    if probs:
        print("PROBLEEMID:")
        for p in probs:
            print("  !", p)
        raise SystemExit(1)
    print("Kontroll OK — iga mudeli valik on kaetud, ühtegi valideerimata")
    print("kohta ei ole märgitud kõrge usaldusega.")
    print("\nNäide:\n")
    print(render("pinnas", "ICE"))
