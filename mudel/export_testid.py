"""Välismaa rehvitestide tulemused rehvilehtedele (testid_ext.json).

Andmed: testid_ext/*.json (vt backtest_ext.py). Siin need ainult
NÄIDATAKSE, mitte ei arvutata nendega: backtest näitas, et ühe testi
tulemus ei ennusta sama rehvi tulemust teises testis/mõõdus märjal
paremini kui selle mõõdu EL-i märgis (4,7 % vs 4,2 %). Seepärast jääb
arvutus märgise (ja testitud rehvide) peale ning välistestid on lehel
mõõdetud faktina: kus, mis mõõdus, mis kiiruselt, mitu meetrit, mitmes.

Rehv seotakse EPREL-i mudeliga (models.json) margi + nime järgi; kui
vaste ei ole üheselt kindel, jäetakse rehv lehelt välja (test ise jääb
allikate nimekirja).

Käivita:  python3 -m mudel.export_testid
"""
from __future__ import annotations

import collections
import json
import os
import re

from . import backtest_ext as B

HERE = os.path.dirname(__file__)
OUTS = [os.path.join(HERE, "..", "veeb", "static", "data", "testid_ext.json")]
DISC = {("asphalt", True): "märg asfalt", ("asphalt", False): "kuiv asfalt",
        ("concrete", True): "märg betoon", ("snow", False): "lumi", ("ice", False): "jää"}


def model_index():
    p = os.path.join(B.CORE, "models.json")
    models = json.load(open(p, encoding="utf-8"))
    idx = collections.defaultdict(list)
    for slug, m in models.items():
        bt = B._tok(m["mark"])
        if bt:
            idx[bt[0]].append((slug, bt, "".join(B._tok(m["nimi"]))))
    # testitud rehvid (core.json), millel EPREL-i mudelit ei ole — nt naastrehvid.
    # Ka siis, kui testitud rehv on seotud EPREL-i mudeliga, mille nimi on teine
    # (test_eprel_alias.py: „Maxxis Premitra Snow WP6“ = EPREL „WP6“): testi nimi
    # peab ikka sama slugi leidma, muidu kaovad selle rehvi testid uuel ekspordil.
    core = json.load(open(os.path.join(B.CORE, "core.json"), encoding="utf-8"))
    for t in core.get("tyres", []):
        slug = t.get("slug")
        if not slug:
            continue
        tk = B._tok(t["name"])
        if len(tk) > 1:
            idx[tk[0]].append((slug, tk[:1], "".join(tk[1:])))
    return idx


