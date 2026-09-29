"""Pidurdusmaa mudeli testid (Pythoni mootor = tõe allikas).

    python3 -m unittest mudel.test_mudel        (repo juurest)

Rühmad:
  Valem        integraator analüütilise lahendi vastu, v²-seadus, ühikud
  Sisend       vigane sisend -> InputError, mitte number
  Äärmus       auto ei peatu -> inf; pikk pidurdus ei kärbita
  Füüsika      monotoonsus kiiruse, pinna, G, kalde ja koorma järgi
  Andmed       autode ja tehasemõõtude terviklikkus
  Regressioon  kindlad numbrid (muutuvad ainult teadliku mudelimuudatusega)
"""
import math
import re
import unittest
from dataclasses import replace

from .model import (AbsClass, BrakingModel, Calibration, Conditions, G_ACC,
                    InputError, Surface, Texture, Tyre, TyreCategory, Vehicle,
                    parse_size)
from .presets import TYRES, VEHICLES, vehicle_make
from .oem_sizes import OEM_SIZES

M = BrakingModel()
GOLF = VEHICLES["vw_golf_8"]
SUMMER = Tyre("suvi B", TyreCategory.SUMMER_TOURING, 1.47, size="205/55 R16")
UI = {  # sama mis app.js COND
    "wet": dict(surface=Surface.ASPHALT, water_mm=1.0, temp_c=10),
    "dry": dict(surface=Surface.ASPHALT, water_mm=0.0, temp_c=15),
    "snow": dict(surface=Surface.SNOW_PACKED, temp_c=-5),
    "ice": dict(surface=Surface.ICE, temp_c=-5),
}


def d(tyre=SUMMER, veh=GOLF, **c):
    return M.stopping_distance(tyre, veh, Conditions(**c)).distance_m


class Valem(unittest.TestCase):
    def test_integraator_vs_analyytiline(self):
        """Konstantne haare + lineaarne pidurite ülesehitus: täpne lahend on
        teada. Viga peab olema alla 0,05 % kogu kiirusvahemikus."""
        cal = Calibration()
        cal.crr = 0.0
        m = BrakingModel(cal)
        mu = 0.9
        m.mu_at_speed = lambda *a, **k: mu
        veh = replace(GOLF, cda_m2=0.0)
        a = mu * G_ACC * cal.abs_eff[veh.abs_class]
        tb = cal.brake_buildup_s[veh.abs_class]
        for kmh in (5, 20, 60, 100, 160, 250):
            v0 = kmh / 3.6
            if a * tb / 2 < v0:
                s = v0 * tb - a * tb ** 2 / 6 + (v0 - a * tb / 2) ** 2 / (2 * a)
            else:
                T = math.sqrt(2 * v0 * tb / a)
                s = v0 * T - a * T ** 3 / (6 * tb)
            got = m.stopping_distance(SUMMER, veh, Conditions(speed_kmh=kmh)).distance_m
            self.assertLess(abs(got - s) / s, 5e-4, f"{kmh} km/h: {got} vs {s}")

    def test_kmh_ms(self):
        """Reaktsioonitee = v[m/s] * t -- püüab km/h vs m/s vea."""
        r = M.stopping_distance(SUMMER, GOLF, Conditions(speed_kmh=72, reaction_time_s=1.0))
        self.assertAlmostEqual(r.reaction_m, 20.0, places=9)
        self.assertAlmostEqual(r.total_distance_m, r.distance_m + 20.0, places=9)

    def test_ruuduseadus(self):
        k = d(speed_kmh=100) / d(speed_kmh=50)
        self.assertTrue(3.6 < k < 4.4, k)

    def test_vahemik_katab(self):
        r = M.stopping_distance(SUMMER, GOLF, Conditions(speed_kmh=90, reaction_time_s=1))
        self.assertLess(r.low_m, r.total_distance_m)
        self.assertGreater(r.high_m, r.total_distance_m)
        self.assertAlmostEqual(r.low_m, r.total_distance_m * (1 - r.sigma_rel))

    def test_determinism(self):
        self.assertEqual(d(speed_kmh=87.3, water_mm=1.2), d(speed_kmh=87.3, water_mm=1.2))

    def test_parse_size(self):
        self.assertEqual(parse_size("225/40 R18"), (225, 40, 18))
        self.assertEqual(parse_size("225/40R18"), (225, 40, 18))
        self.assertIsNone(parse_size(""))
        self.assertIsNone(parse_size("abc"))


