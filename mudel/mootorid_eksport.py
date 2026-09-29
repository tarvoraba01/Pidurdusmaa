"""Mootorid lehe autovalikusse (export_wp kutsub attach()).

Iga põlvkond (mark + mudel + aastasilt) saab mootorite nimekirja
mootorid.py-st. Olemasolevad read (nt "1.5 TSI" ja "R 2.0 TSI") seotakse
sobiva mootoriga ja saavad selle nime; ülejäänud mootorid lähevad
kompaktselt rea välja "eng" alla ja brauser teeb neist valikud, mis
kasutavad selle rea andmeid (mass, pidurid, rehvid, ABS).

"eng" kirje: [silt, kütus, aastad, slug, järjekord]  (nime teeb brauser)
Valiku võti brauseris: <rea võti>~<slug>.
"""
import re
from collections import OrderedDict

try:
    from .mootorid import MOOTORID
except Exception:            # fail puudub -> mootoreid ei lisata
    MOOTORID = {}

KYTUS_JRK = {"b": 0, "bg": 1, "g": 2, "d": 3, "h": 4, "p": 5, "e": 6}


def silt(lab, hp, kw, drive):
    return f"{lab}{' ' + drive if drive else ''} · {hp} hj ({kw} kW)"


def _tok(s):
    return [t for t in re.split(r"[\s/,]+", (s or "").lower()) if t]


def _compact(s):
    return re.sub(r"[^a-z0-9.]", "", (s or "").lower())


def _slug(lab, hp, drive):
    s = re.sub(r"[^a-z0-9]+", "-", f"{lab} {drive} {hp}".lower()).strip("-")
    return s


def _row_match(row_var, eng_lab):
    """None = ei sobi; muidu (lisatokenite arv) -- väiksem on parem."""
    if not row_var or row_var == "—":
        return None
    if _compact(row_var) == _compact(eng_lab):
        return 0
    rt, et = _tok(row_var), _tok(eng_lab)
    if rt and all(t in et for t in rt):
        return len(et) - len(rt)
    return None


def attach(vehicles):
    """Muudab `vehicles` (export_wp dictid) kohapeal. Tagastab statistika."""
    groups = OrderedDict()
    for d in vehicles:
        groups.setdefault((d["make"], d["model"], d["yearLabel"]), []).append(d)
    n_grp = n_virt = n_claim = 0
    for rows in groups.values():
        key = next((r["key"] for r in rows if r["key"] in MOOTORID), None)
        if not key:
            continue
        engs = MOOTORID[key]["eng"]
        order = sorted(range(len(engs)), key=lambda i: (KYTUS_JRK.get(engs[i][3], 9), i))
        n_grp += 1
        for r in rows:
            r["_var0"] = r["variant"]
        # 1) iga rida võtab parima sobiva mootori
        claimed = {}
        for r in rows:
            cand = []
            for i in order:
                if i in claimed.values():
                    continue
                m = _row_match(r["variant"], engs[i][0] + (" " + engs[i][5] if engs[i][5] else ""))
                if m is not None:
                    cand.append((m, engs[i][1], i))
            if cand:
                # mitu võrdset (nt 2.0 TDI 122/150/190 hj): rea võimsust ei
                # tea, võtame keskmise -- tüüpilisim, mitte nõrgim ega tugevaim
                bm = min(c[0] for c in cand)
                ties = sorted(c for c in cand if c[0] == bm)
                claimed[r["key"]] = ties[len(ties) // 2][2]
        # 2) mall = esimene rida; kui ta ei sobinud millegagi, saab ta
        #    esimese vaba mootori (tema andmed on põlvkonna tüüpilised)
        tmpl = rows[0]
        if tmpl["key"] not in claimed:
            if not any(_row_match(tmpl["variant"], e[0]) is not None for e in engs):
                free = [i for i in order if i not in claimed.values()]
                if free:
                    claimed[tmpl["key"]] = free[0]
        by_key = {r["key"]: r for r in rows}
        for rk, i in claimed.items():
            lab, hp, kw, fu, yrs, drv = engs[i]
            r = by_key[rk]
            r["variant"] = silt(lab, hp, kw, drv)
            r["fuel"], r["engOrd"] = fu, order.index(i)
            n_claim += 1
        # 3) ülejäänud mootorid: kõige täpsemini sobiva rea koopiana, muidu malli
        for i in order:
            if i in claimed.values():
                continue
            lab, hp, kw, fu, yrs, drv = engs[i]
            host, hs = tmpl, -1
            for r in rows:
                orig = r.get("_var0", r["variant"])
                rt = _tok(orig)
                if orig != "—" and rt and all(t in _tok(lab) for t in rt) and len(rt) > hs:
                    host, hs = r, len(rt)
            host.setdefault("eng", []).append(
                [silt(lab, hp, kw, drv), fu, yrs, _slug(lab, hp, drv), order.index(i)])
            n_virt += 1
        for r in rows:
            r.pop("_var0", None)
    return {"polvkondi": n_grp, "seotud_ridu": n_claim, "lisavalikuid": n_virt}
