# -*- coding: utf-8 -*-
"""Rehvi nime kanooniline võti: sama rehv eri kirjaviisides → üks võti.

  kanooniline("Nokian HKPL R3")              == kanooniline("Nokian Hakkapeliitta R3")
  kanooniline("Pirelli IceZero FR")          == kanooniline("Pirelli Ice Zero FR")
  kanooniline("Hankook Winter i*Pike RS2 W429") == kanooniline("Hankook i-Pike RS2")
  kanooniline("Nordman 7")                   == kanooniline("Nokian Nordman 7")
  kanooniline("Continental ContiIceContact 2") == kanooniline("Continental IceContact 2")

Tagastab (bränd, mudel) — mõlemad väiketähtedes, ilma tühikute ja kirjavahemärkideta.
Variandid (SUV, Plus, +, 10p) JÄÄVAD eri võtmeteks: need on eri rehvid.
Kasutavad export_testid.py (ajakirjatestid → mudelileht) ja naastud_tuleta.py.
"""
import re
import unicodedata

# bränd → kanooniline bränd; teine element = mudelisõna, mis lisatakse ette
# (Nordman on Nokiani alabränd ja meie andmetes „Nokian NORDMAN 7“)
BRAND = {
    "conti": ("continental", None),
    "nokiantyres": ("nokian", None),
    "nokiantires": ("nokian", None),
    "nordman": ("nokian", "nordman"),
    "bfgoodrich": ("bfgoodrich", None),
    "bfg": ("bfgoodrich", None),
    "westlake": ("goodride", None),      # sama tehas, sama mudel (IceMaster Spike Z-506)
    "roadstone": ("nexen", None),        # Nexeni ekspordibränd, samad mudelid
    "gtradial": ("gtradial", None),
    "gt": ("gtradial", None),
}
TWO_WORD = {("bf", "goodrich"): "bfgoodrich", ("gt", "radial"): "gtradial",
            ("nokian", "tyres"): "nokian", ("nokian", "tires"): "nokian",
            ("double", "coin"): "doublecoin", ("double", "star"): "doublestar",
            ("tri", "ace"): "triace", ("star", "performer"): "starperformer",
            ("point", "s"): "points", ("general", "tire"): "generaltire"}
TOKEN = {
    "hkpl": "hakkapeliitta",
    "icelynk": "icelynx", "icelink": "icelynx", "iceiynx": "icelynx",
    "iceguard": "iceguard", "ice": "ice",
    "ug": "ultragrip",
    "winguard": "winguard",
    "xice": "xice",
}
# sõnad, mis ei erista mudelit
MYRA = {"tyre", "tyres", "tire", "tires", "winter", "studded", "studless", "friction", "nastarengas"}
HANKOOK_CODE = re.compile(r"^(?:w|k|h|rw|ra)\d{3}[a-z]?$")   # W429, W616, RW10 — poe/kataloogi kood


def _tok(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    s = s.lower().replace("+", " plus ").replace("*", "").replace("'", "")
    return [t for t in re.split(r"[^a-z0-9]+", s) if t]


def kanooniline(nimi, mark=None):
    """nimi = „Nokian Hakkapeliitta 9“ või mudel ilma margita, kui mark antud."""
    t = _tok((mark + " " if mark else "") + str(nimi or ""))
    if not t:
        return ("", "")
    if len(t) > 1 and (t[0], t[1]) in TWO_WORD:
        t = [TWO_WORD[(t[0], t[1])]] + t[2:]
    brand, lisa = BRAND.get(t[0], (t[0], None))
    rest = t[1:]
    if lisa:
        rest = [lisa] + rest
    rest = [TOKEN.get(x, x) for x in rest if x not in MYRA]
    if brand == "hankook":
        ilma = [x for x in rest if not HANKOOK_CODE.match(x)]
        if ilma:
            rest = ilma
    model = "".join(rest)
    if brand == "continental":
        model = re.sub(r"^conti(?=[a-z])", "", model)
    # „Winter i-Pike“ → „ipike“; „i cept“ → „icept“ — juba kokku; „ultragrip“ eesliide ühtlane
    return (brand, model)


def voti(nimi, mark=None):
    b, m = kanooniline(nimi, mark)
    return b + "|" + m