class Sisend(unittest.TestCase):
    def test_vigane_sisend_annab_vea(self):
        bad = [
            dict(speed_kmh=float("nan")), dict(speed_kmh=-10), dict(speed_kmh=float("inf")),
            dict(speed_kmh=400), dict(payload_kg=-100), dict(temp_c=90), dict(water_mm=-1),
            dict(reaction_time_s=-1), dict(brake_condition=0), dict(gradient_pct=80),
        ]
        for c in bad:
            with self.assertRaises(InputError, msg=str(c)):
                M.stopping_distance(SUMMER, GOLF, Conditions(**{"speed_kmh": 80, **c}))
        for veh in (replace(GOLF, kerb_mass_kg=0), replace(GOLF, recommended_pressure_bar=0),
                    replace(GOLF, brake_capacity_g=0), replace(GOLF, oem_size="000/00 R00")):
            with self.assertRaises(InputError):
                M.stopping_distance(SUMMER, veh, Conditions(speed_kmh=80))
        for ty in (replace(SUMMER, wet_grip_index=0), replace(SUMMER, wet_grip_index=float("nan")),
                   replace(SUMMER, pressure_bar=0), replace(SUMMER, size="999/99 R99"),
                   replace(SUMMER, tread_depth_mm=-1)):
            with self.assertRaises(InputError):
                M.stopping_distance(ty, GOLF, Conditions(speed_kmh=80, water_mm=1))

    def test_null_kiirus(self):
        self.assertEqual(d(speed_kmh=0), 0.0)
        self.assertTrue(0 < d(speed_kmh=1) < 0.1)


class Aarmus(unittest.TestCase):
    def test_ei_peatu_allamage_jaal(self):
        r = M.stopping_distance(SUMMER, GOLF, Conditions(
            speed_kmh=60, surface=Surface.ICE, temp_c=-5, gradient_pct=-12))
        self.assertTrue(math.isinf(r.distance_m))
        self.assertEqual(r.confidence, "madal")
        self.assertTrue(any("ei peatu" in w for w in r.warnings))

    def test_pikk_pidurdus_ei_karbita(self):
        # testiväljaku jää (sõidutee jääl on aeg u 40 s, alla 60 s piiri)
        r = M.stopping_distance(SUMMER, GOLF, Conditions(speed_kmh=200, surface=Surface.ICE, temp_c=-5,
                                                         ice_road=False))
        self.assertTrue(math.isfinite(r.distance_m))
        self.assertGreater(r.time_s, 60.0)

    def test_temperatuur_ei_ekstrapoleeri(self):
        """Asfaldi temperatuurikõver hoitakse otspunktis (-10 °C suverehvil)."""
        a = d(speed_kmh=80, temp_c=-10)
        b = d(speed_kmh=80, temp_c=-40)
        self.assertAlmostEqual(a, b, places=9)


