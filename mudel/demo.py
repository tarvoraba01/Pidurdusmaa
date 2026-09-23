"""
Näited: mida mootor oskab.

Käivita:  python3 -m pidurdus.demo
"""

from dataclasses import replace

from .model import (AbsClass, BrakingModel, Conditions, Surface, Texture,
                    Tyre, TyreCategory)
from .presets import TYRES, VEHICLES, tyre, vehicle

M = BrakingModel()


def hr(title):
    print("\n" + "=" * 92)
    print(title)
    print("=" * 92)


# ---------------------------------------------------------------------------
def demo_single():
    hr("1) ÜKS ARVUTUS — BMW 320d, Michelin Pilot Sport 5, märg asfalt")
    veh = VEHICLES["bmw_320d"]
    ty = tyre("michelin_ps5", pressure_bar=2.3, tread_depth_mm=6.0)
    cond = Conditions(speed_kmh=90, surface=Surface.ASPHALT, water_mm=0.5,
                      temp_c=8, payload_kg=150)
    r = M.stopping_distance(ty, veh, cond)
    print(f"  Auto:    {veh.name}  ({veh.kerb_mass_kg} kg + {cond.payload_kg:.0f} kg)")
    print(f"  Rehv:    {ty.name}  (märghaardumine {ty.wet_grip_class}, "
          f"G={ty.wet_grip_index:.2f}, muster {ty.tread_depth_mm} mm, "
          f"{ty.pressure_bar} bar)")
    print(f"  Olukord: {cond.speed_kmh:.0f} km/h, märg asfalt "
          f"({cond.water_mm} mm vett), {cond.temp_c:.0f} °C")
    print()
    print("  " + str(r).replace("\n", "\n  "))


# ---------------------------------------------------------------------------
def demo_compare():
    hr("2) REHVIDE VÕRDLUS — VW Golf 8, 90 km/h, märg asfalt 1 mm, +10 °C")
    veh = VEHICLES["vw_golf_8"]
    cond = Conditions(speed_kmh=90, water_mm=1.0, temp_c=10, payload_kg=150)
    keys = ["conti_pc7", "michelin_primacy5", "pirelli_p7c2", "bridgestone_t6",
            "hankook_prime4", "vredestein_ultrac", "budget_c", "budget_e"]
    rows = M.compare_tyres([TYRES[k] for k in keys], veh, cond)
    best = rows[0][1].distance_m
    print(f"  {'rehv':<38}{'märgis':>7}{'maa':>9}{'vahe':>9}   graafik")
    for ty, r in rows:
        bar = "█" * int(round(r.distance_m / best * 26))
        print(f"  {ty.name:<38}{ty.wet_grip_class:>7}"
              f"{r.distance_m:>7.1f} m{r.distance_m - best:>+8.1f} m   {bar}")
    print(f"\n  Parima ja halvima vahe: {rows[-1][1].distance_m - best:.1f} m "
          f"({(rows[-1][1].distance_m / best - 1) * 100:.0f} %)")
    # mida see tähendab
    v0 = cond.speed_kmh / 3.6
    a = 2 * 9.80665 * rows[0][1].mu_effective * 0.965
    import math
    v_res = math.sqrt(max(0.0, v0 * v0 - a * best)) * 3.6
    v_res_bad = math.sqrt(max(0.0, v0 * v0 - 2 * 9.80665
                              * rows[-1][1].mu_effective * 0.965 * best)) * 3.6
    print(f"  Seal, kus parim rehv on juba seisma jäänud, sõidab halvim "
          f"veel u {v_res_bad:.0f} km/h.")


# ---------------------------------------------------------------------------
def demo_pressure():
    hr("3) REHVIRÕHU MÕJU — Škoda Octavia, Continental PremiumContact 7, 100 km/h")
    veh = VEHICLES["skoda_octavia"]
    print(f"  Soovituslik rõhk: {veh.recommended_pressure_bar} bar\n")
    print(f"  {'rõhk':>7}{'kuiv +20 °C':>16}{'märg 1 mm +10 °C':>20}"
          f"{'märg 3 mm +10 °C':>20}")
    base = {}
    for p in (1.6, 1.9, 2.2, 2.4, 2.7, 3.0, 3.3):
        ty = tyre("conti_pc7", pressure_bar=p)
        out = []
        for label, c in (("dry", Conditions(speed_kmh=100, temp_c=20)),
                         ("w1", Conditions(speed_kmh=100, water_mm=1.0, temp_c=10)),
                         ("w3", Conditions(speed_kmh=100, water_mm=3.0, temp_c=10))):
            d = M.stopping_distance(ty, veh, c).distance_m
            base.setdefault(label, d if p == 2.4 else None)
            out.append(d)
        marker = "  <- soovituslik" if abs(p - veh.recommended_pressure_bar) < .01 else ""
        print(f"  {p:>5.1f} b{out[0]:>13.1f} m{out[1]:>18.1f} m"
              f"{out[2]:>18.1f} m{marker}")