# Käsitsi üle vaadatud nimevasted (testi nimi → mudeli slug), kus automaatne
# sobitus ei leia: EPREL-i lühendid (HKPL), Nordman ilma Nokian'ita,
# vanad „Conti“-eesliitega nimed, kirjavead allikas. Ainult kindlad.
NIMI_ALIAS = {
    "nokian hakkapeliitta r2": "nokian-hkpl-r2",
    "nokian hakkapeliitta r3": "nokian-hkpl-r3",
    "nokian hakkapeliitta r3 suv": "nokian-hkpl-r3-suv",
    "kumho ecsta hs52": "kumho-hs52",
    "kumho wintercraft wp52": "kumho-wp52-wp52",
    "kumho wintercraft wp52+": "kumho-wp52",
    "kumho wintercraft wp52 plus": "kumho-wp52",
    "nordman rs2": "nokian-nordman-rs2",
    "nordman rs 2": "nokian-nordman-rs2",
    "nordman rs2 suv": "nokian-nordman-rs2-suv",
    "nordman 7": "nokian-nordman-7",
    "nordman 7 suv": "nokian-nordman-7-suv",
    "nordman 8": "nokian-nordman-8",
    "nordman 8 suv": "nokian-nordman-8-suv",
    "nordman north 9": "nokian-nordman-north-9",
    "nordman north 9 suv": "nokian-nordman-north-9-suv",
    "continental conticecontact 2": "continental-icecontact-2",
    "continental contiicecontact 2": "continental-icecontact-2",
    "continental contiicecontact 2 suv": "continental-icecontact-2-suv",
    "continental contiwintercontact ts 850 p": "continental-wintercontact-ts-850-p",
    "hankook winter i*cept evo3 x w330a": "hankook-winter-i-cept-evo3-x",
    "goodyear ug performance 3": "goodyear-ultragrip-performance-3",
    "firestone multiseason gen 02": "firestone-multiseason2",
    "kumho solus 4s ha32": "kumho-ha32",
    "dunlop sp sport maxx rt2": "dunlop-sport-maxx-rt2",
    "momo w-20 north pole": "momo-w-2-north-pole",
    "tomket sport": "tomket-tomket-sport",
    "tomket sport 3": "tomket-tomket-sport-3",
    "giti allseason as1": "giti-gitiallseason-as1",
    "giti allseason as2": "giti-gitiallseason-as2",
    "giti synergy h2": "giti-gitisynergy-h2",
    "nexen winguard sport 2 wu7": "nexen-winguard-sport-2",
    "triangle icelynk ti501": "triangle-icelynx-ti501",
    "bridgestone blizzak 6 enliten": "bridgestone-blizzak-6",
    "rotalla setula s-pace ru01": "rotalla-setula-s-race-ru01",
    "tracmax s210": "tracmax-ice-plus-s210",
    "wanli sa302 sport macro": "wanli-sa302",
    # 2026-10-18: EPREL-i nimi on ainult mustrikood (sama rehv, kontrollitud käsitsi)
    "maxxis premitra snow wp6": "maxxis-wp6",
    "maxxis premitra hp5": "maxxis-hp5",
    "maxxis premitra hp6": "maxxis-hp6",
    "maxxis victra sport 5 vs5": "maxxis-vs5",
    "maxxis wp-05 arctictrekker": "maxxis-wp-05",
    "goodride all season elite z-401": "goodride-z-401",
    "goodride zupersnow z-507": "goodride-z-507",
    "goodride zupereco z-107": "goodride-z-107",
    "nankang winter activa sv-3": "nankang-sv-3",
    "nankang cross seasons aw-6": "nankang-aw-6",
    "nankang green sport eco-2 plus": "nankang-eco-2",
    "nankang green sport eco-2+": "nankang-eco-2",
    "nankang sportnex as-2+": "nankang-as-2",
    "nankang ice activa ice-1": "nankang-ice-1",
    "triangletire ta-01 season x": "triangle-seasonx",
    "wanli winter-max a1 sw211": "wanli-sw211",
    "wanli s 1083 snow grip": "wanli-snowgrip",
    "cst adreno ad-r9": "cst-ad-r9",
    "cst medallion winter wcp1": "cst-wcp1",
    "cst medallion all season acp1": "cst-acp1",
    "marshal izen kw31": "marshal-kw31",
    "marshal i'zen kw31": "marshal-kw31",
    "kumho ecsta ps71": "kumho-ps71",
    "kumho ecsta hs51": "kumho-hs51",
    "kumho wintercraft ws51": "kumho-ws51",
    "kumho wintercraft ice wi51": "kumho-wi51",
    "kumho wintercraft wp51": "kumho-wp51",
    "kumho wintercraft wp71": "kumho-wp71",
    "nokian hakka black 3 silentdrive": "nokian-hakka-black-3",
    "pirelli cinturato p7 c2": "pirelli-cinturato-p7-p7c2",
    "gt radial champiro fe2": "gt-radial-fe2",
    "gt radial champiro winterpro 2": "gt-radial-winterpro2",
    "firestone roadhawk 2 enliten": "firestone-roadhawk-2",
    "hankook ventus s1 evo z k129": "hankook-ventus-s1-evo-z",
    "matador hectorra 3": "matador-mp47-hectorra-3",
    "maxxis ap3 premitra all season": "maxxis-ap3",
    "maxxis premitra all season ap3": "maxxis-ap3",
    "maxxis premitra all season ap3 suv": "maxxis-ap3-suv",
    "hankook kinergy 4s 2 x h750a": "hankook-kinergy-4s-2-x",
}
# Kahesõnaline bränd testinimes (EPREL kirjutab kokku)
_BRAND2 = {("bf", "goodrich"): "bfgoodrich", ("west", "lake"): "westlake"}
_LI_SI = re.compile(r"\s+\d{2,3}[a-z]{1,2}(\s+xl)?$")


# Nimed, mida EI tohi siduda, kuigi reeglid leiaks paari (teine põlvkond, mitte sama rehv)
NIMI_EI = {
    "hankook winter i*pike rs w419",   # i*Pike RS (2012) ≠ RS+ (W419D, 2016)
}


def match(idx, name):
    return match_info(idx, name)[0]


def match_info(idx, name):
    """-> (slug või None, kas leiti ühtlustatud nime kaudu)"""
    if _LI_SI.sub("", " ".join(str(name).lower().split())) in NIMI_EI:
        return None, False
    slug = _match(idx, name)
    if slug is None:
        # tuletatud rehvide ühtlustatud nimi (naastud_tuleta.ilus): Westlake = Goodride,
        # Roadstone = Nexen, „Hakkapeliitta 10p“ = „10P“, „Ice Guard“ = „iceGUARD“ …
        from .naastud_tuleta import ilus
        ilusam = ilus(" ".join(str(name).split()))
        if ilusam != " ".join(str(name).split()):
            slug = _match(idx, ilusam)
            return slug, slug is not None
    return slug, False