class Fyysika(unittest.TestCase):
    TY = [t for t in TYRES.values()][::6]
    VEH = [VEHICLES[k] for k in ("vw_golf_8", "toyota_aygo_x", "mb_g_w463", "renault_trafic_3",
                                  "bmw_m3_g80", "tesla_model3_highland", "vaz_2101" if "vaz_2101" in VEHICLES else "lada_2101")]

    def test_kiirusega_kasvav(self):
        for t in self.TY:
            for v in self.VEH:
                for ck, c in UI.items():
                    prev = 0.0
                    for s in (10, 30, 60, 90, 130):
                        x = d(t, v, speed_kmh=s, **c)
                        self.assertGreater(x, prev, f"{t.name} {v.name} {ck} {s}")
                        prev = x

    def test_pindade_jarjestus(self):
        for t in self.TY:
            for v in self.VEH:
                for s in (30, 80, 120):
                    x = {ck: d(t, v, speed_kmh=s, **c) for ck, c in UI.items()}
                    # Kuiv vs märg SAMAL temperatuuril: lehe eelseaded on
                    # kuiv 15 °C / märg 10 °C ja talverehv haarab 10 °C
                    # juures paremini, nii et eelseadete otsevõrdlus ei
                    # mõõda pinda, vaid temperatuuri.
                    dry10 = d(t, v, speed_kmh=s, **dict(UI["dry"], temp_c=10))
                    # võrdne on lubatud: madalal kiirusel on lagi aktiivne
                    self.assertLessEqual(dry10, x["wet"] + 1e-9, f"{t.name} {v.name} {s}")
                    self.assertLess(x["wet"], x["snow"], f"{t.name} {v.name} {s}")
                    self.assertLess(x["snow"], x["ice"], f"{t.name} {v.name} {s}")

    def test_parem_G_lyhem_marjal(self):
        for cat in TyreCategory:
            prev = math.inf
            for g in (1.05, 1.17, 1.32, 1.47, 1.60, 1.75):
                x = d(Tyre("x", cat, g, size="205/55 R16"), speed_kmh=90, **UI["wet"])
                self.assertLess(x, prev, f"{cat} G={g}")
                prev = x

    def test_madalam_haare_pikem(self):
        """Veekile, mustri kulumine, alarõhk, vanus, pidurite rike: iga
        halvenemine pikendab (monotoonsus ühe muutuja kaupa)."""
        base = d(speed_kmh=90, **UI["wet"])
        self.assertGreater(d(speed_kmh=90, surface=Surface.ASPHALT, water_mm=3.0, temp_c=10), base)
        self.assertGreater(d(replace(SUMMER, tread_depth_mm=3.0), speed_kmh=90, **UI["wet"]), base)
        self.assertGreater(d(replace(SUMMER, age_years=10), speed_kmh=90, **UI["wet"]), base)
        self.assertGreater(d(speed_kmh=90, brake_condition=0.5, **UI["dry"]), d(speed_kmh=90, **UI["dry"]))

    def test_kalle(self):
        flat = d(speed_kmh=80, **UI["wet"])
        self.assertLess(d(speed_kmh=80, gradient_pct=8, **UI["wet"]), flat)
        self.assertGreater(d(speed_kmh=80, gradient_pct=-8, **UI["wet"]), flat)

    def test_mass_vaike_moju(self):
        """a = mu*g: mass taandub. Jääb koormustundlikkus (+) ja aero (-)."""
        a = d(veh=replace(GOLF, kerb_mass_kg=900), speed_kmh=100)
        b = d(veh=replace(GOLF, kerb_mass_kg=2800), speed_kmh=100)
        self.assertLess(abs(a - b) / a, 0.03)

    def test_moodu_ylekanne(self):
        """size = autol olev mõõt (laius -> vesi), g_size = kust G pärineb."""
        t = replace(SUMMER, size="205/55 R16", g_size="225/40 R18")
        r1 = M.stopping_distance(t, GOLF, Conditions(speed_kmh=90, **UI["wet"]))
        r2 = M.stopping_distance(replace(t, g_size=""), GOLF, Conditions(speed_kmh=90, **UI["wet"]))
        self.assertEqual(r1.distance_m, r2.distance_m)
        self.assertGreater(r1.sigma_rel, r2.sigma_rel)


class Andmed(unittest.TestCase):
    SZ = re.compile(r"^(\d{3})/(\d{2}) R(\d{2})C?$")

    def test_autod(self):
        for k, v in VEHICLES.items():
            if k.startswith("yld_"):
                continue
            with self.subTest(k):
                self.assertNotEqual(vehicle_make(k), "Muu")
                self.assertTrue(500 <= v.kerb_mass_kg <= 3500, v.kerb_mass_kg)
                self.assertTrue(0.3 <= v.cda_m2 <= 2.0, v.cda_m2)
                self.assertTrue(1.8 <= v.wheelbase_m <= 4.5, v.wheelbase_m)
                self.assertTrue(1.5 <= v.recommended_pressure_bar <= 4.5)
                self.assertTrue(0.656 <= v.brake_capacity_g <= 1.45)
                m = self.SZ.match(v.oem_size)
                self.assertTrue(m, v.oem_size)
                w, p, r = int(m[1]), int(m[2]), int(m[3])
                self.assertTrue(125 <= w <= 335 and 25 <= p <= 85 and 12 <= r <= 23, v.oem_size)
                dia = r * 25.4 + 2 * w * p / 100
                self.assertTrue(520 <= dia <= 860, (v.oem_size, dia))

    def test_tehasemoodud(self):
        for k, row in OEM_SIZES.items():
            with self.subTest(k):
                self.assertIn(k, VEHICLES)
                base, alls = row[0], row[1]
                self.assertTrue(self.SZ.match(base), base)
                for s in alls:
                    self.assertTrue(self.SZ.match(s), s)
                self.assertIn(base, alls)
                self.assertEqual(VEHICLES[k].oem_size, base)

    def test_nimed_unikaalsed(self):
        names = [v.name for v in VEHICLES.values()]
        self.assertEqual(len(names), len(set(names)))