# ---------------------------------------------------------------------------
def demo_tread_and_temp():
    hr("4) MUSTRISÜGAVUS JA TEMPERATUUR — Toyota Corolla, 100 km/h, märg 1 mm")
    veh = VEHICLES["toyota_corolla"]
    print(f"  {'muster':>8}" + "".join(f"{t:>10}" for t in
                                       ("+25 °C", "+15 °C", "+5 °C", "0 °C")))
    for td in (8.0, 6.0, 4.0, 3.0, 2.0, 1.6):
        ty = tyre("michelin_primacy5", tread_depth_mm=td)
        row = []
        for temp in (25, 15, 5, 0):
            c = Conditions(speed_kmh=100, water_mm=1.0, temp_c=temp)
            row.append(M.stopping_distance(ty, veh, c).distance_m)
        print(f"  {td:>6.1f} mm" + "".join(f"{d:>8.1f} m" for d in row))


# ---------------------------------------------------------------------------
def demo_surfaces():
    hr("5) SAMA AUTO, SAMA KIIRUS, ERI PINNAD — VW Golf 8, 80 km/h")
    veh = VEHICLES["vw_golf_8"]
    cases = [
        ("kuiv asfalt, +20 °C", "michelin_primacy5",
         Conditions(speed_kmh=80, temp_c=20)),
        ("niiske asfalt 0,2 mm, +15 °C", "michelin_primacy5",
         Conditions(speed_kmh=80, water_mm=0.2, temp_c=15)),
        ("märg asfalt 1 mm, +10 °C", "michelin_primacy5",
         Conditions(speed_kmh=80, water_mm=1.0, temp_c=10)),
        ("väga märg 3 mm, +10 °C", "michelin_primacy5",
         Conditions(speed_kmh=80, water_mm=3.0, temp_c=10)),
        ("kulunud sile asfalt, märg 1 mm", "michelin_primacy5",
         Conditions(speed_kmh=80, water_mm=1.0, temp_c=10,
                    texture=Texture.WORN_SMOOTH)),
        ("tallatud lumi, -5 °C (talverehv)", "conti_vc8",
         Conditions(speed_kmh=80, surface=Surface.SNOW_PACKED, temp_c=-5)),
        ("jää, -5 °C (talverehv)", "conti_vc8",
         Conditions(speed_kmh=80, surface=Surface.ICE, temp_c=-5)),
        ("jää, -5 °C (naastrehv)", "nokian_hkpl10",
         Conditions(speed_kmh=80, surface=Surface.ICE, temp_c=-5)),
        ("jää, -15 °C (naastrehv)", "nokian_hkpl10",
         Conditions(speed_kmh=80, surface=Surface.ICE, temp_c=-15)),
        ("kruus", "michelin_primacy5",
         Conditions(speed_kmh=80, surface=Surface.GRAVEL, temp_c=10)),
    ]
    print(f"  {'olukord':<36}{'maa':>9}{'μ':>7}{'usaldus':>10}")
    for label, key, c in cases:
        r = M.stopping_distance(TYRES[key], veh, c)
        print(f"  {label:<36}{r.distance_m:>7.1f} m{r.mu_effective:>7.2f}"
              f"{r.confidence:>10}")


# ---------------------------------------------------------------------------
def demo_hydroplaning():
    hr("6) AKVAPLANEERIMISE LÄVI — Škoda Octavia, 3 mm vett")
    veh = VEHICLES["skoda_octavia"]
    print(f"  {'muster':>8}{'2,0 bar':>12}{'2,4 bar':>12}{'2,8 bar':>12}")
    for td in (8.0, 6.0, 4.0, 3.0, 2.0, 1.6):
        row = []
        for p in (2.0, 2.4, 2.8):
            ty = tyre("conti_pc7", tread_depth_mm=td, pressure_bar=p)
            c = Conditions(speed_kmh=100, water_mm=3.0, temp_c=15)
            row.append(M.hydroplane_speed_kmh(ty, veh, c))
        print(f"  {td:>6.1f} mm" + "".join(f"{v:>9.0f} km/h" for v in row))
    print("\n  (Horne'i valem, kohandatud mustrisügavuse ja veekile paksusega.")
    print("   Alla ~72 % sellest kiirusest mudel akvaplaneeringut ei arvesta.)")


