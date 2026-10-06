# -*- coding: utf-8 -*-
"""EPREL-i rehvimõõdu normaliseerimine (öövahetus 7.10.2026).

EPREL-i mõõduväli on vaba tekst. Varem tehti võti lihtsalt kõigi
mittesümbolite eemaldamisega, nii et "205/55 R16 91W" -> "20555R1691W" ja
"175/65 R14 C 6 PR" -> "17565R14C6PR". Need ~690 võtit said oma faili,
millele ükski leht ei viidanud, ja rehvid puudusid oma õige mõõdu alt.

Reeglid (rehvimõõdu standardtähistus, ETRTO/ISO 4000):
  * laius/profiil R velg [C]   -> põhivõti, nt 20555R16, 19575R16C
  * Z enne R-i (ZR) on kiirusklassi vana tähis -> sama mõõt
  * P (P-metric) ja HL (High Load) eesliide -> sama mõõt, teine
    koormusindeks (nagu XL)
  * lõpus koormusindeks ja kiirusklass (91W), kihtide arv (6 PR),
    WSW (valge külg) või mudeli nimi -> sama mõõt
  * "155R13 (155/80R13)" -> sulgudes antud täismõõt
JÄETAKSE VÄLJA (tagastab None), sest need ei ole sõiduauto rehvid:
  * LT (light truck) eesliide või lõpp
  * poolikud veljed (17.5, 19.5): veoauto
  * kõik, mida ei õnnestu üheselt lugeda
"""
import re

_TAIS = re.compile(r"\(\s*(\d{3})\s*/\s*(\d{2})\s*R\s*(\d{2})\s*(C)?\s*\)", re.I)
_POHI = re.compile(
    r"^\s*(P|HL|LT)?\s*(\d{3})\s*/\s*(\d{2})\s*(Z)?\s*R\s*(\d{2})(\.\d)?\s*(C(?![A-Za-z]))?(.*)$",
    re.I)


def puhas_moot(moot):
    """Vaba tekstiga mõõt -> võti (nt '20555R16') või None."""
    if not moot:
        return None
    s = str(moot).strip()
    t = _TAIS.search(s)
    if t:
        return t.group(1) + t.group(2) + "R" + t.group(3) + ("C" if t.group(4) else "")
    m = _POHI.match(s)
    if not m:
        return None
    pre, w, p, _z, r, pool, c, rest = m.groups()
    if pre and pre.upper() == "LT":
        return None
    if pool:
        return None
    rest = rest.strip()
    if re.search(r"(^|[^A-Za-z])LT($|[^A-Za-z])", rest):
        return None
    return w + p + "R" + r + ("C" if c else "")


if __name__ == "__main__":
    for x in ["205/55 R16 91W", "175/65 R14 C 6 PR", "LT225/75R16", "245/70R17.5",
              "155R13(155/80R13)", "165R13C (165/80R13C)", "HL 285/35 R 22",
              "P205/75R15", "155/65R14 4seasonDrive", "205/70R15 WSW",
              "205/55R16 CrossClimate", "195/75 R16C", "185/75R16LT", "235/35 ZR19"]:
        print(f"{x!r:28} -> {puhas_moot(x)}")