class Regressioon(unittest.TestCase):
    """Kindlad numbrid. Kui see kukub, on mudel muutunud: kas see oli
    teadlik (siis uuenda numbrid ja kirjuta miks) või on see viga."""
    CASES = {
        # 2026-09-28 QA järel. Mõistlikkus: ADAC-i testides on B-klassi
        # suverehv kuival 100->0 u 34-38 m ja märjal 80->0 u 30-36 m.
        ("vw_golf_8", "dry", 100): 36.644,
        ("vw_golf_8", "wet", 80): 32.785,
        ("vw_golf_8", "snow", 50): 26.176,
        # 2026-09-29: jää on nüüd SÕIDUTEE jää (ice_road_add 0,05), mitte
        # testiväljak. Testiväljaku väärtus (ice_road=False) on endiselt 47,6.
        ("vw_golf_8", "ice", 50): 38.947,
    }

    def test_numbrid(self):
        for (vk, ck, s), want in self.CASES.items():
            got = d(SUMMER if ck in ("dry", "wet") else Tyre("talv", TyreCategory.WINTER_NORDIC, 1.225, size="205/55 R16"),
                    VEHICLES[vk], speed_kmh=s, **UI[ck])
            self.assertLess(abs(got - want) / want, 0.01, f"{vk} {ck} {s}: {got:.2f} (oli {want})")


class Mootorid(unittest.TestCase):
    """Tehase mootorid (mootorid.py -> mootorid_eksport.attach)."""

    def test_kirjed_korras(self):
        from .mootorid import MOOTORID
        for g, d in MOOTORID.items():
            self.assertIn(g, VEHICLES, g)
            self.assertTrue(d["eng"], g)
            for lab, hp, kw, fu, yrs, drv in d["eng"]:
                self.assertTrue(lab.strip(), g)
                self.assertTrue(20 <= hp <= 1300, (g, lab, hp))
                self.assertLess(abs(kw - hp * 0.7355), 3, (g, lab))
                self.assertIn(fu, ("b", "d", "h", "p", "e", "g", "bg"), (g, lab))

    def test_sidumine(self):
        from .mootorid_eksport import attach
        vs = [{"key": "x1", "make": "M", "model": "A", "yearLabel": "I", "variant": "2.0 TDI",
               "gen": "I", "years": "2000-2005"},
              {"key": "x2", "make": "M", "model": "A", "yearLabel": "I", "variant": "R 2.0 TSI",
               "gen": "I", "years": "2000-2005"}]
        import pidurdus.mootorid_eksport as E
        vana = E.MOOTORID
        E.MOOTORID = {"x1": {"src": [], "eng": [
            ("1.4 TSI", 125, 92, "b", "", ""), ("R 2.0 TSI", 300, 221, "b", "", ""),
            ("2.0 TDI", 122, 90, "d", "", ""), ("2.0 TDI", 150, 110, "d", "", ""),
            ("2.0 TDI", 190, 140, "d", "", "")]}}
        try:
            st = attach(vs)
        finally:
            E.MOOTORID = vana
        self.assertEqual(vs[0]["variant"], "2.0 TDI · 150 hj (110 kW)")   # keskmine võrdsetest
        self.assertEqual(vs[1]["variant"], "R 2.0 TSI · 300 hj (221 kW)")
        self.assertEqual(st["lisavalikuid"], 3)
        keys = [e[3] for e in vs[0].get("eng", [])]
        self.assertEqual(len(keys), len(set(keys)))


if __name__ == "__main__":
    unittest.main()
