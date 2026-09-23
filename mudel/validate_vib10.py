# -*- coding: utf-8 -*-
"""VALJASPOOL-VALIMI KONTROLL: Vi Bilagare 2010 kahe testi vastu.

MEETOD -- sama, mis README 3. jaos "uks parameeter, neli ennustust"
-------------------------------------------------------------------
Iga rehvi kohta tuletatakse G AINULT margast tulemusest (bisektsioon,
kuni mudel taastoodab moodetud marja pidurdusmaa). Koik ULEJAANUD
pinnad -- kuiv, lumi, jaa -- on siis ENNUSTUSED, mitte sobitused.

Mudelit EI muudeta. See fail ainult mootab, kui kaugel ta on.

MIDA SIIT OODATA JA MIDA MITTE
------------------------------
Suur viga siin EI tahenda automaatselt, et mudel on vale. Need testid
on 15 aastat vanemad, teisest moodust ja TEISTELT KIIRUSTELT kui koik
olemasolevad ankrud, ja pidurdus on 5 km/h-ni, mitte seisakuni. Suur
viga tahendab: siin on midagi, mida mudel ei tea. Vaike viga tahendab,
et mudel kannab valjapoole oma kalibreerimisala -- ja SEE on ainus
pohjus, miks seda kontrolli uldse teha.
"""
import sys
from collections import defaultdict
from statistics import mean

sys.path.insert(0, "/home/claude")
from pidurdus import presets                                       # noqa: E402
from pidurdus.anchors_vib10 import (CONDS, KATEGOORIA_KAHTLUS,     # noqa: E402
                                    SIZE, VEHICLE_KEY, VIB10D, VIB10F)
from pidurdus.model import (BrakingModel, Conditions,              # noqa: E402
                            Tyre, replace)

M = BrakingModel()
VEH = presets.VEHICLES[VEHICLE_KEY]


def tee_rehv(nimi, kat, g, tread=9.0):
    return Tyre(name=nimi, category=kat, wet_grip_index=g,
                tread_depth_mm=tread, tread_depth_new_mm=tread,
                size=SIZE, g_source="test")


def vahemaa(tyre, votme):
    surf, water, temp, v0, v1 = CONDS[votme]
    c = Conditions(speed_kmh=v0, surface=surf, water_mm=water, temp_c=temp)
    return M.distance_between(tyre, VEH, c, v0, v1)


def tuleta_g(nimi, kat, marg_m, lo=0.55, hi=2.20):
    """Leia G, mis taastoodab moodetud marja pidurdusmaa."""
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        d = vahemaa(tee_rehv(nimi, kat, mid), "marg")
        if d > marg_m:                 # liiga pikk -> vaja paremat haaret
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def aja(pealkiri, andmed, veerud, lume_votme):
    print("\n" + "=" * 74)
    print(pealkiri)
    print("=" * 74)
    print(f"{'rehv':<34} {'G':>5}  " +
          "  ".join(f"{k:>13}" for k, _ in veerud))
    vead = defaultdict(list)
    for key, rida in andmed.items():
        nimi, kat = rida[0], rida[1]
        marg = rida[veerud_index(veerud, andmed)]
        if kat is None:
            print(f"{nimi:<34}   --   kategooria kinnitamata, vahele")
            continue
        g = tuleta_g(nimi, kat, marg)
        t = tee_rehv(nimi, kat, g)
        tekst = []
        for votme, veeru_nr in veerud:
            if votme == "marg":
                tekst.append(f"{'(alus)':>13}")
                continue
            m_ = rida[veeru_nr]
            p = vahemaa(t, lume_votme if votme == "lumi" else votme)
            viga = 100.0 * (p - m_) / m_
            vead[votme].append(abs(viga))
            tekst.append(f"{p:5.1f}/{m_:<4.1f}{viga:+5.0f}%")
        print(f"{nimi:<34} {g:5.3f}  " + "  ".join(tekst))
    print("\nKESKMINE ABSOLUUTVIGA PINNA KAUPA:")
    for votme, v in vead.items():
        print(f"   {votme:<8} {mean(v):6.1f} %   (n={len(v)})")
    return vead


def veerud_index(veerud, andmed):
    for votme, nr in veerud:
        if votme == "marg":
            return nr
    raise ValueError("marga veergu ei ole")


def main():
    # VIB10D: (nimi, kat, lumi, jaa_k, jaa_s, lorts, marg, kuiv)
    aja("[VIB10D] Vi Bilagare 2010, NAASTREHVID, 205/55 R16",
        VIB10D,
        [("marg", 6), ("kuiv", 7), ("jaa_k", 3), ("jaa_s", 4), ("lumi", 2)],
        "lumi_d")

    # VIB10F: (nimi, kat, lumi, jaa, marg, kuiv)
    aja("[VIB10F] Vi Bilagare 2010, NAELUTUD TALVEREHVID, 205/55 R16",
        VIB10F,
        [("marg", 4), ("kuiv", 5), ("jaa_f", 3), ("lumi", 2)],
        "lumi_f")

    print("\nKATEGOORIA KINNITAMATA, seetottu valja jaetud: "
          + ", ".join(KATEGOORIA_KAHTLUS))

    # --- see, mida tegelikult sobitati ------------------------------------
    # ABSOLUUTNE jaapidurdusmaa selles testis EI OLE kolblik siht: Arvidsjauri
    # jaa oli lihtsalt vahem haarav kui Ivalo oma, millelt mu_ice_base tuli
    # (mudel on seal jarjekindlalt luhike, juba enne igasugust muudatust).
    # SUHE seevastu on kolblik, sest rehvi enda jaahaare taandub valja.
    print("\n" + "=" * 74)
    print("JAA TEMPERATUURISUHE -- see on see, mida ice_temp_exp sobitab")
    print("=" * 74)
    print(f"{'rehv':<34} {'moodetud':>9} {'mudel':>8} {'viga':>7}")
    for _key, r in VIB10D.items():
        nimi, kat, kulm, soe = r[0], r[1], r[3], r[4]
        t = tee_rehv(nimi, kat, 1.2)
        p = vahemaa(t, "jaa_s") / vahemaa(t, "jaa_k")
        m_ = soe / kulm
        print(f"{nimi:<34} {m_:9.3f} {p:8.3f} {100*(p-m_)/m_:+6.1f} %")


if __name__ == "__main__":
    main()