# ---------------------------------------------------------------------------
def demo_vehicles():
    hr("7) AUTO MÕJU — Michelin Primacy 5, 100 km/h, märg 1 mm, +10 °C")
    c = Conditions(speed_kmh=100, water_mm=1.0, temp_c=10, payload_kg=150)
    print(f"  {'auto':<34}{'mass':>7}{'ABS':>32}{'maa':>9}")
    rows = []
    for key, veh in VEHICLES.items():
        r = M.stopping_distance(TYRES["michelin_primacy5"], veh, c)
        rows.append((veh, r))
    for veh, r in sorted(rows, key=lambda x: x[1].distance_m):
        print(f"  {veh.name:<34}{veh.kerb_mass_kg:>6.0f} kg"
              f"{veh.abs_class.value:>32}{r.distance_m:>7.1f} m")
    print("\n  Massi mõju on väike (füüsikas mass taandub); suure osa vahest")
    print("  teevad ABS-i põlvkond, õhutakistus ja rehvi koormus.")


# ---------------------------------------------------------------------------
def demo_reaction():
    hr("8) TÄIELIK PEATUMISTEE (koos reaktsiooniajaga) — 1,0 s")
    veh = VEHICLES["skoda_octavia"]
    ty = TYRES["conti_pc7"]
    print(f"  {'kiirus':>8}{'kuiv':>22}{'märg 1 mm +10 °C':>26}")
    print(f"  {'':>8}{'pidurdus + reaktsioon':>22}{'pidurdus + reaktsioon':>26}")
    for v in (30, 50, 70, 90, 110, 130):
        a = M.stopping_distance(ty, veh, Conditions(speed_kmh=v, temp_c=20,
                                                    reaction_time_s=1.0))
        b = M.stopping_distance(ty, veh, Conditions(speed_kmh=v, water_mm=1.0,
                                                    temp_c=10, reaction_time_s=1.0))
        print(f"  {v:>5.0f} km/h{a.distance_m:>10.1f} +{a.total_distance_m - a.distance_m:>5.1f}"
              f" = {a.total_distance_m:>5.1f} m"
              f"{b.distance_m:>11.1f} +{b.total_distance_m - b.distance_m:>5.1f}"
              f" = {b.total_distance_m:>5.1f} m")


def demo_brakes():
    hr("9) PIDURITE SEISUKORD — Škoda Octavia, Continental PC7, 100 km/h")
    from .selgitused import PIDURID
    veh, ty = VEHICLES["skoda_octavia"], TYRES["conti_pc7"]
    print(f"  Terve auto pidurid: {veh.brake_capacity_g} g. "
          f"Rehv suudab edasi anda ~1,15 g kuival, ~0,75 g märjal.\n")
    print(f"  {'tase':<22}{'võimekus':>10}{'KUIV':>18}{'MÄRG 1 mm':>20}")
    d0 = {}
    for name, frac in PIDURID.items():
        row = []
        for key, c in (("kuiv", Conditions(speed_kmh=100, temp_c=20,
                                           brake_condition=frac)),
                       ("märg", Conditions(speed_kmh=100, water_mm=1.0,
                                           temp_c=15, brake_condition=frac))):
            r = M.stopping_distance(ty, veh, c)
            d0.setdefault(key, r.distance_m)
            row.append((r.distance_m, r.distance_m / d0[key] - 1, r.limiter))
        print(f"  {name:<22}{frac*100:>8.0f} %"
              + "".join(f"{d:>8.1f} m ({p*100:+5.1f} %)" for d, p, _ in row))
    print("\n  Pane tähele: nõrgenenud pidurid annavad end üles KUIVAL, mitte")
    print("  märjal. Märjal on rehv niikuinii nõrgem lüli, nii et pidurite")
    print("  langus kuni ~65 %-ni ei muuda seal mitte midagi.")


if __name__ == "__main__":
    demo_single()
    demo_compare()
    demo_pressure()
    demo_tread_and_temp()
    demo_surfaces()
    demo_hydroplaning()
    demo_vehicles()
    demo_reaction()
    demo_brakes()
    print()