def _match(idx, name):
    key = " ".join(str(name).lower().split())
    key = _LI_SI.sub("", key)   # „… 94V XL“ → „…“ (koormus-/kiirusindeks ei ole mudel)
    if key in NIMI_ALIAS:
        return NIMI_ALIAS[key]
    name = key
    t = B._tok(name)
    if not t:
        return None
    # „Nokian Tyres Snowproof 2“ → nokian snowproof 2
    if len(t) > 2 and t[1] in ("tyres", "tires"):
        t = t[:1] + t[2:]
    # „BF Goodrich g-Force …“ → bfgoodrich g force …
    if len(t) > 2 and (t[0], t[1]) in _BRAND2:
        t = [_BRAND2[(t[0], t[1])]] + t[2:]
    cands = []
    for slug, bt, rn in idx.get(B.BRAND_ALIAS.get(t[0], t[0]), []):
        model = t[len(bt):] if t[:len(bt)] == bt else t[1:]
        tm = "".join(model)
        if not tm:
            continue
        if tm == rn:
            cands.append((0, slug))
        elif rn.startswith(tm) and rn[len(tm):] in B.SUFFIX_OK:
            cands.append((1, slug))
        elif tm.startswith(rn) and re.fullmatch(r"[a-z]{0,2}\d{2,4}|suv|xl", tm[len(rn):]):
            cands.append((2, slug))
    if not cands:
        return None
    best = min(d for d, _ in cands)
    top = sorted({s for d, s in cands if d == best})
    return top[0] if len(top) == 1 else None


def kiiruseta():
    """Tulemused, mille kiirust allikas ei trüki (TM 2013, Test World 2020, Vi 2018 …).
    Backtest jätab need välja (mudeli kontrolliks on kiirus vaja), aga lehel on
    need mõõdetud fakt: koht samas testis samal pinnal ei sõltu kiirusest.
    v0/v1 = None → leht näitab „kiirus märkimata“."""
    out = []
    for f in sorted(os.listdir(B.DATA)):
        if not f.endswith(".json"):
            continue
        for t in json.load(open(os.path.join(B.DATA, f), encoding="utf-8")):
            if t["test_id"] in B.SKIP_TESTS:
                continue
            ds = {x["id"]: x for x in t["disciplines"]}
            size, _ = B.size_key(t["size"])
            for ty in t["tyres"]:
                for did, val in (ty.get("results") or {}).items():
                    x = ds.get(did)
                    if val is None or x is None or (t["test_id"], did) in B.SKIP:
                        continue
                    if x.get("v_from") is not None and x.get("v_to") is not None:
                        continue  # need on juba B.load()-is
                    if x["surface"] not in B.SURF:
                        continue
                    wet = bool(x.get("wet")) and x["surface"] in ("asphalt", "concrete")
                    out.append(dict(test=t["test_id"], size=size, tyre=ty["name"].strip(), surface=x["surface"],
                                    wet=wet, v0=None, v1=None, measured=float(val), disc=did))
    return out


def main():
    obs, _ = B.load()
    obs += kiiruseta()
    idx = model_index()
    # koht testis: sama test + distsipliin
    grp = collections.defaultdict(list)
    for o in obs:
        grp[(o["test"], o["disc"])].append(o["measured"])
    tests, per = {}, collections.defaultdict(list)
    raw = {}
    for f in sorted(os.listdir(B.DATA)):
        if f.endswith(".json"):
            for t in json.load(open(os.path.join(B.DATA, f), encoding="utf-8")):
                raw[t["test_id"]] = t
    unmatched = 0
    sobitus = [match_info(idx, o["tyre"]) for o in obs]
    # Sama testi sees on mõnikord mõlemad nimed (Auto Bild: Westlake ja Goodride kõrvuti):
    # ühtlustatud nime kaudu leitud rida jääb ära, kui sellel lehel on sama testi, ala ja
    # kiiruse otsene tulemus olemas — muidu oleks lehel üks test kahe eri numbriga.
    otse = {(sl, o["test"], o["disc"], o["v0"]) for o, (sl, fb) in zip(obs, sobitus) if sl and not fb}
    for o, (slug, fb) in zip(obs, sobitus):
        t = raw[o["test"]]
        tests[o["test"]] = {"pub": t["publication"], "year": t["year"], "season": t["season"],
                            "size": o["size"] or t["size"], "car": t.get("car"), "url": t.get("url")}
        if not slug:
            unmatched += 1
            continue
        if fb and (slug, o["test"], o["disc"], o["v0"]) in otse:
            unmatched += 1
            continue
        allv = sorted(grp[(o["test"], o["disc"])])
        per[slug].append({"t": o["test"], "d": DISC.get((o["surface"], o["wet"]), o["surface"]),
                          "v0": o["v0"], "v1": o["v1"], "m": o["measured"],
                          "pos": allv.index(o["measured"]) + 1, "n": len(allv), "best": allv[0],
                          "nimi": o["tyre"]})
    for v in per.values():
        v.sort(key=lambda x: (-tests[x["t"]]["year"], x["t"], x["d"]))
    out = {"allikad": tests, "rehvid": per}
    for p in OUTS:
        json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(f"testid_ext.json: {len(tests)} testi, {len(per)} rehvimudelit, "
          f"{sum(len(v) for v in per.values())} tulemust; sidumata {unmatched}")


if __name__ == "__main__":
    main()
